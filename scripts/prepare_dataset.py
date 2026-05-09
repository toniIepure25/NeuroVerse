"""Prepare a training-ready Phase 2 feature dataset."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.datasets.registry import create_dataset_adapter
from app.ml.feature_dataset import save_feature_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare a NeuroVerse feature dataset")
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--target", default=None)
    args = parser.parse_args()
    adapter = create_dataset_adapter(args.config)
    dataset = adapter.to_feature_dataset(target=args.target)
    path = save_feature_dataset(dataset, args.output)
    print(f"Wrote {dataset.X.shape[0]} samples x {dataset.X.shape[1]} features to {path}")


if __name__ == "__main__":
    main()
