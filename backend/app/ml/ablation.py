from __future__ import annotations

import numpy as np

from app.datasets.schemas import FeatureDataset


def prefixes_for_modality_set(name: str) -> list[str]:
    key = name.lower().replace(" ", "")
    if key in {"all", "all_modalities"}:
        return ["eeg_", "physio_", "gaze_", "multimodal_"]
    if key in {"all+sqi", "all_with_sqi", "sqi_weighted"}:
        return ["eeg_", "physio_", "gaze_", "multimodal_", "sqi_"]
    prefixes: list[str] = []
    for part in key.split("+"):
        if part in {"eeg", "physio", "gaze", "multimodal", "sqi"}:
            prefixes.append(f"{part}_")
    if not prefixes:
        raise ValueError(f"Unknown ablation set: {name}")
    return prefixes


def filter_feature_dataset(dataset: FeatureDataset, modality_set: str) -> FeatureDataset:
    prefixes = prefixes_for_modality_set(modality_set)
    keep = [
        i
        for i, name in enumerate(dataset.feature_names)
        if any(name.startswith(p) for p in prefixes)
    ]
    if not keep:
        raise ValueError(f"No features matched ablation set {modality_set}")
    return FeatureDataset(
        X=dataset.X[:, np.asarray(keep, dtype=int)],
        y=dataset.y,
        feature_names=[dataset.feature_names[i] for i in keep],
        label_names=dataset.label_names,
        groups=dataset.groups,
        metadata={**dataset.metadata, "ablation_set": modality_set},
    )
