from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from app.acquisition.alpha_reactivity import analyze_alpha_reactivity
from app.acquisition.brainflow_adapter import BrainFlowAcquisition, discover_brainflow_devices
from app.acquisition.channel_mapping import validate_profile
from app.acquisition.timing import summarize_window_timing
from app.acquisition.validation import run_hardware_validation
from app.api.routes_calibration import CalibrationStartRequest, start_calibration
from app.api.routes_runtime import api_emergency_stop, api_freeze, api_runtime_status, api_unfreeze
from app.api.routes_sessions import start_session, stop_session
from app.api.routes_shadow import ShadowStartRequest, start_shadow_mode
from app.core.runtime_status import runtime_status
from app.main import create_app
from app.schemas.events import BaseEvent
from app.sessions.recorder import SessionRecorder
from app.sessions.storage import delete_session_data, export_session_bundle


def test_timing_diagnostics_perfect_timestamps() -> None:
    timestamps = [i / 250.0 for i in range(500)]
    report = summarize_window_timing(timestamps, expected_rate_hz=250.0)
    assert report["pass"]
    assert report["gap_count"] == 0
    assert report["duplicate_count"] == 0
    assert abs(report["observed_rate_hz"] - 250.0) < 0.01


def test_v1_route_aliases_exist() -> None:
    app = create_app()
    paths = {route.path for route in app.routes if hasattr(route, "path")}
    expected = {
        "/api/v1/session/start",
        "/api/v1/sessions/{session_id}/export",
        "/api/v1/sessions/{session_id}/delete",
        "/api/v1/runtime/emergency-stop",
        "/api/v1/runtime/freeze",
        "/api/v1/runtime/unfreeze",
        "/api/v1/acquisition/validation/status",
        "/api/v1/acquisition/profiles",
        "/api/v1/acquisition/brainflow/status",
        "/api/v1/acquisition/brainflow/devices",
        "/api/v1/acquisition/brainflow/test",
        "/api/v1/hardware-trials/latest",
        "/api/v1/calibration/start",
        "/api/v1/acquisition/shadow/start",
    }
    assert not (expected - paths)


def test_brainflow_device_discovery_graceful() -> None:
    report = discover_brainflow_devices()
    assert "devices" in report
    assert "warnings" in report
    assert "next_commands" in report


def test_alpha_reactivity_detects_synthetic_alpha_increase() -> None:
    sampling_rate = 100.0
    t = np.arange(0, 4.0, 1.0 / sampling_rate)
    eyes_open = np.vstack([
        np.sin(2 * np.pi * 10 * t),
        0.5 * np.sin(2 * np.pi * 10 * t),
    ])
    eyes_closed = np.vstack([
        3.0 * np.sin(2 * np.pi * 10 * t),
        1.5 * np.sin(2 * np.pi * 10 * t),
    ])
    report = analyze_alpha_reactivity(
        {
            "eyes_open": {"data": eyes_open.tolist()},
            "eyes_closed": {"data": eyes_closed.tolist()},
        },
        sampling_rate=sampling_rate,
        channel_names=["O1", "C3"],
    )
    assert report["status"] == "visible_reactivity"
    assert report["aggregate_alpha_ratio"] and report["aggregate_alpha_ratio"] > 1.2
    assert report["closed_loop_allowed"] is False


def test_alpha_reactivity_missing_phase_is_graceful() -> None:
    report = analyze_alpha_reactivity(
        {"eyes_open": {"data": [[0.0, 1.0]]}},
        sampling_rate=100.0,
        channel_names=["O1"],
    )
    assert report["status"] == "insufficient_data"
    assert report["closed_loop_allowed"] is False


def test_timing_diagnostics_detect_jitter_gap_drift_duplicate() -> None:
    timestamps = [i / 200.0 for i in range(100)]
    timestamps[20] += 0.02
    timestamps[40] = timestamps[39]
    report = summarize_window_timing(timestamps, expected_rate_hz=250.0)
    assert not report["pass"]
    assert report["gap_count"] >= 1
    assert report["duplicate_count"] >= 1
    assert report["warnings"]


def test_channel_mapping_validation() -> None:
    valid = validate_profile({
        "profile_id": "unit",
        "required_modalities": ["eeg"],
        "channels": [{"name": "C3", "index": 0, "modality": "eeg", "enabled": True}],
    })
    assert valid["ok"]
    duplicate = validate_profile({
        "profile_id": "bad",
        "required_modalities": ["eeg"],
        "channels": [
            {"name": "C3", "index": 0, "modality": "eeg", "enabled": True},
            {"name": "C4", "index": 0, "modality": "eeg", "enabled": True},
        ],
    })
    assert not duplicate["ok"]
    missing = validate_profile({
        "profile_id": "missing",
        "required_modalities": ["eeg"],
        "channels": [{"name": "HR", "index": 0, "modality": "physio", "enabled": True}],
    })
    assert not missing["ok"]


