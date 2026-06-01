#!/usr/bin/env python3
"""Run the complete IMAGINA v1 baseline pipeline.

Workflow: validate manifest -> prepare dataset -> train baseline model -> evaluate model.
IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

import sys
import argparse
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

def run_step(cmd: list[str], step_name: str) -> None:
    print(f"\n==================================================")
    print(f" STEP: {step_name}")
    print(f"==================================================")
    res = subprocess.run(cmd, cwd=str(REPO_ROOT))
    if res.returncode != 0:
        print(f"Error: Step '{step_name}' failed with exit code {res.returncode}")
        sys.exit(res.returncode)

def main():
    parser = argparse.ArgumentParser(description="Run IMAGINA v1 baseline pipeline")
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
        help="Model architecture type",
    )
    parser.add_argument(
        "--split-strategy",
        type=str,
        default="fixture",
        help="Cross validation split strategy",
    )
    args = parser.parse_args()
    
    print("Starting IMAGINA v1 Baseline Model Pipeline...")
    print(f"Manifest:       {args.manifest}")
    print(f"Model architecture: {args.model_type}")
    print(f"Split strategy:     {args.split_strategy}")
    
    # 1. Validate
    run_step(
        [sys.executable, "scripts/validate_imagina_manifest.py", "--manifest", args.manifest],
        "Manifest Validation"
    )
    
    # 2. Prepare
    run_step(
        [sys.executable, "scripts/prepare_imagina_dataset.py", "--manifest", args.manifest],
        "Dataset Preparation"
    )
    
    # 3. Train & Register
    run_step(
        [
            sys.executable,
            "scripts/train_imagina_baseline.py",
            "--manifest", args.manifest,
            "--model-type", args.model_type,
            "--split-strategy", args.split_strategy
        ],
        "Model Training & Registration"
    )
    
    # 4. Evaluate
    run_step(
        [sys.executable, "scripts/evaluate_imagina_baseline.py", "--manifest", args.manifest],
        "Model Evaluation"
    )
    
    print("\n==================================================")
    print(" IMAGINA v1 Baseline Model Pipeline COMPLETED!")
    print("==================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
