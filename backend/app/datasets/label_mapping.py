from __future__ import annotations

from collections.abc import Mapping
from typing import Any

PHASE_LABELS = [
    "baseline",
    "focus",
    "workload",
    "relaxation",
    "imagery",
    "noisy",
    "fatigue",
]

PHASE_TO_WORKLOAD_SCORE = {
    "baseline": 0.25,
    "focus": 0.45,
    "workload": 0.9,
    "relaxation": 0.15,
    "imagery": 0.55,
    "noisy": 0.5,
    "fatigue": 0.65,
}

WORKLOAD_CLASS_TO_SCORE = {
    "low": 0.15,
    "medium": 0.5,
    "moderate": 0.5,
    "high": 0.9,
}


def normalize_phase_label(raw: Any) -> str:
    text = str(raw).strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "increasing_focus": "focus",
        "high_workload": "workload",
        "relaxation_recovery": "relaxation",
        "imagery_engagement": "imagery",
        "noisy_period": "noisy",
        "fatigue_drift": "fatigue",
    }
    return aliases.get(text, text)


def workload_score_from_label(raw: Any) -> float:
    if raw is None:
        return 0.5
    if isinstance(raw, (int, float)):
        return float(max(0.0, min(1.0, raw)))
    label = normalize_phase_label(raw)
    if label in PHASE_TO_WORKLOAD_SCORE:
        return PHASE_TO_WORKLOAD_SCORE[label]
    return WORKLOAD_CLASS_TO_SCORE.get(label, 0.5)


def workload_class_from_score(score: float) -> str:
    if score < 0.34:
        return "low"
    if score < 0.67:
        return "medium"
    return "high"


def map_clare_workload(raw: Any, mapping: Mapping[str, float] | None = None) -> tuple[str, float]:
    label = str(raw).strip().lower()
    score_mapping = dict(mapping or WORKLOAD_CLASS_TO_SCORE)
    score = score_mapping.get(label, workload_score_from_label(label))
    return workload_class_from_score(score), float(max(0.0, min(1.0, score)))
