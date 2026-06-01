# Raw-Epoch CSP BCI Benchmark

- Benchmark: 20260510T110949Z_raw_bci
- Split: group_run
- Shape: [450, 64, 480]
- Labels: {'RIGHT_HAND_IMAGERY': 220, 'LEFT_HAND_IMAGERY': 230}
- Best model: fbcsp_logreg csp=6
- Best balanced accuracy: 0.636203349985307
- Closed-loop allowed: False

## Model Comparison

| Model | CSP components | Status | Balanced accuracy | Macro F1 |
| --- | ---: | --- | ---: | ---: |
| csp_lda | 2 | ok | 0.5075668527769615 | 0.47507953340402975 |
| csp_lda | 4 | ok | 0.519761974728181 | 0.4913170731707317 |
| csp_lda | 6 | ok | 0.49566558918601233 | 0.47182691195186854 |
| csp_lda | 8 | ok | 0.5506171025565678 | 0.5409774436090226 |
| fbcsp_logreg | 2 | ok | 0.5575962386129886 | 0.5575757575757576 |
| fbcsp_logreg | 4 | ok | 0.5937408169262416 | 0.5934017433520908 |
| fbcsp_logreg | 6 | ok | 0.636203349985307 | 0.6360294117647058 |
| fbcsp_logreg | 8 | ok | 0.6302527181898325 | 0.6302487050439 |
| riemann_mdm | 2 | ok | 0.5204231560387893 | 0.5125462772521596 |
| riemann_mdm | 4 | ok | 0.5204231560387893 | 0.5125462772521596 |
| riemann_mdm | 6 | ok | 0.5204231560387893 | 0.5125462772521596 |
| riemann_mdm | 8 | ok | 0.5204231560387893 | 0.5125462772521596 |
| riemann_ts_logreg | 2 | ok | 0.5880840434910373 | 0.5874999999999999 |
| riemann_ts_logreg | 4 | ok | 0.5880840434910373 | 0.5874999999999999 |
| riemann_ts_logreg | 6 | ok | 0.5880840434910373 | 0.5874999999999999 |
| riemann_ts_logreg | 8 | ok | 0.5880840434910373 | 0.5874999999999999 |

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.