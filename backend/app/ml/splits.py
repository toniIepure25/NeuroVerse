from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.model_selection import GroupShuffleSplit, train_test_split

from app.datasets.schemas import FeatureDataset


def make_split_indices(
    dataset: FeatureDataset,
    config: dict[str, Any] | None = None,
) -> dict[str, np.ndarray]:
    cfg = config or {}
    split_type = str(cfg.get("type", "stratified"))
    train_size = float(cfg.get("train_size", 0.7))
    val_size = float(cfg.get("val_size", 0.15))
    test_size = float(cfg.get("test_size", 0.15))
    seed = int(cfg.get("seed", 42))
    n = len(dataset.y)
    indices = np.arange(n)
    if n < 3:
        return {"train": indices, "val": np.array([], dtype=int), "test": np.array([], dtype=int)}

    if split_type == "temporal":
        train_end = max(1, int(n * train_size))
        val_end = max(train_end, int(n * (train_size + val_size)))
        return {
            "train": indices[:train_end],
            "val": indices[train_end:val_end],
            "test": indices[val_end:],
        }

    if split_type.startswith("group"):
        groups = np.asarray(dataset.groups)
        gss = GroupShuffleSplit(n_splits=1, train_size=train_size, random_state=seed)
        train_idx, rest_idx = next(gss.split(dataset.X, dataset.y, groups))
        if len(rest_idx) < 2:
            return {"train": train_idx, "val": np.array([], dtype=int), "test": rest_idx}
        rest_groups = groups[rest_idx]
        rel_test = test_size / max(test_size + val_size, 1e-9)
        gss2 = GroupShuffleSplit(n_splits=1, test_size=rel_test, random_state=seed + 1)
        val_rel, test_rel = next(gss2.split(dataset.X[rest_idx], dataset.y[rest_idx], rest_groups))
        return {"train": train_idx, "val": rest_idx[val_rel], "test": rest_idx[test_rel]}

    stratify = dataset.y if split_type == "stratified" and _can_stratify(dataset.y) else None
    train_idx, rest_idx = train_test_split(
        indices,
        train_size=train_size,
        random_state=seed,
        stratify=stratify,
    )
    if len(rest_idx) < 2:
        return {"train": train_idx, "val": np.array([], dtype=int), "test": rest_idx}
    rest_y = dataset.y[rest_idx]
    rest_strat = rest_y if split_type == "stratified" and _can_stratify(rest_y) else None
    rel_test = test_size / max(test_size + val_size, 1e-9)
    val_idx, test_idx = train_test_split(
        rest_idx,
        test_size=rel_test,
        random_state=seed + 1,
        stratify=rest_strat,
    )
    return {"train": train_idx, "val": val_idx, "test": test_idx}


def _can_stratify(y: np.ndarray) -> bool:
    _, counts = np.unique(y, return_counts=True)
    return bool(len(counts) > 1 and np.all(counts >= 2))


def leakage_warnings(dataset: FeatureDataset, splits: dict[str, np.ndarray]) -> list[str]:
    warnings: list[str] = []
    split_groups = {
        name: set(np.asarray(dataset.groups)[idx].tolist()) for name, idx in splits.items()
    }
    for left, right in (("train", "val"), ("train", "test"), ("val", "test")):
        overlap = split_groups[left] & split_groups[right]
        if overlap:
            warnings.append(f"Group leakage between {left} and {right}: {sorted(overlap)[:5]}")
    _, counts = np.unique(dataset.y, return_counts=True)
    if len(counts) > 1 and counts.min() / counts.sum() < 0.1:
        warnings.append(
            "Label imbalance detected; use balanced metrics and group-aware validation."
        )
    if len(splits.get("test", [])) < 5:
        warnings.append("Test split is small; metrics may be unstable.")
    return warnings
