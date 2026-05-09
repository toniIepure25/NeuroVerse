"""Run public/local EEG validation plus event-locked classifier evidence workflow."""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.event_epochs import read_feature_csv  # noqa: E402
from app.ml.registry import get_model_metadata, load_model  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run public EEG validation fixture/local suite")
    parser.add_argument("--input-file", default=None)
    parser.add_argument("--fixture-mode", action="store_true", default=True)
    parser.add_argument("--output-dir", default="reports/public_eeg_validation")
    parser.add_argument("--model", default="logistic_regression")
    parser.add_argument("--model-id", default="eeg_event_classifier_fixture")
    parser.add_argument("--skip-lsl", action="store_true")
    args = parser.parse_args()
    if args.input_file:
        args.fixture_mode = False
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_public_eeg")
    output = _resolve(args.output_dir) / run_id
    output.mkdir(parents=True, exist_ok=True)

    summary: dict[str, Any] = {
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "fixture_mode": args.fixture_mode,
        "input_file": args.input_file,
        "closed_loop_allowed": False,
        "scientific_note": (
            "Event-locked EEG classifiers predict dataset task labels under controlled "
            "conditions; they are not general mind-reading models."
        ),
        "artifacts": {},
        "failures": [],
    }
    try:
        train_script = _load_script("train_eeg_event_classifier.py")
        compare_script = _load_script("compare_heuristic_vs_eeg_classifier.py")
        inspection = _run_json([
            sys.executable,
            str(ROOT / "scripts" / "inspect_eeg_file.py"),
            *(_source_args(args)),
            "--output",
            str(output / "eeg_file_inspection.json"),
        ])
        features_path = output / "eeg_event_features.csv"
        feature_summary = _run_json([
            sys.executable,
            str(ROOT / "scripts" / "prepare_event_locked_dataset.py"),
            *(_source_args(args)),
            "--output",
            str(features_path),
        ])
        model_dir = ROOT / "models" / args.model_id
        train_result = train_script.train_event_classifier(
            features_path=features_path,
            model_type=args.model,
            output=str(model_dir),
        )
        shutil.copy2(model_dir / "metrics.json", output / "classifier_metrics.json")
        shutil.copy2(model_dir / "model_card.md", output / "classifier_model_card.md")
        classifier_shadow = _classifier_shadow_report(features_path, args.model_id)
        _write_json(output / "classifier_shadow_report.json", classifier_shadow)

        lsl_results = {}
        if not args.skip_lsl:
            suite_args = [
                sys.executable,
                str(ROOT / "scripts" / "run_eeg_lsl_validation_suite.py"),
                "--output-dir",
                str(output / "lsl"),
                "--skip-evidence-pack",
            ]
            if args.fixture_mode:
                suite_args.append("--fixture-mode")
            if args.input_file:
                suite_args.extend(["--input-file", args.input_file])
            completed = subprocess.run(
                suite_args,
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            if completed.returncode != 0:
                summary["failures"].append(completed.stderr or completed.stdout)
            else:
                latest = sorted((output / "lsl").glob("*_eeg_lsl"))[-1]
                lsl_results = {
                    "validation": _read(latest / "validation_report.json"),
                    "calibration": _read(latest / "calibration_report.json"),
                    "heuristic_shadow": _read(latest / "shadow_report.json"),
                    "run_dir": str(latest),
                }
                shutil.copy2(latest / "validation_report.json", output / "lsl_validation_report.json")
                shutil.copy2(latest / "calibration_report.json", output / "calibration_report.json")
                shutil.copy2(latest / "shadow_report.json", output / "heuristic_shadow_report.json")

        comparison = compare_script.compare_reports(
            heuristic=lsl_results.get("heuristic_shadow", {}),
            classifier=classifier_shadow,
            validation=lsl_results.get("validation", {}),
            calibration=lsl_results.get("calibration", {}),
        )
        _write_json(output / "heuristic_vs_classifier_comparison.json", comparison)
        (output / "heuristic_vs_classifier_comparison.md").write_text(
            _comparison_markdown(comparison),
            encoding="utf-8",
        )
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
            "completed_at": datetime.now(timezone.utc).isoformat(),
        })
    except Exception as exc:
        summary["failures"].append(str(exc))
        summary["completed_at"] = datetime.now(timezone.utc).isoformat()
        _write_summary(output, summary)
        raise SystemExit(1) from exc
    _write_summary(output, summary)
    print(json.dumps(summary, indent=2, default=str))