@pytest.mark.asyncio
async def test_hardware_validation_report_generated_from_simulator() -> None:
    report = await run_hardware_validation(
        adapter="simulator",
        profile_id="synthetic_multimodal",
        duration_seconds=0.5,
    )
    assert report["passed"]
    assert report["timing"]["observed_rate_hz"] is not None
    assert report["closed_loop_allowed"] is False


@pytest.mark.asyncio
async def test_hardware_validation_missing_dependency_fails_gracefully(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "app.acquisition.validation.optional_dependency_status",
        lambda: {"brainflow": False, "pylsl": False, "pyxdf": False, "mne": False},
    )
    report = await run_hardware_validation(adapter="brainflow", duration_seconds=0.5)
    assert not report["passed"]
    assert report["failure_reasons"]


@pytest.mark.asyncio
async def test_brainflow_synthetic_validation_when_available() -> None:
    if not BrainFlowAcquisition.is_available():
        pytest.skip("BrainFlow optional dependency not installed")
    report = await run_hardware_validation(
        adapter="brainflow",
        config={"adapter_type": "brainflow"},
        profile_id="brainflow_synthetic_eeg",
        duration_seconds=0.5,
    )
    assert report["adapter"] == "brainflow"
    assert report["board"]["physical_or_synthetic"] == "synthetic"
    assert report["channel_mapping"]["observed_channel_count"] == 16
    assert report["closed_loop_allowed"] is False


@pytest.mark.asyncio
async def test_emergency_freeze_and_unfreeze_runtime_controls() -> None:
    await api_freeze()
    status = await api_runtime_status()
    assert status["adaptation_frozen"] is True
    await api_unfreeze()
    status = await api_runtime_status()
    assert status["adaptation_frozen"] is False
    await api_emergency_stop()
    status = await api_runtime_status()
    assert status["emergency_stop_active"] is True
    with pytest.raises(Exception):
        await api_unfreeze()
    runtime_status.stop_session()


@pytest.mark.asyncio
async def test_emergency_stop_logs_event_when_session_active() -> None:
    started = await start_session()
    session_id = started["session_id"]
    await api_emergency_stop()
    await stop_session()
    events = Path("data/sessions") / f"{session_id}.jsonl"
    assert "neuroverse.runtime.emergency_stop" in events.read_text(encoding="utf-8")


def test_session_export_and_delete_lifecycle(tmp_path: Path) -> None:
    recorder = SessionRecorder("delete_fixture", base_dir=tmp_path)
    recorder.record(
        BaseEvent(
            session_id="delete_fixture",
            event_type="neuroverse.session.started",
            timestamp=0,
            source="test",
            payload={},
        )
    )
    recorder.close()
    bundle = export_session_bundle("delete_fixture", base_dir=tmp_path)
    assert bundle.exists()
    denied = delete_session_data("delete_fixture", confirm=False, base_dir=tmp_path)
    assert denied["deleted"] is False
    deleted = delete_session_data("delete_fixture", confirm=True, base_dir=tmp_path)
    assert deleted["deleted"]
    with pytest.raises(ValueError):
        delete_session_data("../outside", confirm=True, base_dir=tmp_path)


@pytest.mark.asyncio
async def test_calibration_profile_generated_from_simulator() -> None:
    report = await start_calibration(CalibrationStartRequest(duration_seconds=0.5))
    assert report["calibration_id"]
    assert report["baseline_sqi"] is not None
    assert report["timestamp_quality"]["observed_rate_hz"] is not None


@pytest.mark.asyncio
async def test_brainflow_calibration_and_shadow_when_available() -> None:
    if not BrainFlowAcquisition.is_available():
        pytest.skip("BrainFlow optional dependency not installed")
    calibration = await start_calibration(
        CalibrationStartRequest(
            source="brainflow",
            profile_id="brainflow_synthetic_eeg",
            duration_seconds=0.5,
        )
    )
    assert calibration["source"] == "brainflow"
    assert calibration["baseline_sqi"] is not None
    shadow = await start_shadow_mode(
        ShadowStartRequest(
            source="brainflow",
            profile_id="brainflow_synthetic_eeg",
            duration_seconds=0.5,
        )
    )
    assert shadow["source"] == "brainflow"
    assert shadow["real_adaptation_actions_emitted"] == 0
    assert shadow["closed_loop_allowed"] is False


@pytest.mark.asyncio
async def test_shadow_mode_does_not_emit_real_adaptation_actions() -> None:
    report = await start_shadow_mode(ShadowStartRequest(duration_seconds=0.5))
    assert report["real_adaptation_actions_emitted"] == 0
    assert report["would_be_actions"]
