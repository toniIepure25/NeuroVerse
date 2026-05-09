from __future__ import annotations

from collections.abc import Iterator
from importlib.util import find_spec
from pathlib import Path
from typing import Any

from app.datasets.base import BaseDatasetAdapter
from app.datasets.generic_csv_adapter import GenericCSVAdapter
from app.datasets.schemas import DatasetMetadata, WindowedSample


class PhysioNetMIAdapter(BaseDatasetAdapter):
    """PhysioNet EEG Motor Movement/Imagery adapter with optional MNE EDF support."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.path = self._resolve_path(config.get("path", "")) if config.get("path") else Path()
        self.fixture_csv = (
            str(self._resolve_path(config["fixture_csv"])) if config.get("fixture_csv") else None
        )

    def _resolve_path(self, raw_path: str) -> Path:
        path = Path(raw_path)
        if path.is_absolute():
            return path
        config_path = self.config.get("_config_path")
        if config_path:
            return (Path(config_path).parent / path).resolve()
        return path

    def load_metadata(self) -> DatasetMetadata:
        return DatasetMetadata(
            dataset_id=self.dataset_id,
            name=str(self.config.get("name", "PhysioNet EEG Motor Imagery local adapter")),
            version=str(self.config.get("version", "edf-optional-v1")),
            source="physionet_mi_local",
            local_path=str(self.path) if self.path else None,
            modalities=["eeg"],
            sampling_rates={"eeg": float(self.config.get("sampling_rate", 160.0))},
            subjects=[],
            sessions=[],
            labels=[
                "rest",
                "left_fist",
                "right_fist",
                "both_fists",
                "both_feet",
                "imagined_left_fist",
                "imagined_right_fist",
            ],
            notes=(
                "EDF parsing requires optional dependency mne. "
                "Tests use fixture CSVs, not full PhysioNet data."
            ),
        )

    def validate(self) -> dict[str, Any]:
        mne_available = find_spec("mne") is not None
        meta = self.load_metadata()
        return {
            "ok": bool(self.fixture_csv or mne_available),
            "dataset_id": self.dataset_id,
            "modalities": meta.modalities,
            "labels": meta.labels,
            "mne_available": mne_available,
            "notes": meta.notes,
        }

    def iter_windows(self) -> Iterator[WindowedSample]:
        if self.fixture_csv:
            cfg = dict(self.config)
            cfg["type"] = "generic_csv"
            cfg["path"] = self.fixture_csv
            yield from GenericCSVAdapter(cfg).iter_windows()
            return

        if find_spec("mne") is None:
            raise RuntimeError(
                "PhysioNet MI EDF replay requires optional dependency mne. "
                "Install the backend hardware extra or provide fixture_csv."
            )

        edf_files = sorted(self.path.glob("*.edf"))
        if not edf_files:
            raise FileNotFoundError(f"No EDF files found under {self.path}")

        raise NotImplementedError(
            "MNE is available, but full PhysioNet event-window extraction is intentionally "
            "left conservative until a local dataset layout is verified."
        )
