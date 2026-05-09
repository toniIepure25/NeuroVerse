# Real Public EEG Validation

This workflow validates NeuroVerse against local public EEG files, with PhysioNet
EEG Motor Movement/Imagery as the first supported path.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics.

Event-locked EEG classifiers predict controlled dataset task labels under
experimental conditions; they should not be interpreted as general mind-reading
models.

## Safety Position

Real public EEG validation is record-only, calibration, shadow inference, and
report-first. It does not unlock closed-loop corridor adaptation. NeuroVerse is a
research prototype, not clinically validated, and not a medical device.

## PhysioNet EEGBCI Local Workflow

Print dataset/run guidance:

```bash
make physionet-eegbci-info
```

Create a local config without downloading data:

```bash
make physionet-eegbci-config LOCAL_ROOT=data/external/eegbci SUBJECTS="1 2 3" RUNS="4 8 12"
```

Explicit download is opt-in only:

```bash
make physionet-eegbci-download SUBJECTS="1 2 3" RUNS="4 8 12"
```

No large EEG files should be committed. Store them under `data/external/`.

## Inspection

```bash
make inspect-physionet-eegbci
```

The inspection report includes file counts, subjects, runs, channel/sampling-rate
distributions, annotation labels, missing files, and split recommendations.

## Event Mapping

PhysioNet EEGBCI `T0`, `T1`, and `T2` labels are normalized by run context:

- Runs `4`, `8`, `12`: imagined left hand vs right hand.
- Runs `6`, `10`, `14`: imagined both hands vs both feet.
- Runs `3`, `7`, `11`: executed left hand vs right hand.
- Runs `5`, `9`, `13`: executed both hands vs both feet.
- `T0` maps to `REST`.

Original labels are preserved in feature datasets and reports.

## Event-Locked Features

```bash
make prepare-physionet-eegbci-events
```

Features are extracted from epochs around annotations and include EEG-prefixed
statistics and bandpower summaries. Output rows include subject/run/file metadata
for group-aware evaluation.

## Classifier Training

```bash
make train-physionet-eegbci-classifier
```

The default split is `group_run`. Other script-level strategies include
`stratified`, `group_subject`, `within_subject`, `leave_one_subject_out`, and
explicit train/test runs.

Metrics include balanced accuracy, macro F1, confusion matrix, per-subject
metrics when available, per-run metrics, calibration when probabilities exist,
and leakage warnings.

## Full Suite

With local files present:

```bash
make real-public-eeg-suite DATASET_CONFIG=configs/datasets/physionet_eegbci_local.yaml
```

For a single EDF/FIF/GDF/BDF file:

```bash
make real-public-eeg-file-suite FILE=/path/to/file.edf
```

The suite inspects the data, prepares features, trains/registers a classifier,
replays a representative file over LSL, runs validation/calibration/shadow
inference, compares heuristic proxy summaries against classifier predictions,
and updates the evidence pack.

If local files are missing, the suite writes a failure summary instead of
fabricating results.

## First Real PhysioNet EEGBCI Run

The first real-public validation run used a deliberately small subset:

- Subjects: `S001`, `S002`, `S003`.
- Runs: `4`, `8`, `12`.
- Task context: motor imagery left hand vs right hand, plus rest.
- Files: 9 EDF files downloaded only after the explicit `physionet-eegbci-download` command.
- Channels: 64 EEG channels.
- Sampling rate: 160 Hz.
- Annotations: 270 total labels: `T0`/REST = 135, `T1`/LEFT_HAND_IMAGERY = 69, `T2`/RIGHT_HAND_IMAGERY = 66.

Event-locked feature generation produced 270 epochs and 517 features using a
0.0-2.0 second epoch window. The first baseline was logistic regression with a
`group_run` split:

| Metric | Value |
| --- | ---: |
| Accuracy | 0.508 |
| Balanced accuracy | 0.478 |
| Macro F1 | 0.479 |
| Weighted F1 | 0.507 |
| Macro AUROC | 0.655 |

The representative EDF `S001R04.edf` was replayed over LSL. Record-only LSL
validation passed with observed rate 159.798 Hz, drift -0.126%, jitter p95
0.085 ms, zero gaps, and zero duplicate timestamps. The marker stream was
detected, although the short validation window captured one unaligned marker;
the shadow window aligned one `T0` marker successfully.

Closed-loop adaptation remained disabled. Shadow inference emitted 0 real
adaptation actions. The classifier shadow report is useful for checking
prediction plumbing, but the group-run holdout metrics above are the honest
model-evaluation metrics for this run.

## BCI Benchmark Layer

Run:

```bash
make bci-benchmark-small
```

The benchmark compares logistic regression, ridge classifier, random forest,
histogram gradient boosting, and linear SVM using the same event-feature CSV and
`group_run` split. It writes `reports/bci_benchmark/physionet_eegbci_small/`
with model comparison, bootstrap confidence intervals, leakage warnings, model
cards, and best-model metadata.

CSP/FBCSP are deferred in this CSV benchmark because true CSP requires raw epoch
tensors. This is documented rather than approximated from flattened features.

## Raw-Epoch CSP Follow-Up

Run:

```bash
make prepare-raw-epochs-small
make raw-bci-benchmark-small
make raw-bci-loso-small
make compare-bci-benchmarks
```

This path exports binary left-vs-right motor imagery epochs as raw tensors and
trains CSP baselines inside leakage-aware splits. It is the scientifically
appropriate path for CSP/FBCSP-style models. The raw benchmark remains
offline/shadow-only and does not enable real EEG closed-loop control.

## Medium-Cohort Raw Benchmark

The opt-in medium run uses PhysioNet EEGBCI subjects `S001-S010`, runs `4/8/12`.
With local EDF files present, run:

```bash
make prepare-raw-epochs-medium
make raw-bci-benchmark-medium
make raw-bci-group-subject-medium
make raw-bci-loso-medium
make live-shadow-best-raw-bci-model
```

Latest local results: 450 binary motor-imagery epochs, 64 channels, 320 samples;
group-run best `fbcsp_lda` balanced accuracy approximately 0.576;
group-subject best `fbcsp_logreg` approximately 0.509; LOSO fold mean
approximately 0.488. The live raw-shadow report ran in `live_lsl` mode by
buffering replayed EDF samples and markers into marker-locked epochs. It emitted
0 real adaptation actions and left closed-loop disabled.

## Physical Hardware Mapping

The same staged path applies to OpenBCI, Galea, or other LSL-capable systems:
record-only validation, channel mapping, timing/SQI diagnostics, calibration,
shadow inference, human review, then an explicitly enabled safety-gated
experiment. Hardware closed-loop remains disabled by default.
