# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260508T151555Z_raw_bci
- Split: leave_one_subject_out
- Shape: [135, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 66, 'LEFT_HAND_IMAGERY': 69}
- Best model: csp_lda csp=6
- Best balanced accuracy: 0.5207509881422925
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.5 | 0.3283582089552239 |
| csp_lda | 4 | ok | 0.4990118577075099 | 0.3630769230769231 |
| csp_lda | 6 | ok | 0.5207509881422925 | 0.4050480769230769 |
| csp_lda | 8 | ok | 0.5 | 0.3283582089552239 |
| csp_logreg | 2 | ok | 0.5 | 0.3283582089552239 |
| csp_logreg | 4 | ok | 0.4772727272727273 | 0.3181818181818182 |
| csp_logreg | 6 | ok | 0.5 | 0.3283582089552239 |
| csp_logreg | 8 | ok | 0.5 | 0.3283582089552239 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.