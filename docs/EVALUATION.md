# NeuroVerse Phase 2 Evaluation

Phase 2 evaluation is designed for reproducible baseline comparisons and replay diagnostics.

## Metrics

Classification reports include:

- accuracy
- balanced accuracy
- macro F1 and weighted F1
- per-class precision/recall/F1
- confusion matrix
- AUROC when probabilities and class structure support it

Regression helpers include MAE, RMSE, R2, Pearson correlation, and Spearman correlation.

## Calibration

Calibration utilities compute:

- Brier score for binary probabilistic classifiers;
- expected calibration error;
- maximum calibration error;
- reliability-bin table.

Calibration describes model probability behavior on dataset-derived labels. It does not validate
clinical confidence or real-world safety.

## Leakage Prevention

The split module supports:

- random split;
- stratified split;
- group split by subject/session group IDs;
- temporal split.

For biosignal studies, prefer group-aware splits when evaluating generalization across subjects or sessions.

## Fusion Ablations

Ablations filter feature columns by prefix:

- `eeg_`
- `physio_`
- `gaze_`
- `multimodal_`
- `sqi_`

The `fusion_ablation.yaml` example compares EEG-only, physio-only, gaze-only, pairwise combinations,
all modalities, and all modalities plus SQI features.

## Closed-Loop Replay

Dataset replay records features, state predictions, safety decisions, and adaptation actions as JSONL.
Closed-loop summaries can track safety block rate, action distribution, state oscillation, action
oscillation, and replay determinism. These are engineering validation metrics, not claims of efficacy.

## Dataset Validation Reports

Run:

```bash
python3 scripts/validate_dataset.py --dataset-config configs/datasets/synthetic.yaml
```

Reports are written to `reports/datasets/` and include metadata, label distribution, feature health,
windowing settings, and leakage-risk warnings. One-subject synthetic data intentionally warns that
subject-level generalization cannot be tested.

## Replay Summary Reports

Dataset replay writes `{session_id}_summary.json` and `{session_id}_summary.md` beside the JSONL file.
Summaries include event counts, safety block rate, state averages, action distribution, oscillation
rates, model used, and dataset id.

## Public EEG Event-Locked Evaluation

`make public-eeg-fixture-suite` creates an event-locked classifier report with balanced accuracy,
macro F1, confusion matrix, classifier shadow predictions, LSL validation artifacts, calibration,
heuristic shadow output, and a heuristic-vs-learned comparison.

Interpretation is deliberately narrow: the learned model predicts controlled event/task labels from
annotated epochs. It is not a general cognitive decoder.


## Real Public EEG Validation

PhysioNet EEGBCI support is local-first. Use `make physionet-eegbci-config` to create a config for local EDF files, then `make inspect-physionet-eegbci`, `make prepare-physionet-eegbci-events`, and `make train-physionet-eegbci-classifier` when files are present. Downloads happen only with `make physionet-eegbci-download`.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Closed-loop adaptation remains disabled by default.

The first real PhysioNet EEGBCI subset run used subjects `S001-S003`, runs
`4/8/12`, and a `group_run` split. The logistic-regression baseline reported
accuracy 0.508, balanced accuracy 0.478, macro F1 0.479, and macro AUROC 0.655.
Those values are deliberately reported as modest baseline evidence, not as a
claim of scientific or clinical validity.

The same suite replayed `S001R04.edf` over LSL and produced timing diagnostics:
observed rate 159.798 Hz against a 160 Hz nominal rate, jitter p95 0.085 ms,
zero gaps, zero duplicate timestamps, and closed-loop allowed = false.

## BCI Benchmarking

`make bci-benchmark-small` compares several baseline classifiers on the real
PhysioNet event-feature CSV using a leakage-aware `group_run` split. It produces
`model_comparison.csv`, per-model metrics, confusion matrices, bootstrap
confidence intervals for accuracy/balanced accuracy/macro F1, leakage warnings,
and `best_model.json`.

The first small benchmark selected histogram gradient boosting by balanced
accuracy. This remains an offline/shadow-only model; it does not unlock real EEG
closed-loop adaptation.

## Raw-Epoch CSP Evaluation

`make prepare-raw-epochs-small` exports binary left-vs-right motor imagery
epochs from PhysioNet EEGBCI as raw tensors. `make raw-bci-benchmark-small`
then evaluates CSP + LDA, CSP + logistic regression, and CSP + linear SVM with
CSP fit only on training data.

The latest small group-run raw benchmark added Filter Bank CSP and selected
`fbcsp_logreg` with 8 CSP components per band: accuracy 0.617, balanced
accuracy 0.615, and macro F1 0.614. LOSO is available through
`make raw-bci-loso-small` and produced a harder mean balanced accuracy near
0.510 on the three-subject subset.

Raw CSP results are benchmark evidence for controlled task-label classification,
not thought decoding or clinical validation.

Medium-cohort evaluation targets are available for subjects 1-10, runs 4/8/12,
including `group_run`, `group_subject`, and LOSO commands. They require local
EDF files or an explicit PhysioNet download and are not part of CI. The latest
local medium run reported group-run FBCSP balanced accuracy around 0.576,
group-subject around 0.509, and LOSO fold mean around 0.488, with closed-loop
adaptation still disabled.

## First Physical EEG Trial Evaluation

`make physical-eeg-trial-synthetic` validates the software protocol for
eyes-open / eyes-closed recording, alpha-band summary, timing/SQI/artifact
reporting, calibration, and shadow-only inference. With a real OpenBCI board,
run `make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0`.

Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal
behavior, not a medical test. The report uses `visible`, `weak`,
`inconclusive`, `noisy_signal`, or `insufficient_data` language and never
unlocks closed-loop adaptation.
