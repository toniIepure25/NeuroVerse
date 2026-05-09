"""Conformal prediction uncertainty quantification (future implementation).

Conformal prediction can provide distribution-free prediction intervals
for state estimates, enabling the safety gate to use statistically
valid uncertainty bounds rather than heuristic thresholds.

Future implementation:
1. Collect calibration set of (features, true_state) pairs
2. Compute nonconformity scores on held-out calibration data
3. At inference, produce prediction sets at a target coverage level (e.g. 90%)
4. If prediction set is wide, reduce confidence -> trigger WAIT/BLOCKED

References:
- Shafer & Vovk, "A Tutorial on Conformal Prediction" (2008)
- Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction" (2022)
"""

from __future__ import annotations


class ConformalPredictor:
    """Stub for conformal prediction-based uncertainty estimation."""

    def __init__(self, coverage: float = 0.90) -> None:
        self.coverage = coverage

    def calibrate(self, scores: list[float]) -> None:
        raise NotImplementedError("Conformal prediction calibration not yet implemented")

    def predict_set(self, point_prediction: float) -> tuple[float, float]:
        raise NotImplementedError("Conformal prediction inference not yet implemented")
