#!/usr/bin/env python3
"""Train an IMAGINA v1 baseline model and register it.

IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

# Add backend directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.append(str(REPO_ROOT / "backend"))

from app.imagina.baseline_model import train_imagina_baseline
from app.imagina.registry import register_imagina_model

def main():
    parser = argparse.ArgumentParser(description="Train IMAGINA baseline model")
    parser.add_argument(
        "--manifest",
        type=str,
        default="configs/imagina/example_imagina_v1_manifest.json",
        help="Path to manifest file relative to repo root",
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="logistic_regression",
        choices=["logistic_regression", "ridge_classifier", "random_forest", "mlp", "ridge_regression"],
        help="Baseline model architecture",
    )
    parser.add_argument(
        "--split-strategy",
        type=str,
        default="fixture",
        choices=["fixture", "stratified", "group_subject", "leave_one_subject_out"],
        help="Train-test cross validation split strategy",
    )
    parser.add_argument(
        "--target-type",
        type=str,
        default="classification",
        choices=["classification", "regression"],
        help="Task target type",
    )
    args = parser.parse_args()
    
    run_id = f"imagina_v1_baseline_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    output_dir = REPO_ROOT / "reports" / "imagina_v1" / run_id
    
    print(f"Training model: {args.model_type}")
    print(f"Split strategy: {args.split_strategy}")
    print(f"Target type:    {args.target_type}")
    print(f"Output folder:  {output_dir}")
    
    try:
        # Run training
        res = train_imagina_baseline(
            manifest_path=args.manifest,
            output_dir=output_dir,
            split_strategy=args.split_strategy,
            model_type=args.model_type,
            target_type=args.target_type,
        )
        
        # Register model
        models_dir = REPO_ROOT / "models"
        register_imagina_model(run_id, res, models_dir=models_dir)
        
        print("\n--- Training Metrics ---")
        print(json.dumps(res["metrics"], indent=2))
        
        if res.get("leakage_warnings"):
            print("\n!!! LEAKAGE WARNINGS !!!")
            for warning in res["leakage_warnings"]:
                print(f" - {warning}")
                
        print(f"\nModel registered successfully as: {run_id}")
        sys.exit(0)
    except Exception as exc:
        print(f"Failed to train baseline model: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
