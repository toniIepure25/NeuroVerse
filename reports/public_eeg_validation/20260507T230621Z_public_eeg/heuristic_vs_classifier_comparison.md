# Heuristic vs EEG Event Classifier

- classifier model: `eeg_event_classifier_fixture`
- classifier accuracy: `0.8333`
- closed-loop allowed: `False`

```json
{
  "marker_labels": {
    "REST": 4,
    "LEFT_HAND_IMAGERY": 3,
    "RIGHT_HAND_IMAGERY": 3,
    "NOISY_SEGMENT": 2
  },
  "classifier_predictions": {
    "LEFT_HAND_IMAGERY": 5,
    "REST": 3,
    "RIGHT_HAND_IMAGERY": 3,
    "NOISY_SEGMENT": 1
  },
  "classifier_accuracy": 0.8333,
  "classifier_model_id": "eeg_event_classifier_fixture",
  "heuristic_proxy_by_marker": {
    "RIGHT_HAND_IMAGERY": {
      "focus": 0.6797,
      "relaxation": 0.749,
      "workload": 0.5783,
      "stress": 0.5,
      "fatigue": 0.542,
      "imagery_engagement": 0.6291,
      "confidence": 0.8808
    }
  },
  "sqi_summary": {
    "count": 12,
    "mean": 0.7377
  },
  "timing": {
    "pass": true,
    "quality": "excellent",
    "expected_rate_hz": 250.0,
    "observed_rate_hz": 249.9353,
    "drift_percent": -0.0259,
    "jitter_ms_mean": 0.3672,
    "jitter_ms_p50": 0.2002,
    "jitter_ms_p95": 1.8937,
    "jitter_ms_p99": 1.907,
    "jitter_ms_max": 1.9084,
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
  "calibration_id": "20260507T230634Z_lsl_calibration",
  "real_adaptation_actions_emitted": 0,
  "interpretation": "Heuristic output is a cognitive proxy summary. The learned classifier predicts dataset task labels from event-locked EEG epochs. Neither is mind reading.",
  "closed_loop_allowed": false
}
```