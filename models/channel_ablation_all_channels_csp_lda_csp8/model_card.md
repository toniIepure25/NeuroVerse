# Model Card: channel_ablation_all_channels_csp_lda_csp8

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
  "accuracy": 0.4222222222222222,
  "balanced_accuracy": 0.4226190476190476,
  "macro_f1": 0.42193675889328064,
  "weighted_f1": 0.4227931488801054,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.45454545454545453,
      "recall": 0.4166666666666667,
      "f1-score": 0.43478260869565216,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.391304347826087,
      "recall": 0.42857142857142855,
      "f1-score": 0.4090909090909091,
      "support": 21.0
    },
    "accuracy": 0.4222222222222222,
    "macro avg": {
      "precision": 0.42292490118577075,
      "recall": 0.4226190476190476,
      "f1-score": 0.42193675889328064,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.42503293807641634,
      "recall": 0.4222222222222222,
      "f1-score": 0.4227931488801054,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      10,
      14
    ],
    [
      12,
      9
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.20338234540219097,
    "mce": 0.28626234584033766,
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
        "count": 18,
        "accuracy": 0.3888888888888889,
        "confidence": 0.5422444052683587
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 17,
        "accuracy": 0.35294117647058826,
        "confidence": 0.6392035223109259
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 7,
        "accuracy": 0.5714285714285714,
        "confidence": 0.7235009813994557
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 3,
        "accuracy": 0.6666666666666666,
        "confidence": 0.8202798330620688
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.28082461779703605
  },
  "auroc": 0.45833333333333326,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.33057313337647226,
    "p95_inference_latency_ms": 0.4859049997321562,
    "p99_inference_latency_ms": 0.7167014801234481,
    "throughput_samples_per_sec": 3025.0492221978393
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4222222222222222,
      "balanced_accuracy": 0.4226190476190476,
      "macro_f1": 0.42193675889328064,
      "weighted_f1": 0.4227931488801054,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.4166666666666667,
          "f1-score": 0.43478260869565216,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.391304347826087,
          "recall": 0.42857142857142855,
          "f1-score": 0.4090909090909091,
          "support": 21.0
        },
        "accuracy": 0.4222222222222222,
        "macro avg": {
          "precision": 0.42292490118577075,
          "recall": 0.4226190476190476,
          "f1-score": 0.42193675889328064,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.42503293807641634,
          "recall": 0.4222222222222222,
          "f1-score": 0.4227931488801054,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          10,
          14
        ],
        [
          12,
          9
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
      "balanced_accuracy": 0.4017857142857143,
      "macro_f1": 0.4,
      "weighted_f1": 0.4,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.375,
          "f1-score": 0.4,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.375,
          "recall": 0.42857142857142855,
          "f1-score": 0.4,
          "support": 7.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.4017857142857143,
          "recall": 0.4017857142857143,
          "f1-score": 0.4,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.4035714285714286,
          "recall": 0.4,
          "f1-score": 0.4,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
        ],
        [
          4,
          3
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
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3214285714285714,
      "macro_f1": 0.3055555555555555,
      "weighted_f1": 0.31481481481481477,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.5,
          "f1-score": 0.4444444444444444,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2,
          "recall": 0.14285714285714285,
          "f1-score": 0.16666666666666666,
          "support": 7.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.30000000000000004,
          "recall": 0.3214285714285714,
          "f1-score": 0.3055555555555555,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3066666666666667,
          "recall": 0.3333333333333333,
          "f1-score": 0.31481481481481477,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
        ],
        [
          6,
          1
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5446428571428572,
      "macro_f1": 0.5248868778280543,
      "weighted_f1": 0.5206636500754148,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.375,
          "f1-score": 0.46153846153846156,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.7142857142857143,
          "f1-score": 0.5882352941176471,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.55,
          "recall": 0.5446428571428572,
          "f1-score": 0.5248868778280543,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5533333333333333,
          "recall": 0.5333333333333333,
          "f1-score": 0.5206636500754148,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
        ],
        [
          2,
          5
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
      "mean": 0.425,
      "lower_95": 0.2772,
      "upper_95": 0.5778
    },
    "balanced_accuracy": {
      "mean": 0.4256,
      "lower_95": 0.2801,
      "upper_95": 0.5722
    },
    "macro_f1": {
      "mean": 0.4192,
      "lower_95": 0.2681,
      "upper_95": 0.5556
    }
  }
}
```