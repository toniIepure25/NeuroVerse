from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.inference.heuristic_model import HeuristicStateEstimator
from app.inference.learned_model import LearnedModelEstimator
from app.ml.registry import DEFAULT_MODELS_DIR, get_model_metadata, load_model

ACTIVE_MODEL_FILE = DEFAULT_MODELS_DIR / "active_model.json"
ALLOWED_PREDICTION_SEMANTICS = {
    "phase_proxy",
    "workload_proxy",
    "motor_intent",
    "state_regression",
}
KNOWN_FEATURE_PREFIXES = ("eeg_", "physio_", "gaze_", "multimodal_", "sqi_")


class ModelActivationError(ValueError):
    pass


def validate_model_for_activation(
    model_id: str,
    models_dir: str | Path = DEFAULT_MODELS_DIR,
) -> dict[str, Any]:
    root = Path(models_dir)
    model_dir = root / model_id
    if not (model_dir / "model.joblib").exists():
        raise FileNotFoundError(f"Model artifact not found: {model_dir / 'model.joblib'}")
    metadata = get_model_metadata(model_id, root)
    semantics = metadata.get("prediction_semantics")
    if semantics not in ALLOWED_PREDICTION_SEMANTICS:
        raise ModelActivationError(
            f"Unsupported prediction_semantics {semantics!r}; "
            f"expected one of {sorted(ALLOWED_PREDICTION_SEMANTICS)}"
        )

    feature_names = metadata.get("feature_names") or []
    if not isinstance(feature_names, list) or not feature_names:
        raise ModelActivationError("Model metadata must include non-empty feature_names")
    incompatible = [
        name for name in feature_names if not str(name).startswith(KNOWN_FEATURE_PREFIXES)
    ]
    if incompatible:
        raise ModelActivationError(
            "Model feature_names must use known NeuroVerse prefixes; "
            f"incompatible examples: {incompatible[:5]}"
        )

    model = load_model(model_id, root)
    if not set(model.feature_names).issubset(set(feature_names)):
        raise ModelActivationError("Model artifact feature_names are not compatible with metadata")

    return {
        "model_id": model_id,
        "active_estimator": "learned",
        "prediction_semantics": semantics,
        "target": metadata.get("target"),
        "model_type": metadata.get("model_type"),
        "feature_count": len(feature_names),
    }


def activate_model(model_id: str, models_dir: str | Path = DEFAULT_MODELS_DIR) -> dict[str, Any]:
    payload = validate_model_for_activation(model_id, models_dir)
    root = Path(models_dir)
    root.mkdir(parents=True, exist_ok=True)
    (root / "active_model.json").write_text(json.dumps(payload, indent=2))
    return payload


def deactivate_model(models_dir: str | Path = DEFAULT_MODELS_DIR) -> dict[str, Any]:
    payload = {
        "active_estimator": "heuristic",
        "model_id": None,
        "prediction_semantics": None,
    }
    root = Path(models_dir)
    root.mkdir(parents=True, exist_ok=True)
    (root / "active_model.json").write_text(json.dumps(payload, indent=2))
    return payload


def get_active_model_status(models_dir: str | Path = DEFAULT_MODELS_DIR) -> dict[str, Any]:
    path = Path(models_dir) / "active_model.json"
    if not path.exists():
        return {
            "active_estimator": "heuristic",
            "model_id": None,
            "prediction_semantics": None,
        }
    with open(path) as f:
        return json.load(f)


def load_active_estimator(models_dir: str | Path = DEFAULT_MODELS_DIR):
    status = get_active_model_status(models_dir)
    if status.get("active_estimator") != "learned" or not status.get("model_id"):
        return HeuristicStateEstimator()
    try:
        return LearnedModelEstimator.from_model_dir(Path(models_dir) / str(status["model_id"]))
    except Exception:
        return HeuristicStateEstimator()
