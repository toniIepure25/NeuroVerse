"""IMAGINA Model Registry.

Registers and retrieves trained IMAGINA v1 baseline models.
IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.imagina.baseline_model import ImaginaBaselineModelAdapter

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_IMAGINA_MODELS_DIR = REPO_ROOT / "models"


def register_imagina_model(
    model_id: str,
    run_result: dict[str, Any],
    models_dir: str | Path = DEFAULT_IMAGINA_MODELS_DIR,
) -> Path:
    """Register a trained IMAGINA model in the central models folder."""
    root = Path(models_dir)
    target_dir = root / model_id
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy all files from run_result artifacts
    artifacts = run_result.get("artifacts", {})
    for name, src_path in artifacts.items():
        src = Path(src_path)
        if src.exists():
            shutil.copy(src, target_dir / src.name)

    # Enrich and write registry.json
    registry_path = root / "registry.json"
    registry = {}
    if registry_path.exists():
        try:
            with open(registry_path) as f:
                registry = json.load(f)
        except Exception:
            registry = {}

    # Add registry entry
    registry[model_id] = {
        "model_id": model_id,
        "path": str(target_dir),
        "model_type": run_result["metrics"].get("model_type", "imagina_v1_baseline"),
        "dataset_id": run_result["manifest_summary"].get("dataset_name", "fixture_demo"),
        "target": run_result["metrics"].get("target_type", "classification"),
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "imagina_model": True,
    }

    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2, default=str)

    return target_dir


def list_imagina_models(models_dir: str | Path = DEFAULT_IMAGINA_MODELS_DIR) -> list[dict[str, Any]]:
    """List all registered IMAGINA models."""
    root = Path(models_dir)
    registry_path = root / "registry.json"
    if not registry_path.exists():
        return []

    try:
        with open(registry_path) as f:
            registry = json.load(f)
    except Exception:
        return []

    items = []
    for model_id, item in registry.items():
        if item.get("imagina_model") or "imagina" in model_id:
            enriched = dict(item)
            model_dir = Path(item.get("path", root / model_id))
            metrics_path = model_dir / "metrics.json"
            if metrics_path.exists():
                try:
                    with open(metrics_path) as f:
                        enriched["metrics"] = json.load(f)
                except Exception:
                    pass
            items.append(enriched)

    return sorted(items, key=lambda x: x.get("registered_at", ""), reverse=True)


def get_latest_imagina_model(models_dir: str | Path = DEFAULT_IMAGINA_MODELS_DIR) -> dict[str, Any] | None:
    """Return the most recently registered IMAGINA model, if any."""
    models = list_imagina_models(models_dir)
    return models[0] if models else None


def load_imagina_model(
    model_id: str,
    models_dir: str | Path = DEFAULT_IMAGINA_MODELS_DIR,
) -> ImaginaBaselineModelAdapter:
    """Load a registered IMAGINA model by its ID."""
    root = Path(models_dir)
    model_file = root / model_id / "model.joblib"
    if not model_file.exists():
        raise FileNotFoundError(f"IMAGINA model joblib not found: {model_file}")
    return ImaginaBaselineModelAdapter.load(model_file)
