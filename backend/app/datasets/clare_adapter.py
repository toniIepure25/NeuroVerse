from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pandas as pd

from app.datasets.base import BaseDatasetAdapter
from app.datasets.label_mapping import map_clare_workload
from app.datasets.schemas import DatasetMetadata, WindowedSample
from app.datasets.windowing import align_point_labels, window_starts


class ClareLikeAdapter(BaseDatasetAdapter):
    """Flexible CLARE-like adapter.

    Expected local layout is intentionally simple and documented:
    ``signals.csv`` with timestamps and feature/signal columns, and optional ``labels.csv`` with
    timestamped workload labels. This is a compatibility layer, not validated full CLARE support.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.root = self._resolve_path(config["path"])
        self.signals_file = self.root / str(config.get("signals_file", "signals.csv"))
        self.labels_file = self.root / str(config.get("labels_file", "labels.csv"))
        self.timestamp_col = str(config.get("timestamp_col", "timestamp"))
        self.label_col = str(config.get("label_col", "workload_label"))
        self.subject_col = str(config.get("subject_id_col", "subject_id"))
        self.session_col = str(config.get("session_id_col", "session_id"))
        self.feature_cols = list(config.get("feature_cols") or [])
        self.window_size_s = float(config.get("window_size_seconds", 2.0))
        self.overlap = float(config.get("overlap", 0.5))

    def _resolve_path(self, raw_path: str) -> Path:
        path = Path(raw_path)
        if path.is_absolute():
            return path
        config_path = self.config.get("_config_path")
        if config_path:
            return (Path(config_path).parent / path).resolve()
        return path

    def _signals(self) -> pd.DataFrame:
        return pd.read_csv(self.signals_file)

    def _labels(self) -> pd.DataFrame:
        if self.labels_file.exists():
            return pd.read_csv(self.labels_file)
        return pd.DataFrame(columns=[self.timestamp_col, self.label_col])

    def load_metadata(self) -> DatasetMetadata:
        frame = self._signals()
        subjects = (
            sorted(frame[self.subject_col].astype(str).unique())
            if self.subject_col in frame
            else ["unknown"]
        )
        sessions = (
            sorted(frame[self.session_col].astype(str).unique())
            if self.session_col in frame
            else ["unknown"]
        )
        return DatasetMetadata(
            dataset_id=self.dataset_id,
            name=str(self.config.get("name", "CLARE-like local cognitive load dataset")),
            version=str(self.config.get("version", "assumption-v1")),
            source="clare_like_local",
            local_path=str(self.root),
            modalities=["eeg", "physio", "gaze", "features"],
            sampling_rates={
                str(k): float(v) for k, v in dict(self.config.get("sampling_rates") or {}).items()
            },
            subjects=[str(x) for x in subjects],
            sessions=[str(x) for x in sessions],
            labels=["workload_label", "workload_class", "workload_score"],
            notes=(
                "Fixture-compatible CLARE-like adapter. "
                "Real CLARE format assumptions must be verified locally."
            ),
        )

    def iter_windows(self) -> Iterator[WindowedSample]:
        signals = self._signals().sort_values(self.timestamp_col)
        labels = self._labels().sort_values(self.timestamp_col)
        group_cols = [c for c in [self.subject_col, self.session_col] if c in signals.columns]
        grouped = signals.groupby(group_cols, dropna=False) if group_cols else [("", signals)]
        idx = 0
        for _, group in grouped:
            subject_id = (
                str(group[self.subject_col].iloc[0]) if self.subject_col in group else "unknown"
            )
            session_id = (
                str(group[self.session_col].iloc[0]) if self.session_col in group else "unknown"
            )
            label_group = labels
            for col, value in ((self.subject_col, subject_id), (self.session_col, session_id)):
                if col in label_group.columns:
                    label_group = label_group[label_group[col].astype(str) == value]
            t_min = float(group[self.timestamp_col].min())
            t_max = float(group[self.timestamp_col].max())
            for start in window_starts(t_min, t_max, self.window_size_s, self.overlap):
                end = start + self.window_size_s
                win = group[
                    (group[self.timestamp_col] >= start) & (group[self.timestamp_col] < end)
                ]
                if win.empty:
                    continue
                raw_label = self._label_for_window(label_group, group, start, end)
                workload_class, workload_score = map_clare_workload(
                    raw_label, self.config.get("label_score_mapping")
                )
                features = self._features(win)
                yield WindowedSample(
                    sample_id=f"{self.dataset_id}:{idx:06d}",
                    dataset_id=self.dataset_id,
                    subject_id=subject_id,
                    session_id=session_id,
                    start_time=start,
                    end_time=end,
                    modalities=["features"],
                    features=features,
                    labels={
                        "workload_label": raw_label,
                        "workload_class": workload_class,
                        "workload_score": workload_score,
                    },
                    metadata={"source": "clare_like_fixture"},
                )
                idx += 1

    def _label_for_window(
        self,
        labels: pd.DataFrame,
        signals: pd.DataFrame,
        start: float,
        end: float,
    ) -> Any:
        source = labels if not labels.empty and self.label_col in labels.columns else signals
        if self.label_col not in source.columns:
            return None
        return align_point_labels(
            source[self.timestamp_col].to_numpy(),
            source[self.label_col].to_numpy(),
            start,
            end,
            strategy=str(self.config.get("label_strategy", "nearest_previous")),  # type: ignore[arg-type]
        )

    def _features(self, frame: pd.DataFrame) -> dict[str, float]:
        cols = self.feature_cols or [
            c
            for c in frame.columns
            if c not in {self.timestamp_col, self.subject_col, self.session_col, self.label_col}
            and pd.api.types.is_numeric_dtype(frame[c])
        ]
        return {str(col): float(frame[col].mean()) for col in cols}
