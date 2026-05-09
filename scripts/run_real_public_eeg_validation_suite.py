"""Run real public/local EEG validation with event-locked classifier evidence."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.event_epochs import inspect_eeg_dataset_config  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real public EEG validation suite")
    parser.add_argument("--dataset-config", default=None)
    parser.add_argument("--input-file", default=None)
    parser.add_argument("--subjects", nargs="*", default=None)
    parser.add_argument("--runs", nargs="*", default=None)
    parser.add_argument("--model", default="logistic_regression")
    parser.add_argument("--split", default="group_run")
    parser.add_argument("--profile-id", default="physionet_mi_lsl")
    parser.add_argument("--output-dir", default="reports/real_public_eeg_validation")
    parser.add_argument("--skip-lsl", action="store_true")
    parser.add_argument("--skip-evidence-pack", action="store_true")
    args = parser.parse_args()
    if not args.dataset_config and not args.input_file:
        raise SystemExit("--dataset-config or --input-file is required")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_real_public_eeg")
    output = _resolve(args.output_dir) / run_id
    output.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "source_mode": "dataset_config" if args.dataset_config else "single_file",
        "dataset_config": args.dataset_config,
        "input_file": args.input_file,
        "split_strategy": args.split,
        "closed_loop_allowed": False,
        "failures": [],
        "scientific_note": (
            "Event-locked EEG classifiers predict controlled dataset task labels under "
            "experimental conditions; they are not general mind-reading models."
        ),
    }
    try:
        train_script = _load_script("train_eeg_event_classifier.py")
        compare_script = _load_script("compare_heuristic_vs_eeg_classifier.py")
        source_args = _source_args(args)
        if args.dataset_config:
            inspection = inspect_eeg_dataset_config(_resolve(args.dataset_config))
            _write_json(output / "dataset_inspection.json", inspection)
            (output / "dataset_inspection.md").write_text(_dataset_md(inspection), encoding="utf-8")
            representative = _representative_file(args.dataset_config)
        else:
            inspection = _run_json([
                sys.executable,
                str(ROOT / "scripts" / "inspect_eeg_file.py"),
                "--input-file",
                str(args.input_file),
                "--output",
                str(output / "dataset_inspection.json"),
            ])
            representative = str(_resolve(str(args.input_file)))

        features_path = output / "event_features.csv"
        feature_summary = _run_json([
            sys.executable,
            str(ROOT / "scripts" / "prepare_event_locked_dataset.py"),
            *source_args,
            "--output",
            str(features_path),
            "--tmin",
            "0.0",
            "--tmax",
            "2.0",
        ])
        feature_md = _feature_md(feature_summary)
        (output / "event_dataset_summary.md").write_text(feature_md, encoding="utf-8")

        model_id = f"{Path(representative).stem}_event_classifier"
        model_dir = ROOT / "models" / model_id
        train_result = train_script.train_event_classifier(
            features_path=features_path,
            model_type=args.model,
            output=str(model_dir),
            split=args.split,
        )
        _copy_if_exists(model_dir / "metrics.json", output / "classifier_metrics.json")
        _copy_if_exists(model_dir / "confusion_matrix.csv", output / "confusion_matrix.csv")
        _copy_if_exists(model_dir / "per_subject_metrics.csv", output / "per_subject_metrics.csv")
        _copy_if_exists(model_dir / "per_run_metrics.csv", output / "per_run_metrics.csv")
        _copy_if_exists(model_dir / "model_card.md", output / "classifier_model_card.md")

        classifier_shadow = _classifier_shadow(features_path, model_id)
        _write_json(output / "classifier_shadow_report.json", classifier_shadow)
        lsl_results: dict[str, Any] = {}
        if not args.skip_lsl:
            lsl_results = _run_lsl(representative, output, args.profile_id)
        comparison = compare_script.compare_reports(
            heuristic=lsl_results.get("heuristic_shadow", {}),
            classifier=classifier_shadow,
            validation=lsl_results.get("validation", {}),
            calibration=lsl_results.get("calibration", {}),
        )
        _write_json(output / "heuristic_vs_classifier_comparison.json", comparison)
        (output / "heuristic_vs_classifier_comparison.md").write_text(
            _comparison_md(comparison),
            encoding="utf-8",
        )
        if not args.skip_evidence_pack:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "generate_evidence_pack.py")],
                cwd=ROOT,
                check=True,
            )
        summary.update({
            "inspection": inspection,
            "feature_summary": feature_summary,
            "classifier_metrics": train_result["metrics"],
            "model_dir": train_result["model_dir"],
            "classifier_shadow": classifier_shadow,
            "comparison": comparison,
            "lsl": lsl_results,
            "representative_file": representative,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as exc:
        summary["failures"].append(str(exc))
        summary["completed_at"] = datetime.now(timezone.utc).isoformat()
        _write_summary(output, summary)
        print(json.dumps(summary, indent=2, default=str))
        raise SystemExit(1) from exc
    _write_summary(output, summary)
    print(json.dumps(summary, indent=2, default=str))


def _source_args(args: argparse.Namespace) -> list[str]:
    if args.dataset_config:
        return ["--dataset-config", str(_resolve(args.dataset_config))]
    return ["--input-file", str(_resolve(str(args.input_file)))]


def _representative_file(config_path: str) -> str:
    cfg = yaml.safe_load(_resolve(config_path).read_text(encoding="utf-8")) or {}
    root = Path(str(cfg.get("local_root", "")))
    if not root.is_absolute():
        root = (ROOT / root).resolve()
    for item in cfg.get("files") or []:
        path = Path(str(item.get("path", "")))
        candidate = path if path.is_absolute() else root / path
        if candidate.exists():
            return str(candidate)
    raise FileNotFoundError("No existing EDF files found in dataset config.")


def _run_lsl(representative_file: str, output: Path, profile_id: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_eeg_lsl_validation_suite.py"),
            "--input-file",
            representative_file,
            "--output-dir",
            str(output / "lsl"),
            "--profile-id",
            profile_id,
            "--skip-evidence-pack",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return {"failure": completed.stderr or completed.stdout}
    latest = sorted((output / "lsl").glob("*_eeg_lsl"))[-1]
    for src, dst in {
        "validation_report.json": "lsl_validation_report.json",
        "calibration_report.json": "calibration_report.json",
        "shadow_report.json": "heuristic_shadow_report.json",
    }.items():
        _copy_if_exists(latest / src, output / dst)
    return {
        "run_dir": str(latest),
        "validation": _read(latest / "validation_report.json"),
        "calibration": _read(latest / "calibration_report.json"),
        "heuristic_shadow": _read(latest / "shadow_report.json"),
    }


def _classifier_shadow(features_path: Path, model_id: str) -> dict[str, Any]:
    public_suite = _load_script("run_public_eeg_validation_suite.py")
    return public_suite._classifier_shadow_report(features_path, model_id)


def _load_script(filename: str) -> Any:
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_summary(output: Path, summary: dict[str, Any]) -> None:
    _write_json(output / "real_public_eeg_validation_summary.json", summary)
    metrics = summary.get("classifier_metrics") or {}
    feature_summary = summary.get("feature_summary") or {}
    lines = [
        f"# Real Public EEG Validation: {summary['run_id']}",
        "",
        f"- source mode: `{summary.get('source_mode')}`",
        f"- representative file: `{summary.get('representative_file')}`",
        f"- split strategy: `{summary.get('split_strategy')}`",
        f"- epochs: `{feature_summary.get('row_count')}`",
        f"- balanced accuracy: `{metrics.get('balanced_accuracy')}`",
        f"- macro F1: `{metrics.get('macro_f1')}`",
        f"- closed-loop allowed: `{summary.get('closed_loop_allowed')}`",
        f"- failures: `{len(summary.get('failures') or [])}`",
        "",
        (
            "Event-locked EEG classifiers predict controlled dataset task labels under "
            "experimental conditions; they should not be interpreted as general "
            "mind-reading models."
        ),
        "",
        (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
    ]
    (output / "real_public_eeg_validation_summary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def _dataset_md(report: dict[str, object]) -> str:
    return "\n".join([
        f"# Dataset Inspection: {report.get('dataset_id')}",
        "",
        f"- files configured: `{report.get('file_count')}`",
        f"- files inspected: `{report.get('inspected_file_count')}`",
        f"- annotation distribution: `{report.get('annotation_label_distribution')}`",
        f"- warnings: `{len(report.get('warnings') or [])}`",
    ])


def _feature_md(summary: dict[str, object]) -> str:
    return "\n".join([
        "# Event Feature Dataset",
        "",
        f"- rows: `{summary.get('row_count')}`",
        f"- features: `{summary.get('feature_count')}`",
        f"- labels: `{summary.get('label_distribution')}`",
        f"- subjects: `{summary.get('subject_distribution')}`",
        f"- runs: `{summary.get('run_distribution')}`",
    ])


def _comparison_md(result: dict[str, Any]) -> str:
    return "\n".join([
        "# Heuristic vs Public EEG Event Classifier",
        "",
        f"- classifier model: `{result.get('classifier_model_id')}`",
        f"- classifier accuracy: `{result.get('classifier_accuracy')}`",
        f"- closed-loop allowed: `{result.get('closed_loop_allowed')}`",
        "",
        "The learned model predicts dataset event labels in shadow mode only.",
    ])


def _run_json(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
    start = completed.stdout.find("{")
    end = completed.stdout.rfind("}")
    return json.loads(completed.stdout[start : end + 1])


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def _copy_if_exists(src: Path, dst: Path) -> None:
    if src.exists():
        shutil.copy2(src, dst)


def _resolve(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
