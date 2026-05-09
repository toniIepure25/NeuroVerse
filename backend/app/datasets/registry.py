from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from app.datasets.base import BaseDatasetAdapter


def load_dataset_config(path: str | Path) -> dict[str, Any]:
    cfg_path = Path(path)
    with open(cfg_path) as f:
        if cfg_path.suffix.lower() in {".yaml", ".yml"}:
            data = yaml.safe_load(f) or {}
        else:
            data = json.load(f)
    data.setdefault("_config_path", str(cfg_path))
    return data


def create_dataset_adapter(config_or_path: dict[str, Any] | str | Path) -> BaseDatasetAdapter:
    config = (
        load_dataset_config(config_or_path)
        if isinstance(config_or_path, (str, Path))
        else dict(config_or_path)
    )
    adapter_type = str(config.get("type", "synthetic")).lower()
    if adapter_type == "synthetic":
        from app.datasets.synthetic_dataset import SyntheticDatasetAdapter

        return SyntheticDatasetAdapter(config)
    if adapter_type == "generic_csv":
        from app.datasets.generic_csv_adapter import GenericCSVAdapter

        return GenericCSVAdapter(config)
    if adapter_type in {"clare", "clare_like"}:
        from app.datasets.clare_adapter import ClareLikeAdapter

        return ClareLikeAdapter(config)
    if adapter_type in {"physionet_mi", "physionet_motor_imagery"}:
        from app.datasets.physionet_mi_adapter import PhysioNetMIAdapter

        return PhysioNetMIAdapter(config)
    raise ValueError(f"Unknown dataset adapter type: {adapter_type}")
