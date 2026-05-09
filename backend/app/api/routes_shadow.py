from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.acquisition.brainflow_adapter import BRAINFLOW_INSTALL_HINT, BrainFlowAcquisition
from app.acquisition.channel_mapping import get_profile
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
from app.ml.event_epochs import extract_epoch_features
from app.ml.registry import get_model_metadata, load_model
from app.policy.adaptation_policy import AdaptationPolicy
from app.safety.safety_gate import SafetyGate

router = APIRouter(prefix="/api/v1/acquisition/shadow", tags=["acquisition"])
REPO_ROOT = Path(__file__).resolve().parents[3]
SHADOW_DIR = REPO_ROOT / "reports" / "shadow"
SHADOW_DIR.mkdir(parents=True, exist_ok=True)


class ShadowStartRequest(BaseModel):
    source: str = "simulator"
    duration_seconds: float = Field(default=2.0, ge=0.1, le=30.0)
    profile_id: str | None = "synthetic_multimodal"
    stream_name: str | None = None
    stream_type: str | None = "EEG"
    source_id: str | None = None
    marker_stream_name: str | None = None
    marker_stream_type: str | None = "Markers"
    calibration_id: str | None = None
    model_id: str | None = None
    shadow_only: bool = True
    board_id: int | str | None = None
    serial_port: str | None = None


@router.post("/start")
async def start_shadow_mode(request: ShadowStartRequest) -> dict[str, Any]:
    if request.source in {"lsl", "eeg_lsl_replay"}:
        if not pylsl_available():
            raise HTTPException(status_code=409, detail=PYLSL_INSTALL_HINT)
        return await _run_lsl_shadow(request)
    if request.source == "brainflow":
        if not BrainFlowAcquisition.is_available():
            raise HTTPException(status_code=409, detail=BRAINFLOW_INSTALL_HINT)
        return await _run_brainflow_shadow(request)
    if request.source != "simulator":
        raise HTTPException(
            status_code=409,
            detail=(
                "Shadow mode currently supports simulator unless hardware is "
                "explicitly configured."
            ),
        )
    report_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_shadow")
    simulator = BiosignalSimulator(
        duration_s=max(request.duration_seconds, 0.5),
        tick_interval_ms=settings.tick_interval_ms,
    )
    estimator = HeuristicStateEstimator()
    safety_gate = SafetyGate()
    policy = AdaptationPolicy()
    predictions = []
    safety_decisions = []
    would_be_actions = []
    await simulator.start()
    try:
        window_count = max(1, int(round(request.duration_seconds / settings.tick_interval_s)))
        for _ in range(window_count):
            features = extract_features_and_sqi(await simulator.get_window())
            prediction = estimator.predict(features)
            safety = safety_gate.evaluate(prediction, features.sqi_scores, policy.action_history)
            action = policy.decide(prediction, safety)
            predictions.append(prediction.model_dump())
            safety_decisions.append(safety.model_dump())
            would_be_actions.append(action.model_dump())
    finally:
        await simulator.stop()

    report = {
        "report_id": report_id,
        "source": request.source,
        "profile_id": request.profile_id,
        "duration_seconds": request.duration_seconds,
        "predicted_states": predictions,
        "safety_decisions": safety_decisions,
        "would_be_actions": would_be_actions,
        "real_adaptation_actions_emitted": 0,
        "blocked_actions": sum(
            1
            for decision in safety_decisions
            if str(decision.get("decision", "")).lower() == "block"
        ),
        "scientific_note": (
            "Shadow mode computes what would have happened without adapting the corridor."
        ),
    }
    path = SHADOW_DIR / f"{report_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


