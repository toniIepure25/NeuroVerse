# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260510T110725Z_raw_bci
- Split: group_run
- Shape: [450, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: fbcsp_logreg csp=4
- Best balanced accuracy: 0.6123273582133412
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.5202027622685865 | 0.5070156196815552 |
| csp_lda | 4 | ok | 0.5260799294739935 | 0.5075757575757576 |
| csp_lda | 6 | ok | 0.5449603291213635 | 0.5421584224351623 |
| csp_lda | 8 | ok | 0.5266676461945342 | 0.5222007722007722 |
| fbcsp_logreg | 2 | ok | 0.5033059065530414 | 0.5021342360906682 |
| fbcsp_logreg | 4 | ok | 0.6123273582133412 | 0.611764705882353 |
| fbcsp_logreg | 6 | ok | 0.5575227740229209 | 0.5575107453804049 |
| fbcsp_logreg | 8 | ok | 0.5694975022039377 | 0.5691272205671412 |
| riemann_mdm | 2 | ok | 0.508742286218043 | 0.5072811059907834 |
| riemann_mdm | 4 | ok | 0.508742286218043 | 0.5072811059907834 |
| riemann_mdm | 6 | ok | 0.508742286218043 | 0.5072811059907834 |
| riemann_mdm | 8 | ok | 0.508742286218043 | 0.5072811059907834 |
| riemann_ts_logreg | 2 | ok | 0.5697178959741405 | 0.5696969696969697 |
| riemann_ts_logreg | 4 | ok | 0.5697178959741405 | 0.5696969696969697 |
| riemann_ts_logreg | 6 | ok | 0.5697178959741405 | 0.5696969696969697 |
| riemann_ts_logreg | 8 | ok | 0.5697178959741405 | 0.5696969696969697 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.