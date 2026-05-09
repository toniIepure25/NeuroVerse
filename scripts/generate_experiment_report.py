"""Generate a Markdown experiment report from saved model artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.datasets.registry import create_dataset_adapter
from app.datasets.validation import validate_dataset_config
from app.experiments.tracking import create_run_dir
from app.ml.reports import write_experiment_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a NeuroVerse experiment report")
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--experiment-id", default="phase2_report")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--run-config", default=None)
    args = parser.parse_args()
    model_dir = Path(args.model_dir)
    metadata = json.loads((model_dir / "metadata.json").read_text())
    metrics = (
        json.loads((model_dir / "metrics.json").read_text())
        if (model_dir / "metrics.json").exists()
        else {}
    )
    dataset_meta = create_dataset_adapter(args.dataset_config).load_metadata().to_dict()
    validation = validate_dataset_config(args.dataset_config, write_report=True)
    run_config = {
        "dataset_config": args.dataset_config,
        "model_dir": args.model_dir,
        "experiment_id": args.experiment_id,
    }
    out = Path(args.output_dir) if args.output_dir else create_run_dir(args.experiment_id)
    path = write_experiment_report(
        out,
        title=f"NeuroVerse Phase 2 Report: {args.experiment_id}",
        dataset_metadata=dataset_meta,
        model_metadata=metadata,
        metrics=metrics,
        run_config=run_config,
        dataset_validation_summary=validation,
        limitations=[
            "Dataset-derived labels are proxies, not clinical ground truth.",
            "This report does not validate therapeutic or diagnostic claims.",
        ],
    )
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
