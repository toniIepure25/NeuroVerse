from __future__ import annotations

import json
import platform
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def write_experiment_report(
    output_dir: str | Path,
    title: str,
    dataset_metadata: dict[str, Any],
    model_metadata: dict[str, Any],
    metrics: dict[str, Any],
    run_config: dict[str, Any] | None = None,
    dataset_validation_summary: dict[str, Any] | None = None,
    limitations: list[str] | None = None,
) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2, default=str))
    if run_config is not None:
        (out / "run_config.yaml").write_text(yaml.safe_dump(run_config, sort_keys=False))
    if dataset_validation_summary is not None:
        (out / "dataset_validation_summary.json").write_text(
            json.dumps(dataset_validation_summary, indent=2, default=str)
        )
    _write_confusion_matrix(out, metrics)
    _write_reliability_bins(out, metrics)
    _write_environment(out)
    _write_model_card(out / "model_card.md", model_metadata, metrics)
    report = [
        f"# {title}",
        "",
        "## Summary",
        f"- Experiment ID: `{model_metadata.get('model_id', title)}`",
        f"- Dataset ID: `{dataset_metadata.get('dataset_id')}`",
        f"- Adapter/source: `{dataset_metadata.get('source')}`",
        f"- Target: `{model_metadata.get('target')}`",
        f"- Model type: `{model_metadata.get('model_type')}`",
        f"- Prediction semantics: `{model_metadata.get('prediction_semantics')}`",
        "",
        "## Metrics",
        _metrics_table(metrics),
        "",
        "## Calibration",
        _calibration_summary(metrics),
        "",
        "## Leakage Warnings",
        "\n".join(f"- {item}" for item in metrics.get("warnings", [])) or "- None recorded",
        "",
        "## Limitations",
        "\n".join(
            f"- {item}" for item in (limitations or ["Research prototype; proxy labels only."])
        ),
        "",
        "## Intended Use",
        str(model_metadata.get("intended_use", "Research baseline comparison.")),
        "",
        "## Not Intended Use",
        str(model_metadata.get("not_intended_use", "Clinical or consequential use.")),
        "",
        "## Next Recommended Experiment",
        "Validate on a real local dataset copy with subject/session group splits.",
    ]
    path = out / "report.md"
    path.write_text("\n".join(report))
    return path


def summarize_report_dir(report_dir: str | Path) -> dict[str, Any]:
    path = Path(report_dir)
    metrics_path = path / "metrics.json"
    metrics = json.loads(metrics_path.read_text()) if metrics_path.exists() else {}
    return {
        "report_id": path.name,
        "path": str(path / "report.md"),
        "metrics": {
            "accuracy": metrics.get("accuracy"),
            "balanced_accuracy": metrics.get("balanced_accuracy"),
            "macro_f1": metrics.get("macro_f1"),
            "ece": (metrics.get("calibration") or {}).get("ece"),
            "safety_block_rate": metrics.get("safety_block_rate"),
        },
    }


def _write_confusion_matrix(out: Path, metrics: dict[str, Any]) -> None:
    matrix = metrics.get("confusion_matrix")
    labels = metrics.get("class_labels")
    if matrix is None:
        return
    frame = pd.DataFrame(matrix, index=labels, columns=labels)
    frame.to_csv(out / "confusion_matrix.csv")


def _write_reliability_bins(out: Path, metrics: dict[str, Any]) -> None:
    bins = (metrics.get("calibration") or {}).get("reliability_bins")
    if bins:
        pd.DataFrame(bins).to_csv(out / "reliability_bins.csv", index=False)


def _write_environment(out: Path) -> None:
    env = {
        "python": sys.version,
        "platform": platform.platform(),
    }
    (out / "environment.json").write_text(json.dumps(env, indent=2))


def _write_model_card(path: Path, metadata: dict[str, Any], metrics: dict[str, Any]) -> None:
    text = "\n".join(
        [
            f"# Model Card: {metadata.get('model_id', 'model')}",
            "",
            f"- Model type: `{metadata.get('model_type')}`",
            f"- Dataset: `{metadata.get('dataset_id')}`",
            f"- Target: `{metadata.get('target')}`",
            f"- Prediction semantics: `{metadata.get('prediction_semantics')}`",
            "",
            "## Metrics",
            _metrics_table(metrics),
            "",
            "## Limitations",
            str(
                metadata.get(
                    "limitations",
                    "Dataset-derived proxy labels; not clinically validated.",
                )
            ),
            "",
        ]
    )
    path.write_text(text)


def _metrics_table(metrics: dict[str, Any]) -> str:
    keys = ["accuracy", "balanced_accuracy", "macro_f1", "weighted_f1", "auroc", "auroc_ovr_macro"]
    rows = ["| Metric | Value |", "|---|---|"]
    for key in keys:
        value = metrics.get(key)
        if value is not None:
            rows.append(f"| {key} | {value} |")
    return "\n".join(rows) if len(rows) > 2 else "No scalar metrics recorded."


def _calibration_summary(metrics: dict[str, Any]) -> str:
    calibration = metrics.get("calibration") or {}
    if not calibration.get("available"):
        return "Calibration metrics unavailable."
    return "\n".join(
        [
            f"- ECE: `{calibration.get('ece')}`",
            f"- MCE: `{calibration.get('mce')}`",
            f"- Brier score: `{calibration.get('brier_score')}`",
        ]
    )
