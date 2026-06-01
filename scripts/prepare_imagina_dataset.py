#!/usr/bin/env python3
"""Prepare and summarize an IMAGINA dataset manifest.

IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

import sys
import argparse
import json
from pathlib import Path

# Add backend directory to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.append(str(REPO_ROOT / "backend"))

from app.imagina.dataset_adapter import summarize_manifest

def main():
    parser = argparse.ArgumentParser(description="Prepare IMAGINA dataset summary")
    parser.add_argument(
        "--manifest",
        type=str,
        default="configs/imagina/example_imagina_v1_manifest.json",
        help="Path to manifest file relative to repo root",
    )
    args = parser.parse_args()
    
    print(f"Preparing dataset from manifest: {args.manifest}")
    try:
        summary = summarize_manifest(args.manifest)
        print("\n--- Dataset Summary ---")
        print(json.dumps(summary, indent=2))
        sys.exit(0)
    except Exception as exc:
        print(f"Failed to prepare dataset: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    main()
