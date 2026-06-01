# Model Card: channel_ablation_motor_subset_riemann_ts_logreg_csp6

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
  "accuracy": 0.7111111111111111,
  "balanced_accuracy": 0.6994047619047619,
  "macro_f1": 0.6961038961038961,
  "weighted_f1": 0.7006060606060606,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6774193548387096,
      "recall": 0.875,
      "f1-score": 0.7636363636363637,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.7857142857142857,
      "recall": 0.5238095238095238,
      "f1-score": 0.6285714285714286,
      "support": 21.0
    },
    "accuracy": 0.7111111111111111,
    "macro avg": {
      "precision": 0.7315668202764977,
      "recall": 0.6994047619047619,
      "f1-score": 0.6961038961038961,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.7279569892473118,
      "recall": 0.7111111111111111,
      "f1-score": 0.7006060606060606,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      21,
      3
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
    "ece": 0.0772538174213891,
    "mce": 0.18696200734110413,
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
        "count": 17,
        "accuracy": 0.5294117647058824,
        "confidence": 0.5474032675093529
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 13,
        "accuracy": 0.7692307692307693,
        "confidence": 0.6561421526236739
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 13,
        "accuracy": 0.8461538461538461,
        "confidence": 0.7441161380208412
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 2,
        "accuracy": 1.0,
        "confidence": 0.8130379926588959
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.19248553316059536
  },
  "auroc": 0.7956349206349206,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.9508669331909105,
    "p95_inference_latency_ms": 1.843184599420054,
    "p99_inference_latency_ms": 3.758541200222682,
    "throughput_samples_per_sec": 1051.6718639528342
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.7111111111111111,
      "balanced_accuracy": 0.6994047619047619,
      "macro_f1": 0.6961038961038961,
      "weighted_f1": 0.7006060606060606,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6774193548387096,
          "recall": 0.875,
          "f1-score": 0.7636363636363637,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7857142857142857,
          "recall": 0.5238095238095238,
          "f1-score": 0.6285714285714286,
          "support": 21.0
        },
        "accuracy": 0.7111111111111111,
        "macro avg": {
          "precision": 0.7315668202764977,
          "recall": 0.6994047619047619,
          "f1-score": 0.6961038961038961,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.7279569892473118,
          "recall": 0.7111111111111111,
          "f1-score": 0.7006060606060606,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          21,
          3
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6607142857142857,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6636500754147813,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.75,
          "f1-score": 0.7058823529411765,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5714285714285714,
          "f1-score": 0.6153846153846154,
          "support": 7.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6666666666666666,
          "recall": 0.6607142857142857,
          "f1-score": 0.660633484162896,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6666666666666666,
          "recall": 0.6666666666666666,
          "f1-score": 0.6636500754147813,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
        ],
        [
          3,
          4
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7232142857142857,
      "macro_f1": 0.7222222222222222,
      "weighted_f1": 0.725925925925926,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7,
          "recall": 0.875,
          "f1-score": 0.7777777777777778,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 0.5714285714285714,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.75,
          "recall": 0.7232142857142857,
          "f1-score": 0.7222222222222222,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7466666666666666,
          "recall": 0.7333333333333333,
          "f1-score": 0.725925925925926,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
        ],
        [
          3,
          4
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7142857142857143,
      "macro_f1": 0.7,
      "weighted_f1": 0.7066666666666668,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 1.0,
          "f1-score": 0.8,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.42857142857142855,
          "f1-score": 0.6,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.8333333333333333,
          "recall": 0.7142857142857143,
          "f1-score": 0.7,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8222222222222222,
          "recall": 0.7333333333333333,
          "f1-score": 0.7066666666666668,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          8,
          0
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.7134,
      "lower_95": 0.5661,
      "upper_95": 0.8222
    },
    "balanced_accuracy": {
      "mean": 0.702,
      "lower_95": 0.5715,
      "upper_95": 0.8187
    },
    "macro_f1": {
      "mean": 0.6936,
      "lower_95": 0.5471,
      "upper_95": 0.8207
    }
  }
}
```