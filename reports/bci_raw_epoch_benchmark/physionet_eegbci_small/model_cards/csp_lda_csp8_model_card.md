# Model Card: physionet_eegbci_small_csp_lda_csp8

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
  "accuracy": 0.5833333333333334,
  "balanced_accuracy": 0.5734149054505006,
  "macro_f1": 0.5368941031182464,
  "weighted_f1": 0.5417824431408871,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5625,
      "recall": 0.8709677419354839,
      "f1-score": 0.6835443037974683,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6666666666666666,
      "recall": 0.27586206896551724,
      "f1-score": 0.3902439024390244,
      "support": 29.0
    },
    "accuracy": 0.5833333333333334,
    "macro avg": {
      "precision": 0.6145833333333333,
      "recall": 0.5734149054505006,
      "f1-score": 0.5368941031182464,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.6128472222222221,
      "recall": 0.5833333333333334,
      "f1-score": 0.5417824431408871,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      27,
      4
    ],
    [
      21,
      8
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.21183670296752238,
    "mce": 0.2720793854728075,
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
        "count": 9,
        "accuracy": 0.4444444444444444,
        "confidence": 0.5248516147145283
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 8,
        "accuracy": 0.5,
        "confidence": 0.6528769914462939
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 8,
        "accuracy": 0.5,
        "confidence": 0.7605112789782701
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 17,
        "accuracy": 0.5882352941176471,
        "confidence": 0.8603146795904546
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 18,
        "accuracy": 0.7222222222222222,
        "confidence": 0.9474489960659083
      }
    ],
    "brier_score": 0.27630210101451397
  },
  "auroc": 0.6384872080088988,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.5698005998662362,
    "p95_inference_latency_ms": 2.613890848442677,
    "p99_inference_latency_ms": 3.6976138797399445,
    "throughput_samples_per_sec": 1754.9999073970007
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.43333333333333335,
      "macro_f1": 0.3453145057766367,
      "weighted_f1": 0.3453145057766367,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.8,
          "f1-score": 0.5853658536585366,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.06666666666666667,
          "f1-score": 0.10526315789473684,
          "support": 15.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.3557692307692308,
          "recall": 0.43333333333333335,
          "f1-score": 0.3453145057766367,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.3557692307692308,
          "recall": 0.43333333333333335,
          "f1-score": 0.3453145057766367,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          12,
          3
        ],
        [
          14,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.8660714285714286,
      "macro_f1": 0.8660714285714286,
      "weighted_f1": 0.8666666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.875,
          "recall": 0.875,
          "f1-score": 0.875,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8571428571428571,
          "recall": 0.8571428571428571,
          "f1-score": 0.8571428571428571,
          "support": 7.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.8660714285714286,
          "recall": 0.8660714285714286,
          "f1-score": 0.8660714285714286,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8666666666666667,
          "recall": 0.8666666666666667,
          "f1-score": 0.8666666666666667,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
    },
    "S003": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5714285714285714,
      "macro_f1": 0.48863636363636365,
      "weighted_f1": 0.5045454545454545,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 1.0,
          "f1-score": 0.7272727272727273,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.14285714285714285,
          "f1-score": 0.25,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.7857142857142857,
          "recall": 0.5714285714285714,
          "f1-score": 0.48863636363636365,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7714285714285715,
          "recall": 0.6,
          "f1-score": 0.5045454545454545,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          8,
          0
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.42857142857142855,
      "macro_f1": 0.2857142857142857,
      "weighted_f1": 0.26666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.8571428571428571,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.21428571428571427,
          "recall": 0.42857142857142855,
          "f1-score": 0.2857142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.2,
          "recall": 0.4,
          "f1-score": 0.26666666666666666,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
        ],
        [
          8,
          0
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5089285714285714,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4592592592592592,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.875,
          "f1-score": 0.6666666666666666,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.14285714285714285,
          "f1-score": 0.2222222222222222,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5192307692307692,
          "recall": 0.5089285714285714,
          "f1-score": 0.4444444444444444,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5205128205128206,
          "recall": 0.5333333333333333,
          "f1-score": 0.4592592592592592,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          2
        ],
        [
          12,
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
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.8660714285714286,
      "macro_f1": 0.8660714285714286,
      "weighted_f1": 0.8666666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.875,
          "recall": 0.875,
          "f1-score": 0.875,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8571428571428571,
          "recall": 0.8571428571428571,
          "f1-score": 0.8571428571428571,
          "support": 7.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.8660714285714286,
          "recall": 0.8660714285714286,
          "f1-score": 0.8660714285714286,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8666666666666667,
          "recall": 0.8666666666666667,
          "f1-score": 0.8666666666666667,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
      "mean": 0.583,
      "lower_95": 0.45,
      "upper_95": 0.7087
    },
    "balanced_accuracy": {
      "mean": 0.5718,
      "lower_95": 0.4722,
      "upper_95": 0.6777
    },
    "macro_f1": {
      "mean": 0.5323,
      "lower_95": 0.4033,
      "upper_95": 0.6652
    }
  }
}
```