# Model Card: eeg_event_classifier_fixture

## Intended Use
Event-locked controlled EEG task-label classification.

## Not Intended Use
Not for thought reading, clinical diagnosis, unrestricted mental-state inference, or direct closed-loop control.

## Limitations
Fixture or local dataset annotations define labels; performance is not clinical validation and may not generalize across subjects or hardware.

## Metrics
```json
{
  "task_type": "classification",
  "accuracy": 0.6,
  "balanced_accuracy": 0.5,
  "macro_f1": 0.4,
  "weighted_f1": 0.6,
  "per_class": {
    "BASELINE": {
      "precision": 0.0,
      "recall": 0.0,
      "f1-score": 0.0,
      "support": 1.0
    },
    "LEFT_HAND_IMAGERY": {
      "precision": 1.0,
      "recall": 1.0,
      "f1-score": 1.0,
      "support": 1.0
    },
    "NOISY_SEGMENT": {
      "precision": 0.0,
      "recall": 0.0,
      "f1-score": 0.0,
      "support": 1.0
    },
    "REST": {
      "precision": 1.0,
      "recall": 1.0,
      "f1-score": 1.0,
      "support": 2.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.0,
      "recall": 0.0,
      "f1-score": 0.0,
      "support": 0.0
    },
    "accuracy": 0.6,
    "macro avg": {
      "precision": 0.4,
      "recall": 0.4,
      "f1-score": 0.4,
      "support": 5.0
    },
    "weighted avg": {
      "precision": 0.6,
      "recall": 0.6,
      "f1-score": 0.6,
      "support": 5.0
    }
  },
  "confusion_matrix": [
    [
      0,
      0,
      1,
      0,
      0
    ],
    [
      0,
      1,
      0,
      0,
      0
    ],
    [
      0,
      0,
      0,
      0,
      1
    ],
    [
      0,
      0,
      0,
      2,
      0
    ],
    [
      0,
      0,
      0,
      0,
      0
    ]
  ],
  "class_labels": [
    "BASELINE",
    "LEFT_HAND_IMAGERY",
    "NOISY_SEGMENT",
    "REST",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.7664930737486982,
    "mce": 0.999983855449787,
    "reliability_bins": [
      {
        "lo": 0.0,
        "hi": 0.1,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.1,
        "hi": 0.2,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.2,
        "hi": 0.30000000000000004,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.30000000000000004,
        "hi": 0.4,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.4,
        "hi": 0.5,
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.49652621489248405
      },
      {
        "lo": 0.5,
        "hi": 0.6,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 2,
        "accuracy": 0.0,
        "confidence": 0.7592011811947627
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.8175529360116944
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.999983855449787
      }
    ]
  },
  "auroc": null,
  "latency": {
    "mean_inference_latency_ms": 0.37317940150387585,
    "p95_inference_latency_ms": 0.4469748033443466,
    "p99_inference_latency_ms": 0.4642509639961645,
    "throughput_samples_per_sec": 2679.6763057395437
  }
}
```