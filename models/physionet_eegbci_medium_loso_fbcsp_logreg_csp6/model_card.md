# Model Card: physionet_eegbci_medium_loso_fbcsp_logreg_csp6

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
  "balanced_accuracy": 0.5625,
  "macro_f1": 0.5454545454545454,
  "weighted_f1": 0.5535353535353535,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5757575757575758,
      "recall": 0.7916666666666666,
      "f1-score": 0.6666666666666666,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5833333333333334,
      "recall": 0.3333333333333333,
      "f1-score": 0.42424242424242425,
      "support": 21.0
    },
    "accuracy": 0.5777777777777777,
    "macro avg": {
      "precision": 0.5795454545454546,
      "recall": 0.5625,
      "f1-score": 0.5454545454545454,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5792929292929293,
      "recall": 0.5777777777777777,
      "f1-score": 0.5535353535353535,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      19,
      5
    ],
    [
      14,
      7
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.24239734720967523,
    "mce": 0.3761059946847567,
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
        "count": 3,
        "accuracy": 0.6666666666666666,
        "confidence": 0.5479437130536041
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 8,
        "accuracy": 0.625,
        "confidence": 0.6361389588091937
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 8,
        "accuracy": 0.375,
        "confidence": 0.7511059946847567
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 11,
        "accuracy": 0.5454545454545454,
        "confidence": 0.8494434793706876
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 15,
        "accuracy": 0.6666666666666666,
        "confidence": 0.9406582575044686
      }
    ],
    "brier_score": 0.3090549095651238
  },
  "auroc": 0.5833333333333333,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.969916488742456,
    "p95_inference_latency_ms": 7.350877800854505,
    "p99_inference_latency_ms": 8.407477359287444,
    "throughput_samples_per_sec": 143.4737419903326
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5777777777777777,
      "balanced_accuracy": 0.5625,
      "macro_f1": 0.5454545454545454,
      "weighted_f1": 0.5535353535353535,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5757575757575758,
          "recall": 0.7916666666666666,
          "f1-score": 0.6666666666666666,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 0.3333333333333333,
          "f1-score": 0.42424242424242425,
          "support": 21.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5795454545454546,
          "recall": 0.5625,
          "f1-score": 0.5454545454545454,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5792929292929293,
          "recall": 0.5777777777777777,
          "f1-score": 0.5535353535353535,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          19,
          5
        ],
        [
          14,
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
      "mean": 0.5758,
      "lower_95": 0.4444,
      "upper_95": 0.7111
    },
    "balanced_accuracy": {
      "mean": 0.5606,
      "lower_95": 0.435,
      "upper_95": 0.6841
    },
    "macro_f1": {
      "mean": 0.5372,
      "lower_95": 0.3849,
      "upper_95": 0.6759
    }
  }
}
```