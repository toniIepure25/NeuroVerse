from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.acquisition.brainflow_adapter import BRAINFLOW_INSTALL_HINT, BrainFlowAcquisition
from app.acquisition.channel_mapping import get_profile
from app.acquisition.diagnostics import optional_dependency_status
from app.acquisition.lsl_adapter import LSLAcquisition
from app.acquisition.lsl_discovery import PYLSL_INSTALL_HINT, pylsl_available
from app.acquisition.marker_collector import BackgroundMarkerCollector
from app.acquisition.markers import (
    MarkerEvent,
    empty_marker_report,
    marker_report,
)
from app.acquisition.pipeline import extract_features_and_sqi
from app.acquisition.simulator import BiosignalSimulator
from app.acquisition.timing import summarize_window_timing
from app.core.config import settings
from app.inference.heuristic_model import HeuristicStateEstimator
from app.sessions.protocol import create_calibration_profile

router = APIRouter(prefix="/api/v1/calibration", tags=["calibration"])
REPO_ROOT = Path(__file__).resolve().parents[3]
CALIBRATION_DIR = REPO_ROOT / "reports" / "calibration"
CALIBRATION_DIR.mkdir(parents=True, exist_ok=True)


class CalibrationStartRequest(BaseModel):
    duration_seconds: float = Field(default=2.0, ge=0.1, le=30.0)
    source: str = "simulator"
    profile_id: str | None = "synthetic_multimodal"
    stream_name: str | None = None
    stream_type: str | None = "EEG"
    source_id: str | None = None
    marker_stream_name: str | None = None
    marker_stream_type: str | None = "Markers"
    board_id: int | str | None = None
    serial_port: str | None = None
    protocol: str | None = "resting_baseline"


@router.post("/start")
async def start_calibration(request: CalibrationStartRequest) -> dict[str, Any]:
    if request.source not in {
        "simulator",
        "hardware_record_only",
        "dataset_replay",
        "lsl",
        "eeg_lsl_replay",
        "brainflow",
    }:
        raise HTTPException(status_code=400, detail="Unsupported calibration source")
    if request.source == "brainflow":
        if not BrainFlowAcquisition.is_available():
            raise HTTPException(status_code=409, detail=BRAINFLOW_INSTALL_HINT)
        return await _run_brainflow_calibration(request)
    if request.source in {"lsl", "eeg_lsl_replay"}:
        if not pylsl_available():
            raise HTTPException(status_code=409, detail=PYLSL_INSTALL_HINT)
        return await _run_lsl_calibration(request)
    if request.source != "simulator":
        raise HTTPException(
            status_code=409,
            detail="Only simulator calibration is implemented without configured hardware.",
        )

    calibration_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_calibration")
    simulator = BiosignalSimulator(
        duration_s=max(request.duration_seconds, 0.5),
        tick_interval_ms=settings.tick_interval_ms,
    )
    estimator = HeuristicStateEstimator()
    await simulator.start()
    states: list[dict[str, Any]] = []
    sqi_values: list[float] = []
    timestamps: list[float] = []
    sample_cursor = 0
    try:
        window_count = max(1, int(round(request.duration_seconds / settings.tick_interval_s)))
        for _ in range(window_count):
            window = await simulator.get_window()
            features = extract_features_and_sqi(window)
            state = estimator.predict(features)
            states.append(state.model_dump())
            sqi = features.sqi_scores.get("multimodal")
            if sqi is not None:
                sqi_values.append(float(sqi))
            sample_count = len(window.data[0]) if window.data else 0
            for i in range(sample_count):
                timestamps.append((sample_cursor + i) / window.sampling_rate)
            sample_cursor += sample_count
    finally:
        await simulator.stop()

    profile = create_calibration_profile(
        calibration_id,
        states,
        duration_seconds=request.duration_seconds,
        sqi_values=sqi_values,
    )
    report = {
        **profile.model_dump(),
        "calibration_id": calibration_id,
        "source": request.source,
        "profile_id": request.profile_id,
        "baseline_state_proxy_means": {
            key: round(mean([state[key] for state in states]), 4)
            for key in states[0]
            if key not in {"model_version", "feature_window_ms"}
        },
        "baseline_sqi": round(mean(sqi_values), 4) if sqi_values else None,
        "timestamp_quality": summarize_window_timing(timestamps, expected_rate_hz=250.0),
        "warnings": [
            "Calibration values are session-local proxy baselines, not clinical measurements."
        ],
    }
    path = CALIBRATION_DIR / f"{calibration_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


