from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
from scipy.signal import butter, sosfiltfilt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from app.acquisition.eeg_fixture import load_mne

DEFAULT_FBCSP_BANDS = [
    (8.0, 12.0),
    (12.0, 16.0),
    (16.0, 20.0),
    (20.0, 24.0),
    (24.0, 30.0),
]


class RawEpochModelAdapter:
    def __init__(
        self,
        model_type: str,
        estimator: Any,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.model_type = model_type
        self.estimator = estimator
        self._metadata = metadata or {}

    def fit(self, x: np.ndarray, y: np.ndarray) -> RawEpochModelAdapter:
        self.estimator.fit(x, y)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.estimator.predict(x)

    def predict_proba(self, x: np.ndarray) -> np.ndarray | None:
        if hasattr(self.estimator, "predict_proba"):
            return self.estimator.predict_proba(x)
        if hasattr(self.estimator, "decision_function"):
            scores = np.asarray(self.estimator.decision_function(x), dtype=float)
            if scores.ndim == 1:
                pos = 1.0 / (1.0 + np.exp(-scores))
                return np.vstack([1.0 - pos, pos]).T
            exp = np.exp(scores - np.max(scores, axis=1, keepdims=True))
            return exp / np.sum(exp, axis=1, keepdims=True)
        return None

    def save(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, out)
        return out

    @classmethod
    def load(cls, path: str | Path) -> RawEpochModelAdapter:
        return joblib.load(path)

    def metadata(self) -> dict[str, Any]:
        return {"model_type": self.model_type, **self._metadata}


def create_raw_epoch_model(
    model_type: str,
    *,
    n_components: int = 4,
    random_state: int = 42,
    sampling_rate: float = 160.0,
    bands: list[tuple[float, float]] | None = None,
) -> RawEpochModelAdapter:
    mne = load_mne()
    model_key = model_type.lower()
    if model_key in {"fbcsp_logreg", "fbcsp_lda"}:
        classifier = "lda" if model_key == "fbcsp_lda" else "logreg"
        return FBCSPModelAdapter(
            model_key,
            n_components=int(n_components),
            sampling_rate=float(sampling_rate),
            bands=bands or DEFAULT_FBCSP_BANDS,
            classifier=classifier,
            random_state=random_state,
        )
    csp = mne.decoding.CSP(
        n_components=int(n_components),
        reg=None,
        log=True,
        norm_trace=False,
    )
    if model_key == "csp_lda":
        clf = LinearDiscriminantAnalysis()
    elif model_key == "csp_logreg":
        clf = LogisticRegression(max_iter=1000, random_state=random_state)
    elif model_key in {"csp_svm_linear", "csp_linear_svm"}:
        clf = SVC(kernel="linear", probability=True, random_state=random_state)
        model_key = "csp_svm_linear"
    else:
        raise ValueError(f"Unknown raw epoch model type: {model_type}")
    return RawEpochModelAdapter(
        model_key,
        Pipeline([("csp", csp), ("clf", clf)]),
        metadata={
            "raw_epoch_model": True,
            "spatial_filter": "mne.decoding.CSP",
            "csp_components": int(n_components),
        },
    )


class FBCSPModelAdapter(RawEpochModelAdapter):
    def __init__(
        self,
        model_type: str,
        *,
        n_components: int,
        sampling_rate: float,
        bands: list[tuple[float, float]],
        classifier: str,
        random_state: int,
    ) -> None:
        super().__init__(
            model_type,
            estimator=None,
            metadata={
                "raw_epoch_model": True,
                "spatial_filter": "filter_bank_mne.decoding.CSP",
                "csp_components": int(n_components),
                "filter_bank_bands": [list(band) for band in bands],
                "sampling_rate_hz": float(sampling_rate),
                "classifier": classifier,
            },
        )
        self.n_components = int(n_components)
        self.sampling_rate = float(sampling_rate)
        self.bands = [(float(low), float(high)) for low, high in bands]
        self.classifier_name = classifier
        self.random_state = int(random_state)
        self.csps: list[Any] = []
        self.classifier: Any | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> FBCSPModelAdapter:
        mne = load_mne()
        features = []
        self.csps = []
        for band in self.bands:
            filtered = _bandpass_epochs(x, self.sampling_rate, band)
            csp = mne.decoding.CSP(
                n_components=self.n_components,
                reg=None,
                log=True,
                norm_trace=False,
            )
            features.append(csp.fit_transform(filtered, y))
            self.csps.append(csp)
        train_features = np.concatenate(features, axis=1)
        self.classifier = self._new_classifier()
        self.classifier.fit(train_features, y)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self._require_classifier().predict(self._transform(x))

    def predict_proba(self, x: np.ndarray) -> np.ndarray | None:
        clf = self._require_classifier()
        features = self._transform(x)
        if hasattr(clf, "predict_proba"):
            return clf.predict_proba(features)
        if hasattr(clf, "decision_function"):
            scores = np.asarray(clf.decision_function(features), dtype=float)
            if scores.ndim == 1:
                pos = 1.0 / (1.0 + np.exp(-scores))
                return np.vstack([1.0 - pos, pos]).T
        return None

    def _transform(self, x: np.ndarray) -> np.ndarray:
        if not self.csps:
            raise RuntimeError("FBCSP model has not been fit.")
        features = []
        for band, csp in zip(self.bands, self.csps, strict=False):
            features.append(csp.transform(_bandpass_epochs(x, self.sampling_rate, band)))
        return np.concatenate(features, axis=1)

    def _new_classifier(self) -> Any:
        if self.classifier_name == "lda":
            return LinearDiscriminantAnalysis()
        return LogisticRegression(max_iter=1000, random_state=self.random_state)

    def _require_classifier(self) -> Any:
        if self.classifier is None:
            raise RuntimeError("FBCSP classifier has not been fit.")
        return self.classifier


def _bandpass_epochs(
    x: np.ndarray,
    sampling_rate: float,
    band: tuple[float, float],
) -> np.ndarray:
    nyquist = sampling_rate / 2.0
    low = max(float(band[0]), 0.001)
    high = min(float(band[1]), nyquist - 0.001)
    if not low < high:
        return np.asarray(x, dtype=float)
    sos = butter(4, [low, high], btype="bandpass", fs=sampling_rate, output="sos")
    return sosfiltfilt(sos, np.asarray(x, dtype=float), axis=2)
