# IMAGINA Model Card: v1 LOGISTIC_REGRESSION (classification)

## Intended Use
This baseline model estimates conservative mental-imagery and perception proxies under controlled task guidelines for portfolio demonstration.

## Not Intended Use
- Unrestricted thought decoding, dream reading, clinical diagnostic evaluation, or direct hardware closed-loop control.

## Baseline Details
- **Model Type:** logistic_regression
- **Target Type:** classification
- **Split Strategy:** fixture
- **Sample Count:** 6
- **Subject Count:** 2

## Metrics
```json
{
  "accuracy": 1.0,
  "balanced_accuracy": 1.0,
  "macro_f1": 1.0,
  "confusion_matrix": [
    [
      2,
      0
    ],
    [
      0,
      4
    ]
  ],
  "sample_count": 6,
  "subject_count": 2,
  "split_strategy": "fixture",
  "leakage_warnings": [
    "Fixture validation metrics: This model is trained on synthetic/fixture demo data for workflow verification only. No scientific validity is claimed."
  ],
  "model_type": "logistic_regression",
  "target_type": "classification"
}
```

## Safety Governance
- **Status:** Closed-Loop from Real EEG is Locked/Disabled.
- **Pipeline Warnings:**
  - Fixture validation metrics: This model is trained on synthetic/fixture demo data for workflow verification only. No scientific validity is claimed.