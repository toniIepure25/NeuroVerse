from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pandas as pd

from app.datasets.base import BaseDatasetAdapter
from app.datasets.label_mapping import workload_class_from_score, workload_score_from_label
from app.datasets.schemas import DatasetMetadata, WindowedSample
from app.datasets.windowing import align_point_labels, window_starts


class GenericCSVAdapter(BaseDatasetAdapter):
    """Config-driven adapter for local CSV data or precomputed features."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.path = self._resolve_path(config["path"])
        self.timestamp_col = str(config.get("timestamp_col", "timestamp"))
        self.label_col = config.get("label_col")
        self.subject_col = config.get("subject_id_col", "subject_id")
        self.session_col = config.get("session_id_col", "session_id")
        self.feature_cols = list(config.get("feature_cols") or [])
        self.window_size_s = float(config.get("window_size_seconds", 2.0))
        self.overlap = float(config.get("overlap", 0.5))
        self.sampling_rates = dict(config.get("sampling_rates") or {})

    def _resolve_path(self, raw_path: str) -> Path:
        path = Path(raw_path)
        if path.is_absolute():
            return path
        config_path = self.config.get("_config_path")
        if config_path:
            return (Path(config_path).parent / path).resolve()
        return path

    def _read(self) -> pd.DataFrame:
        return pd.read_csv(self.path)

    def load_metadata(self) -> DatasetMetadata:
        frame = self._read()
        modalities = []
        for key in ("eeg_cols", "physio_cols", "gaze_cols", "multimodal_cols"):
            if self.config.get(key):
                modalities.append(key.replace("_cols", ""))
        if self.feature_cols:
            modalities.append("features")
        subjects = (
            sorted(frame[self.subject_col].astype(str).unique().tolist())
            if self.subject_col in frame.columns
            else ["unknown_subject"]
        )
        sessions = (
            sorted(frame[self.session_col].astype(str).unique().tolist())
            if self.session_col in frame.columns
            else ["unknown_session"]
        )
        labels = [str(self.label_col)] if self.label_col else []
        if self.label_col and self.label_col in frame.columns:
            labels.extend(sorted(str(x) for x in frame[self.label_col].dropna().unique()))
        return DatasetMetadata(
            dataset_id=self.dataset_id,
            name=str(self.config.get("name", self.dataset_id)),
            version=str(self.config.get("version", "local-csv")),
            source="generic_csv",
            local_path=str(self.path),
            modalities=sorted(set(modalities)),
            sampling_rates={str(k): float(v) for k, v in self.sampling_rates.items()},
            subjects=subjects,
            sessions=sessions,
            labels=labels,
            notes=str(self.config.get("notes", "Local CSV adapter; schema is config-defined.")),
        )

    def iter_windows(self) -> Iterator[WindowedSample]:
        frame = self._read().sort_values(self.timestamp_col)
        if self.timestamp_col not in frame.columns:
            raise ValueError(f"Missing timestamp column: {self.timestamp_col}")
        group_cols = [c for c in [self.subject_col, self.session_col] if c in frame.columns]
        grouped = frame.groupby(group_cols, dropna=False) if group_cols else [("", frame)]
        sample_idx = 0
        for _, group in grouped:
            subject_id = (
                str(group[self.subject_col].iloc[0]) if self.subject_col in group else "unknown"
            )
            session_id = (
                str(group[self.session_col].iloc[0]) if self.session_col in group else "unknown"
            )
            t_min = float(group[self.timestamp_col].min())
            t_max = float(group[self.timestamp_col].max())
            for start in window_starts(t_min, t_max, self.window_size_s, self.overlap):
                end = start + self.window_size_s
                win = group[
                    (group[self.timestamp_col] >= start) & (group[self.timestamp_col] < end)
                ]
                if win.empty:
                    continue
                label = self._aligned_label(group, start, end)
                features = self._feature_window(win) if self.feature_cols else None
                data_by_modality = {} if features is not None else self._raw_window(win)
                score = workload_score_from_label(label)
                labels = {}
                if self.label_col:
                    labels[str(self.label_col)] = label
                    labels["label"] = label
                labels.setdefault("workload_score", score)
                labels.setdefault("workload_class", workload_class_from_score(score))
                yield WindowedSample(
                    sample_id=f"{self.dataset_id}:{sample_idx:06d}",
                    dataset_id=self.dataset_id,
                    subject_id=subject_id,
                    session_id=session_id,
                    start_time=start,
                    end_time=end,
                    modalities=list(data_by_modality.keys()) or ["features"],
                    data_by_modality=data_by_modality,
                    features=features,
                    labels=labels,
                    metadata={"source": "generic_csv"},
                )
                sample_idx += 1

    def _aligned_label(self, frame: pd.DataFrame, start: float, end: float) -> Any:
        if not self.label_col or self.label_col not in frame.columns:
            return None
        strategy = str(self.config.get("label_strategy", "majority"))
        return align_point_labels(
            frame[self.timestamp_col].to_numpy(),
            frame[self.label_col].to_numpy(),
            start,
            end,
            strategy=strategy,  # type: ignore[arg-type]
        )

    def _feature_window(self, frame: pd.DataFrame) -> dict[str, float]:
        missing = [c for c in self.feature_cols if c not in frame.columns]
        if missing:
            raise ValueError(f"Missing feature columns: {missing}")
        return {str(col): float(frame[col].mean()) for col in self.feature_cols}

    def _raw_window(self, frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
        out: dict[str, dict[str, Any]] = {}
        for modality, key in (
            ("eeg", "eeg_cols"),
            ("physio", "physio_cols"),
            ("gaze", "gaze_cols"),
            ("multimodal", "multimodal_cols"),
        ):
            cols = list(self.config.get(key) or [])
            if not cols:
                continue
            missing = [c for c in cols if c not in frame.columns]
            if missing:
                raise ValueError(f"Missing {modality} columns: {missing}")
            out[modality] = {
                "data": [frame[col].astype(float).tolist() for col in cols],
                "channel_names": cols,
                "sampling_rate": float(
                    self.sampling_rates.get(modality, self.config.get("sampling_rate", 1.0))
                ),
            }
        return out
