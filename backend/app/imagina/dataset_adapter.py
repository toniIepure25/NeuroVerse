"""IMAGINA v1 Dataset Adapter.

Loads, validates, and prepares feature-level imagery datasets from JSON manifests.
IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

import numpy as np

from app.fusion.models import (
    IMAGINA_LIMITATION,
    FusionInput,
    ModalityFeaturePacket,
)
from app.imagina.models import ImaginaDatasetManifest, ImaginaSample

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_manifest(path: str | Path) -> ImaginaDatasetManifest:
    """Load and parse an IMAGINA dataset manifest from JSON."""
    p = Path(path)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if not p.exists():
        raise FileNotFoundError(f"IMAGINA manifest file not found: {p}")

    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    return ImaginaDatasetManifest.model_validate(data)


def validate_manifest(path: str | Path) -> dict[str, Any]:
    """Validate an IMAGINA manifest and return issues, warnings, and summary."""
    issues = []
    warnings = []

    try:
        manifest = load_manifest(path)
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

    if not manifest.dataset_name:
        issues.append("dataset_name is required.")
    if not manifest.feature_schema:
        warnings.append("feature_schema is empty.")
    if not manifest.samples:
        issues.append("No samples found in the manifest.")

    for i, sample in enumerate(manifest.samples):
        if not sample.sample_id:
            issues.append(f"Sample at index {i} is missing sample_id.")
        if not sample.features and not sample.features_path:
            warnings.append(f"Sample '{sample.sample_id}' has no inline features or features_path.")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "dataset_name": manifest.dataset_name,
        "sample_count": len(manifest.samples),
        "modality": manifest.modality,
        "paradigm": manifest.paradigm,
    }


def summarize_manifest(path: str | Path) -> dict[str, Any]:
    """Provide a summary of the manifest's dataset composition."""
    manifest = load_manifest(path)
    subjects = set()
    sessions = set()
    tasks = {}
    labels = {}

    for sample in manifest.samples:
        if sample.subject_id:
            subjects.add(sample.subject_id)
        if sample.session_id:
            sessions.add(sample.session_id)

        tasks[sample.task] = tasks.get(sample.task, 0) + 1
        if sample.label:
            labels[sample.label] = labels.get(sample.label, 0) + 1

    return {
        "dataset_name": manifest.dataset_name,
        "dataset_version": manifest.dataset_version,
        "modality": manifest.modality,
        "paradigm": manifest.paradigm,
        "sample_count": len(manifest.samples),
        "subject_count": len(subjects),
        "subjects": list(subjects),
        "session_count": len(sessions),
        "tasks": tasks,
        "labels": labels,
        "feature_count": len(manifest.feature_schema),
        "feature_schema": manifest.feature_schema,
    }


def build_feature_table(
    manifest: ImaginaDatasetManifest,
    target_type: Literal["classification", "regression"] = "classification",
) -> dict[str, Any]:
    """Extract features (X) and targets (y) from the manifest samples.

    Returns a dict with:
        "X": np.ndarray of shape (n_samples, n_features)
        "y": np.ndarray of shape (n_samples,)
        "feature_names": list[str]
        "subject_ids": list[str] (for group splitting)
        "target_mapping": dict (for classification labels)
        "classes": list (class labels)
    """
    feature_names = list(manifest.feature_schema)
    if not feature_names:
        # Auto-infer if empty
        all_keys = set()
        for s in manifest.samples:
            all_keys.update(s.features.keys())
        feature_names = sorted(list(all_keys))

    X_list = []
    y_list = []
    subject_ids = []

    # Target mapping
    target_mapping = {}
    classes = sorted(list(manifest.labels)) if manifest.labels else []

    if target_type == "classification":
        if not classes:
            # Auto-infer class names
            all_labels = set()
            for s in manifest.samples:
                if s.label:
                    all_labels.add(s.label)
                elif s.task:
                    all_labels.add(s.task)
            classes = sorted(list(all_labels))

        target_mapping = {lbl: idx for idx, lbl in enumerate(classes)}

    for sample in manifest.samples:
        # Load features (inline first, otherwise fallback)
        feat_dict = dict(sample.features)
        if not feat_dict and sample.features_path:
            try:
                p = Path(sample.features_path)
                if not p.is_absolute():
                    p = REPO_ROOT / p
                if p.exists():
                    with open(p) as f:
                        loaded = json.load(f)
                        if isinstance(loaded, dict):
                            feat_dict = loaded
            except Exception:
                pass

        # Build feature row
        row = [float(feat_dict.get(fname, 0.0)) for fname in feature_names]
        X_list.append(row)

        # Build target
        if target_type == "classification":
            lbl = sample.label or sample.task
            val = target_mapping.get(lbl, 0)
            y_list.append(val)
        else:
            # Regression target: look for self_report vividness or a feature
            val = 0.5
            if sample.self_report:
                val = sample.self_report.get("vividness", sample.self_report.get("imagery_vividness", 0.5))
            y_list.append(float(val))

        subject_ids.append(sample.subject_id or "unknown_subject")

    return {
        "X": np.array(X_list, dtype=np.float32),
        "y": np.array(y_list),
        "feature_names": feature_names,
        "subject_ids": subject_ids,
        "target_mapping": target_mapping,
        "classes": classes,
    }


def convert_sample_to_fusion_input(
    sample: ImaginaSample,
    manifest: ImaginaDatasetManifest | None = None,
) -> FusionInput:
    """Convert an IMAGINA sample into a FusionInput for evaluation."""
    packets = []

    # EEG feature packet
    feat_dict = dict(sample.features)
    if feat_dict:
        packets.append(
            ModalityFeaturePacket(
                modality_id="eeg",
                source="replay",
                quality_score=0.75,
                confidence=0.70,
                features=feat_dict,
                limitations=[
                    "EEG features loaded from IMAGINA baseline dataset manifest.",
                    IMAGINA_LIMITATION,
                ],
                provenance={
                    "source": "imagina_v1_baseline_pipeline",
                    "sample_id": sample.sample_id,
                    "dataset_name": manifest.dataset_name if manifest else "unknown",
                },
            )
        )

    # Self-report packet
    if sample.self_report:
        sr_dict = dict(sample.self_report)
        if "vividness" in sr_dict:
            sr_dict.setdefault("imagery_vividness", sr_dict["vividness"])
        if "controllability" in sr_dict:
            sr_dict.setdefault("imagery_controllability", sr_dict["controllability"])

        packets.append(
            ModalityFeaturePacket(
                modality_id="self_report",
                source="replay",
                quality_score=0.70,
                confidence=0.65,
                features=sr_dict,
                limitations=[
                    "Self-report features loaded from IMAGINA baseline dataset manifest.",
                    IMAGINA_LIMITATION,
                ],
                provenance={
                    "source": "imagina_v1_baseline_pipeline",
                    "sample_id": sample.sample_id,
                },
            )
        )

    return FusionInput(
        session_id=f"imagina_v1_{sample.sample_id}",
        context={
            "mode": "replay",
            "data_source": "imagina_v1_baseline",
            "imagery_task_active": sample.task == "imagery",
            "imagery_task_label": sample.label or sample.task,
            "imagina_sample_id": sample.sample_id,
        },
        packets=packets,
    )
