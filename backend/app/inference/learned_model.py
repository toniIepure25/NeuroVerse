from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from app.datasets.label_mapping import workload_score_from_label
from app.inference.base import StateEstimator
from app.ml.baselines import BaselineModelAdapter
from app.ml.registry import get_model_metadata, load_model
from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


class LearnedModelEstimator(StateEstimator):
    """StateEstimator wrapper for honest learned baselines.

    The model may predict a phase, workload class, motor-intent class, or direct state regression.
    Mapping to NeuroVerse state scores is intentionally conservative and metadata-driven.
    """

    def __init__(
        self,
        model: BaselineModelAdapter,
        metadata: dict[str, Any],
    ) -> None:
        self.model = model
        self.metadata = metadata
        self.feature_names = list(metadata.get("feature_names") or model.feature_names)
        self.semantics = str(metadata.get("prediction_semantics", "phase_proxy"))
        self.model_id = str(metadata.get("model_id", "learned_model"))

    @classmethod
    def from_model_dir(cls, model_dir: str | Path) -> LearnedModelEstimator:
        path = Path(model_dir)
        model = load_model(path)
        try:
            metadata = get_model_metadata(path.name, path.parent)
        except FileNotFoundError:
            metadata = model.metadata()
            metadata["model_id"] = path.name
        return cls(model, metadata)

    def predict(self, features: FeaturePayload) -> StatePredictionPayload:
        row = np.array(
            [[self._flatten_features(features).get(name, 0.0) for name in self.feature_names]],
            dtype=float,
        )
        pred = self.model.predict(row)[0]
        probs = self.model.predict_proba(row)
        confidence = float(np.max(probs)) if probs is not None else 0.6
        if self.semantics == "workload_proxy":
            return self._map_workload(pred, confidence)
        if self.semantics == "motor_intent":
            return self._map_motor_intent(pred, confidence)
        if self.semantics == "state_regression":
            return self._map_state_regression(pred, confidence)
        return self._map_phase(pred, confidence)

    def _flatten_features(self, features: FeaturePayload) -> dict[str, float]:
        out: dict[str, float] = {}
        for prefix, values in (
            ("eeg", features.eeg),
            ("physio", features.physio),
            ("gaze", features.gaze),
            ("multimodal", features.multimodal),
            ("sqi", features.sqi_scores),
        ):
            for key, value in values.items():
                try:
                    out[f"{prefix}_{key}"] = float(value)
                except (TypeError, ValueError):
                    out[f"{prefix}_{key}"] = 0.0
        return out

    def _base(self, confidence: float) -> dict[str, float | str | int]:
        return {
            "focus": 0.5,
            "relaxation": 0.5,
            "workload": 0.5,
            "stress": 0.35,
            "fatigue": 0.25,
            "imagery_engagement": 0.25,
            "confidence": float(np.clip(confidence, 0.0, 1.0)),
            "model_version": f"learned:{self.model_id}",
            "feature_window_ms": int(self.metadata.get("feature_window_ms", 1000)),
        }

    def _map_phase(self, pred: Any, confidence: float) -> StatePredictionPayload:
        label = str(pred)
        state = self._base(confidence)
        if label == "focus":
            state.update({"focus": 0.82, "workload": 0.45, "stress": 0.25})
        elif label == "workload":
            state.update({"workload": 0.85, "stress": 0.65, "focus": 0.55})
        elif label == "relaxation":
            state.update({"relaxation": 0.85, "stress": 0.15, "workload": 0.2})
        elif label == "imagery":
            state.update({"imagery_engagement": 0.82, "focus": 0.55})
        elif label == "noisy":
            state.update({"confidence": min(float(state["confidence"]), 0.25)})
        elif label == "fatigue":
            state.update({"fatigue": 0.85, "focus": 0.25, "workload": 0.55})
        elif label == "baseline":
            state.update({"stress": 0.25, "workload": 0.25})
        return StatePredictionPayload(**state)  # type: ignore[arg-type]

    def _map_workload(self, pred: Any, confidence: float) -> StatePredictionPayload:
        score = workload_score_from_label(pred)
        state = self._base(confidence)
        state.update(
            {
                "workload": score,
                "stress": min(1.0, 0.25 + 0.45 * score),
                "relaxation": max(0.0, 0.75 - 0.55 * score),
            }
        )
        return StatePredictionPayload(**state)  # type: ignore[arg-type]

    def _map_motor_intent(self, pred: Any, confidence: float) -> StatePredictionPayload:
        state = self._base(confidence)
        state.update(
            {
                "imagery_engagement": 0.75 if str(pred) != "rest" else 0.25,
                "stress": 0.3,
                "workload": 0.45,
            }
        )
        return StatePredictionPayload(**state)  # type: ignore[arg-type]

    def _map_state_regression(self, pred: Any, confidence: float) -> StatePredictionPayload:
        arr = np.asarray(pred, dtype=float).reshape(-1)
        names = ["focus", "relaxation", "workload", "stress", "fatigue", "imagery_engagement"]
        state = self._base(confidence)
        for name, value in zip(names, arr, strict=False):
            state[name] = float(np.clip(value, 0.0, 1.0))
        return StatePredictionPayload(**state)  # type: ignore[arg-type]
