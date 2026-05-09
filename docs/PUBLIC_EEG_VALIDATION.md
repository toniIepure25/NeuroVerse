# Public EEG Validation And Event-Locked Classifier

This workflow turns a local MNE-compatible EEG file, or the deterministic NeuroVerse EEG fixture, into an event-locked BCI ML evidence run.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

Event-locked EEG classifiers predict dataset task labels under controlled conditions; they should not be interpreted as general mind-reading models.

## Fixture Mode

```bash
make inspect-eeg-fixture
make prepare-eeg-fixture-events
make train-eeg-fixture-classifier
make public-eeg-fixture-suite
make generate-evidence-pack
```

The fixture is deterministic EEG-like MNE `RawArray` data with 10-20-style channel labels and task annotations. It is useful for CI and demos; it is not an external public EEG recording.

## Local File Mode

```bash
make inspect-eeg-file FILE=/path/to/file.edf
make prepare-eeg-file-events FILE=/path/to/file.edf
make public-eeg-file-suite FILE=/path/to/file.edf
```

Supported formats follow MNE reader support, including EDF/BDF/FIF/GDF and EEG Lab `.set` when local dependencies support it. NeuroVerse does not download or commit large EEG datasets automatically.

## Reports

The flagship suite writes:

```text
reports/public_eeg_validation/<run_id>/
  eeg_file_inspection.json
  eeg_event_features.csv
  classifier_metrics.json
  classifier_model_card.md
  lsl_validation_report.json
  calibration_report.json
  heuristic_shadow_report.json
  classifier_shadow_report.json
  heuristic_vs_classifier_comparison.md
  public_eeg_validation_summary.md
```

The learned classifier is shadow-only by default. It predicts controlled event labels from epochs; it does not issue corridor commands.


## Real Public EEG Validation

PhysioNet EEGBCI support is local-first. Use `make physionet-eegbci-config` to create a config for local EDF files, then `make inspect-physionet-eegbci`, `make prepare-physionet-eegbci-events`, and `make train-physionet-eegbci-classifier` when files are present. Downloads happen only with `make physionet-eegbci-download`.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Closed-loop adaptation remains disabled by default.
