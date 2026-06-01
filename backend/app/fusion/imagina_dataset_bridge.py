"""IMAGINA Dataset Bridge Foundation.

Defines how future real IMAGINA datasets will plug into the fusion system.
This is a bridge for feature-level manifests only — it does NOT require
raw EEG and does NOT claim to be a trained IMAGINA model.

IMAGINA plugin outputs are imagery-quality proxies, not decoded thoughts or dreams.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from app.fusion.models import (
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    FusionInput,
    ModalityFeaturePacket,
)

_ROOT = Path(__file__).resolve().parent.parent.parent.parent

DATASET_BRIDGE_LIMITATION = (
    "The IMAGINA dataset bridge is a data loading interface, not a trained model. "
    "No decoded imagery content is produced."
)


class ImaginaTaskMetadata(BaseModel):
    """Metadata for a single task in an IMAGINA dataset."""

    task_id: str
    label: str
    description: str = ""


class ImaginaSample(BaseModel):
    """A single sample from an IMAGINA dataset manifest."""

    sample_id: str
    features_path: str | None = None
    features: dict[str, Any] = Field(default_factory=dict)
    self_report: dict[str, float] = Field(default_factory=dict)
    task: str = "imagery"
    label: str = ""
    subject_id: str | None = None
    session_id: str | None = None
    provenance: dict[str, Any] = Field(default_factory=dict)


class ImaginaDatasetSpec(BaseModel):
    """Specification for an IMAGINA dataset manifest."""

    dataset_name: str
    modality: str = "eeg"
    tasks: list[str] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)
    samples: list[ImaginaSample] = Field(default_factory=list)
    feature_columns: list[str] = Field(default_factory=list)
    description: str = ""
    limitations: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)
    not_a_trained_model: bool = True


def load_imagina_manifest(path: str | Path) -> ImaginaDatasetSpec:
    """Load and parse an IMAGINA dataset manifest from JSON."""
    p = Path(path)
    if not p.is_absolute():
        p = _ROOT / p
    if not p.exists():
        raise FileNotFoundError(f"IMAGINA manifest not found: {p}")
    data = json.loads(p.read_text(encoding="utf-8"))
    return ImaginaDatasetSpec.model_validate(data)


def validate_imagina_manifest(path: str | Path) -> dict[str, Any]:
    """Validate an IMAGINA manifest and return validation results."""
    issues: list[str] = []
    warnings: list[str] = []

    try:
        spec = load_imagina_manifest(path)
    except FileNotFoundError as exc:
        return {
            "valid": False,
            "issues": [str(exc)],
            "warnings": [],
            "sample_count": 0,
        }
    except Exception as exc:
        return {
            "valid": False,
            "issues": [f"Failed to parse manifest: {exc}"],
            "warnings": [],
            "sample_count": 0,
        }

    if not spec.dataset_name:
        issues.append("dataset_name is required.")
    if not spec.tasks:
        warnings.append("No tasks defined in manifest.")
    if not spec.labels:
        warnings.append("No labels defined in manifest.")
    if not spec.samples:
        issues.append("No samples defined in manifest.")

    for i, sample in enumerate(spec.samples):
        if not sample.sample_id:
            issues.append(f"Sample {i} missing sample_id.")
        if not sample.features and not sample.features_path:
            warnings.append(f"Sample '{sample.sample_id}' has no features or features_path.")
        if sample.task and sample.task not in spec.tasks:
            warnings.append(
                f"Sample '{sample.sample_id}' task '{sample.task}' not in manifest tasks."
            )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "sample_count": len(spec.samples),
        "dataset_name": spec.dataset_name,
        "modality": spec.modality,
        "tasks": spec.tasks,
        "labels": spec.labels,
        "not_a_trained_model": spec.not_a_trained_model,
        "limitations": [
            IMAGINA_LIMITATION,
            DATASET_BRIDGE_LIMITATION,
            PROXY_LIMITATION,
        ],
    }


def convert_imagina_sample_to_fusion_input(
    sample: ImaginaSample,
    *,
    dataset_spec: ImaginaDatasetSpec | None = None,
) -> FusionInput:
    """Convert an IMAGINA sample into a FusionInput for evaluation.

    If the sample has inline features, uses those directly. If it has a
    features_path, loads features from that file. Falls back to empty features.
    """
    features = dict(sample.features)

    # Attempt to load features from path if inline features are empty
    if not features and sample.features_path:
        features_path = Path(sample.features_path)
        if not features_path.is_absolute():
            features_path = _ROOT / features_path
        if features_path.exists():
            try:
                data = json.loads(features_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    features = data
            except Exception:
                pass

    packets: list[ModalityFeaturePacket] = []

    # EEG features from the dataset
    eeg_features = {k: v for k, v in features.items() if isinstance(v, (int, float))}
    if eeg_features:
        packets.append(
            ModalityFeaturePacket(
                modality_id="eeg",
                source="replay",
                quality_score=0.60,
                confidence=0.55,
                features=eeg_features,
                limitations=[
                    "Features loaded from IMAGINA dataset manifest.",
                    IMAGINA_LIMITATION,
                ],
                provenance={
                    "source": "imagina_dataset_bridge",
                    "sample_id": sample.sample_id,
                    "dataset_name": dataset_spec.dataset_name if dataset_spec else "unknown",
                },
            )
        )

    # Self-report from the sample
    if sample.self_report:
        sr_features = dict(sample.self_report)
        # Map vividness/controllability to fusion-expected keys
        if "vividness" in sr_features:
            sr_features.setdefault("imagery_vividness", sr_features["vividness"])
        packets.append(
            ModalityFeaturePacket(
                modality_id="self_report",
                source="replay",
                quality_score=0.60,
                confidence=0.50,
                features=sr_features,
                limitations=[
                    "Self-report from IMAGINA dataset manifest.",
                    IMAGINA_LIMITATION,
                ],
                provenance={
                    "source": "imagina_dataset_bridge",
                    "sample_id": sample.sample_id,
                },
            )
        )

    return FusionInput(
        session_id=f"imagina_{sample.sample_id}",
        context={
            "mode": "replay",
            "data_source": "imagina_dataset_bridge",
            "imagery_task_active": sample.task == "imagery",
            "imagery_task_label": sample.label or sample.task,
            "imagina_sample_id": sample.sample_id,
            "not_a_trained_model": True,
        },
        packets=packets,
    )