def _classifier_shadow_report(features_path: Path, model_id: str) -> dict[str, Any]:
    x, y, _features, rows = read_feature_csv(features_path)
    model = load_model(model_id)
    metadata = get_model_metadata(model_id)
    predictions = model.predict(x)
    probabilities = model.predict_proba(x)
    labels = list(metadata.get("event_labels") or sorted(np.unique(y).tolist()))
    prediction_rows = []
    for idx, pred in enumerate(predictions):
        confidence = None
        if probabilities is not None:
            confidence = float(np.max(probabilities[idx]))
        prediction_rows.append({
            "sample_id": rows[idx].get("sample_id"),
            "marker_label": str(y[idx]),
            "predicted_label": str(pred),
            "confidence": round(confidence, 4) if confidence is not None else None,
            "event_onset_seconds": rows[idx].get("event_onset_seconds"),
        })
    accuracy = float(np.mean(predictions == y)) if len(y) else None
    return {
        "model_id": model_id,
        "prediction_semantics": metadata.get("prediction_semantics"),
        "event_labels": labels,
        "accuracy": round(accuracy, 4) if accuracy is not None else None,
        "predictions": prediction_rows,
        "real_adaptation_actions_emitted": 0,
        "closed_loop_allowed": False,
        "scientific_note": (
            "Classifier shadow inference predicts event labels and does not adapt the corridor."
        ),
    }


def _load_script(filename: str) -> Any:
    path = ROOT / "scripts" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_summary(output: Path, summary: dict[str, Any]) -> None:
    _write_json(output / "public_eeg_validation_summary.json", summary)
    metrics = summary.get("classifier_metrics") or {}
    lines = [
        f"# Public EEG Validation: {summary['run_id']}",
        "",
        f"- fixture mode: `{summary.get('fixture_mode')}`",
        f"- model: `{summary.get('model_dir')}`",
        f"- balanced accuracy: `{metrics.get('balanced_accuracy')}`",
        f"- macro F1: `{metrics.get('macro_f1')}`",
        f"- closed-loop allowed: `{summary.get('closed_loop_allowed')}`",
        f"- failures: `{len(summary.get('failures') or [])}`",
        "",
        (
            "Event-locked EEG classifiers predict dataset task labels under controlled "
            "conditions; they should not be interpreted as general mind-reading models."
        ),
        "",
        (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
    ]
    (output / "public_eeg_validation_summary.md").write_text("\n".join(lines), encoding="utf-8")


def _comparison_markdown(result: dict[str, Any]) -> str:
    return "\n".join([
        "# Heuristic vs EEG Event Classifier",
        "",
        f"- classifier model: `{result.get('classifier_model_id')}`",
        f"- classifier accuracy: `{result.get('classifier_accuracy')}`",
        f"- closed-loop allowed: `{result.get('closed_loop_allowed')}`",
        "",
        "```json",
        json.dumps(result, indent=2),
        "```",
    ])


def _source_args(args: argparse.Namespace) -> list[str]:
    if args.fixture_mode:
        return ["--fixture-mode"]
    return ["--input-file", str(args.input_file)]


def _run_json(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=True)
    start = completed.stdout.find("{")
    end = completed.stdout.rfind("}")
    return json.loads(completed.stdout[start : end + 1])


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
