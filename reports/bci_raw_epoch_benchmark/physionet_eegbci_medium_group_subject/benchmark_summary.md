# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260508T150227Z_raw_bci
- Split: group_subject
- Shape: [450, 64, 320]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: fbcsp_logreg csp=6
- Best balanced accuracy: 0.5090301830776843
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.46004453240969817 | 0.4221215910242979 |
| csp_lda | 4 | ok | 0.4804552201880258 | 0.4650471637162424 |
| csp_lda | 6 | ok | 0.4784760019792182 | 0.45317659490159823 |
| csp_lda | 8 | ok | 0.4944334487877288 | 0.46598219940664687 |
| csp_logreg | 2 | ok | 0.5007422068283028 | 0.4769515255580504 |
| csp_logreg | 4 | ok | 0.49208312716476993 | 0.4791666666666667 |
| csp_logreg | 6 | ok | 0.4678377041068778 | 0.4445903361344538 |
| csp_logreg | 8 | ok | 0.48911429985155863 | 0.46172248803827753 |
| fbcsp_logreg | 2 | ok | 0.46882731321128157 | 0.45064935064935063 |
| fbcsp_logreg | 4 | ok | 0.49096981692231567 | 0.4365305476416588 |
| fbcsp_logreg | 6 | ok | 0.5090301830776843 | 0.49767441860465117 |
| fbcsp_logreg | 8 | ok | 0.47946561108362196 | 0.45945945945945943 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.