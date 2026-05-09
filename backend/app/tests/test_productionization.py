from __future__ import annotations

from pathlib import Path

import pytest

from app.acquisition.brainflow_adapter import BrainFlowAcquisition
from app.acquisition.diagnostics import acquisition_status, test_adapter
from app.acquisition.lsl_adapter import LSLAcquisition
from app.api.routes_acquisition import api_acquisition_status
from app.api.routes_health import deep_health, ready
from app.api.routes_runtime import api_runtime_latency, api_runtime_metrics
from app.core.telemetry import telemetry
from app.sessions.protocol import calibrate_state, create_calibration_profile

ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.asyncio
async def test_ready_and_deep_health_endpoints() -> None:
    readiness = await ready()
    deep = await deep_health()
    assert "checks" in readiness
    assert "checks" in deep
    assert "session_storage_writable" in deep["checks"]
    assert "websocket" in deep


@pytest.mark.asyncio
async def test_runtime_latency_and_metrics_endpoints() -> None:
    telemetry.record_tick({"inference": 1.5, "safety": 0.5})
    latency = await api_runtime_latency()
    metrics = await api_runtime_metrics()
    assert "total_tick" in latency["latency_ms"]
    assert metrics["ticks_processed"] >= 1
    assert "average_end_to_end_latency_ms" in metrics


@pytest.mark.asyncio
async def test_acquisition_diagnostics_endpoint_reports_optional_dependencies() -> None:
    status = await api_acquisition_status()
    assert status["active_adapter"] in {"simulator", "brainflow", "lsl", "csv_replay", "xdf_replay"}
    assert "optional_dependencies" in status
    assert "brainflow" in status["optional_dependencies"]


@pytest.mark.asyncio
async def test_acquisition_test_reports_simulator_capabilities() -> None:
    result = await test_adapter("simulator", {})
    assert result["ok"]
    assert "eeg" in result["capabilities"]["modalities"]


def test_brainflow_and_lsl_missing_dependencies_are_graceful() -> None:
    brainflow = BrainFlowAcquisition()
    lsl = LSLAcquisition()
    assert brainflow.status()["available"] in {True, False}
    assert lsl.status()["available"] in {True, False}
    assert brainflow.capabilities()["dependency"] == "brainflow"
    assert lsl.capabilities()["dependency"] == "pylsl"


def test_acquisition_status_has_adapter_catalog() -> None:
    status = acquisition_status()
    assert "available_adapters" in status
    assert "simulator" in status["available_adapters"]


def test_calibration_profile_and_relative_scores() -> None:
    profile = create_calibration_profile(
        "calibration_unit",
        [
            {"focus": 0.4, "relaxation": 0.5, "workload": 0.2, "stress": 0.1},
            {"focus": 0.6, "relaxation": 0.7, "workload": 0.4, "stress": 0.3},
        ],
        duration_seconds=10,
        sqi_values=[0.8, 0.9],
    )
    calibrated = calibrate_state({"focus": 0.8, "stress": 0.2}, profile)
    assert profile.baseline_focus == 0.5
    assert profile.baseline_sqi == 0.85
    assert calibrated["focus_relative_to_baseline"] == 0.3


def test_evidence_pack_script_exists() -> None:
    assert (ROOT / "scripts" / "generate_evidence_pack.py").exists()
