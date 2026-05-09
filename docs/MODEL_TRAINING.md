# NeuroVerse Phase 2 Model Training

Phase 2 trains simple sklearn baselines against dataset-derived labels. These are research baselines,
not clinical models and not transformer fusion.

## Prepare Features

```bash
python3 scripts/prepare_dataset.py \
  --config configs/datasets/synthetic.yaml \
  --target phase_label \
  --output data/processed/synthetic_features.parquet
```

If parquet support is unavailable, the script falls back to CSV.

## Train A Baseline

```bash
python3 scripts/train_baseline.py \
  --dataset-config configs/datasets/synthetic.yaml \
  --experiment-config configs/experiments/workload_baseline.yaml \
  --model random_forest \
  --target phase_label \
  --output models/synthetic_phase_rf
```

Artifacts are registered under `models/<model_id>/`:

- `model.joblib`
- `metadata.json`
- `metrics.json`
- `model_card.md`

## Evaluate A Model

```bash
python3 scripts/evaluate_model.py \
  --model-dir models/synthetic_phase_rf \
  --dataset-config configs/datasets/synthetic.yaml \
  --target phase_label \
  --output reports/synthetic_phase_rf_metrics.json
```

## Replay A Dataset

```bash
python3 scripts/replay_dataset.py \
  --dataset-config configs/datasets/synthetic.yaml \
  --speed 2.0 \
  --use-model models/synthetic_phase_rf
```

Dataset replay emits the same JSONL event envelope used by Phase 1 sessions. The heuristic estimator
remains the default unless `--use-model` is supplied.

## Learned Estimator Semantics

Learned models declare `prediction_semantics`:

- `phase_proxy`: maps phase labels to conservative state proxies;
- `workload_proxy`: maps workload classes or scores to workload/stress proxies;
- `motor_intent`: maps motor imagery labels to intent candidates;
- `state_regression`: uses direct numeric state dimensions if a compatible model exists.

These mappings are explicit approximations and are not validated cognitive or clinical measurements.

## Activation Safety

Use:

```bash
curl -X POST http://localhost:8000/api/models/synthetic_phase_rf/activate
curl -X POST http://localhost:8000/api/models/deactivate
```

Activation checks model artifacts, metadata, feature names, and `prediction_semantics`. It is rejected
while a live session is running. Deactivation returns the runtime to the heuristic estimator. The
heuristic estimator remains the default because learned baselines are dataset-derived proxy models.

## Event-Locked EEG Classifier

Prepare fixture epochs and train a baseline:

```bash
make prepare-eeg-fixture-events
make train-eeg-fixture-classifier
```

The resulting model is registered with `prediction_semantics = event_label_classifier`.
It predicts dataset task labels from controlled EEG epochs. It is not intended for
thought reading, diagnosis, unrestricted mental-state inference, or direct closed-loop control.

Run the full evidence workflow:

```bash
make public-eeg-fixture-suite
```


## Real Public EEG Validation

PhysioNet EEGBCI support is local-first. Use `make physionet-eegbci-config` to create a config for local EDF files, then `make inspect-physionet-eegbci`, `make prepare-physionet-eegbci-events`, and `make train-physionet-eegbci-classifier` when files are present. Downloads happen only with `make physionet-eegbci-download`.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Closed-loop adaptation remains disabled by default.

First real-public baseline:

- Dataset subset: PhysioNet EEGBCI subjects `S001-S003`, runs `4/8/12`.
- Labels: `REST`, `LEFT_HAND_IMAGERY`, `RIGHT_HAND_IMAGERY`.
- Features: 270 event-locked epochs, 517 features.
- Split: `group_run`.
- Model: logistic regression registered with `prediction_semantics = event_label_classifier`.
- Metrics: accuracy 0.508, balanced accuracy 0.478, macro F1 0.479.

This model card is useful BCI workflow evidence. It is not intended for direct
closed-loop control, thought reading, diagnosis, or unrestricted mental-state
inference.

## BCI Benchmarking

Run:

```bash
make bci-benchmark-small
```

The benchmark trains and registers multiple baseline models with the same
dataset, target, split strategy, and not-intended-use language. The best model is
selected by balanced accuracy and saved in `best_model.json`, but remains
shadow-only. CSP/FBCSP live in the raw-epoch benchmark because those methods
must consume `n_epochs x n_channels x n_times` tensors rather than flattened
feature CSVs.

## Raw-Epoch CSP Models

Raw-epoch CSP training is now available:

```bash
make prepare-raw-epochs-small
make raw-bci-benchmark-small
make raw-bci-loso-small
```

This path trains CSP pipelines on tensors shaped `n_epochs x n_channels x
n_times`. Implemented models are `csp_lda`, `csp_logreg`, `csp_svm_linear`,
`fbcsp_logreg`, and `fbcsp_lda`. Model cards include `raw_epoch_model = true`,
CSP component count, filter-bank bands where applicable, split strategy,
intended use, not-intended use, and limitations.

These models are registered for offline and shadow-only review. They do not
activate real EEG control of the Dream Corridor.

Medium-cohort targets are available for subjects 1-10, runs 4/8/12, but require
local EDF files or the explicit PhysioNet download target. The latest local
medium run selected FBCSP variants for group-run and group-subject evaluation
and keeps those models registered for shadow-only review, not real EEG control
of the Dream Corridor.

## Hardware Trial Relationship

The physical EEG trial protocol does not train a model. It records
eyes-open/eyes-closed hardware data, computes alpha reactivity as a signal
sanity check, creates a session-local calibration profile, and can run heuristic
shadow inference. Learned EEG models remain offline or shadow-only unless a
future safety-reviewed protocol explicitly changes that.
