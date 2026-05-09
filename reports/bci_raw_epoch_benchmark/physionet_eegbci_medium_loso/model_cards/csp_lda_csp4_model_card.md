# Model Card: physionet_eegbci_medium_loso_csp_lda_csp4

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
  "accuracy": 0.5333333333333333,
  "balanced_accuracy": 0.5297619047619048,
  "macro_f1": 0.5296167247386759,
  "weighted_f1": 0.5324041811846689,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.56,
      "recall": 0.5833333333333334,
      "f1-score": 0.5714285714285714,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.47619047619047616,
      "f1-score": 0.4878048780487805,
      "support": 21.0
    },
    "accuracy": 0.5333333333333333,
    "macro avg": {
      "precision": 0.53,
      "recall": 0.5297619047619048,
      "f1-score": 0.5296167247386759,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.532,
      "recall": 0.5333333333333333,
      "f1-score": 0.5324041811846689,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      14,
      10
    ],
    [
      11,
      10
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.10462269329113022,
    "mce": 0.3032127028785823,
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
        "count": 28,
        "accuracy": 0.5714285714285714,
        "confidence": 0.542685124952242
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 12,
        "accuracy": 0.3333333333333333,
        "confidence": 0.6365460362119156
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 5,
        "accuracy": 0.8,
        "confidence": 0.7470695475558704
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
    "brier_score": 0.25757308925456557
  },
  "auroc": 0.5079365079365079,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.28281806670646703,
    "p95_inference_latency_ms": 0.29916159983258694,
    "p99_inference_latency_ms": 0.3881342797103574,
    "throughput_samples_per_sec": 3535.8420048811317
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5297619047619048,
      "macro_f1": 0.5296167247386759,
      "weighted_f1": 0.5324041811846689,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.5833333333333334,
          "f1-score": 0.5714285714285714,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.47619047619047616,
          "f1-score": 0.4878048780487805,
          "support": 21.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.53,
          "recall": 0.5297619047619048,
          "f1-score": 0.5296167247386759,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.532,
          "recall": 0.5333333333333333,
          "f1-score": 0.5324041811846689,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          14,
          10
        ],
        [
          11,
          10
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.45535714285714285,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.45185185185185184,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.625,
          "f1-score": 0.5555555555555556,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.2857142857142857,
          "f1-score": 0.3333333333333333,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.45,
          "recall": 0.45535714285714285,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.45333333333333337,
          "recall": 0.4666666666666667,
          "f1-score": 0.45185185185185184,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "mean": 0.5388,
      "lower_95": 0.4,
      "upper_95": 0.6889
    },
    "balanced_accuracy": {
      "mean": 0.5356,
      "lower_95": 0.388,
      "upper_95": 0.6875
    },
    "macro_f1": {
      "mean": 0.5295,
      "lower_95": 0.3789,
      "upper_95": 0.685
    }
  }
}
```