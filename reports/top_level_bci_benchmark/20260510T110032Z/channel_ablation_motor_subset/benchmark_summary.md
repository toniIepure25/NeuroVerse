# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260510T125759Z_raw_bci
- Split: leave_one_subject_out
- Shape: [450, 7, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: riemann_ts_logreg csp=2
- Best balanced accuracy: 0.6994047619047619
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.5595238095238095 | 0.5553359683794465 |
| csp_lda | 4 | ok | 0.5892857142857143 | 0.5701357466063348 |
| csp_lda | 6 | ok | 0.5863095238095238 | 0.5744151319064211 |
| csp_lda | 8 | ok | 0.5386904761904762 | 0.5324096981692232 |
| fbcsp_logreg | 2 | ok | 0.5863095238095237 | 0.5745798319327731 |
| fbcsp_logreg | 4 | ok | 0.5773809523809523 | 0.533410138248848 |
| fbcsp_logreg | 6 | ok | 0.5565476190476191 | 0.5166760881854155 |
| fbcsp_logreg | 8 | ok | 0.5416666666666666 | 0.5273109243697479 |
| riemann_mdm | 2 | ok | 0.6101190476190476 | 0.595 |
| riemann_mdm | 4 | ok | 0.6101190476190476 | 0.595 |
| riemann_mdm | 6 | ok | 0.6101190476190476 | 0.595 |
| riemann_mdm | 8 | ok | 0.6101190476190476 | 0.595 |
| riemann_ts_logreg | 2 | ok | 0.6994047619047619 | 0.6961038961038961 |
| riemann_ts_logreg | 4 | ok | 0.6994047619047619 | 0.6961038961038961 |
| riemann_ts_logreg | 6 | ok | 0.6994047619047619 | 0.6961038961038961 |
| riemann_ts_logreg | 8 | ok | 0.6994047619047619 | 0.6961038961038961 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.