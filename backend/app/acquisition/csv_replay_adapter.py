from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from app.acquisition.base import BaseAcquisition
from app.schemas.signals import RawSignalPayload


class CSVReplayAcquisition(BaseAcquisition):
    """Replay timestamped CSV rows as local acquisition windows."""

    def __init__(self, path: str | Path, sampling_rate: float = 1.0) -> None:
        self.path = Path(path)
        self.sampling_rate = float(sampling_rate)
        self._running = False
        self._rows: pd.DataFrame | None = None
        self._cursor = 0

    async def start(self) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f"CSV replay file not found: {self.path}")
        self._rows = pd.read_csv(self.path)
        self._cursor = 0
        self._running = True

    async def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    async def get_window(self) -> RawSignalPayload:
        if not self._running or self._rows is None:
            raise RuntimeError("CSVReplayAcquisition is not running")
        if self._cursor >= len(self._rows):
            self._running = False
            raise RuntimeError("CSV replay completed")
        row = self._rows.iloc[self._cursor]
        self._cursor += 1
        feature_cols = [
            col
            for col in self._rows.columns
            if col not in {"timestamp", "label", "subject_id", "session_id"}
        ]
        return RawSignalPayload(
            modality="csv_replay",
            sampling_rate=self.sampling_rate,
            channel_names=feature_cols,
            data=[[float(row[col])] for col in feature_cols],
            window_size_ms=max(1, int(round(1000 / self.sampling_rate))),
            signal_quality_hint=None,
        )

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "csv_replay",
            "running": self._running,
            "path": str(self.path),
            "cursor": self._cursor,
            "rows": 0 if self._rows is None else len(self._rows),
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "modalities": ["csv_replay"],
            "hardware_required": False,
            "timestamped_streams": "timestamp" in self._rows.columns
            if self._rows is not None
            else None,
        }
