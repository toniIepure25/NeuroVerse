# Model Card: channel_ablation_all_channels_fbcsp_logreg_csp2

## Intended Use
Offline event-locked motor imagery task-label classification.

## Not Intended Use
Not for thought reading, clinical diagnosis, unrestricted mental-state inference, or direct closed-loop control.

## Limitations
Small public EEG subset; CSP is fit inside train splits. Metrics are benchmark evidence only and do not establish clinical validity.

## Metrics
```json
{
  "task_type": "classification",
  "accuracy": 0.6,
  "balanced_accuracy": 0.6071428571428572,
  "macro_f1": 0.5982142857142857,
  "weighted_f1": 0.5964285714285714,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6666666666666666,
      "recall": 0.5,
      "f1-score": 0.5714285714285714,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5555555555555556,
      "recall": 0.7142857142857143,
      "f1-score": 0.625,
      "support": 21.0
    },
    "accuracy": 0.6,
    "macro avg": {
      "precision": 0.6111111111111112,
      "recall": 0.6071428571428572,
      "f1-score": 0.5982142857142857,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.6148148148148148,
      "recall": 0.6,
      "f1-score": 0.5964285714285714,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      12,
      12
    ],
    [
      6,
      15
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.16821034797498313,
    "mce": 0.43724552763537283,
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
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.5,
        "hi": 0.6,
        "count": 13,
        "accuracy": 0.6153846153846154,
        "confidence": 0.5485805874429891
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 11,
        "accuracy": 0.36363636363636365,
        "confidence": 0.6551951531288812
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 7,
        "accuracy": 0.5714285714285714,
        "confidence": 0.7385159032703115
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 10,
        "accuracy": 0.9,
        "confidence": 0.8424726822218267
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 4,
        "accuracy": 0.5,
        "confidence": 0.9372455276353728
      }
    ],
    "brier_score": 0.24444843159929747
  },
  "auroc": 0.6726190476190478,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.741443733315261,
    "p95_inference_latency_ms": 6.949153800451313,
    "p99_inference_latency_ms": 7.355712119606324,
    "throughput_samples_per_sec": 148.33617835570465
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.6071428571428572,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.5964285714285714,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5,
          "f1-score": 0.5714285714285714,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.7142857142857143,
          "f1-score": 0.625,
          "support": 21.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6111111111111112,
          "recall": 0.6071428571428572,
          "f1-score": 0.5982142857142857,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.6148148148148148,
          "recall": 0.6,
          "f1-score": 0.5964285714285714,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          12,
          12
        ],
        [
          6,
          15
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.39285714285714285,
      "macro_f1": 0.3891402714932127,
      "weighted_f1": 0.3945701357466064,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5,
          "f1-score": 0.47058823529411764,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.2857142857142857,
          "f1-score": 0.3076923076923077,
          "support": 7.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.38888888888888884,
          "recall": 0.39285714285714285,
          "f1-score": 0.3891402714932127,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.39259259259259255,
          "recall": 0.4,
          "f1-score": 0.3945701357466064,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
        ],
        [
          5,
          2
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    },
    "4": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.625,
      "macro_f1": 0.55,
      "weighted_f1": 0.5399999999999999,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.25,
          "f1-score": 0.4,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 1.0,
          "f1-score": 0.7,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.7692307692307692,
          "recall": 0.625,
          "f1-score": 0.55,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7846153846153847,
          "recall": 0.6,
          "f1-score": 0.5399999999999999,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          6
        ],
        [
          0,
          7
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.8035714285714286,
      "macro_f1": 0.8,
      "weighted_f1": 0.8,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8571428571428571,
          "recall": 0.75,
          "f1-score": 0.8,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.8571428571428571,
          "f1-score": 0.8,
          "support": 7.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.8035714285714286,
          "recall": 0.8035714285714286,
          "f1-score": 0.8,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8071428571428572,
          "recall": 0.8,
          "f1-score": 0.8,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
        ],
        [
          1,
          6
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.6018,
      "lower_95": 0.455,
      "upper_95": 0.7556
    },
    "balanced_accuracy": {
      "mean": 0.6082,
      "lower_95": 0.4624,
      "upper_95": 0.7613
    },
    "macro_f1": {
      "mean": 0.5938,
      "lower_95": 0.4471,
      "upper_95": 0.7476
    }
  }
}
```