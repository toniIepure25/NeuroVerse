"""Run subject-specific calibration benchmark for raw EEG epochs."""

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.metrics import evaluate_classification
from app.ml.raw_epoch_models import create_raw_epoch_model
from scripts.run_raw_epoch_bci_benchmark import load_raw_epochs, parse_bands


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", required=True)
    parser.add_argument("--models", nargs="+", default=["csp_lda", "fbcsp_logreg"])
    parser.add_argument("--train-runs", nargs="+", default=["4", "8"])
    parser.add_argument("--test-runs", nargs="+", default=["12"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    run_subject_specific(
        epochs_path=Path(args.epochs),
        models=args.models,
        train_runs=args.train_runs,
        test_runs=args.test_runs,
        output_dir=Path(args.output),
    )


def run_subject_specific(
    epochs_path: Path,
    models: list[str],
    train_runs: list[str],
    test_runs: list[str],
    output_dir: Path,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    data = load_raw_epochs(epochs_path)
    x = data["X"]
    y = data["y"]
    subjects = data["subject_ids"]
    runs = data["run_ids"]
    labels = sorted(np.unique(y).tolist())
    sampling_rate = float(np.asarray(data.get("sampling_rate", np.asarray(160.0))).reshape(-1)[0])

    unique_subjects = sorted(set(subjects.tolist()))
    
    results = []
    
    for subject in unique_subjects:
        for model_name in models:
            train_mask = (subjects == subject) & np.isin(runs, train_runs)
            test_mask = (subjects == subject) & np.isin(runs, test_runs)
            
            x_train, y_train = x[train_mask], y[train_mask]
            x_test, y_test = x[test_mask], y[test_mask]
            
            if len(set(y_train)) < 2 or len(set(y_test)) < 1:
                results.append({
                    "subject": subject,
                    "model": model_name,
                    "status": "skipped",
                    "reason": "Missing classes in train/test"
                })
                continue
                
            try:
                model = create_raw_epoch_model(
                    model_name,
                    n_components=4,
                    sampling_rate=sampling_rate,
                )
                model.fit(x_train, y_train)
                preds = model.predict(x_test)
                probs = model.predict_proba(x_test)
                metrics = evaluate_classification(y_test, preds, probs, labels)
                
                results.append({
                    "subject": subject,
                    "model": model_name,
                    "status": "ok",
                    "accuracy": metrics["accuracy"],
                    "balanced_accuracy": metrics["balanced_accuracy"],
                    "macro_f1": metrics["macro_f1"],
                    "test_rows": len(y_test)
                })
            except Exception as e:
                results.append({
                    "subject": subject,
                    "model": model_name,
                    "status": "failed",
                    "reason": str(e)
                })

    # Save CSV
    with open(output_dir / "subject_specific_metrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["subject", "model", "status", "accuracy", "balanced_accuracy", "macro_f1", "test_rows", "reason"])
        for r in results:
            writer.writerow([
                r["subject"], r["model"], r["status"],
                r.get("accuracy", ""), r.get("balanced_accuracy", ""), r.get("macro_f1", ""),
                r.get("test_rows", ""), r.get("reason", "")
            ])

    # Summary
    ok_results = [r for r in results if r["status"] == "ok"]
    model_means = {}
    for model_name in models:
        model_results = [r for r in ok_results if r["model"] == model_name]
        if model_results:
            model_means[model_name] = {
                "mean_balanced_accuracy": float(np.mean([r["balanced_accuracy"] for r in model_results])),
                "mean_macro_f1": float(np.mean([r["macro_f1"] for r in model_results]))
            }
            
    summary = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "train_runs": train_runs,
        "test_runs": test_runs,
        "models": models,
        "model_means": model_means,
        "results": results
    }
    
    with open(output_dir / "subject_specific_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
        
    with open(output_dir / "subject_specific_summary.md", "w") as f:
        f.write("# Subject-Specific Calibration\n\n")
        f.write(f"Trained on runs {train_runs}, tested on {test_runs}.\n\n")
        for m, means in model_means.items():
            f.write(f"- **{m}**: {means['mean_balanced_accuracy']:.3f} Balanced Accuracy\n")
            
    return summary

if __name__ == "__main__":
    main()
