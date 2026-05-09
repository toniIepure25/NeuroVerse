from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass(slots=True)
class DatasetMetadata:
    dataset_id: str
    name: str
    version: str = "unknown"
    source: str = "local"
    local_path: str | None = None
    modalities: list[str] = field(default_factory=list)
    sampling_rates: dict[str, float] = field(default_factory=dict)
    subjects: list[str] = field(default_factory=list)
    sessions: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "version": self.version,
            "source": self.source,
            "local_path": self.local_path,
            "modalities": self.modalities,
            "sampling_rates": self.sampling_rates,
            "subjects": self.subjects,
            "sessions": self.sessions,
            "labels": self.labels,
            "notes": self.notes,
        }


@dataclass(slots=True)
class RawDatasetRecord:
    subject_id: str
    session_id: str
    timestamp: float
    modality: str
    channel_names: list[str]
    sampling_rate: float
    data: list[list[float]]
    trial_id: str | None = None
    label: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WindowedSample:
    sample_id: str
    dataset_id: str
    subject_id: str
    session_id: str
    start_time: float
    end_time: float
    modalities: list[str]
    data_by_modality: dict[str, dict[str, Any]] = field(default_factory=dict)
    features: dict[str, float] | None = None
    labels: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FeatureDataset:
    X: np.ndarray
    y: np.ndarray
    feature_names: list[str]
    label_names: list[str]
    groups: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_frame(self) -> pd.DataFrame:
        frame = pd.DataFrame(self.X, columns=self.feature_names)
        for i, name in enumerate(self.label_names):
            if self.y.ndim == 1:
                frame[name] = self.y
            else:
                frame[name] = self.y[:, i]
        frame["group"] = self.groups
        return frame

    @classmethod
    def from_frame(
        cls,
        frame: pd.DataFrame,
        feature_names: list[str],
        label_names: list[str],
        metadata: dict[str, Any] | None = None,
    ) -> FeatureDataset:
        groups = (
            frame["group"].astype(str).tolist() if "group" in frame.columns else [""] * len(frame)
        )
        y_data = frame[label_names].to_numpy()
        if len(label_names) == 1:
            y_data = y_data.reshape(-1)
        return cls(
            X=frame[feature_names].to_numpy(dtype=float),
            y=y_data,
            feature_names=feature_names,
            label_names=label_names,
            groups=groups,
            metadata=metadata or {},
        )

    def save_npz(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            out,
            X=self.X,
            y=self.y,
            feature_names=np.array(self.feature_names, dtype=object),
            label_names=np.array(self.label_names, dtype=object),
            groups=np.array(self.groups, dtype=object),
            metadata=np.array([self.metadata], dtype=object),
        )
        return out

    @classmethod
    def load_npz(cls, path: str | Path) -> FeatureDataset:
        data = np.load(Path(path), allow_pickle=True)
        metadata_arr = data.get("metadata")
        metadata = dict(metadata_arr[0]) if metadata_arr is not None and len(metadata_arr) else {}
        return cls(
            X=data["X"],
            y=data["y"],
            feature_names=[str(x) for x in data["feature_names"].tolist()],
            label_names=[str(x) for x in data["label_names"].tolist()],
            groups=[str(x) for x in data["groups"].tolist()],
            metadata=metadata,
        )