async def _run_brainflow_shadow(request: ShadowStartRequest) -> dict[str, Any]:
    report_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_brainflow_shadow")
    profile = get_profile(request.profile_id) if request.profile_id else {}
    adapter = BrainFlowAcquisition({
        **profile,
        "profile_id": request.profile_id,
        "board_id": request.board_id if request.board_id is not None else profile.get("board_id"),
        "serial_port": request.serial_port or profile.get("serial_port"),
        "window_seconds": settings.tick_interval_s,
    })
    estimator = HeuristicStateEstimator()
    safety_gate = SafetyGate()
    policy = AdaptationPolicy()
    predictions = []
    safety_decisions = []
    would_be_actions = []
    sqi_values: list[float] = []
    timestamps: list[float] = []
    try:
        await adapter.start()
        end_time = datetime.now(timezone.utc).timestamp() + request.duration_seconds
        while datetime.now(timezone.utc).timestamp() < end_time:
            window = await adapter.get_window()
            features = extract_features_and_sqi(window)
            prediction = estimator.predict(features)
            safety = safety_gate.evaluate(prediction, features.sqi_scores, policy.action_history)
            action = policy.decide(prediction, safety)
            predictions.append(prediction.model_dump())
            safety_decisions.append(safety.model_dump())
            would_be_actions.append(action.model_dump())
            sqi = features.sqi_scores.get("multimodal")
            if sqi is not None:
                sqi_values.append(float(sqi))
            timestamps.extend(window.timestamps or [])
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        await adapter.stop()

    status = adapter.status()
    report = {
        "report_id": report_id,
        "source": request.source,
        "profile_id": request.profile_id,
        "calibration_id": request.calibration_id,
        "duration_seconds": request.duration_seconds,
        "board": {
            "board_name": status.get("board_name"),
            "board_id": status.get("board_id"),
            "physical_or_synthetic": status.get("physical_or_synthetic"),
            "serial_port": status.get("serial_port"),
        },
        "predicted_states": predictions,
        "safety_decisions": safety_decisions,
        "would_be_actions": would_be_actions,
        "real_adaptation_actions_emitted": 0,
        "closed_loop_allowed": False,
        "window_count": len(predictions),
        "blocked_actions": sum(
            1
            for decision in safety_decisions
            if str(decision.get("decision", "")).lower() == "block"
        ),
        "sqi_summary": {
            "count": len(sqi_values),
            "mean": round(sum(sqi_values) / len(sqi_values), 4) if sqi_values else None,
            "min": round(min(sqi_values), 4) if sqi_values else None,
            "max": round(max(sqi_values), 4) if sqi_values else None,
        },
        "timing": summarize_window_timing(
            timestamps,
            expected_rate_hz=float(status.get("sampling_rate") or 1.0),
            max_gap_ms=(1000.0 / float(status.get("sampling_rate") or 1.0)) * 5.0,
        ),
        "closed_loop_recommendation": "blocked: hardware shadow requires human review",
        "scientific_note": (
            "BrainFlow shadow mode computes would-be actions without adapting the corridor."
        ),
    }
    path = SHADOW_DIR / f"{report_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


