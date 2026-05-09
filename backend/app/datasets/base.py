from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any

from app.datasets.schemas import DatasetMetadata, FeatureDataset, RawDatasetRecord, WindowedSample


class BaseDatasetAdapter(ABC):
    """Common interface for local dataset replay and feature generation."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.dataset_id = str(config.get("dataset_id", config.get("id", "dataset")))

    @abstractmethod
    def load_metadata(self) -> DatasetMetadata: ...

    def iter_raw_records(self) -> Iterator[RawDatasetRecord]:
        return iter(())

    @abstractmethod
    def iter_windows(self) -> Iterator[WindowedSample]: ...

    def to_feature_dataset(self, target: str | None = None) -> FeatureDataset:
        from app.ml.feature_dataset import build_feature_dataset

        return build_feature_dataset(list(self.iter_windows()), target=target)

    def get_label_space(self) -> list[str]:
        return self.load_metadata().labels

    def get_sampling_info(self) -> dict[str, float]:
        return self.load_metadata().sampling_rates

    def validate(self) -> dict[str, Any]:
        metadata = self.load_metadata()
        return {
            "ok": True,
            "dataset_id": metadata.dataset_id,
            "modalities": metadata.modalities,
            "labels": metadata.labels,
            "notes": metadata.notes,
        }
