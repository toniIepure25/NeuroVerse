from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

from app.core.numeric import clamp


def _f(d: Mapping[str, Any], key: str, default: float = 0.5) -> float:
    v = d.get(key, default)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def extract_multimodal_features(
    eeg: dict[str, Any],
    physio: dict[str, Any],
    gaze: dict[str, Any],
) -> dict[str, float]:
    engagement = _f(eeg, "engagement_index", 0.5)
    fixation = _f(gaze, "fixation_stability", 0.5)
    stress = _f(physio, "stress_index", 0.5)
    relax_eeg = _f(eeg, "relaxation_index", 0.5)
    relax_hrv = _f(physio, "rmssd_proxy", 0.5)
    relax_eda = 1.0 - _f(physio, "eda_phasic", 0.5)

    inv_stress = clamp(1.0 - stress, 0.0, 1.0)
    cognitive_zone_score = clamp(
        0.40 * engagement + 0.35 * fixation + 0.25 * inv_stress,
        0.0,
        1.0,
    )

    arous_hi = clamp(
        0.5 * stress + 0.25 * (1.0 - relax_hrv) + 0.25 * _f(eeg, "beta_power", 0.5),
        0.0,
        1.0,
    )
    arous_lo = clamp(0.45 * relax_eeg + 0.35 * relax_hrv + 0.20 * relax_eda, 0.0, 1.0)
    denom = arous_hi + arous_lo + 1e-9
    arousal_balance = clamp(1.0 - abs(arous_hi - arous_lo) / denom, 0.0, 1.0)

    focus_stability = clamp(1.0 - abs(engagement - fixation), 0.0, 1.0)

    est_eeg = clamp(0.5 * engagement + 0.5 * _f(eeg, "fatigue_index", 0.5), 0.0, 1.0)
    est_physio = clamp(stress, 0.0, 1.0)
    est_gaze = clamp(1.0 - fixation, 0.0, 1.0)
    vec = np.array([est_eeg, est_physio, est_gaze], dtype=float)
    sensor_consensus = clamp(1.0 - float(np.std(vec)), 0.0, 1.0)

    modality_agreement = clamp(1.0 - float(np.var(vec)), 0.0, 1.0)

    return {
        "cognitive_zone_score": cognitive_zone_score,
        "arousal_balance": arousal_balance,
        "focus_stability": focus_stability,
        "sensor_consensus": sensor_consensus,
        "modality_agreement": modality_agreement,
    }
