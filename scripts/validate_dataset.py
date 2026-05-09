"""Generate a Phase 2.5 dataset validation report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.datasets.validation import validate_dataset_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a NeuroVerse dataset config")
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument("--target", default=None)
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()
    report = validate_dataset_config(
        args.dataset_config,
        target=args.target,
        output_dir=args.output_dir or Path("reports") / "datasets",
    )
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
