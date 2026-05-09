from __future__ import annotations

import asyncio
from collections.abc import Iterator
from typing import Any

import numpy as np

from app.acquisition.simulator import BiosignalSimulator
from app.datasets.base import BaseDatasetAdapter
from app.datasets.label_mapping import (
    PHASE_LABELS,
    workload_class_from_score,
    workload_score_from_label,
)
from app.datasets.schemas import DatasetMetadata, RawDatasetRecord, WindowedSample


def phase_label_at(t: float, duration_s: float) -> str:
    base_edges = np.array([0.0, 30, 60, 90, 120, 150, 170, 180], dtype=float)
    edges = base_edges * (duration_s / 180.0)
    wrapped = float(np.mod(t, duration_s))
    for i in range(len(edges) - 1):
        if edges[i] <= wrapped < edges[i + 1]:
            return PHASE_LABELS[i]
    return "fatigue"


class SyntheticDatasetAdapter(BaseDatasetAdapter):
    """Dataset adapter exposing the existing simulator as deterministic labeled windows."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.duration_s = float(config.get("duration_seconds", config.get("duration_s", 180.0)))
        self.tick_s = float(config.get("tick_seconds", 1.0))
        self.seed = int(config.get("seed", 42))
        self.sampling_rate = float(config.get("sampling_rate", 250.0))

    def load_metadata(self) -> DatasetMetadata:
        return DatasetMetadata(
            dataset_id=self.dataset_id,
            name="Synthetic NeuroVerse phase dataset",
            version="phase2-fixture-v1",
            source="BiosignalSimulator",
            modalities=["eeg", "physio", "gaze", "multimodal"],
            sampling_rates={"multimodal": self.sampling_rate},
            subjects=["synthetic_subject"],
            sessions=["synthetic_session"],
            labels=["phase_label", "workload_class", "workload_score"],
            notes=(
                "Deterministic simulator-derived labels for development and CI, "
                "not real physiology."
            ),
        )

    async def _collect_raw(self) -> list[RawDatasetRecord]:
        rng = np.random.default_rng(self.seed)
        sim = BiosignalSimulator(
            duration_s=self.duration_s,
            tick_interval_ms=self.tick_s * 1000.0,
            sampling_rate=self.sampling_rate,
            rng=rng,
        )
        await sim.start()
        records: list[RawDatasetRecord] = []
        tick = 0
        while tick * self.tick_s < self.duration_s - 1e-9:
            window = await sim.get_window()
            t0 = tick * self.tick_s
            label = phase_label_at(t0, self.duration_s)
            records.append(
                RawDatasetRecord(
                    subject_id="synthetic_subject",
                    session_id="synthetic_session",
                    timestamp=t0,
                    modality="multimodal",
                    channel_names=window.channel_names,
                    sampling_rate=window.sampling_rate,
                    data=window.data,
                    label=label,
                    metadata={"sqi_hint": window.signal_quality_hint},
                )
            )
            tick += 1
        await sim.stop()
        return records

    def iter_raw_records(self) -> Iterator[RawDatasetRecord]:
        yield from asyncio.run(self._collect_raw())

    def iter_windows(self) -> Iterator[WindowedSample]:
        for i, record in enumerate(self.iter_raw_records()):
            score = workload_score_from_label(record.label)
            labels = {
                "phase_label": record.label,
                "workload_score": score,
                "workload_class": workload_class_from_score(score),
            }
            yield WindowedSample(
                sample_id=f"{self.dataset_id}:{i:06d}",
                dataset_id=self.dataset_id,
                subject_id=record.subject_id,
                session_id=record.session_id,
                start_time=record.timestamp,
                end_time=record.timestamp + self.tick_s,
                modalities=["multimodal"],
                data_by_modality={
                    "multimodal": {
                        "data": record.data,
                        "channel_names": record.channel_names,
                        "sampling_rate": record.sampling_rate,
                    }
                },
                labels=labels,
                metadata=record.metadata,
            )
