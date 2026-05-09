"""ONNX Runtime model loader for state estimation (future implementation).

Integration path:
1. Export a trained model (PyTorch, sklearn, etc.) to ONNX format
2. Place the .onnx file in the models/ directory
3. Configure the model path in NeuroVerseSettings
4. This loader handles input/output tensor mapping

Expected usage:
    estimator = ONNXStateEstimator(model_path="models/state_estimator_v1.onnx")
    prediction = estimator.predict(features)

Requirements:
    pip install onnxruntime
"""

from __future__ import annotations

from app.inference.base import StateEstimator
from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


class ONNXStateEstimator(StateEstimator):
    """Load and run an ONNX model for cognitive state estimation."""

    def __init__(self, model_path: str = "models/state_estimator.onnx") -> None:
        self.model_path = model_path
        self._session = None

    def predict(self, features: FeaturePayload) -> StatePredictionPayload:
        raise NotImplementedError(
            f"ONNX model not available at {self.model_path}. "
            "Export a trained model to ONNX format first. See models/README.md"
        )
