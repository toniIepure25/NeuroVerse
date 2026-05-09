from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

from app.acquisition.channel_mapping import get_profile, validate_profile_against_stream
from app.acquisition.lsl_adapter import LSLAcquisition
from app.acquisition.lsl_discovery import pylsl_available
from app.acquisition.timing import summarize_window_timing
from app.acquisition.validation import run_hardware_validation
from app.api.routes_acquisition import api_lsl_status, api_lsl_streams
from app.api.routes_calibration import CalibrationStartRequest, start_calibration
from app.api.routes_shadow import ShadowStartRequest, start_shadow_mode
from app.main import create_app

ROOT = Path(__file__).resolve().parents[3]


def test_lsl_missing_dependency_status_is_safe() -> None:
    adapter = LSLAcquisition()
    status = adapter.status()
    assert status["available"] in {True, False}
    assert adapter.capabilities()["dependency"] == "pylsl"


@pytest.mark.asyncio
async def test_lsl_status_endpoint_handles_missing_pylsl() -> None:
    status = await api_lsl_status()
    assert "pylsl_available" in status
    if not status["pylsl_available"]:
        assert "pip install" in status["install_hint"]


@pytest.mark.asyncio
async def test_lsl_streams_endpoint_returns_safe_response_without_pylsl() -> None:
    response = await api_lsl_streams(stream_type="EEG")
    if not pylsl_available():
        assert response["available"] is False
        assert response["streams"] == []


def test_lsl_streamer_fails_gracefully_without_pylsl() -> None:
    if pylsl_available():
        pytest.skip("pylsl installed; missing-dependency path not applicable")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "lsl_synthetic_streamer.py"), "--duration", "0.1"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "pylsl is not installed" in result.stderr


def test_lsl_live_suite_fails_gracefully_without_pylsl(tmp_path: Path) -> None:
    if pylsl_available():
        pytest.skip("pylsl installed; live suite should run an integration workflow")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_lsl_live_validation_suite.py"),
            "--output-dir",
            str(tmp_path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "pylsl is not installed" in result.stderr
    summaries = list(tmp_path.glob("*/live_validation_summary.json"))
    assert summaries


def test_check_hardware_extra_script_reports_optional_status() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_hardware_extra.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "pylsl" in result.stdout


def test_lsl_timing_diagnostics_include_extended_fields() -> None:
    timestamps = [i / 250.0 for i in range(500)]
    report = summarize_window_timing(
        timestamps,
        expected_rate_hz=250,
        clock_offsets=[0.001, 0.002, 0.0015],
    )
    assert report["jitter_ms_p50"] == 0
    assert report["jitter_ms_p99"] == 0
    assert report["quality"] == "excellent"
    assert report["monotonic_timestamp_pass"]
    assert report["clock_offset_estimate"] is not None


def test_lsl_timing_quality_classifies_gaps_as_warning() -> None:
    timestamps = [0.0, 0.004, 0.008, 0.050, 0.054]
    report = summarize_window_timing(timestamps, expected_rate_hz=250)
    assert report["quality"] in {"warning", "failed"}
    assert report["gap_count"] >= 1


def test_lsl_profile_validation_against_stream() -> None:
    profile = get_profile("lsl_synthetic_eeg")
    stream = {
        "name": "NeuroVerseSyntheticEEG",
        "type": "EEG",
        "channel_count": 8,
        "nominal_srate": 250,
        "channel_names": [f"EEG{i + 1}" for i in range(8)],
    }
    assert validate_profile_against_stream(profile, stream)["ok"]
    bad = {**stream, "channel_count": 4}
    assert not validate_profile_against_stream(profile, bad)["ok"]


@pytest.mark.asyncio
async def test_lsl_validation_fails_gracefully_when_missing_or_no_stream() -> None:
    report = await run_hardware_validation(
        adapter="lsl",
        config={"adapter_type": "lsl", "stream_name": "NeuroVerseSyntheticEEG"},
        profile_id="lsl_synthetic_eeg",
        duration_seconds=0.5,
    )
    assert report["adapter"] == "lsl"
    assert report["closed_loop_allowed"] is False
    assert "markers" in report
    if not pylsl_available():
        assert not report["passed"]
        assert report["failure_reasons"]


@pytest.mark.asyncio
async def test_lsl_calibration_and_shadow_unavailable_are_clear() -> None:
    if pylsl_available():
        pytest.skip("pylsl installed; no-stream behavior depends on local environment")
    with pytest.raises(HTTPException):
        await start_calibration(CalibrationStartRequest(source="lsl"))
    with pytest.raises(HTTPException):
        await start_shadow_mode(ShadowStartRequest(source="lsl"))


def test_lsl_routes_exist() -> None:
    app = create_app()
    paths = {route.path for route in app.routes if hasattr(route, "path")}
    expected = {
        "/api/v1/acquisition/lsl/status",
        "/api/v1/acquisition/lsl/streams",
        "/api/v1/acquisition/lsl/streams/{stream_id}/metadata",
        "/api/v1/acquisition/lsl/select",
    }
    assert not (expected - paths)
