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
  "balanced_accuracy": 0.625,
  "macro_f1": 0.5416666666666666,
  "weighted_f1": 0.5666666666666667,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.3333333333333333,
      "recall": 1.0,
      "f1-score": 0.5,
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
      "recall": 0.5,
      "f1-score": 0.6666666666666666,
      "support": 2.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 1.0,
      "recall": 1.0,
      "f1-score": 1.0,
      "support": 1.0
    },
    "accuracy": 0.6,
    "macro avg": {
      "precision": 0.5833333333333333,
      "recall": 0.625,
      "f1-score": 0.5416666666666666,
      "support": 5.0
    },
    "weighted avg": {
      "precision": 0.6666666666666667,
      "recall": 0.6,
      "f1-score": 0.5666666666666667,
      "support": 5.0
    }
  },
  "confusion_matrix": [
    [
      1,
      0,
      0,
      0
    ],
    [
      1,
      0,
      0,
      0
    ],
    [
      1,
      0,
      1,
      0
    ],
    [
      0,
      0,
      0,
      1
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "NOISY_SEGMENT",
    "REST",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.27438913865532205,
    "mce": 0.46090275437699724,
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
        "count": 2,
        "accuracy": 0.0,
        "confidence": 0.46090275437699724
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
        "count": 1,
        "accuracy": 1.0,
        "confidence": 0.7954804578862245
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 2,
        "accuracy": 1.0,
        "confidence": 0.8771896787955799
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ]
  },
  "auroc_ovr_macro": 1.0,
  "latency": {
    "mean_inference_latency_ms": 0.3889081985107623,
    "p95_inference_latency_ms": 0.4812255996512249,
    "p99_inference_latency_ms": 0.5023347196402028,
    "throughput_samples_per_sec": 2571.300897819275
  },
  "split_strategy": "stratified",
  "split_warnings": [],
  "per_subject": {
    "fixture": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.625,
      "macro_f1": 0.5416666666666666,
      "weighted_f1": 0.5666666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 1.0,
          "f1-score": 0.5,
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
          "recall": 0.5,
          "f1-score": 0.6666666666666666,
          "support": 2.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 1.0,
          "f1-score": 1.0,
          "support": 1.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5833333333333333,
          "recall": 0.625,
          "f1-score": 0.5416666666666666,
          "support": 5.0
        },
        "weighted avg": {
          "precision": 0.6666666666666667,
          "recall": 0.6,
          "f1-score": 0.5666666666666667,
          "support": 5.0
        }
      },
      "confusion_matrix": [
        [
          1,
          0,
          0,
          0
        ],
        [
          1,
          0,
          0,
          0
        ],
        [
          1,
          0,
          1,
          0
        ],
        [
          0,
          0,
          0,
          1
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "NOISY_SEGMENT",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    }
  },
  "per_run": {
    "unknown": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.625,
      "macro_f1": 0.5416666666666666,
      "weighted_f1": 0.5666666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 1.0,
          "f1-score": 0.5,
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
          "recall": 0.5,
          "f1-score": 0.6666666666666666,
          "support": 2.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 1.0,
          "f1-score": 1.0,
          "support": 1.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5833333333333333,
          "recall": 0.625,
          "f1-score": 0.5416666666666666,
          "support": 5.0
        },
        "weighted avg": {
          "precision": 0.6666666666666667,
          "recall": 0.6,
          "f1-score": 0.5666666666666667,
          "support": 5.0
        }
      },
      "confusion_matrix": [
        [
          1,
          0,
          0,
          0
        ],
        [
          1,
          0,
          0,
          0
        ],
        [
          1,
          0,
          1,
          0
        ],
        [
          0,
          0,
          0,
          1
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "NOISY_SEGMENT",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    }
  }
}
```