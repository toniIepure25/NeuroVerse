from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.ml.baselines import BaselineModelAdapter

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODELS_DIR = REPO_ROOT / "models"


def register_model(
    model: BaselineModelAdapter,
    model_id: str,
    metadata: dict[str, Any],
    metrics: dict[str, Any] | None = None,
    models_dir: str | Path = DEFAULT_MODELS_DIR,
) -> Path:
    root = Path(models_dir)
    model_dir = root / model_id
    model_dir.mkdir(parents=True, exist_ok=True)
    model.save(model_dir / "model.joblib")
    full_metadata = {
        "model_id": model_id,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        **model.metadata(),
        **metadata,
    }
    _write_json(model_dir / "metadata.json", full_metadata)
    _write_json(model_dir / "metrics.json", metrics or {})
    _write_model_card(model_dir / "model_card.md", full_metadata, metrics or {})
    registry = _read_registry(root)
    registry[model_id] = {
        "model_id": model_id,
        "path": str(model_dir),
        "model_type": full_metadata.get("model_type"),
        "dataset_id": full_metadata.get("dataset_id"),
        "target": full_metadata.get("target"),
        "registered_at": full_metadata["registered_at"],
    }
    _write_json(root / "registry.json", registry)
    return model_dir


def list_models(models_dir: str | Path = DEFAULT_MODELS_DIR) -> list[dict[str, Any]]:
    root = Path(models_dir)
    items = []
    for item in _read_registry(root).values():
        enriched = dict(item)
        model_dir = Path(str(item.get("path", root / str(item.get("model_id")))))
        metadata_path = model_dir / "metadata.json"
        metrics_path = model_dir / "metrics.json"
        if metadata_path.exists():
            with open(metadata_path) as f:
                metadata = json.load(f)
            enriched["prediction_semantics"] = metadata.get("prediction_semantics")
            enriched["feature_count"] = len(metadata.get("feature_names") or [])
        if metrics_path.exists():
            with open(metrics_path) as f:
                metrics = json.load(f)
            enriched["metrics"] = {
                "accuracy": metrics.get("accuracy"),
                "balanced_accuracy": metrics.get("balanced_accuracy"),
                "macro_f1": metrics.get("macro_f1"),
                "ece": (metrics.get("calibration") or {}).get("ece"),
            }
        items.append(enriched)
    return items


def load_model(
    model_id_or_dir: str | Path, models_dir: str | Path = DEFAULT_MODELS_DIR
) -> BaselineModelAdapter:
    path = Path(model_id_or_dir)
    if not path.exists():
        path = Path(models_dir) / str(model_id_or_dir)
    return BaselineModelAdapter.load(path / "model.joblib")


def get_model_metadata(
    model_id: str, models_dir: str | Path = DEFAULT_MODELS_DIR
) -> dict[str, Any]:
    path = Path(models_dir) / model_id / "metadata.json"
    if not path.exists():
        raise FileNotFoundError(f"Model metadata not found: {path}")
    with open(path) as f:
        return json.load(f)


def get_best_model(
    metric: str, models_dir: str | Path = DEFAULT_MODELS_DIR
) -> dict[str, Any] | None:
    best = None
    best_value = None
    for item in list_models(models_dir):
        metrics_path = Path(item["path"]) / "metrics.json"
        if not metrics_path.exists():
            continue
        with open(metrics_path) as f:
            value = json.load(f).get(metric)
        if isinstance(value, (int, float)) and (best_value is None or value > best_value):
            best = item
            best_value = value
    return best


def validate_model_compatibility(
    model: BaselineModelAdapter, feature_names: list[str]
) -> dict[str, Any]:
    expected = list(model.feature_names)
    missing = [name for name in expected if name not in feature_names]
    extra = [name for name in feature_names if name not in expected]
    return {"ok": not missing, "missing": missing, "extra": extra}


def _read_registry(root: Path) -> dict[str, Any]:
    path = root / "registry.json"
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def _write_model_card(path: Path, metadata: dict[str, Any], metrics: dict[str, Any]) -> None:
    lines = [
        f"# Model Card: {metadata.get('model_id')}",
        "",
        "## Intended Use",
        str(
            metadata.get("intended_use", "Research prototype baseline for dataset-derived labels.")
        ),
        "",
        "## Not Intended Use",
        str(
            metadata.get(
                "not_intended_use", "Not for clinical use, diagnosis, or consequential decisions."
            )
        ),
        "",
        "## Limitations",
        str(metadata.get("limitations", "Dataset-derived proxy labels; not clinically validated.")),
        "",
        "## Metrics",
        "```json",
        json.dumps(metrics, indent=2, default=str),
        "```",
    ]
    path.write_text("\n".join(lines))
