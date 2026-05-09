from __future__ import annotations

import numpy as np

from app.datasets.schemas import FeatureDataset
from app.ml.baselines import BaselineModelAdapter
from app.ml.metrics import evaluate_classification, measure_inference_latency


def evaluate_model_on_dataset(
    model: BaselineModelAdapter,
    dataset: FeatureDataset,
    indices: np.ndarray | None = None,
) -> dict:
    idx = indices if indices is not None else np.arange(len(dataset.y))
    x_values = dataset.X[idx]
    y = dataset.y[idx]
    pred = model.predict(x_values)
    probs = model.predict_proba(x_values)
    labels = [str(x) for x in getattr(model.estimator, "classes_", [])]
    if not labels and hasattr(model.estimator, "named_steps"):
        clf = model.estimator.named_steps.get("clf")
        labels = [str(x) for x in getattr(clf, "classes_", [])]
    metrics = evaluate_classification(y, pred, probs, labels or None)
    metrics["latency"] = measure_inference_latency(model, x_values)
    return metrics
