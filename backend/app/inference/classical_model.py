from __future__ import annotations

from app.inference.base import StateEstimator
from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


class ClassicalStateEstimator(StateEstimator):
    """Placeholder for scikit-learn based state estimation.

    Future implementation:
    1. Collect labeled feature vectors from calibration sessions
    2. Train a RandomForest/GradientBoosting per cognitive dimension
    3. Export models as .joblib files
    4. Load and predict here
    """

    def __init__(self, model_path: str | None = None):
        self.model_path = model_path
        self.models: dict = {}

    def predict(self, features: FeaturePayload) -> StatePredictionPayload:
        raise NotImplementedError(
            "Classical model not yet trained. Use HeuristicStateEstimator."
        )
