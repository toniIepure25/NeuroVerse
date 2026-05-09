"""Evaluate a saved Phase 2 model against a dataset config."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.datasets.registry import create_dataset_adapter
from app.ml.evaluator import evaluate_model_on_dataset
from app.ml.registry import load_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a NeuroVerse baseline")
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument("--target", default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    adapter = create_dataset_adapter(args.dataset_config)
    dataset = adapter.to_feature_dataset(target=args.target)
    model = load_model(args.model_dir)
    metrics = evaluate_model_on_dataset(model, dataset)
    text = json.dumps(metrics, indent=2, default=str)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    print(text)


if __name__ == "__main__":
    main()
