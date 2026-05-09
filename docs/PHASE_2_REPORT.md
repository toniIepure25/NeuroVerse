# NeuroVerse Phase 2 Report

## What Phase 2 Adds

Phase 2 moves NeuroVerse from a purely simulated live demo toward a research-grade prototype layer:

- local dataset adapters;
- deterministic synthetic dataset replay;
- generic CSV and CLARE-like fixtures;
- optional PhysioNet MI adapter path;
- feature dataset generation;
- sklearn baseline training and evaluation;
- calibration metrics;
- local model registry;
- offline dataset replay through the existing safety and policy loop.

## Architecture Changes

The Phase 1 live session path remains intact. New modules live under:

- `backend/app/datasets/`
- `backend/app/ml/`
- `backend/app/experiments/`
- `backend/app/inference/learned_model.py`
- `scripts/*_dataset.py`, `train_baseline.py`, and report utilities

The heuristic estimator remains the default for live sessions.

## Implemented Adapters

- `SyntheticDatasetAdapter`: deterministic simulator-derived windows and phase labels.
- `GenericCSVAdapter`: local CSV features or raw-ish modality columns.
- `ClareLikeAdapter`: flexible workload fixture format with documented assumptions.
- `PhysioNetMIAdapter`: fixture mode plus graceful optional-MNE handling.

## Implemented Models

Baseline model wrappers support logistic regression, ridge classifier, random forest, histogram gradient
boosting, and sklearn MLP. Models are serialized with joblib and registered locally.

## Limitations

- Dataset labels are proxies and may not represent true cognitive state.
- Real CLARE and PhysioNet layouts require local verification.
- No transformer model is trained.
- No real hardware streaming is added in Phase 2.
- The system is not clinically validated and is not a medical device.

## Next Steps

- Validate adapters against real local dataset copies.
- Add stronger dataset validation reports.
- Add model cards for every experiment run.
- Expand replay summaries for safety/action oscillation.
- Consider optional frontend research status panel after backend workflows stabilize.
