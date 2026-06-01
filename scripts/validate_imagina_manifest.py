#!/usr/bin/env python3
"""Validate an IMAGINA dataset manifest.

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

from app.imagina.dataset_adapter import validate_manifest

def main():
    parser = argparse.ArgumentParser(description="Validate IMAGINA manifest")
    parser.add_argument(
        "--manifest",
        type=str,
        default="configs/imagina/example_imagina_v1_manifest.json",
        help="Path to manifest file relative to repo root",
    )
    args = parser.parse_args()
    
    print(f"Validating manifest: {args.manifest}")
    res = validate_manifest(args.manifest)
    
    print(json.dumps(res, indent=2))
    
    if not res.get("valid"):
        print("Manifest validation FAILED!")
        sys.exit(1)
    else:
        print("Manifest validation PASSED.")
        sys.exit(0)

if __name__ == "__main__":
    main()
