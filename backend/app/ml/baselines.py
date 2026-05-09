from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class BaselineModelAdapter:
    def __init__(
        self,
        model_type: str,
        estimator: Any,
        feature_names: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.model_type = model_type
        self.estimator = estimator
        self.feature_names = feature_names or []
        self._metadata = metadata or {}

    def fit(self, x: np.ndarray, y: np.ndarray) -> BaselineModelAdapter:
        self.estimator.fit(x, y)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.estimator.predict(x)

    def predict_proba(self, x: np.ndarray) -> np.ndarray | None:
        if hasattr(self.estimator, "predict_proba"):
            return self.estimator.predict_proba(x)
        if hasattr(self.estimator, "decision_function"):
            scores = self.estimator.decision_function(x)
            arr = np.asarray(scores, dtype=float)
            if arr.ndim == 1:
                pos = 1.0 / (1.0 + np.exp(-arr))
                return np.vstack([1.0 - pos, pos]).T
            exp = np.exp(arr - np.max(arr, axis=1, keepdims=True))
            return exp / np.sum(exp, axis=1, keepdims=True)
        return None

    def save(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, out)
        return out

    @classmethod
    def load(cls, path: str | Path) -> BaselineModelAdapter:
        return joblib.load(path)

    def metadata(self) -> dict[str, Any]:
        return {
            "model_type": self.model_type,
            "feature_names": self.feature_names,
            **self._metadata,
        }


def create_baseline_model(
    model_type: str,
    params: dict[str, Any] | None = None,
    feature_names: list[str] | None = None,
) -> BaselineModelAdapter:
    params = dict(params or {})
    model_key = model_type.lower()
    seed = int(params.pop("random_state", params.pop("seed", 42)))
    if model_key in {"logistic_regression", "logistic"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("scale", StandardScaler()),
                (
                    "clf",
                    LogisticRegression(
                        max_iter=int(params.pop("max_iter", 1000)), random_state=seed, **params
                    ),
                ),
            ]
        )
    elif model_key in {"ridge", "ridge_classifier"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("scale", StandardScaler()),
                ("clf", RidgeClassifier(**params)),
            ]
        )
    elif model_key in {"random_forest", "rf"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("clf", RandomForestClassifier(random_state=seed, **params)),
            ]
        )
    elif model_key in {"hist_gradient_boosting", "gradient_boosting", "hgb"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("clf", HistGradientBoostingClassifier(random_state=seed, **params)),
            ]
        )
    elif model_key in {"mlp", "mlp_classifier"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("scale", StandardScaler()),
                (
                    "clf",
                    MLPClassifier(
                        random_state=seed, max_iter=int(params.pop("max_iter", 500)), **params
                    ),
                ),
            ]
        )
    elif model_key in {"svm_linear", "linear_svm"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("scale", StandardScaler()),
                (
                    "clf",
                    SVC(
                        kernel="linear",
                        probability=True,
                        random_state=seed,
                        **params,
                    ),
                ),
            ]
        )
    elif model_key in {"svm_rbf", "rbf_svm"}:
        estimator = Pipeline(
            [
                ("impute", SimpleImputer()),
                ("scale", StandardScaler()),
                (
                    "clf",
                    SVC(
                        kernel="rbf",
                        probability=True,
                        random_state=seed,
                        **params,
                    ),
                ),
            ]
        )
    else:
        raise ValueError(f"Unknown baseline model type: {model_type}")
    return BaselineModelAdapter(model_key, estimator, feature_names=feature_names)
