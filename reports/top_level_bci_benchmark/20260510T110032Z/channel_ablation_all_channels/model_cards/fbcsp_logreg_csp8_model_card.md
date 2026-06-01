# Model Card: channel_ablation_all_channels_fbcsp_logreg_csp8

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
  "balanced_accuracy": 0.5684523809523809,
  "macro_f1": 0.5639979602243753,
  "weighted_f1": 0.5691653918069013,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5862068965517241,
      "recall": 0.7083333333333334,
      "f1-score": 0.6415094339622641,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5625,
      "recall": 0.42857142857142855,
      "f1-score": 0.4864864864864865,
      "support": 21.0
    },
    "accuracy": 0.5777777777777777,
    "macro avg": {
      "precision": 0.5743534482758621,
      "recall": 0.5684523809523809,
      "f1-score": 0.5639979602243753,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5751436781609195,
      "recall": 0.5777777777777777,
      "f1-score": 0.5691653918069013,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      17,
      7
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
    "ece": 0.1934974095040524,
    "mce": 0.36814562097185466,
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
        "count": 8,
        "accuracy": 0.5,
        "confidence": 0.5461087493057761
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 6,
        "accuracy": 0.5,
        "confidence": 0.6555554826540965
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 12,
        "accuracy": 0.5833333333333334,
        "confidence": 0.7494519600013763
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 7,
        "accuracy": 0.7142857142857143,
        "confidence": 0.8562870808046856
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 12,
        "accuracy": 0.5833333333333334,
        "confidence": 0.951478954305188
      }
    ],
    "brier_score": 0.2915031964332571
  },
  "auroc": 0.5952380952380952,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.679793488870524,
    "p95_inference_latency_ms": 7.0203501998548745,
    "p99_inference_latency_ms": 7.139143439562758,
    "throughput_samples_per_sec": 149.70522691549382
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5777777777777777,
      "balanced_accuracy": 0.5684523809523809,
      "macro_f1": 0.5639979602243753,
      "weighted_f1": 0.5691653918069013,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5862068965517241,
          "recall": 0.7083333333333334,
          "f1-score": 0.6415094339622641,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5625,
          "recall": 0.42857142857142855,
          "f1-score": 0.4864864864864865,
          "support": 21.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5743534482758621,
          "recall": 0.5684523809523809,
          "f1-score": 0.5639979602243753,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5751436781609195,
          "recall": 0.5777777777777777,
          "f1-score": 0.5691653918069013,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          17,
          7
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
      "mean": 0.5806,
      "lower_95": 0.4222,
      "upper_95": 0.7111
    },
    "balanced_accuracy": {
      "mean": 0.5719,
      "lower_95": 0.4321,
      "upper_95": 0.7077
    },
    "macro_f1": {
      "mean": 0.5616,
      "lower_95": 0.4081,
      "upper_95": 0.7059
    }
  }
}
```