async def _run_lsl_shadow(request: ShadowStartRequest) -> dict[str, Any]:
    report_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_lsl_shadow")
    adapter = LSLAcquisition({
        "stream_name": request.stream_name,
        "stream_type": request.stream_type,
        "source_id": request.source_id,
        "window_seconds": settings.tick_interval_s,
    })
    estimator = HeuristicStateEstimator()
    safety_gate = SafetyGate()
    policy = AdaptationPolicy()
    predictions = []
    safety_decisions = []
    would_be_actions = []
    sqi_values: list[float] = []
    timestamps: list[float] = []
    clock_offsets: list[float] = []
    windows: list[dict[str, Any]] = []
    raw_windows: list[dict[str, Any]] = []
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
            prediction = estimator.predict(features)
            safety = safety_gate.evaluate(prediction, features.sqi_scores, policy.action_history)
            action = policy.decide(prediction, safety)
            predictions.append(prediction.model_dump())
            safety_decisions.append(safety.model_dump())
            would_be_actions.append(action.model_dump())
            sqi = features.sqi_scores.get("multimodal")
            if sqi is not None:
                sqi_values.append(float(sqi))
            timestamps.extend(window.timestamps or [])
            if window.timestamps:
                windows.append({
                    "start_time": min(window.timestamps),
                    "end_time": max(window.timestamps),
                })
                raw_windows.append({
                    "start_time": min(window.timestamps),
                    "end_time": max(window.timestamps),
                    "data": window.data,
                    "sampling_rate": window.sampling_rate,
                    "channel_names": window.channel_names,
                })
            if window.metadata and window.metadata.get("clock_offset") is not None:
                clock_offsets.append(float(window.metadata["clock_offset"]))
    except Exception as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    finally:
        markers = marker_collector.stop()
        await adapter.stop()

    stream = adapter.status().get("selected_stream") or {}
    report = {
        "report_id": report_id,
        "source": request.source,
        "profile_id": request.profile_id,
        "calibration_id": request.calibration_id,
        "duration_seconds": request.duration_seconds,
        "stream_metadata": stream,
        "predicted_states": predictions,
        "safety_decisions": safety_decisions,
        "would_be_actions": would_be_actions,
        "real_adaptation_actions_emitted": 0,
        "window_count": len(predictions),
        "blocked_actions": sum(
            1
            for decision in safety_decisions
            if str(decision.get("decision", "")).lower() == "block"
        ),
        "sqi_summary": {
            "count": len(sqi_values),
            "mean": round(sum(sqi_values) / len(sqi_values), 4) if sqi_values else None,
        },
        "timing": summarize_window_timing(
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
        "marker_conditioned_summary": _marker_conditioned_summary(predictions, markers, windows),
        "event_classifier": _classifier_shadow_predictions(
            request.model_id,
            markers,
            raw_windows,
        ),
        "closed_loop_recommendation": "blocked: human review required",
        "scientific_note": (
            "LSL shadow mode computes would-be actions without adapting the corridor."
        ),
    }
    path = SHADOW_DIR / f"{report_id}.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def _marker_conditioned_summary(
    predictions: list[dict[str, Any]],
    markers: list[MarkerEvent],
    windows: list[dict[str, Any]],
) -> dict[str, Any]:
    if not predictions or not markers or not windows:
        return {}
    result: dict[str, dict[str, float]] = {}
    numeric_keys = [
        key
        for key, value in predictions[0].items()
        if isinstance(value, int | float) and key != "feature_window_ms"
    ]
    for marker in markers:
        idx = _window_index_for_marker(marker.timestamp, windows)
        if idx is None or idx >= len(predictions):
            continue
        bucket = result.setdefault(marker.label, {key: 0.0 for key in numeric_keys})
        count = bucket.get("_count", 0.0) + 1.0
        bucket["_count"] = count
        for key in numeric_keys:
            bucket[key] += float(predictions[idx].get(key, 0.0))
    for bucket in result.values():
        count = bucket.pop("_count", 1.0)
        for key, value in list(bucket.items()):
            bucket[key] = round(value / count, 4)
    return result


def _classifier_shadow_predictions(
    model_id: str | None,
    markers: list[MarkerEvent],
    raw_windows: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not model_id:
        return None
    try:
        model = load_model(model_id)
        metadata = get_model_metadata(model_id)
    except Exception as exc:
        return {"model_id": model_id, "available": False, "error": str(exc)}
    predictions = []
    for marker in markers:
        idx = _window_index_for_marker(marker.timestamp, raw_windows)
        if idx is None:
            continue
        window = raw_windows[idx]
        features = extract_epoch_features(
            np.asarray(window["data"], dtype=float),
            float(window["sampling_rate"]),
            list(window["channel_names"]),
        )
        vector = np.asarray([[float(features.get(name, 0.0)) for name in model.feature_names]])
        pred = model.predict(vector)[0]
        proba = model.predict_proba(vector)
        confidence = float(np.max(proba[0])) if proba is not None else None
        predictions.append({
            "marker_label": marker.label,
            "predicted_label": str(pred),
            "confidence": round(confidence, 4) if confidence is not None else None,
            "timestamp": marker.timestamp,
        })
    accuracy = None
    if predictions:
        accuracy = sum(
            1 for item in predictions if item["marker_label"] == item["predicted_label"]
        ) / len(predictions)
    return {
        "model_id": model_id,
        "available": True,
        "prediction_semantics": metadata.get("prediction_semantics"),
        "predictions": predictions,
        "accuracy_if_markers_available": round(accuracy, 4) if accuracy is not None else None,
        "real_adaptation_actions_emitted": 0,
        "scientific_note": (
            "Event classifier predictions are shadow-only task-label estimates, not closed-loop "
            "commands or thought decoding."
        ),
    }


def _window_index_for_marker(timestamp: float, windows: list[dict[str, Any]]) -> int | None:
    for idx, window in enumerate(windows):
        start = window.get("start_time")
        end = window.get("end_time")
        if start is not None and end is not None and float(start) <= timestamp <= float(end):
            return idx
    return None


@router.get("/{report_id}")
async def get_shadow_report(report_id: str) -> dict[str, Any]:
    path = SHADOW_DIR / f"{report_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Shadow report not found")
    return json.loads(path.read_text(encoding="utf-8"))
