from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean
from typing import Any

from pydantic import BaseModel, Field


class CalibrationProfile(BaseModel):
    """Session-local baseline profile for proxy normalization."""

    session_id: str
    baseline_focus: float
    baseline_relaxation: float
    baseline_workload: float
    baseline_stress: float
    baseline_fatigue: float
    baseline_imagery_engagement: float
    baseline_sqi: float | None = None
    duration_seconds: float
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = "Scores are proxy baselines for this session only; not clinical measures."


class SelfReport(BaseModel):
    session_id: str
    perceived_focus: int | None = Field(default=None, ge=1, le=7)
    perceived_relaxation: int | None = Field(default=None, ge=1, le=7)
    perceived_workload: int | None = Field(default=None, ge=1, le=7)
    perceived_stress: int | None = Field(default=None, ge=1, le=7)
    perceived_imagery_vividness: int | None = Field(default=None, ge=1, le=7)
    discomfort: int | None = Field(default=None, ge=1, le=7)
    notes: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


_STATE_KEYS = [
    "focus",
    "relaxation",
    "workload",
    "stress",
    "fatigue",
    "imagery_engagement",
]


def create_calibration_profile(
    session_id: str,
    state_payloads: list[dict[str, Any]],
    duration_seconds: float,
    sqi_values: list[float] | None = None,
) -> CalibrationProfile:
    if not state_payloads:
        raise ValueError("Calibration requires at least one state payload")
    averages = {
        key: _mean([payload.get(key) for payload in state_payloads])
        for key in _STATE_KEYS
    }
    return CalibrationProfile(
        session_id=session_id,
        baseline_focus=averages["focus"],
        baseline_relaxation=averages["relaxation"],
        baseline_workload=averages["workload"],
        baseline_stress=averages["stress"],
        baseline_fatigue=averages["fatigue"],
        baseline_imagery_engagement=averages["imagery_engagement"],
        baseline_sqi=_mean(sqi_values or []),
        duration_seconds=duration_seconds,
    )


def calibrate_state(
    state_payload: dict[str, Any],
    profile: CalibrationProfile,
) -> dict[str, float]:
    baselines = {
        "focus": profile.baseline_focus,
        "relaxation": profile.baseline_relaxation,
        "workload": profile.baseline_workload,
        "stress": profile.baseline_stress,
        "fatigue": profile.baseline_fatigue,
        "imagery_engagement": profile.baseline_imagery_engagement,
    }
    calibrated: dict[str, float] = {}
    for key, baseline in baselines.items():
        raw = state_payload.get(key)
        if isinstance(raw, int | float):
            calibrated[f"{key}_relative_to_baseline"] = round(float(raw) - baseline, 4)
    return calibrated


def _mean(values: list[Any]) -> float:
    numeric = [float(value) for value in values if isinstance(value, int | float)]
    if not numeric:
        return 0.0
    return round(mean(numeric), 4)
