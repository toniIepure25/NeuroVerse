# BCI Benchmark Comparison

| Pipeline | Model | Split | Balanced accuracy | Macro F1 |
| --- | --- | --- | ---: | ---: |
| Flattened features | hist_gradient_boosting | group_run | 0.5151217402051663 | 0.5196078431372548 |
| Raw epochs / CSP | fbcsp_logreg csp=8 | group_run | 0.6145717463848721 | 0.613986013986014 |
| Raw epochs / FBCSP | fbcsp_logreg csp=8 | group_run | 0.6145717463848721 | 0.613986013986014 |
| Medium group_run | fbcsp_lda csp=2 | group_run | 0.5761093153100205 | 0.5744916003536693 |
| Medium group_subject | fbcsp_logreg csp=6 | group_subject | 0.5090301830776843 | 0.49767441860465117 |
| Medium loso | fbcsp_logreg csp=4 | leave_one_subject_out | 0.6160714285714286 | 0.6153846153846154 |

Live raw shadow mode: `live_lsl`; predictions: 5; missed epochs: 0.

Flattened features are an engineered tabular baseline; CSP models are raw-epoch spatial-filter baselines. Neither result is a thought-reading or clinical claim.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.