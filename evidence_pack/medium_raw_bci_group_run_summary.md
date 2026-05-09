# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260508T145929Z_raw_bci
- Split: group_run
- Shape: [450, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: fbcsp_lda csp=2
- Best balanced accuracy: 0.5761093153100205
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.5330590655304144 | 0.5322337174625382 |
| csp_lda | 4 | ok | 0.5684689979429915 | 0.5506156737887913 |
| csp_lda | 6 | ok | 0.5685424625330591 | 0.5528796610816381 |
| csp_lda | 8 | ok | 0.5321040258595358 | 0.5126395335455906 |
| csp_logreg | 2 | ok | 0.5390831619159565 | 0.5380194518125552 |
| csp_logreg | 4 | ok | 0.5504701733764326 | 0.5372195269860521 |
| csp_logreg | 6 | ok | 0.574786952688804 | 0.5640851449275363 |
| csp_logreg | 8 | ok | 0.520129297678519 | 0.5048433048433049 |
| csp_svm_linear | 2 | ok | 0.5330590655304144 | 0.5322337174625382 |
| csp_svm_linear | 4 | ok | 0.5563473405818395 | 0.537956960374391 |
| csp_svm_linear | 6 | ok | 0.550396708786365 | 0.5351050868108438 |
| csp_svm_linear | 8 | ok | 0.5628122245077872 | 0.5549895115373089 |
| fbcsp_logreg | 2 | ok | 0.5759623861298854 | 0.5753676470588236 |
| fbcsp_logreg | 4 | ok | 0.5752277402292095 | 0.5722222222222222 |
| fbcsp_logreg | 6 | ok | 0.5325448133999413 | 0.5248868778280543 |
| fbcsp_logreg | 8 | ok | 0.520276226858654 | 0.5090210554069833 |
| fbcsp_lda | 2 | ok | 0.5761093153100205 | 0.5744916003536693 |
| fbcsp_lda | 4 | ok | 0.5634734058183956 | 0.5632352941176471 |
| fbcsp_lda | 6 | ok | 0.52101087275933 | 0.5205781749972416 |
| fbcsp_lda | 8 | ok | 0.5330590655304144 | 0.5322337174625382 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.