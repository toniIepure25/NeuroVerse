#!/usr/bin/env python3
"""Evaluate the latest IMAGINA baseline model on a manifest.

IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

import sys
import argparse
import json
from pathlib import Path
import numpy as np

# Add backend directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.append(str(REPO_ROOT / "backend"))

from app.imagina.registry import get_latest_imagina_model, load_imagina_model
from app.imagina.dataset_adapter import load_manifest

def main():
    parser = argparse.ArgumentParser(description="Evaluate latest IMAGINA baseline model")
    parser.add_argument(
        "--manifest",
        type=str,
        default="configs/imagina/example_imagina_v1_manifest.json",
        help="Path to manifest file relative to repo root",
    )
    args = parser.parse_args()
    
    print(f"Evaluating latest model on manifest: {args.manifest}")
    
    models_dir = REPO_ROOT / "models"
    latest = get_latest_imagina_model(models_dir=models_dir)
    if not latest:
        print("Error: No trained baseline model is registered. Train one first.")
        sys.exit(1)
        
    print(f"Loaded registered model: {latest['model_id']}")
    
    try:
        manifest = load_manifest(args.manifest)
        model = load_imagina_model(latest["model_id"], models_dir=models_dir)
        
        print("\n--- Predictions ---")
        correct = 0
        for sample in manifest.samples:
            feat_dict = dict(sample.features)
            row = [float(feat_dict.get(fname, 0.0)) for fname in model.feature_names]
            pred_idx = int(model.predict(np.array([row]))[0])
            pred_lbl = model.classes[pred_idx] if model.classes else str(pred_idx)
            true_lbl = sample.label or sample.task
            
            is_correct = (pred_lbl == true_lbl)
            if is_correct:
                correct += 1
                
            status_str = "CORRECT" if is_correct else "INCORRECT"
            print(f"Sample: {sample.sample_id} | True: {true_lbl} | Pred: {pred_lbl} | {status_str}")
            
        acc = correct / len(manifest.samples) if manifest.samples else 0.0
        print(f"\nOverall accuracy on this manifest: {acc:.2%}")
        sys.exit(0)
    except Exception as exc:
        print(f"Failed to run evaluation: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
