# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260508T150405Z_raw_bci
- Split: leave_one_subject_out
- Shape: [450, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: fbcsp_logreg csp=4
- Best balanced accuracy: 0.6160714285714286
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.49404761904761907 | 0.37788018433179726 |
| csp_lda | 4 | ok | 0.5297619047619048 | 0.5296167247386759 |
| csp_lda | 6 | ok | 0.5297619047619048 | 0.48004201680672265 |
| csp_lda | 8 | ok | 0.48214285714285715 | 0.4444444444444444 |
| csp_logreg | 2 | ok | 0.5148809523809523 | 0.41492368569813454 |
| csp_logreg | 4 | ok | 0.4494047619047619 | 0.44334487877288475 |
| csp_logreg | 6 | ok | 0.5535714285714286 | 0.49760765550239233 |
| csp_logreg | 8 | ok | 0.48214285714285715 | 0.4444444444444444 |
| fbcsp_logreg | 2 | ok | 0.5863095238095238 | 0.5744151319064211 |
| fbcsp_logreg | 4 | ok | 0.6160714285714286 | 0.6153846153846154 |
| fbcsp_logreg | 6 | ok | 0.5625 | 0.5454545454545454 |
| fbcsp_logreg | 8 | ok | 0.5446428571428572 | 0.537037037037037 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.