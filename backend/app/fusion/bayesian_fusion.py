from __future__ import annotations

import numpy as np

from app.schemas.state import StatePredictionPayload

_NUMERIC_FIELDS = (
    "focus",
    "relaxation",
    "workload",
    "stress",
    "fatigue",
    "imagery_engagement",
    "confidence",
)

_FUSED_MODEL_VERSION = "bayesian-fusion-v1"
SQI_EXCLUDE_BELOW = 0.2


def bayesian_fusion(
    predictions: dict[str, StatePredictionPayload],
    sqi_scores: dict[str, float],
) -> StatePredictionPayload:
    """SQI-weighted fusion: modalities with higher signal quality get more weight."""
    if not predictions:
        raise ValueError("bayesian_fusion requires at least one modality prediction")

    modalities = list(predictions.keys())
    sqis: dict[str, float] = {}
    for m in modalities:
        raw = sqi_scores.get(m, 0.5)
        try:
            s = float(raw)
        except (TypeError, ValueError):
            s = 0.5
        sqis[m] = float(np.clip(s, 0.0, 1.0))

    included = [m for m in modalities if sqis[m] >= SQI_EXCLUDE_BELOW]
    if not included:
        included = modalities
        weights = {m: 1.0 / len(included) for m in included}
    else:
        ssum = float(sum(sqis[m] for m in included))
        if ssum <= 0.0:
            weights = {m: 1.0 / len(included) for m in included}
        else:
            weights = {m: sqis[m] / ssum for m in included}

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
