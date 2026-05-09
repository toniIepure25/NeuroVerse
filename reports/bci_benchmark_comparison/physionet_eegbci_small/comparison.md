# BCI Benchmark Comparison

| Pipeline | Model | Split | Balanced accuracy | Macro F1 |
| --- | --- | --- | ---: | ---: |
| Flattened features | hist_gradient_boosting | group_run | 0.5151217402051663 | 0.5196078431372548 |
| Raw epochs / CSP | fbcsp_logreg csp=8 | group_run | 0.6145717463848721 | 0.613986013986014 |
| Raw epochs / FBCSP | fbcsp_logreg csp=8 | group_run | 0.6145717463848721 | 0.613986013986014 |

Live raw shadow mode: `not_available`; predictions: —; missed epochs: —.

Flattened features are an engineered tabular baseline; CSP models are raw-epoch spatial-filter baselines. Neither result is a thought-reading or clinical claim.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.