"""IMAGINA v1 Module init.

IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

from __future__ import annotations

from app.imagina.baseline_model import (
    ImaginaBaselineModelAdapter,
    create_imagina_model,
    train_imagina_baseline,
)
from app.imagina.dataset_adapter import (
    build_feature_table,
    convert_sample_to_fusion_input,
    load_manifest,
    summarize_manifest,
    validate_manifest,
)
from app.imagina.models import ImaginaDatasetManifest, ImaginaSample
from app.imagina.registry import (
    get_latest_imagina_model,
    list_imagina_models,
    load_imagina_model,
    register_imagina_model,
)

__all__ = [
    "ImaginaDatasetManifest",
    "ImaginaSample",
    "load_manifest",
    "validate_manifest",
    "summarize_manifest",
    "build_feature_table",
    "convert_sample_to_fusion_input",
    "ImaginaBaselineModelAdapter",
    "create_imagina_model",
    "train_imagina_baseline",
    "register_imagina_model",
    "list_imagina_models",
    "get_latest_imagina_model",
    "load_imagina_model",
]
