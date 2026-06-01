# Model Card: channel_ablation_minimal_motor_csp_lda_csp2

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
  "accuracy": 0.6444444444444445,
  "balanced_accuracy": 0.6369047619047619,
  "macro_f1": 0.6356275303643725,
  "weighted_f1": 0.6394062078272604,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6428571428571429,
      "recall": 0.75,
      "f1-score": 0.6923076923076923,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6470588235294118,
      "recall": 0.5238095238095238,
      "f1-score": 0.5789473684210527,
      "support": 21.0
    },
    "accuracy": 0.6444444444444445,
    "macro avg": {
      "precision": 0.6449579831932774,
      "recall": 0.6369047619047619,
      "f1-score": 0.6356275303643725,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.6448179271708684,
      "recall": 0.6444444444444445,
      "f1-score": 0.6394062078272604,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      18,
      6
    ],
    [
      10,
      11
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.0612057263997058,
    "mce": 0.2734520748090489,
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
        "count": 30,
        "accuracy": 0.6,
        "confidence": 0.5445843021824007
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 12,
        "accuracy": 0.6666666666666666,
        "confidence": 0.6440474559140302
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 3,
        "accuracy": 1.0,
        "confidence": 0.7265479251909511
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.22261390405980555
  },
  "auroc": 0.6984126984126984,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.31136466677708086,
    "p95_inference_latency_ms": 0.3410660003282828,
    "p99_inference_latency_ms": 0.42597447929438237,
    "throughput_samples_per_sec": 3211.668203559983
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.6444444444444445,
      "balanced_accuracy": 0.6369047619047619,
      "macro_f1": 0.6356275303643725,
      "weighted_f1": 0.6394062078272604,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6428571428571429,
          "recall": 0.75,
          "f1-score": 0.6923076923076923,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6470588235294118,
          "recall": 0.5238095238095238,
          "f1-score": 0.5789473684210527,
          "support": 21.0
        },
        "accuracy": 0.6444444444444445,
        "macro avg": {
          "precision": 0.6449579831932774,
          "recall": 0.6369047619047619,
          "f1-score": 0.6356275303643725,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.6448179271708684,
          "recall": 0.6444444444444445,
          "f1-score": 0.6394062078272604,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          18,
          6
        ],
        [
          10,
          11
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5267857142857143,
      "macro_f1": 0.5248868778280543,
      "weighted_f1": 0.5291101055806938,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.625,
          "f1-score": 0.5882352941176471,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.42857142857142855,
          "f1-score": 0.46153846153846156,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5277777777777778,
          "recall": 0.5267857142857143,
          "f1-score": 0.5248868778280543,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5296296296296297,
          "recall": 0.5333333333333333,
          "f1-score": 0.5291101055806938,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.5892857142857143,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5888888888888888,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.75,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.42857142857142855,
          "f1-score": 0.5,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6,
          "recall": 0.5892857142857143,
          "f1-score": 0.5833333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.5888888888888888,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.7946428571428572,
      "macro_f1": 0.7963800904977376,
      "weighted_f1": 0.7981900452488688,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7777777777777778,
          "recall": 0.875,
          "f1-score": 0.8235294117647058,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.7142857142857143,
          "f1-score": 0.7692307692307693,
          "support": 7.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.8055555555555556,
          "recall": 0.7946428571428572,
          "f1-score": 0.7963800904977376,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8037037037037038,
          "recall": 0.8,
          "f1-score": 0.7981900452488688,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
      "mean": 0.6488,
      "lower_95": 0.5111,
      "upper_95": 0.8
    },
    "balanced_accuracy": {
      "mean": 0.6414,
      "lower_95": 0.4983,
      "upper_95": 0.7815
    },
    "macro_f1": {
      "mean": 0.6345,
      "lower_95": 0.48,
      "upper_95": 0.7847
    }
  }
}
```