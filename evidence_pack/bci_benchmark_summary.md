# BCI Benchmark: 20260508T121032Z_bci_benchmark

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.

## Dataset
- Features: `/home/tonystark/Desktop/NeuroVerse/data/processed/physionet_eegbci_event_features.csv`
- Split: `group_run`
- Binary left/right only: `False`
- Rows: `270`
- Labels: `{'REST': 135, 'RIGHT_HAND_IMAGERY': 66, 'LEFT_HAND_IMAGERY': 69}`

## Model Comparison
| Model | Status | Accuracy | Balanced Accuracy | Macro F1 | Notes |
| --- | --- | ---: | ---: | ---: | --- |
| logistic_regression | ok | 0.508 | 0.478 | 0.479 |  |
| ridge_classifier | ok | 0.417 | 0.356 | 0.355 |  |
| random_forest | ok | 0.550 | 0.465 | 0.469 |  |
| hist_gradient_boosting | ok | 0.567 | 0.515 | 0.520 |  |
| svm_linear | ok | 0.492 | 0.473 | 0.469 |  |
| csp_lda | deferred | — | — | — | CSP/FBCSP requires raw epoch tensors; this benchmark input is a flattened feature CSV. Deferred rather than approximated from tabular features. |
| csp_logreg | deferred | — | — | — | CSP/FBCSP requires raw epoch tensors; this benchmark input is a flattened feature CSV. Deferred rather than approximated from tabular features. |

## Best Model
- Model: `hist_gradient_boosting`
- Model id: `physionet_eegbci_small_hist_gradient_boosting`
- Primary metric: `balanced_accuracy`

## Leakage Warnings
- None

## Safety
Benchmark models are registered for offline and shadow evaluation only. Real EEG closed-loop adaptation remains disabled by default.