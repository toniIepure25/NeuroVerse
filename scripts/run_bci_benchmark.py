"""Run leakage-aware BCI classifier benchmarks on event-locked EEG features."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.metrics import evaluate_classification  # noqa: E402
from app.ml.registry import get_model_metadata  # noqa: E402

from train_eeg_event_classifier import train_event_classifier  # noqa: E402

PRIMARY_METRIC = "balanced_accuracy"
DEFERRED_MODELS = {"csp_lda", "csp_logreg", "fbcsp_logreg"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run BCI model benchmark")
    parser.add_argument("--features", required=True)
    parser.add_argument("--dataset-config", default=None)
    parser.add_argument(
        "--models",
        nargs="+",
        default=[
            "logistic_regression",
            "ridge_classifier",
            "random_forest",
            "hist_gradient_boosting",
            "svm_linear",
        ],
    )
    parser.add_argument("--split", default="group_run")
    parser.add_argument("--target", default="event_label")
    parser.add_argument("--output", default="reports/bci_benchmark/physionet_eegbci_small")
    parser.add_argument("--binary-left-right", action="store_true", default=False)
    parser.add_argument("--subjects", nargs="*", default=None)
    parser.add_argument("--runs", nargs="*", default=None)
    parser.add_argument("--n-bootstrap", type=int, default=500)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    summary = run_benchmark(
        features_path=_resolve(args.features),
        dataset_config=_resolve(args.dataset_config) if args.dataset_config else None,
        models=args.models,
        split=args.split,
        output_dir=_resolve(args.output),
        binary_left_right=args.binary_left_right,
        subjects=args.subjects,
        runs=args.runs,
        n_bootstrap=args.n_bootstrap,
        random_state=args.random_state,
    )
    print(json.dumps(summary, indent=2, default=str))


def run_benchmark(
    *,
    features_path: Path,
    dataset_config: Path | None,
    models: list[str],
    split: str,
    output_dir: Path,
    binary_left_right: bool = False,
    subjects: list[str] | None = None,
    runs: list[str] | None = None,
    n_bootstrap: int = 500,
    random_state: int = 42,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    benchmark_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_bci_benchmark"
    prepared_features = output_dir / "benchmark_features.csv"
    filter_summary = _write_filtered_features(
        features_path,
        prepared_features,
        binary_left_right=binary_left_right,
        subjects=subjects,
        runs=runs,
    )
    failures: list[dict[str, Any]] = []
    model_results: list[dict[str, Any]] = []
    per_model: dict[str, Any] = {}
    model_cards_dir = output_dir / "model_cards"
    confusion_dir = output_dir / "confusion_matrices"
    model_cards_dir.mkdir(exist_ok=True)
    confusion_dir.mkdir(exist_ok=True)

    for model_name in models:
        model_key = model_name.lower()
        if model_key in DEFERRED_MODELS:
            failure = {
                "model": model_name,
                "status": "deferred",
                "reason": (
                    "CSP/FBCSP requires raw epoch tensors; this benchmark input is a flattened "
                    "feature CSV. Deferred rather than approximated from tabular features."
                ),
            }
            failures.append(failure)
            model_results.append({"model": model_name, "status": "deferred", "reason": failure["reason"]})
            continue
        model_id = f"{output_dir.name}_{model_key}"
        try:
            result = train_event_classifier(
                features_path=prepared_features,
                model_type=model_key,
                output=f"models/{model_id}",
                split=split,
                random_state=random_state,
            )
            metrics = dict(result["metrics"])
            labels = list(result.get("labels") or metrics.get("class_labels") or [])
            ci = bootstrap_metric_intervals(
                metrics,
                labels,
                n_bootstrap=n_bootstrap,
                seed=random_state,
            )
            metrics["bootstrap_confidence_intervals"] = ci
            model_dir = Path(str(result["model_dir"]))
            _safe_copy(model_dir / "model_card.md", model_cards_dir / f"{model_key}_model_card.md")
            _safe_copy(model_dir / "confusion_matrix.csv", confusion_dir / f"{model_key}.csv")
            metadata = get_model_metadata(model_dir.name)
            model_record = {
                "model": model_key,
                "status": "ok",
                "model_id": model_dir.name,
                "model_dir": str(model_dir),
                "metrics": _key_metrics(metrics),
                "bootstrap_confidence_intervals": ci,
                "metadata": {
                    "prediction_semantics": metadata.get("prediction_semantics"),
                    "intended_use": metadata.get("intended_use"),
                    "not_intended_use": metadata.get("not_intended_use"),
                },
            }
            model_results.append(model_record)
            per_model[model_key] = {"metrics": metrics, "model_dir": str(model_dir)}
        except Exception as exc:
            failure = {"model": model_name, "status": "failed", "reason": str(exc)}
            failures.append(failure)
            model_results.append(failure)

    best = _select_best(model_results)
    leakage = _leakage_summary(filter_summary, split)
    summary = {
        "benchmark_id": benchmark_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "features": str(features_path),
        "prepared_features": str(prepared_features),
        "dataset_config": str(dataset_config) if dataset_config else None,
        "split_strategy": split,
        "primary_metric": PRIMARY_METRIC,
        "binary_left_right": binary_left_right,
        "filter_summary": filter_summary,
        "models": model_results,
        "best_model": best,
        "failures": failures,
        "leakage_warnings": leakage,
        "closed_loop_allowed": False,
        "scientific_note": (
            "Event-locked EEG classifiers predict controlled dataset task labels under "
            "experimental conditions; they should not be interpreted as general mind-reading models."
        ),
    }
    _write_json(output_dir / "benchmark_summary.json", summary)
    _write_json(output_dir / "per_model_metrics.json", per_model)
    _write_json(output_dir / "best_model.json", best or {})
    _write_json(output_dir / "leakage_warnings.json", {"warnings": leakage})
    _write_json(
        output_dir / "bootstrap_confidence_intervals.json",
        {
            item["model"]: item.get("bootstrap_confidence_intervals")
            for item in model_results
            if item.get("status") == "ok"
        },
    )
    _write_comparison_csv(output_dir / "model_comparison.csv", model_results)
    _write_markdown(output_dir / "benchmark_summary.md", summary)
    return summary


def _write_filtered_features(
    source: Path,
    destination: Path,
    *,
    binary_left_right: bool,
    subjects: list[str] | None,
    runs: list[str] | None,
) -> dict[str, Any]:
    with open(source, newline="", encoding="utf-8") as f:
        rows = [dict(row) for row in csv.DictReader(f)]
        fieldnames = list(rows[0].keys()) if rows else []
    subject_set = set(subjects or [])
    run_set = set(runs or [])
    kept = []
    for row in rows:
        label = str(row.get("event_label", ""))
        if binary_left_right and label not in {"LEFT_HAND_IMAGERY", "RIGHT_HAND_IMAGERY"}:
            continue
        if subject_set and str(row.get("subject_id", "")) not in subject_set:
            continue
        if run_set and str(row.get("run_id", "")) not in run_set:
            continue
        kept.append(row)
    if not kept:
        raise ValueError("Feature filters removed all rows.")
    with open(destination, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept)
    return {
        "input_rows": len(rows),
        "kept_rows": len(kept),
        "label_distribution": dict(Counter(row["event_label"] for row in kept)),
        "subjects": sorted({str(row.get("subject_id", "")) for row in kept}),
        "runs": sorted({str(row.get("run_id", "")) for row in kept}),
    }


def bootstrap_metric_intervals(
    metrics: dict[str, Any],
    labels: list[str],
    *,
    n_bootstrap: int,
    seed: int,
) -> dict[str, Any]:
    y_true, y_pred = _pairs_from_confusion(metrics.get("confusion_matrix") or [], labels)
    if len(y_true) < 10 or len(set(y_true)) < 2:
        return {"available": False, "warning": "Too few samples/classes for bootstrap CIs."}
    rng = np.random.default_rng(seed)
    values = {"accuracy": [], "balanced_accuracy": [], "macro_f1": []}
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)
    for _ in range(max(n_bootstrap, 1)):
        idx = rng.integers(0, len(y_true_arr), len(y_true_arr))
        sample = evaluate_classification(y_true_arr[idx], y_pred_arr[idx], None, labels)
        for key in values:
            values[key].append(float(sample[key]))
    return {
        "available": True,
        "n_bootstrap": n_bootstrap,
        "seed": seed,
        **{
            key: {
                "mean": round(float(np.mean(vals)), 4),
                "lower_95": round(float(np.percentile(vals, 2.5)), 4),
                "upper_95": round(float(np.percentile(vals, 97.5)), 4),
            }
            for key, vals in values.items()
        },
    }


def _pairs_from_confusion(confusion: list[list[int]], labels: list[str]) -> tuple[list[str], list[str]]:
    y_true: list[str] = []
    y_pred: list[str] = []
    for true_label, row in zip(labels, confusion, strict=False):
        for pred_label, count in zip(labels, row, strict=False):
            for _ in range(int(count)):
                y_true.append(true_label)
                y_pred.append(pred_label)
    return y_true, y_pred


def _key_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "accuracy": metrics.get("accuracy"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "weighted_f1": metrics.get("weighted_f1"),
        "auroc": metrics.get("auroc") or metrics.get("auroc_ovr_macro"),
        "latency": metrics.get("latency"),
    }


def _select_best(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [item for item in items if item.get("status") == "ok"]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda item: float((item.get("metrics") or {}).get(PRIMARY_METRIC) or -1.0),
    )


def _leakage_summary(filter_summary: dict[str, Any], split: str) -> list[str]:
    warnings: list[str] = []
    if split == "group_subject" and len(filter_summary.get("subjects") or []) < 2:
        warnings.append("group_subject split has fewer than two subjects.")
    if split == "group_run" and len(filter_summary.get("runs") or []) < 2:
        warnings.append("group_run split has fewer than two runs.")
    if split == "stratified":
        warnings.append("Random stratified split can overestimate performance for related EEG epochs.")
    if min((filter_summary.get("label_distribution") or {"": 0}).values()) < 5:
        warnings.append("At least one class has fewer than five epochs; metrics may be unstable.")
    return warnings


def _write_comparison_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("model,status,accuracy,balanced_accuracy,macro_f1,weighted_f1,auroc,reason\n")
        for row in rows:
            metrics = row.get("metrics") or {}
            f.write(
                ",".join([
                    str(row.get("model", "")),
                    str(row.get("status", "")),
                    _csv_value(metrics.get("accuracy")),
                    _csv_value(metrics.get("balanced_accuracy")),
                    _csv_value(metrics.get("macro_f1")),
                    _csv_value(metrics.get("weighted_f1")),
                    _csv_value(metrics.get("auroc")),
                    str(row.get("reason", "")).replace(",", ";"),
                ])
                + "\n"
            )


def _write_markdown(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        f"# BCI Benchmark: {summary['benchmark_id']}",
        "",
        "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
        "",
        "Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.",
        "",
        "## Dataset",
        f"- Features: `{summary['features']}`",
        f"- Split: `{summary['split_strategy']}`",
        f"- Binary left/right only: `{summary['binary_left_right']}`",
        f"- Rows: `{summary['filter_summary']['kept_rows']}`",
        f"- Labels: `{summary['filter_summary']['label_distribution']}`",
        "",
        "## Model Comparison",
        "| Model | Status | Accuracy | Balanced Accuracy | Macro F1 | Notes |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]
    for item in summary["models"]:
        metrics = item.get("metrics") or {}
        lines.append(
            "| {model} | {status} | {accuracy} | {balanced} | {macro} | {notes} |".format(
                model=item.get("model"),
                status=item.get("status"),
                accuracy=_fmt(metrics.get("accuracy")),
                balanced=_fmt(metrics.get("balanced_accuracy")),
                macro=_fmt(metrics.get("macro_f1")),
                notes=str(item.get("reason", "")),
            )
        )
    best = summary.get("best_model") or {}
    lines.extend([
        "",
        "## Best Model",
        f"- Model: `{best.get('model', 'none')}`",
        f"- Model id: `{best.get('model_id', 'none')}`",
        f"- Primary metric: `{summary['primary_metric']}`",
        "",
        "## Leakage Warnings",
    ])
    warnings = summary.get("leakage_warnings") or []
    lines.extend([f"- {warning}" for warning in warnings] or ["- None"])
    lines.extend([
        "",
        "## Safety",
        "Benchmark models are registered for offline and shadow evaluation only. Real EEG closed-loop adaptation remains disabled by default.",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def _safe_copy(src: Path, dst: Path) -> None:
    if src.exists():
        shutil.copy2(src, dst)


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def _csv_value(value: Any) -> str:
    return "" if value is None else str(value)


def _fmt(value: Any) -> str:
    return "—" if value is None else f"{float(value):.3f}"


def _resolve(path: str | None) -> Path:
    if path is None:
        raise ValueError("Path is required")
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
