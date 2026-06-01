"""CSV/JSON replay adapter skeleton for Fusion v1.

This adapter provides a foundation for replaying recorded sensor data from
CSV or JSON files. It maps columns/keys to modality feature packets.

This is a skeleton implementation. Full column mapping and error handling
will be extended as real replay datasets become available.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from app.fusion.adapters.base import FusionSensorAdapter
from app.fusion.models import ModalityFeaturePacket, ModalityId


class CSVReplayAdapter(FusionSensorAdapter):
    """CSV/JSON replay adapter for fusion modalities.

    Reads feature rows from a CSV or JSON file and maps columns to
    modality feature packets. Handles missing columns safely.
    """

    adapter_id = "csv_replay_v1"
    modality_id = "eeg"  # type: ignore[assignment]
    source_type = "replay"  # type: ignore[assignment]
    version = "1.0"

    def __init__(
        self,
        *,
        file_path: str | Path | None = None,
        target_modality: ModalityId = "eeg",
        column_mapping: dict[str, str] | None = None,
    ) -> None:
        self.file_path = Path(file_path) if file_path else None
        self.modality_id = target_modality  # type: ignore[assignment]
        self._column_mapping = column_mapping or {}
        self._rows: list[dict[str, Any]] = []
        self._index = 0
        self._loaded = False

    def is_available(self) -> bool:
        if self.file_path is None:
            return False
        return self.file_path.exists()

    def get_status(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "modality_id": self.modality_id,
            "source_type": self.source_type,
            "available": self.is_available(),
            "file_path": str(self.file_path) if self.file_path else None,
            "loaded": self._loaded,
            "total_rows": len(self._rows),
            "current_index": self._index,
            "limitations": self.limitations,
        }

    def load(self) -> int:
        """Load the replay file. Returns number of rows loaded."""
        if self.file_path is None or not self.file_path.exists():
            return 0

        suffix = self.file_path.suffix.lower()
        if suffix == ".csv":
            self._rows = self._load_csv()
        elif suffix == ".json":
            self._rows = self._load_json()
        else:
            return 0

        self._loaded = True
        self._index = 0
        return len(self._rows)

    def read_packet(self) -> ModalityFeaturePacket:
        if not self._loaded or not self._rows:
            return ModalityFeaturePacket(
                modality_id=self.modality_id,
                source="replay",
                missing=True,
                features={},
                limitations=["No replay data loaded."],
                provenance={"adapter_id": self.adapter_id},
            )

        row = self._rows[self._index % len(self._rows)]
        self._index += 1

        features: dict[str, Any] = {}
        for target_key, source_col in self._column_mapping.items():
            if source_col in row:
                try:
                    features[target_key] = float(row[source_col])
                except (TypeError, ValueError):
                    features[target_key] = row[source_col]

        # Also include any unmapped numeric columns
        for key, value in row.items():
            if key not in self._column_mapping.values() and key not in features:
                try:
                    features[key] = float(value)
                except (TypeError, ValueError):
                    pass

        quality = features.pop("quality_score", 0.6)
        try:
            quality = max(0.0, min(1.0, float(quality)))
        except (TypeError, ValueError):
            quality = 0.6

        return ModalityFeaturePacket(
            modality_id=self.modality_id,
            source="replay",
            quality_score=quality,
            confidence=max(0.0, min(1.0, quality * 0.9)),
            features=features,
            limitations=[
                "Replay data from CSV/JSON file — not live sensor data.",
                "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
            ],
            provenance={
                "adapter_id": self.adapter_id,
                "file_path": str(self.file_path),
                "row_index": self._index - 1,
            },
        )

    def _load_csv(self) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        if self.file_path is None:
            return rows
        with self.file_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(dict(row))
        return rows

    def _load_json(self) -> list[dict[str, Any]]:
        if self.file_path is None:
            return []
        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [row for row in data if isinstance(row, dict)]
        if isinstance(data, dict) and "rows" in data:
            return [row for row in data["rows"] if isinstance(row, dict)]
        return []

    @property
    def limitations(self) -> list[str]:
        return [
            "CSVReplayAdapter replays recorded data — not live sensor input.",
            "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
        ]
