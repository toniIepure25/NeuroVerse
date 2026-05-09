from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from app.datasets.registry import create_dataset_adapter, load_dataset_config
from app.ml.feature_dataset import build_feature_dataset

REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_REPORTS_DIR = REPO_ROOT / "reports" / "datasets"


def validate_dataset_config(
    config_or_path: dict[str, Any] | str | Path,
    target: str | None = None,
    write_report: bool = True,
    output_dir: str | Path = DATASET_REPORTS_DIR,
) -> dict[str, Any]:
    config = (
        load_dataset_config(config_or_path)
        if isinstance(config_or_path, (str, Path))
        else dict(config_or_path)
    )
    adapter = create_dataset_adapter(config)
    metadata = adapter.load_metadata()
    windows = list(adapter.iter_windows())
    warnings: list[str] = []
    errors: list[str] = []

    target_name = target or config.get("target") or (config.get("labels") or {}).get("target")
    if not target_name and windows:
        for key in ("phase_label", "workload_class", "label", "workload_score"):
            if key in windows[0].labels:
                target_name = key
                break

    label_values = (
        [sample.labels.get(str(target_name)) for sample in windows] if target_name else []
    )
    missing_labels = sum(1 for value in label_values if value is None or value == "")
    label_distribution = dict(Counter(str(v) for v in label_values if v is not None and v != ""))
    if missing_labels:
        warnings.append(f"{missing_labels} windows are missing target labels")
    if label_distribution:
        total = sum(label_distribution.values())
        minority = min(label_distribution.values())
        if len(label_distribution) > 1 and minority / max(total, 1) < 0.1:
            warnings.append("Class imbalance detected; prefer balanced metrics and careful splits")

    feature_summary = _feature_summary(windows, target_name, errors, warnings)
    group_counter = Counter(f"{sample.subject_id}:{sample.session_id}" for sample in windows)
    subjects = {sample.subject_id for sample in windows}
    sessions = {sample.session_id for sample in windows}
    if len(subjects) <= 1:
        warnings.append(
            "Only one subject is present; subject-level generalization cannot be tested"
        )
    if len(sessions) <= 1:
        warnings.append("Only one session is present; session-level leakage risk is high")
    if len(group_counter) <= 1:
        warnings.append(
            "Only one subject/session group is present; group split will not be meaningful"
        )

    report = {
        "ok": not errors,
        "dataset_id": metadata.dataset_id,
        "adapter_type": config.get("type", "unknown"),
        "local_path": metadata.local_path,
        "metadata": metadata.to_dict(),
        "target_label": target_name,
        "window_count": len(windows),
        "record_count": len(windows),
        "label_distribution": label_distribution,
        "missing_labels": missing_labels,
        "feature_analysis": feature_summary,
        "leakage_risk": {
            "subject_count": len(subjects),
            "session_count": len(sessions),
            "group_count": len(group_counter),
            "groups_available": bool(group_counter),
        },
        "windowing": {
            "window_size_seconds": config.get("window_size_seconds"),
            "overlap": config.get("overlap"),
            "label_strategy": config.get("label_strategy", "adapter_default"),
            "actual_windows": len(windows),
        },
        "warnings": warnings,
        "errors": errors,
    }
    if write_report:
        paths = write_dataset_validation_report(report, output_dir)
        report["report_paths"] = {key: str(value) for key, value in paths.items()}
    return report


def write_dataset_validation_report(
    report: dict[str, Any],
    output_dir: str | Path = DATASET_REPORTS_DIR,
) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = f"{report['dataset_id']}_validation"
    json_path = out / f"{stem}.json"
    md_path = out / f"{stem}.md"
    json_path.write_text(json.dumps(report, indent=2, default=str))
    md_path.write_text(_dataset_validation_markdown(report))
    return {"json": json_path, "markdown": md_path}


def _feature_summary(
    windows,
    target_name: str | None,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    if not windows:
        errors.append("Dataset produced no windows")
        return {
            "feature_count": 0,
            "feature_names": [],
            "modality_prefixes": [],
            "missing_values": 0,
            "nan_count": 0,
            "inf_count": 0,
            "constant_columns": [],
            "extreme_value_count": 0,
        }
    try:
        dataset = build_feature_dataset(windows, target=target_name)
    except Exception as exc:
        errors.append(f"Feature dataset generation failed: {exc}")
        return {
            "feature_count": 0,
            "feature_names": [],
            "modality_prefixes": [],
            "missing_values": None,
            "nan_count": None,
            "inf_count": None,
            "constant_columns": [],
            "extreme_value_count": None,
        }

    x_values = np.asarray(dataset.X, dtype=float)
    nan_count = int(np.isnan(x_values).sum())
    inf_count = int(np.isinf(x_values).sum())
    constant_columns = [
        name
        for i, name in enumerate(dataset.feature_names)
        if x_values.shape[0] > 1 and float(np.nanstd(x_values[:, i])) < 1e-12
    ]
    extreme_count = int(np.sum(np.abs(x_values[np.isfinite(x_values)]) > 1e6))
    prefixes = sorted({name.split("_", 1)[0] for name in dataset.feature_names if "_" in name})
    if nan_count or inf_count:
        warnings.append("Feature matrix contains NaN or Inf values")
    if constant_columns:
        warnings.append(f"{len(constant_columns)} constant feature columns detected")
    if extreme_count:
        warnings.append(f"{extreme_count} extreme feature values detected")

    return {
        "feature_count": len(dataset.feature_names),
        "feature_names": dataset.feature_names,
        "modality_prefixes": prefixes,
        "missing_values": nan_count,
        "nan_count": nan_count,
        "inf_count": inf_count,
        "constant_columns": constant_columns,
        "extreme_value_count": extreme_count,
    }


def _dataset_validation_markdown(report: dict[str, Any]) -> str:
    warnings = report.get("warnings") or []
    errors = report.get("errors") or []
    labels = report.get("label_distribution") or {}
    feature = report.get("feature_analysis") or {}
    lines = [
        f"# Dataset Validation: {report.get('dataset_id')}",
        "",
        f"- Adapter: `{report.get('adapter_type')}`",
        f"- Target: `{report.get('target_label')}`",
        f"- Windows: `{report.get('window_count')}`",
        f"- Subjects: `{report.get('leakage_risk', {}).get('subject_count')}`",
        f"- Sessions: `{report.get('leakage_risk', {}).get('session_count')}`",
        f"- Features: `{feature.get('feature_count')}`",
        "",
        "## Label Distribution",
        json.dumps(labels, indent=2),
        "",
        "## Feature Warnings",
        *(f"- {item}" for item in warnings),
    ]
    if errors:
        lines.extend(["", "## Errors", *(f"- {item}" for item in errors)])
    lines.extend(
        [
            "",
            "## Scientific Note",
            "Dataset labels are dataset-derived proxies and should not be interpreted as "
            "clinical ground truth or direct access to mental state.",
            "",
        ]
    )
    return "\n".join(lines)
