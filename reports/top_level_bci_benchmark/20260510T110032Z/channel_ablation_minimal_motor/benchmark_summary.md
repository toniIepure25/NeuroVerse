# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260510T125912Z_raw_bci
- Split: leave_one_subject_out
- Shape: [450, 3, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: csp_lda csp=2
- Best balanced accuracy: 0.6369047619047619
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.6369047619047619 | 0.6356275303643725 |
| csp_lda | 4 | ok | 0.6369047619047619 | 0.6356275303643725 |
| csp_lda | 6 | ok | 0.6369047619047619 | 0.6356275303643725 |
| csp_lda | 8 | ok | 0.6369047619047619 | 0.6356275303643725 |
| fbcsp_logreg | 2 | ok | 0.5208333333333334 | 0.509090909090909 |
| fbcsp_logreg | 4 | ok | 0.5446428571428572 | 0.537037037037037 |
| fbcsp_logreg | 6 | ok | 0.5446428571428572 | 0.537037037037037 |
| fbcsp_logreg | 8 | ok | 0.5446428571428572 | 0.537037037037037 |
| riemann_mdm | 2 | ok | 0.6279761904761905 | 0.6214745175655616 |
| riemann_mdm | 4 | ok | 0.6279761904761905 | 0.6214745175655616 |
| riemann_mdm | 6 | ok | 0.6279761904761905 | 0.6214745175655616 |
| riemann_mdm | 8 | ok | 0.6279761904761905 | 0.6214745175655616 |
| riemann_ts_logreg | 2 | ok | 0.5565476190476191 | 0.5553359683794465 |
| riemann_ts_logreg | 4 | ok | 0.5565476190476191 | 0.5553359683794465 |
| riemann_ts_logreg | 6 | ok | 0.5565476190476191 | 0.5553359683794465 |
| riemann_ts_logreg | 8 | ok | 0.5565476190476191 | 0.5553359683794465 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.