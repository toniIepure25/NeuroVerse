# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260508T151555Z_raw_bci
- Split: group_run
- Shape: [135, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 66, 'LEFT_HAND_IMAGERY': 69}
- Best model: fbcsp_logreg csp=8
- Best balanced accuracy: 0.6145717463848721
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.41434927697441604 | 0.4125874125874126 |
| csp_lda | 4 | ok | 0.5939933259176863 | 0.5833333333333333 |
| csp_lda | 6 | ok | 0.5389321468298109 | 0.48717948717948717 |
| csp_lda | 8 | ok | 0.5734149054505006 | 0.5368941031182464 |
| csp_logreg | 2 | ok | 0.4271412680756396 | 0.4097222222222222 |
| csp_logreg | 4 | ok | 0.5778642936596218 | 0.5688416211555045 |
| csp_logreg | 6 | ok | 0.5389321468298109 | 0.48717948717948717 |
| csp_logreg | 8 | ok | 0.5917686318131257 | 0.569377990430622 |
| csp_svm_linear | 2 | ok | 0.5 | 0.34065934065934067 |
| csp_svm_linear | 4 | ok | 0.5617352614015573 | 0.5542857142857143 |
| csp_svm_linear | 6 | ok | 0.5734149054505006 | 0.5368941031182464 |
| csp_svm_linear | 8 | ok | 0.5895439377085651 | 0.55 |
| fbcsp_logreg | 2 | ok | 0.482202447163515 | 0.48203842940685043 |
| fbcsp_logreg | 4 | ok | 0.40155728587319245 | 0.3993325917686318 |
| fbcsp_logreg | 6 | ok | 0.5617352614015573 | 0.5542857142857143 |
| fbcsp_logreg | 8 | ok | 0.6145717463848721 | 0.613986013986014 |
| fbcsp_lda | 2 | ok | 0.5005561735261401 | 0.5 |
| fbcsp_lda | 4 | ok | 0.4555061179087876 | 0.4373401534526854 |
| fbcsp_lda | 6 | ok | 0.5834260289210234 | 0.5832175604334537 |
| fbcsp_lda | 8 | ok | 0.6006674082313682 | 0.6 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.