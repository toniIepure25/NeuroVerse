# Heuristic vs EEG Event Classifier

- classifier model: `eeg_event_classifier_fixture`
- classifier accuracy: `0.8333`
- closed-loop allowed: `False`

```json
{
  "marker_labels": {
    "BASELINE": 1,
    "LEFT_HAND_IMAGERY": 3,
    "REST": 3,
    "RIGHT_HAND_IMAGERY": 3,
    "NOISY_SEGMENT": 2
  },
  "classifier_predictions": {
    "NOISY_SEGMENT": 2,
    "LEFT_HAND_IMAGERY": 3,
    "REST": 3,
    "RIGHT_HAND_IMAGERY": 4
  },
  "classifier_accuracy": 0.8333,
  "classifier_model_id": "eeg_event_classifier_fixture",
  "heuristic_proxy_by_marker": {},
  "sqi_summary": {
    "count": 12,
    "mean": 0.7377
  },
  "timing": {
    "pass": true,
    "quality": "excellent",
    "expected_rate_hz": 250.0,
    "observed_rate_hz": 250.3411,
    "drift_percent": 0.1364,
    "jitter_ms_mean": 0.3592,
    "jitter_ms_p50": 0.1967,
    "jitter_ms_p95": 1.8932,
    "jitter_ms_p99": 1.9012,
    "jitter_ms_max": 1.907,
    "gap_count": 0,
    "gaps": [],
    "duplicate_count": 0,
    "monotonic_timestamp_pass": true,
    "clock_offset_estimate": null,
    "clock_offset_jitter": null,
    "warnings": [
      "LSL clock offset estimate unavailable."
    ]
  },
  "calibration_id": "20260507T223317Z_lsl_calibration",
  "real_adaptation_actions_emitted": 0,
  "interpretation": "Heuristic output is a cognitive proxy summary. The learned classifier predicts dataset task labels from event-locked EEG epochs. Neither is mind reading.",
  "closed_loop_allowed": false
}
```