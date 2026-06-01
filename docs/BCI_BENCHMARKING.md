# BCI Benchmarking

NeuroVerse benchmarks event-locked EEG classifiers as controlled task-label
models. The corridor is not a decoded mental image. It is an adaptive scaffold
driven by experimental proxy metrics.

Event-locked EEG classifiers predict controlled dataset task labels under
experimental conditions; they should not be interpreted as general mind-reading
models.

## Reproduce The Small Benchmark

```bash
make inspect-physionet-eegbci
make prepare-physionet-eegbci-events
make bci-benchmark-small
make generate-evidence-pack
```

The default benchmark uses `data/processed/physionet_eegbci_event_features.csv`
with a `group_run` split. This avoids putting epochs from the same subject/run
group in both train and test partitions.

## Models

Current tabular baselines:

- logistic regression
- ridge classifier
- random forest
- histogram gradient boosting
- linear SVM

CSP/FBCSP are intentionally excluded from the CSV benchmark because true CSP
requires raw epoch tensors, not flattened summary features. The raw-epoch
benchmark implements them separately rather than approximating CSP incorrectly.

## Feature Options

Event feature generation supports:

- epoch window: `--tmin`, `--tmax`
- bandpass filtering: `--bandpass-low`, `--bandpass-high`
- optional notch filtering: `--notch-freq`
- baseline correction: `--baseline-correction`
- channel selection: `--pick-channels`, `--max-channels`
- amplitude quality flagging: `--reject-amplitude-uv`
- feature sets: `statistical`, `bandpower`, `logvar`, `lateralized`, or `combined`

Motor-imagery-oriented example:

```bash
python3 scripts/prepare_event_locked_dataset.py \
  --dataset-config configs/datasets/physionet_eegbci_local.yaml \
  --output data/processed/physionet_eegbci_event_features_mi.csv \
  --tmin 0.5 \
  --tmax 2.5 \
  --bandpass-low 7 \
  --bandpass-high 35 \
  --baseline-correction \
  --feature-set combined
```

## Confidence Intervals

`scripts/run_bci_benchmark.py` reconstructs test predictions from each confusion
matrix and bootstraps accuracy, balanced accuracy, and macro F1. Confidence
intervals are descriptive uncertainty estimates for the held-out test set, not
clinical validation.

## Larger Subsets

Recommended staged subsets:

- Small: subjects `1 2 3`, runs `4 8 12`.
- Medium: subjects `1` through `10`, runs `4 8 12`.
- Larger: subjects `1` through `20`, runs `4 8 12`, if compute allows.

Downloads remain explicit. NeuroVerse does not download large datasets without
the user running the download target.

## Safety

Benchmark winners are registered for offline and shadow evaluation only. They do
not activate real EEG closed-loop adaptation. NeuroVerse remains a research
prototype, not clinically validated, and not a medical device.

## First Small Benchmark Result

On the PhysioNet EEGBCI `S001-S003`, runs `4/8/12` subset with a `group_run`
split:

| Model | Accuracy | Balanced accuracy | Macro F1 |
| --- | ---: | ---: | ---: |
| logistic regression | 0.508 | 0.478 | 0.479 |
| ridge classifier | 0.417 | 0.356 | 0.355 |
| random forest | 0.550 | 0.465 | 0.469 |
| histogram gradient boosting | 0.567 | 0.515 | 0.520 |
| linear SVM | 0.492 | 0.473 | 0.469 |

The selected best model was histogram gradient boosting by balanced accuracy.
Its bootstrap 95% interval for balanced accuracy was approximately 0.421-0.606.
This is a modest baseline result and should be interpreted as engineering
evidence for the benchmark workflow, not as a claim of robust BCI performance.

## Raw-Epoch CSP Extension

The raw-epoch path is documented in
[`RAW_EPOCH_BCI_BENCHMARKING.md`](RAW_EPOCH_BCI_BENCHMARKING.md). It exports
binary motor imagery tensors shaped `n_epochs x n_channels x n_times`, then runs
`csp_lda`, `csp_logreg`, and `csp_svm_linear` with CSP fit inside each train
split.

On the same small PhysioNet subset, the raw-epoch benchmark now compares CSP and
Filter Bank CSP. The latest group-run run selected `fbcsp_logreg` with 8 CSP
components per band. Balanced accuracy was approximately 0.615, macro F1
approximately 0.614, and the bootstrap 95% interval for balanced accuracy was
approximately 0.483-0.730.

LOSO remains harder on the three-subject subset: mean balanced accuracy was
approximately 0.510. This is reported as small-subset benchmark evidence, not a
claim of clinical or general decoding validity.

Medium-cohort subjects `1-10`, runs `4/8/12`, remain opt-in and are not run in
CI. The latest local medium run used 30 EDF files and compared group-run,
group-subject, and LOSO evaluation. Best group-run FBCSP balanced accuracy was
approximately 0.576; best group-subject balanced accuracy was approximately
0.509; LOSO fold mean balanced accuracy was approximately 0.488. These values
are intentionally reported with their split context because subject-held-out
generalization is a harder benchmark.


## Top-Level BCI Benchmark

The top-level BCI benchmark (`make top-level-bci-benchmark`) orchestrates an exhaustive evaluation of raw EEG epochs on the PhysioNet Motor Imagery dataset:

- **Riemannian Geometry**: Optional support for `pyriemann` MDM and Tangent Space classifiers. Install with `pip install -e ".[bci]"`. If `pyriemann` is not installed, the benchmark gracefully skips these models.
- **Benchmark Contexts**: The leaderboard separates results by context:
  - `subject_specific`: Calibrated per-user decoding (train runs 4/8, test run 12). Riemannian MDM achieves ~0.651 balanced accuracy. This is the strongest result but requires per-user calibration.
  - `channel_ablation` (LOSO): Cross-subject generalization. Best LOSO result is Riemannian TS LogReg on motor_subset (7ch) at ~0.699 balanced accuracy.
  - `frequency_window_ablation` (group_run): Run-level generalization.
- **Channel Ablation**: Evaluates `all_channels` (64ch), `motor_subset` (7ch), and `minimal_motor` (3ch). Channel counts are verified to differ across ablations.
- **Provenance**: Every leaderboard row includes `metric_source_file`, `metric_source_field`, `benchmark_type`, and `generated_by_script`. No manually hardcoded values.
- **MOABB-Style Report**: Generates compatibility reports for cross-dataset comparison. Note: This is an internal formatting style, not the official MOABB package.
- **Audit**: `make audit-bci-benchmark` validates provenance integrity and exits non-zero on failure.

> Subject-specific calibrated results should NOT be compared as if they were LOSO or zero-calibration scores. These are different evaluation contexts.
