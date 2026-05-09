from __future__ import annotations

import time
from typing import Any

import numpy as np
from scipy import stats
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)
from sklearn.preprocessing import label_binarize

from app.ml.calibration import calibration_metrics


def evaluate_classification(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    probabilities: np.ndarray | None = None,
    class_labels: list[str] | None = None,
) -> dict[str, Any]:
    labels = class_labels or [str(x) for x in sorted(np.unique(np.concatenate([y_true, y_pred])))]
    metrics: dict[str, Any] = {
        "task_type": "classification",
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        "per_class": classification_report(y_true, y_pred, output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=labels).tolist(),
        "class_labels": labels,
    }
    if probabilities is not None:
        metrics["calibration"] = calibration_metrics(y_true, probabilities, labels)
        try:
            if len(np.unique(y_true)) != len(labels):
                raise ValueError("AUROC skipped because not all classes are present in y_true")
            y_bin = label_binarize(y_true, classes=labels)
            probs = np.asarray(probabilities, dtype=float)
            if probs.shape[1] == 2:
                value = float(roc_auc_score(y_bin[:, 0], probs[:, 1]))
                metrics["auroc"] = value if np.isfinite(value) else None
            elif probs.shape[1] == len(labels):
                value = float(roc_auc_score(y_bin, probs, average="macro", multi_class="ovr"))
                metrics["auroc_ovr_macro"] = value if np.isfinite(value) else None
        except Exception:
            metrics["auroc"] = None
    else:
        metrics["calibration"] = {"available": False}
    return metrics


def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, Any]:
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    return {
        "task_type": "regression",
        "mae": float(mean_absolute_error(yt, yp)),
        "rmse": float(mean_squared_error(yt, yp) ** 0.5),
        "r2": float(r2_score(yt, yp)),
        "pearson_r": float(stats.pearsonr(yt, yp).statistic) if len(yt) > 1 else None,
        "spearman_r": float(stats.spearmanr(yt, yp).statistic) if len(yt) > 1 else None,
    }


def measure_inference_latency(
    model: Any,
    x_values: np.ndarray,
    repeats: int = 1,
) -> dict[str, float]:
    durations: list[float] = []
    for row in x_values:
        sample = row.reshape(1, -1)
        for _ in range(repeats):
            t0 = time.perf_counter()
            model.predict(sample)
            durations.append((time.perf_counter() - t0) * 1000.0)
    arr = np.asarray(durations, dtype=float)
    return {
        "mean_inference_latency_ms": float(np.mean(arr)),
        "p95_inference_latency_ms": float(np.percentile(arr, 95)),
        "p99_inference_latency_ms": float(np.percentile(arr, 99)),
        "throughput_samples_per_sec": float(1000.0 / max(np.mean(arr), 1e-9)),
    }
