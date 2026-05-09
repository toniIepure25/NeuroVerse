# NeuroVerse Phase 2 Datasets

NeuroVerse Phase 2 supports local dataset adapters for research replay and baseline evaluation.
Large public datasets should stay outside Git. Commit only small fixtures and example configs.

## Supported Adapters

| Adapter | Config `type` | Status |
|---|---|---|
| Synthetic simulator | `synthetic` | Deterministic development and CI adapter built from `BiosignalSimulator` |
| Generic CSV | `generic_csv` | Local CSV adapter for precomputed features or raw-ish signal columns |
| CLARE-like | `clare_like` | Flexible fixture-compatible cognitive workload layout; real format assumptions must be verified locally |
| PhysioNet MI | `physionet_mi` | Fixture mode works; EDF parsing requires optional `mne` and verified local layout |

## Generic CSV Example

```yaml
dataset_id: my_local_dataset
type: generic_csv
path: ../../data/external/my_file.csv
timestamp_col: timestamp
subject_id_col: subject_id
session_id_col: session_id
label_col: label
feature_cols:
  - eeg_alpha_power
  - eeg_beta_power
  - physio_heart_rate
  - gaze_fixation_stability
window_size_seconds: 2.0
overlap: 0.5
```

If `feature_cols` are provided, windows average those columns directly. If raw modality columns
are configured instead, the adapter passes windows through the existing NeuroVerse feature extractors.

## CLARE-Like Assumptions

The CLARE-like adapter expects a local directory with:

- `signals.csv`: timestamped features or signal proxies
- `labels.csv`: timestamped workload labels

Supported labels are mapped as dataset-derived workload proxies: `low`, `medium`, and `high`.
This adapter does not claim validated full CLARE support until the real local dataset layout is verified.

## PhysioNet MI

PhysioNet EEG Motor Movement/Imagery data is commonly EDF-based. NeuroVerse keeps MNE optional:

- fixture CSV mode works without extra dependencies;
- EDF parsing raises a clear message if `mne` is unavailable;
- no large PhysioNet files are downloaded automatically.

Motor imagery labels should be interpreted as motor-intent candidates or task labels, not full cognitive
state estimates.

## Privacy And Storage

Place private or public dataset copies under `data/external/` or another local path excluded from Git.
Dataset-derived labels and model outputs are research proxies, not clinical ground truth.
