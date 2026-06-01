# Model Card: channel_ablation_all_channels_fbcsp_logreg_csp6

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
  "accuracy": 0.5777777777777777,
  "balanced_accuracy": 0.5654761904761905,
  "macro_f1": 0.5558441558441558,
  "weighted_f1": 0.5624242424242424,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5806451612903226,
      "recall": 0.75,
      "f1-score": 0.6545454545454545,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5714285714285714,
      "recall": 0.38095238095238093,
      "f1-score": 0.45714285714285713,
      "support": 21.0
    },
    "accuracy": 0.5777777777777777,
    "macro avg": {
      "precision": 0.5760368663594471,
      "recall": 0.5654761904761905,
      "f1-score": 0.5558441558441558,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5763440860215054,
      "recall": 0.5777777777777777,
      "f1-score": 0.5624242424242424,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      18,
      6
    ],
    [
      13,
      8
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.26028575258525466,
    "mce": 0.45067779763598137,
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
        "count": 7,
        "accuracy": 0.7142857142857143,
        "confidence": 0.5624999580743243
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 7,
        "accuracy": 0.2857142857142857,
        "confidence": 0.6623870554182999
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 5,
        "accuracy": 0.4,
        "confidence": 0.755001982428281
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 14,
        "accuracy": 0.7857142857142857,
        "confidence": 0.8450361215111034
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 12,
        "accuracy": 0.5,
        "confidence": 0.9506777976359814
      }
    ],
    "brier_score": 0.30657856138280837
  },
  "auroc": 0.5734126984126984,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.292701888966096,
    "p95_inference_latency_ms": 7.714384000246355,
    "p99_inference_latency_ms": 7.732954240091203,
    "throughput_samples_per_sec": 137.12338927675162
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5777777777777777,
      "balanced_accuracy": 0.5654761904761905,
      "macro_f1": 0.5558441558441558,
      "weighted_f1": 0.5624242424242424,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5806451612903226,
          "recall": 0.75,
          "f1-score": 0.6545454545454545,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.38095238095238093,
          "f1-score": 0.45714285714285713,
          "support": 21.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5760368663594471,
          "recall": 0.5654761904761905,
          "f1-score": 0.5558441558441558,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5763440860215054,
          "recall": 0.5777777777777777,
          "f1-score": 0.5624242424242424,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          18,
          6
        ],
        [
          13,
          8
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
      "balanced_accuracy": 0.4642857142857143,
      "macro_f1": 0.4642857142857143,
      "weighted_f1": 0.4666666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5,
          "f1-score": 0.5,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.42857142857142855,
          "f1-score": 0.42857142857142855,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4642857142857143,
          "recall": 0.4642857142857143,
          "f1-score": 0.4642857142857143,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.4666666666666667,
          "recall": 0.4666666666666667,
          "f1-score": 0.4666666666666667,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
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
      "balanced_accuracy": 0.5803571428571428,
      "macro_f1": 0.55,
      "weighted_f1": 0.56,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 0.875,
          "f1-score": 0.7,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.2857142857142857,
          "f1-score": 0.4,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.625,
          "recall": 0.5803571428571428,
          "f1-score": 0.55,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6222222222222221,
          "recall": 0.6,
          "f1-score": 0.56,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6517857142857143,
      "macro_f1": 0.6411483253588517,
      "weighted_f1": 0.6475279106858054,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6363636363636364,
          "recall": 0.875,
          "f1-score": 0.7368421052631579,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.42857142857142855,
          "f1-score": 0.5454545454545454,
          "support": 7.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6931818181818181,
          "recall": 0.6517857142857143,
          "f1-score": 0.6411483253588517,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6893939393939393,
          "recall": 0.6666666666666666,
          "f1-score": 0.6475279106858054,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
      "mean": 0.5765,
      "lower_95": 0.4328,
      "upper_95": 0.7111
    },
    "balanced_accuracy": {
      "mean": 0.5644,
      "lower_95": 0.423,
      "upper_95": 0.6985
    },
    "macro_f1": {
      "mean": 0.5488,
      "lower_95": 0.4048,
      "upper_95": 0.6958
    }
  }
}
```