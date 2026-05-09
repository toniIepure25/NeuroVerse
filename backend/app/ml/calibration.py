from __future__ import annotations

import numpy as np
from sklearn.metrics import brier_score_loss


def calibration_metrics(
    y_true: np.ndarray,
    probabilities: np.ndarray | None,
    class_labels: list[str] | None = None,
    n_bins: int = 10,
) -> dict:
    if probabilities is None or len(probabilities) == 0:
        return {"available": False}
    probs = np.asarray(probabilities, dtype=float)
    labels = list(class_labels or [])
    if probs.ndim == 1:
        confidence = probs
        predicted = (probs >= 0.5).astype(int)
    else:
        confidence = probs.max(axis=1)
        predicted = probs.argmax(axis=1)

    y_idx = _label_indices(y_true, labels) if labels else np.asarray(y_true)
    correctness = (predicted == y_idx).astype(float)
    bins = []
    ece = 0.0
    mce = 0.0
    for lo in np.linspace(0.0, 1.0, n_bins, endpoint=False):
        hi = min(1.0, lo + 1.0 / n_bins)
        mask = (confidence >= lo) & (confidence < hi if hi < 1.0 else confidence <= hi)
        if not np.any(mask):
            bins.append(
                {"lo": float(lo), "hi": float(hi), "count": 0, "accuracy": None, "confidence": None}
            )
            continue
        acc = float(np.mean(correctness[mask]))
        conf = float(np.mean(confidence[mask]))
        gap = abs(acc - conf)
        ece += gap * float(np.mean(mask))
        mce = max(mce, gap)
        bins.append(
            {
                "lo": float(lo),
                "hi": float(hi),
                "count": int(mask.sum()),
                "accuracy": acc,
                "confidence": conf,
            }
        )

    out = {"available": True, "ece": float(ece), "mce": float(mce), "reliability_bins": bins}
    if probs.ndim == 2 and probs.shape[1] == 2:
        out["brier_score"] = float(brier_score_loss(y_idx, probs[:, 1]))
    return out


def _label_indices(y_true: np.ndarray, labels: list[str]) -> np.ndarray:
    lookup = {str(label): i for i, label in enumerate(labels)}
    return np.array([lookup.get(str(y), -1) for y in y_true], dtype=int)
