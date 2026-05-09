# Models

This directory stores local trained model artifacts for NeuroVerse state estimation experiments.

## Current Status

The live system still defaults to the heuristic rule-based estimator. Phase 2 can register local
sklearn baselines for offline evaluation and optional learned-estimator replay.

## Future Model Types

```text
models/
  registry.json
  synthetic_phase_rf/
    model.joblib
    metadata.json
    metrics.json
    model_card.md
```

## Adding a Model

Use:

```bash
python3 scripts/train_baseline.py \
  --dataset-config configs/datasets/synthetic.yaml \
  --experiment-config configs/experiments/workload_baseline.yaml \
  --output models/synthetic_phase_rf
```

Model metadata must state intended use, limitations, target label, and prediction semantics. These
models are research baselines trained on dataset-derived labels and are not clinical systems.
