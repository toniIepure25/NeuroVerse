"""Run leakage-aware CSP benchmarks on raw EEG epoch tensors."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.model_selection import GroupShuffleSplit, LeaveOneGroupOut, train_test_split

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.metrics import evaluate_classification  # noqa: E402
from app.ml.raw_epoch_models import create_raw_epoch_model  # noqa: E402
from app.ml.registry import register_model  # noqa: E402

PRIMARY_METRIC = "balanced_accuracy"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run raw epoch CSP BCI benchmark")
    parser.add_argument("--epochs", required=True)
    parser.add_argument(
        "--models",
        nargs="+",
        default=["csp_lda", "csp_logreg", "csp_svm_linear"],
    )
    parser.add_argument("--split", default="group_run")
    parser.add_argument("--train-runs", nargs="*", default=None)
    parser.add_argument("--test-runs", nargs="*", default=None)
    parser.add_argument("--n-components-grid", nargs="*", type=int, default=[2, 4, 6, 8])
    parser.add_argument(
        "--filter-bank-bands",
        nargs="*",
        default=["8-12", "12-16", "16-20", "20-24", "24-30"],
    )
    parser.add_argument("--output", default="reports/bci_raw_epoch_benchmark/physionet_eegbci_small")
    parser.add_argument("--n-bootstrap", type=int, default=500)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    summary = run_raw_benchmark(
        epochs_path=_resolve(args.epochs),
        models=args.models,
        split=args.split,
        train_runs=args.train_runs,
        test_runs=args.test_runs,
        n_components_grid=args.n_components_grid,
        filter_bank_bands=parse_bands(args.filter_bank_bands),
        output_dir=_resolve(args.output),
        n_bootstrap=args.n_bootstrap,
        random_state=args.random_state,
    )
    print(json.dumps(summary, indent=2, default=str))


def run_raw_benchmark(
    *,
    epochs_path: Path,
    models: list[str],
    split: str,
    output_dir: Path,
    train_runs: list[str] | None = None,
    test_runs: list[str] | None = None,
    n_components_grid: list[int] | None = None,
    filter_bank_bands: list[tuple[float, float]] | None = None,
    n_bootstrap: int = 500,
    random_state: int = 42,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    data = load_raw_epochs(epochs_path)
    x = data["X"]
    y = data["y"]
    subjects = data["subject_ids"]
    runs = data["run_ids"]
    labels = sorted(np.unique(y).tolist())
    sampling_rate = float(np.asarray(data.get("sampling_rate", np.asarray(160.0))).reshape(-1)[0])
    benchmark_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_raw_bci"
    train_idx, test_idx, split_warnings = make_raw_split(
        y,
        subjects,
        runs,
        split=split,
        train_runs=train_runs,
        test_runs=test_runs,
        random_state=random_state,
    )
    failures: list[dict[str, Any]] = []
    model_results: list[dict[str, Any]] = []
    per_model: dict[str, Any] = {}
    confusion_dir = output_dir / "confusion_matrices"
    model_cards_dir = output_dir / "model_cards"
    confusion_dir.mkdir(exist_ok=True)
    model_cards_dir.mkdir(exist_ok=True)

    for model_name in models:
        for n_components in n_components_grid or [4]:
            key = f"{model_name}_csp{n_components}"
            try:
                result = _fit_evaluate_register(
                    x,
                    y,
                    subjects,
                    runs,
                    labels,
                    train_idx,
                    test_idx,
                    model_name=model_name,
                    n_components=n_components,
                    sampling_rate=sampling_rate,
                    filter_bank_bands=filter_bank_bands,
                    epochs_path=epochs_path,
                    split=split,
                    split_warnings=split_warnings,
                    random_state=random_state,
                    output_dir=output_dir,
                    n_bootstrap=n_bootstrap,
                )
                model_results.append(result["record"])
                per_model[key] = result["metrics"]
                _write_confusion_csv(
                    confusion_dir / f"{key}.csv",
                    labels,
                    result["metrics"]["confusion_matrix"],
                )
                _safe_copy(
                    Path(result["record"]["model_dir"]) / "model_card.md",
                    model_cards_dir / f"{key}_model_card.md",
                )
            except Exception as exc:
                failure = {
                    "model": model_name,
                    "n_components": n_components,
                    "status": "failed",
                    "reason": str(exc),
                }
                failures.append(failure)
                model_results.append(failure)
    loso = (
        run_loso(
            x,
            y,
            subjects,
            runs,
            labels,
            models,
            n_components_grid or [4],
            random_state,
            sampling_rate,
            filter_bank_bands,
        )
        if split == "leave_one_subject_out"
        else {"available": False, "reason": "LOSO not requested for this run."}
    )
    best = _select_best(model_results)
    summary = {
        "benchmark_id": benchmark_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "epochs": str(epochs_path),
        "split_strategy": split,
        "primary_metric": PRIMARY_METRIC,
        "shape": list(x.shape),
        "sampling_rate_hz": sampling_rate,
        "labels": labels,
        "label_distribution": dict(Counter(y.tolist())),
        "subjects": sorted(set(subjects.tolist())),
        "runs": sorted(set(runs.tolist())),
        "models": model_results,
        "best_model": best,
        "failures": failures,
        "leakage_warnings": leakage_warnings(subjects, runs, train_idx, test_idx, split)
        + split_warnings,
        "loso": loso,
        "closed_loop_allowed": False,
        "scientific_note": (
            "Raw-epoch CSP models predict controlled motor imagery task labels; they are not "
            "thought decoders and are not enabled for closed-loop adaptation."
        ),
    }
    _write_json(output_dir / "benchmark_summary.json", summary)
    _write_json(output_dir / "per_model_metrics.json", per_model)
    _write_json(output_dir / "best_model.json", best or {})
    _write_json(output_dir / "leakage_warnings.json", {"warnings": summary["leakage_warnings"]})
    _write_json(output_dir / "bootstrap_confidence_intervals.json", {
        _record_key(item): item.get("bootstrap_confidence_intervals")
        for item in model_results
        if item.get("status") == "ok"
    })
    if loso.get("available"):
        _write_loso_csv(output_dir / "loso_metrics.csv", loso.get("folds") or [])
        _write_json(output_dir / "loso_summary.json", loso)
    _write_comparison_csv(output_dir / "model_comparison.csv", model_results)
    _write_markdown(output_dir / "benchmark_summary.md", summary)
    return summary


def load_raw_epochs(path: Path) -> dict[str, np.ndarray]:
    with np.load(path, allow_pickle=True) as npz:
        return {key: npz[key] for key in npz.files}


def make_raw_split(
    y: np.ndarray,
    subjects: np.ndarray,
    runs: np.ndarray,
    *,
    split: str,
    train_runs: list[str] | None,
    test_runs: list[str] | None,
    random_state: int,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    idx = np.arange(len(y))
    warnings: list[str] = []
    if train_runs or test_runs:
        train_set = set(train_runs or [])
        test_set = set(test_runs or [])
        train_idx = np.asarray([i for i, run in enumerate(runs) if str(run) in train_set])
        test_idx = np.asarray([i for i, run in enumerate(runs) if str(run) in test_set])
        if len(train_idx) and len(test_idx):
            return train_idx, test_idx, []
        warnings.append("Explicit train/test run split was empty; falling back to configured split.")
    if split == "group_subject":
        return _group_split(y, subjects, random_state, warnings)
    if split == "group_run":
        groups = np.asarray([f"{s}_run_{r}" for s, r in zip(subjects, runs, strict=False)])
        return _group_split(y, groups, random_state, warnings)
    if split == "leave_one_subject_out":
        unique = sorted(set(subjects.tolist()))
        if len(unique) < 2:
            warnings.append("LOSO unavailable with fewer than two subjects.")
            return _stratified_split(y, random_state, warnings)
        test_subject = unique[-1]
        train_idx = np.asarray([i for i, subject in enumerate(subjects) if subject != test_subject])
        test_idx = np.asarray([i for i, subject in enumerate(subjects) if subject == test_subject])
        return train_idx, test_idx, []
    if split == "within_subject":
        warnings.append("within_subject can share subject identity; use only for within-participant estimates.")
    return _stratified_split(y, random_state, warnings)


def _group_split(
    y: np.ndarray,
    groups: np.ndarray,
    random_state: int,
    warnings: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    if len(set(groups.tolist())) < 2:
        warnings.append("Group split unavailable with fewer than two groups.")
        return _stratified_split(y, random_state, warnings)
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.35, random_state=random_state)
    train_idx, test_idx = next(splitter.split(np.arange(len(y)), y, groups))
    return train_idx, test_idx, warnings


def _stratified_split(
    y: np.ndarray,
    random_state: int,
    warnings: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    _, counts = np.unique(y, return_counts=True)
    stratify = y if len(counts) > 1 and np.all(counts >= 2) else None
    if stratify is None:
        warnings.append("Stratified split unavailable because a class is too small.")
    train_idx, test_idx = train_test_split(
        np.arange(len(y)),
        test_size=0.35,
        random_state=random_state,
        stratify=stratify,
    )
    return train_idx, test_idx, warnings


def _fit_evaluate_register(
    x: np.ndarray,
    y: np.ndarray,
    subjects: np.ndarray,
    runs: np.ndarray,
    labels: list[str],
    train_idx: np.ndarray,
    test_idx: np.ndarray,
    *,
    model_name: str,
    n_components: int,
    sampling_rate: float,
    filter_bank_bands: list[tuple[float, float]] | None,
    epochs_path: Path,
    split: str,
    split_warnings: list[str],
    random_state: int,
    output_dir: Path,
    n_bootstrap: int,
) -> dict[str, Any]:
    model = create_raw_epoch_model(
        model_name,
        n_components=n_components,
        random_state=random_state,
        sampling_rate=sampling_rate,
        bands=filter_bank_bands,
    )
    model.fit(x[train_idx], y[train_idx])
    preds = model.predict(x[test_idx])
    probs = model.predict_proba(x[test_idx])
    metrics = evaluate_classification(y[test_idx], preds, probs, labels)
    metrics["split_strategy"] = split
    metrics["split_warnings"] = split_warnings
    metrics["latency"] = measure_raw_latency(model, x[test_idx])
    metrics["per_subject"] = grouped_metrics(model, x[test_idx], y[test_idx], subjects[test_idx], labels)
    metrics["per_run"] = grouped_metrics(model, x[test_idx], y[test_idx], runs[test_idx], labels)
    metrics["bootstrap_confidence_intervals"] = bootstrap_intervals(
        y[test_idx],
        preds,
        labels,
        n_bootstrap=n_bootstrap,
        seed=random_state,
    )
    model_id = f"{output_dir.name}_{model.model_type}_csp{n_components}"
    model_dir = register_model(
        model,
        model_id=model_id,
        metadata={
            "dataset_id": epochs_path.stem,
            "target": "event_label",
            "prediction_semantics": "motor_intent",
            "raw_epoch_model": True,
            "epoch_tensor_file": str(epochs_path),
            "event_labels": labels,
            "subjects": sorted(set(subjects.tolist())),
            "runs": sorted(set(runs.tolist())),
            "split_strategy": split,
            "csp_components": n_components,
            "sampling_rate_hz": sampling_rate,
            "filter_bank_bands": filter_bank_bands or [],
            "intended_use": "Offline event-locked motor imagery task-label classification.",
            "not_intended_use": (
                "Not for thought reading, clinical diagnosis, unrestricted mental-state inference, "
                "or direct closed-loop control."
            ),
            "limitations": (
                "Small public EEG subset; CSP is fit inside train splits. Metrics are benchmark "
                "evidence only and do not establish clinical validity."
            ),
        },
        metrics=metrics,
    )
    _write_group_csv(model_dir / "per_subject_metrics.csv", metrics["per_subject"])
    _write_group_csv(model_dir / "per_run_metrics.csv", metrics["per_run"])
    _write_confusion_csv(model_dir / "confusion_matrix.csv", labels, metrics["confusion_matrix"])
    record = {
        "model": model.model_type,
        "n_components": n_components,
        "status": "ok",
        "model_id": model_id,
        "model_dir": str(model_dir),
        "metrics": key_metrics(metrics),
        "bootstrap_confidence_intervals": metrics["bootstrap_confidence_intervals"],
        "metadata": model.metadata(),
    }
    return {"record": record, "metrics": metrics}


def run_loso(
    x: np.ndarray,
    y: np.ndarray,
    subjects: np.ndarray,
    runs: np.ndarray,
    labels: list[str],
    models: list[str],
    n_components_grid: list[int],
    random_state: int,
    sampling_rate: float,
    filter_bank_bands: list[tuple[float, float]] | None,
) -> dict[str, Any]:
    unique = sorted(set(subjects.tolist()))
    if len(unique) < 2:
        return {"available": False, "reason": "Fewer than two subjects."}
    best_model = models[0]
    best_components = n_components_grid[0]
    folds = []
    for train_idx, test_idx in LeaveOneGroupOut().split(np.arange(len(y)), y, subjects):
        held_out = str(subjects[test_idx][0])
        if len(set(y[train_idx])) < 2 or len(set(y[test_idx])) < 2:
            folds.append({"subject": held_out, "status": "skipped", "reason": "Missing class."})
            continue
        model = create_raw_epoch_model(
            best_model,
            n_components=best_components,
            random_state=random_state,
            sampling_rate=sampling_rate,
            bands=filter_bank_bands,
        )
        model.fit(x[train_idx], y[train_idx])
        preds = model.predict(x[test_idx])
        metrics = evaluate_classification(y[test_idx], preds, model.predict_proba(x[test_idx]), labels)
        folds.append({
            "subject": held_out,
            "status": "ok",
            "accuracy": metrics["accuracy"],
            "balanced_accuracy": metrics["balanced_accuracy"],
            "macro_f1": metrics["macro_f1"],
            "test_rows": int(len(test_idx)),
        })
    ok = [fold for fold in folds if fold.get("status") == "ok"]
    return {
        "available": bool(ok),
        "model": best_model,
        "n_components": best_components,
        "folds": folds,
        "mean_balanced_accuracy": float(np.mean([fold["balanced_accuracy"] for fold in ok])) if ok else None,
        "mean_macro_f1": float(np.mean([fold["macro_f1"] for fold in ok])) if ok else None,
    }


def grouped_metrics(
    model: Any,
    x: np.ndarray,
    y: np.ndarray,
    groups: np.ndarray,
    labels: list[str],
) -> dict[str, Any]:
    result = {}
    for group in sorted(set(groups.tolist())):
        idx = np.asarray([i for i, item in enumerate(groups) if item == group])
        if len(idx) == 0:
            continue
        result[str(group)] = evaluate_classification(y[idx], model.predict(x[idx]), None, labels)
    return result


def measure_raw_latency(model: Any, x: np.ndarray, repeats: int = 1) -> dict[str, float]:
    durations = []
    for epoch in x:
        sample = epoch.reshape(1, epoch.shape[0], epoch.shape[1])
        for _ in range(repeats):
            t0 = time.perf_counter()
            model.predict(sample)
            durations.append((time.perf_counter() - t0) * 1000.0)
    arr = np.asarray(durations, dtype=float)
    return {
        "mean_inference_latency_ms": float(np.mean(arr)),
        "p95_inference_latency_ms": float(np.percentile(arr, 95)),
        "p99_inference_latency_ms": float(np.percentile(arr, 99)),
        "throughput_samples_per_sec": float(1000.0 / max(np.mean(arr), 1e-9)),
    }


def bootstrap_intervals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    labels: list[str],
    *,
    n_bootstrap: int,
    seed: int,
) -> dict[str, Any]:
    if len(y_true) < 10 or len(set(y_true.tolist())) < 2:
        return {"available": False, "warning": "Too few samples/classes for bootstrap CIs."}
    rng = np.random.default_rng(seed)
    values = {"accuracy": [], "balanced_accuracy": [], "macro_f1": []}
    for _ in range(max(n_bootstrap, 1)):
        idx = rng.integers(0, len(y_true), len(y_true))
        sample = evaluate_classification(y_true[idx], y_pred[idx], None, labels)
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


def leakage_warnings(
    subjects: np.ndarray,
    runs: np.ndarray,
    train_idx: np.ndarray,
    test_idx: np.ndarray,
    split: str,
) -> list[str]:
    warnings = []
    if split == "group_subject":
        overlap = set(subjects[train_idx].tolist()) & set(subjects[test_idx].tolist())
        if overlap:
            warnings.append(f"Subject leakage detected: {sorted(overlap)}")
    if split == "group_run":
        train_groups = {f"{subjects[i]}_run_{runs[i]}" for i in train_idx}
        test_groups = {f"{subjects[i]}_run_{runs[i]}" for i in test_idx}
        overlap = train_groups & test_groups
        if overlap:
            warnings.append(f"Run leakage detected: {sorted(overlap)[:5]}")
    if split in {"stratified", "within_subject"}:
        warnings.append(f"{split} split can share subject/run identity; use group splits for generalization.")
    return warnings


def key_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "accuracy": metrics.get("accuracy"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "weighted_f1": metrics.get("weighted_f1"),
        "auroc": metrics.get("auroc") or metrics.get("auroc_ovr_macro"),
        "latency": metrics.get("latency"),
    }


def _select_best(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    ok = [item for item in records if item.get("status") == "ok"]
    if not ok:
        return None
    return max(
        ok,
        key=lambda item: (
            float((item.get("metrics") or {}).get("balanced_accuracy") or -1.0),
            float((item.get("metrics") or {}).get("macro_f1") or -1.0),
        ),
    )


def _record_key(item: dict[str, Any]) -> str:
    return f"{item.get('model')}_csp{item.get('n_components')}"


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def _write_comparison_csv(path: Path, records: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "model",
            "n_components",
            "status",
            "accuracy",
            "balanced_accuracy",
            "macro_f1",
            "auroc",
            "reason",
        ])
        for item in records:
            metrics = item.get("metrics") or {}
            writer.writerow([
                item.get("model"),
                item.get("n_components"),
                item.get("status"),
                metrics.get("accuracy"),
                metrics.get("balanced_accuracy"),
                metrics.get("macro_f1"),
                metrics.get("auroc"),
                item.get("reason", ""),
            ])


def _write_markdown(path: Path, summary: dict[str, Any]) -> None:
    best = summary.get("best_model") or {}
    lines = [
        "# Raw-Epoch CSP BCI Benchmark",
        "",
        f"- Benchmark: {summary.get('benchmark_id')}",
        f"- Split: {summary.get('split_strategy')}",
        f"- Shape: {summary.get('shape')}",
        f"- Labels: {summary.get('label_distribution')}",
        f"- Best model: {best.get('model')} csp={best.get('n_components')}",
        f"- Best balanced accuracy: {(best.get('metrics') or {}).get('balanced_accuracy')}",
        f"- Closed-loop allowed: {summary.get('closed_loop_allowed')}",
        "",
        "## Model Comparison",
        "",
        "| Model | CSP components | Status | Balanced accuracy | Macro F1 |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for item in summary.get("models") or []:
        metrics = item.get("metrics") or {}
        lines.append(
            f"| {item.get('model')} | {item.get('n_components', '')} | {item.get('status')} | "
            f"{metrics.get('balanced_accuracy', '')} | {metrics.get('macro_f1', '')} |"
        )
    lines.extend([
        "",
        "Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_confusion_csv(path: Path, labels: list[str], matrix: list[list[int]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("," + ",".join(labels) + "\n")
        for label, row in zip(labels, matrix, strict=False):
            f.write(label + "," + ",".join(str(value) for value in row) + "\n")


def _write_group_csv(path: Path, grouped: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("group,accuracy,balanced_accuracy,macro_f1,row_count\n")
        for group, metrics in grouped.items():
            row_count = ((metrics.get("per_class") or {}).get("macro avg") or {}).get("support")
            f.write(
                f"{group},{metrics.get('accuracy')},{metrics.get('balanced_accuracy')},"
                f"{metrics.get('macro_f1')},{row_count}\n"
            )


def _write_loso_csv(path: Path, folds: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("subject,status,accuracy,balanced_accuracy,macro_f1,test_rows,reason\n")
        for fold in folds:
            f.write(
                f"{fold.get('subject')},{fold.get('status')},{fold.get('accuracy','')},"
                f"{fold.get('balanced_accuracy','')},{fold.get('macro_f1','')},"
                f"{fold.get('test_rows','')},{fold.get('reason','')}\n"
            )


def _safe_copy(src: Path, dst: Path) -> None:
    if src.exists():
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _resolve(path: str) -> Path:
    item = Path(path)
    return item if item.is_absolute() else ROOT / item


def parse_bands(values: list[str]) -> list[tuple[float, float]]:
    bands = []
    for value in values:
        if "-" not in value:
            raise ValueError(f"Filter-bank band must look like low-high: {value}")
        low, high = value.split("-", 1)
        bands.append((float(low), float(high)))
    return bands


if __name__ == "__main__":
    main()
