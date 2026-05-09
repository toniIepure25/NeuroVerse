from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


class StateEstimator(ABC):
    @abstractmethod
    def predict(self, features: FeaturePayload) -> StatePredictionPayload: ...
