# Model Card: channel_ablation_motor_subset_csp_lda_csp2

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
  "accuracy": 0.5555555555555556,
  "balanced_accuracy": 0.5595238095238095,
  "macro_f1": 0.5553359683794465,
  "weighted_f1": 0.5546772068511198,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6,
      "recall": 0.5,
      "f1-score": 0.5454545454545454,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.52,
      "recall": 0.6190476190476191,
      "f1-score": 0.5652173913043478,
      "support": 21.0
    },
    "accuracy": 0.5555555555555556,
    "macro avg": {
      "precision": 0.56,
      "recall": 0.5595238095238095,
      "f1-score": 0.5553359683794465,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5626666666666666,
      "recall": 0.5555555555555556,
      "f1-score": 0.5546772068511198,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      12,
      12
    ],
    [
      8,
      13
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.09099163084200151,
    "mce": 0.2681445620771786,
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
        "count": 27,
        "accuracy": 0.4444444444444444,
        "confidence": 0.5532357696525475
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 14,
        "accuracy": 0.6428571428571429,
        "confidence": 0.6368086172169594
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 4,
        "accuracy": 1.0,
        "confidence": 0.7318554379228214
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
    "brier_score": 0.23022149391600225
  },
  "auroc": 0.6507936507936508,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3155955112257895,
    "p95_inference_latency_ms": 0.3832504004094515,
    "p99_inference_latency_ms": 0.4446582397213208,
    "throughput_samples_per_sec": 3168.612874485913
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5555555555555556,
      "balanced_accuracy": 0.5595238095238095,
      "macro_f1": 0.5553359683794465,
      "weighted_f1": 0.5546772068511198,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.5,
          "f1-score": 0.5454545454545454,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.52,
          "recall": 0.6190476190476191,
          "f1-score": 0.5652173913043478,
          "support": 21.0
        },
        "accuracy": 0.5555555555555556,
        "macro avg": {
          "precision": 0.56,
          "recall": 0.5595238095238095,
          "f1-score": 0.5553359683794465,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5626666666666666,
          "recall": 0.5555555555555556,
          "f1-score": 0.5546772068511198,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          12,
          12
        ],
        [
          8,
          13
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
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3392857142857143,
      "macro_f1": 0.33035714285714285,
      "weighted_f1": 0.3273809523809524,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.25,
          "f1-score": 0.2857142857142857,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.42857142857142855,
          "f1-score": 0.375,
          "support": 7.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3392857142857143,
          "f1-score": 0.33035714285714285,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3333333333333333,
          "f1-score": 0.3273809523809524,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          6
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
      "balanced_accuracy": 0.5982142857142857,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.6,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.625,
          "f1-score": 0.625,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5714285714285714,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5982142857142857,
          "recall": 0.5982142857142857,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.6,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "balanced_accuracy": 0.7410714285714286,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.730952380952381,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.625,
          "f1-score": 0.7142857142857143,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.8571428571428571,
          "f1-score": 0.75,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.75,
          "recall": 0.7410714285714286,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7555555555555554,
          "recall": 0.7333333333333333,
          "f1-score": 0.730952380952381,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "mean": 0.5582,
      "lower_95": 0.4,
      "upper_95": 0.7111
    },
    "balanced_accuracy": {
      "mean": 0.5625,
      "lower_95": 0.4048,
      "upper_95": 0.7137
    },
    "macro_f1": {
      "mean": 0.5522,
      "lower_95": 0.3966,
      "upper_95": 0.7059
    }
  }
}
```