async def _run_brainflow_calibration(request: CalibrationStartRequest) -> dict[str, Any]:
    calibration_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_brainflow_calibration")
    profile = get_profile(request.profile_id) if request.profile_id else {}
    adapter = BrainFlowAcquisition({
        **profile,
        "profile_id": request.profile_id,
        "board_id": request.board_id if request.board_id is not None else profile.get("board_id"),
        "serial_port": request.serial_port or profile.get("serial_port"),
        "window_seconds": settings.tick_interval_s,
    })
    estimator = HeuristicStateEstimator()
    states: list[dict[str, Any]] = []
    sqi_values: list[float] = []
    timestamps: list[float] = []
    try:
        await adapter.start()
        end_time = datetime.now(timezone.utc).timestamp() + request.duration_seconds
        while datetime.now(timezone.utc).timestamp() < end_time:
            window = await adapter.get_window()
            features = extract_features_and_sqi(window)
            states.append(estimator.predict(features).model_dump())
            sqi = features.sqi_scores.get("multimodal")
            if sqi is not None:
                sqi_values.append(float(sqi))
            timestamps.extend(window.timestamps or [])
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        await adapter.stop()

    if not states:
        raise HTTPException(status_code=409, detail="No BrainFlow windows were collected.")

    profile_obj = create_calibration_profile(
        calibration_id,
        states,
        duration_seconds=request.duration_seconds,
        sqi_values=sqi_values,
    )
    status = adapter.status()
    report = {
        **profile_obj.model_dump(),
        "calibration_id": calibration_id,
        "source": request.source,
        "protocol": request.protocol,
        "profile_id": request.profile_id,
        "board": {
            "board_name": status.get("board_name"),
            "board_id": status.get("board_id"),
            "physical_or_synthetic": status.get("physical_or_synthetic"),
            "serial_port": status.get("serial_port"),
        },
        "baseline_state_proxy_means": {
            key: round(mean([state[key] for state in states]), 4)
            for key in states[0]
            if key not in {"model_version", "feature_window_ms"}
        },
        "baseline_sqi": round(mean(sqi_values), 4) if sqi_values else None,
        "timestamp_quality": summarize_window_timing(
            timestamps,
            expected_rate_hz=float(status.get("sampling_rate") or 1.0),
            max_gap_ms=(1000.0 / float(status.get("sampling_rate") or 1.0)) * 5.0,
        ),
        "dependency_status": optional_dependency_status(),
        "warnings": [
            "BrainFlow calibration values are proxy baselines, not clinical measurements."
        ],
    }
    path = CALIBRATION_DIR / f"{calibration_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


async def _run_lsl_calibration(request: CalibrationStartRequest) -> dict[str, Any]:
    calibration_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_lsl_calibration")
    adapter = LSLAcquisition({
        "stream_name": request.stream_name,
        "stream_type": request.stream_type,
        "source_id": request.source_id,
        "window_seconds": settings.tick_interval_s,
    })
    estimator = HeuristicStateEstimator()
    states: list[dict[str, Any]] = []
    sqi_values: list[float] = []
    timestamps: list[float] = []
    clock_offsets: list[float] = []
    windows: list[dict[str, Any]] = []
    markers: list[MarkerEvent] = []
    marker_collector = BackgroundMarkerCollector(
        stream_name=request.marker_stream_name,
        stream_type=request.marker_stream_type or "Markers",
    )
    marker_error: str | None = None
    try:
        await adapter.start()
        try:
            marker_collector.start()
        except Exception as exc:
            marker_error = str(exc)
        end_time = datetime.now(timezone.utc).timestamp() + request.duration_seconds
        while datetime.now(timezone.utc).timestamp() < end_time:
            window = await adapter.get_window()
            features = extract_features_and_sqi(window)
            states.append(estimator.predict(features).model_dump())
            sqi = features.sqi_scores.get("multimodal")
            if sqi is not None:
                sqi_values.append(float(sqi))
            timestamps.extend(window.timestamps or [])
            if window.timestamps:
                windows.append({
                    "start_time": min(window.timestamps),
                    "end_time": max(window.timestamps),
                })
            if window.metadata and window.metadata.get("clock_offset") is not None:
                clock_offsets.append(float(window.metadata["clock_offset"]))
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        markers = marker_collector.stop()
        await adapter.stop()

    if not states:
        raise HTTPException(status_code=409, detail="No LSL windows were collected.")

    profile = create_calibration_profile(
        calibration_id,
        states,
        duration_seconds=request.duration_seconds,
        sqi_values=sqi_values,
    )
    stream = adapter.status().get("selected_stream") or {}
    report = {
        **profile.model_dump(),
        "calibration_id": calibration_id,
        "source": request.source,
        "profile_id": request.profile_id,
        "stream_metadata": stream,
        "baseline_state_proxy_means": {
            key: round(mean([state[key] for state in states]), 4)
            for key in states[0]
            if key not in {"model_version", "feature_window_ms"}
        },
        "baseline_sqi": round(mean(sqi_values), 4) if sqi_values else None,
        "timestamp_quality": summarize_window_timing(
            timestamps,
            expected_rate_hz=float(stream.get("nominal_srate") or 1.0),
            clock_offsets=clock_offsets,
        ),
        "markers": (
            marker_report(
                stream_metadata=marker_collector.stream_metadata,
                markers=markers,
                windows=windows,
            )
            if marker_collector.stream_metadata
            else empty_marker_report(
                marker_error or marker_collector.error or "No marker stream detected."
            )
        ),
        "warnings": [
            "LSL calibration values are proxy baselines, not clinical measurements."
        ],
    }
    path = CALIBRATION_DIR / f"{calibration_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


@router.get("/{calibration_id}")
async def get_calibration(calibration_id: str) -> dict[str, Any]:
    path = CALIBRATION_DIR / f"{calibration_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Calibration profile not found")
    return json.loads(path.read_text(encoding="utf-8"))
