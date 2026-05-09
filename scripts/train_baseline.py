"""Train a simple, honest sklearn baseline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.datasets.registry import load_dataset_config
from app.experiments.config import load_experiment_config
from app.ml.trainer import train_baseline_from_configs


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a NeuroVerse Phase 2 baseline")
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument("--experiment-config", required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--target", default=None)
    parser.add_argument("--ablation", default=None, help="Override ablation mode, e.g. all")
    parser.add_argument("--output", default=None, help="Model id or models/<model_id>")
    args = parser.parse_args()
    model_id = Path(args.output).name if args.output else None
    experiment_config = load_experiment_config(args.experiment_config)
    if args.ablation:
        experiment_config.setdefault("ablation", {})["enabled"] = True
    result = train_baseline_from_configs(
        load_dataset_config(args.dataset_config),
        experiment_config,
        model_type=args.model,
        target=args.target,
        output_model_id=model_id,
    )
    print(f"Saved model to {result['model_dir']}")
    print(result["metrics"])


if __name__ == "__main__":
    main()
