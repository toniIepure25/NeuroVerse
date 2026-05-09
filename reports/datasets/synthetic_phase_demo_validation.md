# Dataset Validation: synthetic_phase_demo

- Adapter: `synthetic`
- Target: `phase_label`
- Windows: `90`
- Subjects: `1`
- Sessions: `1`
- Features: `32`

## Label Distribution
{
  "baseline": 15,
  "focus": 15,
  "workload": 15,
  "relaxation": 15,
  "imagery": 15,
  "noisy": 10,
  "fatigue": 5
}

## Feature Warnings
- Class imbalance detected; prefer balanced metrics and careful splits
- 1 constant feature columns detected
- Only one subject is present; subject-level generalization cannot be tested
- Only one session is present; session-level leakage risk is high
- Only one subject/session group is present; group split will not be meaningful

## Scientific Note
Dataset labels are dataset-derived proxies and should not be interpreted as clinical ground truth or direct access to mental state.
