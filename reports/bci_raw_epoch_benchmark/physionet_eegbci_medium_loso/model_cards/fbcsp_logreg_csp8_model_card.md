# Model Card: physionet_eegbci_medium_loso_fbcsp_logreg_csp8

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
  "balanced_accuracy": 0.5446428571428572,
  "macro_f1": 0.537037037037037,
  "weighted_f1": 0.5432098765432098,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5666666666666667,
      "recall": 0.7083333333333334,
      "f1-score": 0.6296296296296297,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5333333333333333,
      "recall": 0.38095238095238093,
      "f1-score": 0.4444444444444444,
      "support": 21.0
    },
    "accuracy": 0.5555555555555556,
    "macro avg": {
      "precision": 0.55,
      "recall": 0.5446428571428572,
      "f1-score": 0.537037037037037,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.551111111111111,
      "recall": 0.5555555555555556,
      "f1-score": 0.5432098765432098,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      17,
      7
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
    "ece": 0.2345538915658604,
    "mce": 0.3353835805903618,
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
        "count": 5,
        "accuracy": 0.4,
        "confidence": 0.5398109235548635
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 9,
        "accuracy": 0.4444444444444444,
        "confidence": 0.6688721145181928
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 9,
        "accuracy": 0.5555555555555556,
        "confidence": 0.7559535095720061
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 9,
        "accuracy": 0.6666666666666666,
        "confidence": 0.8524948153558786
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 13,
        "accuracy": 0.6153846153846154,
        "confidence": 0.9507681959749772
      }
    ],
    "brier_score": 0.3069215463164347
  },
  "auroc": 0.5912698412698413,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.004556600036772,
    "p95_inference_latency_ms": 7.524881600329536,
    "p99_inference_latency_ms": 7.697924759559101,
    "throughput_samples_per_sec": 142.7642115126531
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5555555555555556,
      "balanced_accuracy": 0.5446428571428572,
      "macro_f1": 0.537037037037037,
      "weighted_f1": 0.5432098765432098,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5666666666666667,
          "recall": 0.7083333333333334,
          "f1-score": 0.6296296296296297,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 0.38095238095238093,
          "f1-score": 0.4444444444444444,
          "support": 21.0
        },
        "accuracy": 0.5555555555555556,
        "macro avg": {
          "precision": 0.55,
          "recall": 0.5446428571428572,
          "f1-score": 0.537037037037037,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.551111111111111,
          "recall": 0.5555555555555556,
          "f1-score": 0.5432098765432098,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          17,
          7
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.56,
      "lower_95": 0.4,
      "upper_95": 0.7111
    },
    "balanced_accuracy": {
      "mean": 0.5499,
      "lower_95": 0.4047,
      "upper_95": 0.6917
    },
    "macro_f1": {
      "mean": 0.5367,
      "lower_95": 0.3789,
      "upper_95": 0.6881
    }
  }
}
```