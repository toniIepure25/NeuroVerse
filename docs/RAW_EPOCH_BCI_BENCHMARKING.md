# Raw-Epoch BCI Benchmarking

NeuroVerse now includes a raw-epoch motor imagery benchmark path for PhysioNet
EEGBCI-style data. This path exists because CSP should be fit on tensors shaped
`n_epochs x n_channels x n_times`, not on flattened feature CSVs.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics.

Event-locked EEG classifiers predict controlled dataset task labels under
experimental conditions; they should not be interpreted as general mind-reading
models.

## Workflow

Small subset:

```bash
make prepare-raw-epochs-small
make raw-bci-benchmark-small
make raw-bci-loso-small
make compare-bci-benchmarks
make shadow-best-raw-bci-model
make generate-evidence-pack
```

The default raw epoch export uses PhysioNet EEGBCI subjects 1-3, runs 4/8/12,
binary labels `LEFT_HAND_IMAGERY` and `RIGHT_HAND_IMAGERY`, a 0.5-2.5 second
epoch window, and a 7-35 Hz bandpass.

## Models

Implemented raw-epoch baselines:

- `csp_lda`
- `csp_logreg`
- `csp_svm_linear`
- `fbcsp_logreg`
- `fbcsp_lda`

The benchmark grid evaluates CSP component counts `2, 4, 6, 8`. CSP is inside
the sklearn pipeline and is fit only on the training split.

Filter Bank CSP uses five motor-imagery bands: 8-12, 12-16, 16-20, 20-24, and
24-30 Hz. Each band is filtered inside the model adapter, fits CSP only on the
training split, concatenates the per-band CSP features, then fits LDA or
logistic regression. Riemannian models remain deferred because `pyriemann` is
not required by the project.

## Splits

Supported benchmark splits:

- `group_run`
- `group_subject`
- `leave_one_subject_out`
- `within_subject`
- explicit `train_runs` / `test_runs`

Group splits report leakage warnings if train and test groups overlap.

## Current Small-Subset Result

On the latest small subset run, the best group-run raw epoch model was
`fbcsp_logreg` with 8 CSP components per band:

- accuracy: approximately 0.617
- balanced accuracy: approximately 0.615
- macro F1: approximately 0.614
- balanced accuracy 95% bootstrap CI: approximately 0.483-0.730

LOSO is harder on this tiny three-subject subset:

- mean balanced accuracy: approximately 0.510
- mean macro F1: approximately 0.419

These are benchmark numbers for a small public EEG subset, not clinical
validation and not evidence of unrestricted mental-state inference.

## Medium Subset

The medium target is subjects 1-10, runs 4/8/12. It is opt-in:

```bash
make physionet-eegbci-download-medium
make physionet-eegbci-config-medium
make inspect-physionet-eegbci-medium
make prepare-raw-epochs-medium
make raw-bci-benchmark-medium
make raw-bci-group-subject-medium
make raw-bci-loso-medium
```

No medium download or benchmark is required for CI.

Latest local medium run:

- 30 EDF files for subjects `S001-S010`, runs `4/8/12`.
- Raw tensor: 450 epochs, 64 channels, 320 samples.
- Group-run best: `fbcsp_lda`, balanced accuracy approximately 0.576.
- Group-subject best: `fbcsp_logreg`, balanced accuracy approximately 0.509.
- LOSO fold summary: mean balanced accuracy approximately 0.488.

The drop from group-run to subject-held-out evaluation is expected for a small
classical BCI baseline and is reported directly rather than tuned away.

## Shadow-Only Use

`make shadow-best-raw-bci-model` runs the best raw model in offline shadow mode
against saved epochs. `make live-shadow-best-raw-bci-model` starts replayed EDF
LSL streams, buffers live EEG timestamps, collects marker samples, builds raw
epochs around target markers, and applies the selected CSP/FBCSP model in
shadow mode. It records `mode = live_lsl` when stream discovery and buffering
succeed, otherwise it records the explicit fallback reason. Both modes emit zero
Dream Corridor adaptation actions and keep closed-loop use disabled.
