"""Run an offline shadow-only pass with the best raw-epoch BCI model."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))
os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-neuroverse")

from app.ml.metrics import evaluate_classification  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run best raw BCI model in offline shadow mode")
    parser.add_argument("--best-model", default="reports/bci_raw_epoch_benchmark/physionet_eegbci_small/best_model.json")
    parser.add_argument("--epochs", default="data/processed/physionet_eegbci_raw_epochs_small.npz")
    parser.add_argument("--output", default="reports/raw_bci_shadow/physionet_eegbci_small_shadow.json")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    result = run_shadow(
        best_model_path=_resolve(args.best_model),
        epochs_path=_resolve(args.epochs),
        output_path=_resolve(args.output),
        limit=args.limit,
    )
    print(json.dumps(result, indent=2, default=str))


def run_shadow(
    *,
    best_model_path: Path,
    epochs_path: Path,
    output_path: Path,
    limit: int,
) -> dict[str, object]:
    best = json.loads(best_model_path.read_text(encoding="utf-8"))
    model_dir = Path(str(best.get("model_dir", "")))
    if not model_dir.is_absolute():
        model_dir = ROOT / model_dir
    model = joblib.load(model_dir / "model.joblib")
    with np.load(epochs_path, allow_pickle=True) as npz:
        x = npz["X"][:limit]
        y = npz["y"][:limit]
        subjects = npz["subject_ids"][:limit]
        runs = npz["run_ids"][:limit]
    preds = model.predict(x)
    probs = model.predict_proba(x) if hasattr(model, "predict_proba") else None
    labels = sorted(set(y.tolist()) | set(preds.tolist()))
    metrics = evaluate_classification(y, preds, probs, labels)
    confidences = (
        np.max(np.asarray(probs, dtype=float), axis=1).tolist() if probs is not None else [None] * len(preds)
    )
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "offline_shadow_only",
        "model_id": best.get("model_id"),
        "model": best.get("model"),
        "n_components": best.get("n_components"),
        "epochs": str(epochs_path),
        "prediction_count": int(len(preds)),
        "predictions": [
            {
                "index": idx,
                "subject_id": str(subjects[idx]),
                "run_id": str(runs[idx]),
                "marker_label": str(y[idx]),
                "predicted_label": str(preds[idx]),
                "confidence": confidences[idx],
            }
            for idx in range(len(preds))
        ],
        "metrics": metrics,
        "real_adaptation_actions_emitted": 0,
        "closed_loop_allowed": False,
        "scientific_note": (
            "Offline raw BCI shadow mode predicts controlled event labels and emits no "
            "Dream Corridor adaptation actions."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    output_path.with_suffix(".md").write_text(_markdown(report), encoding="utf-8")
    return report


def _markdown(report: dict[str, object]) -> str:
    metrics = report.get("metrics") or {}
    return "\n".join([
        "# Raw BCI Shadow Report",
        "",
        f"- Model: {report.get('model_id')}",
        f"- Predictions: {report.get('prediction_count')}",
        f"- Balanced accuracy against available markers: {metrics.get('balanced_accuracy')}",
        f"- Macro F1 against available markers: {metrics.get('macro_f1')}",
        f"- Real adaptation actions emitted: {report.get('real_adaptation_actions_emitted')}",
        f"- Closed-loop allowed: {report.get('closed_loop_allowed')}",
        "",
        "This is offline shadow-only evidence, not real EEG control of the corridor.",
    ])


def _resolve(path: str) -> Path:
    item = Path(path)
    return item if item.is_absolute() else ROOT / item


if __name__ == "__main__":
    main()
