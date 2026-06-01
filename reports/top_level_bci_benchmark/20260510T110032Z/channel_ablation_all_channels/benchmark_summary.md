# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260510T110040Z_raw_bci
- Split: leave_one_subject_out
- Shape: [450, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: fbcsp_logreg csp=4
- Best balanced accuracy: 0.6398809523809523
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.48511904761904756 | 0.48481831757093086 |
| csp_lda | 4 | ok | 0.48511904761904756 | 0.48481831757093086 |
| csp_lda | 6 | ok | 0.4017857142857143 | 0.4 |
| csp_lda | 8 | ok | 0.4226190476190476 | 0.42193675889328064 |
| fbcsp_logreg | 2 | ok | 0.6071428571428572 | 0.5982142857142857 |
| fbcsp_logreg | 4 | ok | 0.6398809523809523 | 0.64 |
| fbcsp_logreg | 6 | ok | 0.5654761904761905 | 0.5558441558441558 |
| fbcsp_logreg | 8 | ok | 0.5684523809523809 | 0.5639979602243753 |
| riemann_mdm | 2 | ok | 0.47619047619047616 | 0.3076923076923077 |
| riemann_mdm | 4 | ok | 0.47619047619047616 | 0.3076923076923077 |
| riemann_mdm | 6 | ok | 0.47619047619047616 | 0.3076923076923077 |
| riemann_mdm | 8 | ok | 0.47619047619047616 | 0.3076923076923077 |
| riemann_ts_logreg | 2 | ok | 0.5565476190476191 | 0.5553359683794465 |
| riemann_ts_logreg | 4 | ok | 0.5565476190476191 | 0.5553359683794465 |
| riemann_ts_logreg | 6 | ok | 0.5565476190476191 | 0.5553359683794465 |
| riemann_ts_logreg | 8 | ok | 0.5565476190476191 | 0.5553359683794465 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.