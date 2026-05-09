from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_experiment_config(path: str | Path) -> dict[str, Any]:
    cfg_path = Path(path)
    with open(cfg_path) as f:
        if cfg_path.suffix.lower() in {".yaml", ".yml"}:
            return yaml.safe_load(f) or {}
        return json.load(f)
