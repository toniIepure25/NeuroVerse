from __future__ import annotations

from app.core.numeric import clamp


def compute_multimodal_sqi(eeg_sqi: float, physio_sqi: float, gaze_sqi: float) -> float:
    """Fuse per-modality SQI with weights and penalties; result in [0, 1]."""
    a = clamp(float(eeg_sqi), 0.0, 1.0)
    b = clamp(float(physio_sqi), 0.0, 1.0)
    c = clamp(float(gaze_sqi), 0.0, 1.0)

    score = 0.4 * a + 0.3 * b + 0.3 * c

    if a < 0.3 or b < 0.3 or c < 0.3:
        score -= 0.15

    if a == 0.0 or b == 0.0 or c == 0.0:
        score -= 0.25

    return clamp(score, 0.0, 1.0)
