"""Compare flattened-feature and raw-epoch BCI benchmark reports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare BCI benchmark reports")
    parser.add_argument("--flattened", default="reports/bci_benchmark/physionet_eegbci_small")
    parser.add_argument("--raw", default="reports/bci_raw_epoch_benchmark/physionet_eegbci_small")
    parser.add_argument("--medium-group-run", default=None)
    parser.add_argument("--medium-group-subject", default=None)
    parser.add_argument("--medium-loso", default=None)
    parser.add_argument("--live-shadow", default=None)
    parser.add_argument("--output", default="reports/bci_benchmark_comparison/physionet_eegbci_small")
    args = parser.parse_args()
    result = compare_benchmarks(
        flattened_dir=_resolve(args.flattened),
        raw_dir=_resolve(args.raw),
        medium_group_run=_resolve(args.medium_group_run) if args.medium_group_run else None,
        medium_group_subject=_resolve(args.medium_group_subject) if args.medium_group_subject else None,
        medium_loso=_resolve(args.medium_loso) if args.medium_loso else None,
        live_shadow=_resolve(args.live_shadow) if args.live_shadow else None,
        output_dir=_resolve(args.output),
    )
    print(json.dumps(result, indent=2, default=str))


def compare_benchmarks(
    *,
    flattened_dir: Path,
    raw_dir: Path,
    medium_group_run: Path | None = None,
    medium_group_subject: Path | None = None,
    medium_loso: Path | None = None,
    live_shadow: Path | None = None,
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    flat = _load(flattened_dir / "benchmark_summary.json")
    raw = _load(raw_dir / "benchmark_summary.json")
    medium = {
        "group_run": _best_summary(_load_report_dir(medium_group_run), "medium_raw_group_run") if medium_group_run else None,
        "group_subject": _best_summary(_load_report_dir(medium_group_subject), "medium_raw_group_subject") if medium_group_subject else None,
        "loso": _best_summary(_load_report_dir(medium_loso), "medium_raw_loso") if medium_loso else None,
    }
    result = {
        "comparison_id": f"{raw_dir.name}_raw_vs_flattened",
        "flattened_benchmark": str(flattened_dir),
        "raw_epoch_benchmark": str(raw_dir),
        "medium_benchmarks": {
            key: value for key, value in medium.items() if value and not value.get("missing")
        },
        "live_shadow": _load_live_shadow(live_shadow),
        "flattened_best": _best_summary(flat, "flattened_feature_model"),
        "raw_epoch_best": _best_summary(raw, "raw_epoch_csp_model"),
        "fbcsp_best": _best_fbcsp(raw),
        "closed_loop_allowed": False,
        "interpretation": (
            "Flattened features are an engineered tabular baseline; CSP models are raw-epoch "
            "spatial-filter baselines. Neither result is a thought-reading or clinical claim."
        ),
        "limitations": [
            "Small PhysioNet EEGBCI subset.",
            "Metrics depend on split strategy and event labels.",
            "Closed-loop adaptation from real EEG remains disabled.",
        ],
    }
    (output_dir / "comparison.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (output_dir / "comparison.md").write_text(_markdown(result), encoding="utf-8")
    return result


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"missing": True, "path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_report_dir(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"missing": True}
    return _load(path / "benchmark_summary.json")


def _best_summary(report: dict[str, Any], pipeline: str) -> dict[str, Any]:
    best = report.get("best_model") or {}
    metrics = best.get("metrics") or {}
    ci = best.get("bootstrap_confidence_intervals") or {}
    return {
        "pipeline": pipeline,
        "benchmark_id": report.get("benchmark_id"),
        "split_strategy": report.get("split_strategy"),
        "model": best.get("model"),
        "model_id": best.get("model_id"),
        "n_components": best.get("n_components"),
        "accuracy": metrics.get("accuracy"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "balanced_accuracy_ci": ci.get("balanced_accuracy"),
    }


def _markdown(result: dict[str, Any]) -> str:
    flat = result["flattened_best"]
    raw = result["raw_epoch_best"]
    fbcsp = result.get("fbcsp_best") or {}
    medium_rows = []
    for name, item in (result.get("medium_benchmarks") or {}).items():
        medium_rows.append(
            f"| Medium {name} | {item.get('model')} csp={item.get('n_components')} | {item.get('split_strategy')} | {item.get('balanced_accuracy')} | {item.get('macro_f1')} |"
        )
    shadow = result.get("live_shadow") or {}
    return "\n".join([
        "# BCI Benchmark Comparison",
        "",
        "| Pipeline | Model | Split | Balanced accuracy | Macro F1 |",
        "| --- | --- | --- | ---: | ---: |",
        f"| Flattened features | {flat.get('model')} | {flat.get('split_strategy')} | {flat.get('balanced_accuracy')} | {flat.get('macro_f1')} |",
        f"| Raw epochs / CSP | {raw.get('model')} csp={raw.get('n_components')} | {raw.get('split_strategy')} | {raw.get('balanced_accuracy')} | {raw.get('macro_f1')} |",
        f"| Raw epochs / FBCSP | {fbcsp.get('model')} csp={fbcsp.get('n_components')} | {fbcsp.get('split_strategy')} | {fbcsp.get('balanced_accuracy')} | {fbcsp.get('macro_f1')} |",
        *medium_rows,
        "",
        f"Live raw shadow mode: `{shadow.get('mode', 'not_available')}`; predictions: {shadow.get('prediction_count', '—')}; missed epochs: {shadow.get('missed_epochs', '—')}.",
        "",
        result["interpretation"],
        "",
        "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
    ])


def _resolve(path: str) -> Path:
    item = Path(path)
    return item if item.is_absolute() else ROOT / item


def _best_fbcsp(report: dict[str, Any]) -> dict[str, Any]:
    items = [
        item
        for item in report.get("models") or []
        if item.get("status") == "ok" and str(item.get("model", "")).startswith("fbcsp")
    ]
    if not items:
        return {
            "pipeline": "raw_epoch_fbcsp_model",
            "status": "not_available",
            "reason": "No successful FBCSP model in benchmark.",
        }
    best = max(
        items,
        key=lambda item: (
            float((item.get("metrics") or {}).get("balanced_accuracy") or -1),
            float((item.get("metrics") or {}).get("macro_f1") or -1),
        ),
    )
    metrics = best.get("metrics") or {}
    ci = best.get("bootstrap_confidence_intervals") or {}
    return {
        "pipeline": "raw_epoch_fbcsp_model",
        "benchmark_id": report.get("benchmark_id"),
        "split_strategy": report.get("split_strategy"),
        "model": best.get("model"),
        "model_id": best.get("model_id"),
        "n_components": best.get("n_components"),
        "accuracy": metrics.get("accuracy"),
        "balanced_accuracy": metrics.get("balanced_accuracy"),
        "macro_f1": metrics.get("macro_f1"),
        "balanced_accuracy_ci": ci.get("balanced_accuracy"),
    }


def _load_live_shadow(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {"status": "not_available"}
    summary = path / "live_shadow_summary.json" if path.is_dir() else path
    if not summary.exists():
        return {"status": "not_available", "path": str(summary)}
    report = json.loads(summary.read_text(encoding="utf-8"))
    return {
        "status": report.get("status", "completed"),
        "path": str(summary),
        "mode": report.get("mode"),
        "model_id": report.get("model_id"),
        "prediction_count": report.get("prediction_count"),
        "markers_seen": report.get("markers_seen"),
        "epochs_built": report.get("epochs_built"),
        "missed_epochs": report.get("missed_epochs"),
        "balanced_accuracy": (report.get("metrics") or {}).get("balanced_accuracy"),
        "closed_loop_allowed": report.get("closed_loop_allowed"),
    }


if __name__ == "__main__":
    main()
