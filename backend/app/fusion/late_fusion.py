from __future__ import annotations

import numpy as np

from app.schemas.state import StatePredictionPayload

MODALITY_WEIGHTS = {"eeg": 0.45, "physio": 0.30, "gaze": 0.25}

_NUMERIC_FIELDS = (
    "focus",
    "relaxation",
    "workload",
    "stress",
    "fatigue",
    "imagery_engagement",
    "confidence",
)

_FUSED_MODEL_VERSION = "late-fusion-v1"


def late_fusion(predictions: dict[str, StatePredictionPayload]) -> StatePredictionPayload:
    """Combine per-modality state predictions using static weights."""
    if not predictions:
        raise ValueError("late_fusion requires at least one modality prediction")

    present = [m for m in predictions if m in MODALITY_WEIGHTS]
    if present:
        raw = {m: MODALITY_WEIGHTS[m] for m in present}
        total_w = sum(raw.values())
        weights = {m: raw[m] / total_w for m in present}
    else:
        keys = list(predictions.keys())
        weights = {m: 1.0 / len(keys) for m in keys}

    fused: dict[str, float] = {}
    for field in _NUMERIC_FIELDS:
        fused[field] = float(
            np.clip(
                sum(weights[m] * getattr(predictions[m], field) for m in weights),
                0.0,
                1.0,
            )
        )

    fw_num = sum(weights[m] * predictions[m].feature_window_ms for m in weights)
    feature_window_ms = int(round(fw_num))

    return StatePredictionPayload(
        focus=fused["focus"],
        relaxation=fused["relaxation"],
        workload=fused["workload"],
        stress=fused["stress"],
        fatigue=fused["fatigue"],
        imagery_engagement=fused["imagery_engagement"],
        confidence=fused["confidence"],
        model_version=_FUSED_MODEL_VERSION,
        feature_window_ms=feature_window_ms,
    )
