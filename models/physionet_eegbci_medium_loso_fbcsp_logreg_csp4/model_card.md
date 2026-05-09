# Model Card: physionet_eegbci_medium_loso_fbcsp_logreg_csp4

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
  "accuracy": 0.6222222222222222,
  "balanced_accuracy": 0.6160714285714286,
  "macro_f1": 0.6153846153846154,
  "weighted_f1": 0.6188034188034188,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6296296296296297,
      "recall": 0.7083333333333334,
      "f1-score": 0.6666666666666666,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6111111111111112,
      "recall": 0.5238095238095238,
      "f1-score": 0.5641025641025641,
      "support": 21.0
    },
    "accuracy": 0.6222222222222222,
    "macro avg": {
      "precision": 0.6203703703703705,
      "recall": 0.6160714285714286,
      "f1-score": 0.6153846153846154,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.6209876543209876,
      "recall": 0.6222222222222222,
      "f1-score": 0.6188034188034188,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      17,
      7
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
    "ece": 0.1628412772618397,
    "mce": 0.3014440204146649,
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
        "accuracy": 0.625,
        "confidence": 0.5573860413104359
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 9,
        "accuracy": 0.6666666666666666,
        "confidence": 0.6726962122735902
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 7,
        "accuracy": 0.5714285714285714,
        "confidence": 0.7504438116350362
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 13,
        "accuracy": 0.6153846153846154,
        "confidence": 0.8513862347724146
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 8,
        "accuracy": 0.625,
        "confidence": 0.9264440204146649
      }
    ],
    "brier_score": 0.27254893257786333
  },
  "auroc": 0.6091269841269841,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.7766684888031,
    "p95_inference_latency_ms": 7.095409799512709,
    "p99_inference_latency_ms": 7.407639519442456,
    "throughput_samples_per_sec": 147.5651349409038
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.6222222222222222,
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.6153846153846154,
      "weighted_f1": 0.6188034188034188,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6296296296296297,
          "recall": 0.7083333333333334,
          "f1-score": 0.6666666666666666,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6111111111111112,
          "recall": 0.5238095238095238,
          "f1-score": 0.5641025641025641,
          "support": 21.0
        },
        "accuracy": 0.6222222222222222,
        "macro avg": {
          "precision": 0.6203703703703705,
          "recall": 0.6160714285714286,
          "f1-score": 0.6153846153846154,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.6209876543209876,
          "recall": 0.6222222222222222,
          "f1-score": 0.6188034188034188,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          17,
          7
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
      "balanced_accuracy": 0.5357142857142857,
      "macro_f1": 0.5333333333333333,
      "weighted_f1": 0.5333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5,
          "f1-score": 0.5333333333333333,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5714285714285714,
          "f1-score": 0.5333333333333333,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5357142857142857,
          "recall": 0.5357142857142857,
          "f1-score": 0.5333333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5380952380952381,
          "recall": 0.5333333333333333,
          "f1-score": 0.5333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.7857142857142857,
      "macro_f1": 0.784688995215311,
      "weighted_f1": 0.7885167464114832,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7272727272727273,
          "recall": 1.0,
          "f1-score": 0.8421052631578947,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.5714285714285714,
          "f1-score": 0.7272727272727273,
          "support": 7.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.8636363636363636,
          "recall": 0.7857142857142857,
          "f1-score": 0.784688995215311,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8545454545454546,
          "recall": 0.8,
          "f1-score": 0.7885167464114832,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          8,
          0
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.6208,
      "lower_95": 0.4889,
      "upper_95": 0.7556
    },
    "balanced_accuracy": {
      "mean": 0.6142,
      "lower_95": 0.4697,
      "upper_95": 0.7476
    },
    "macro_f1": {
      "mean": 0.6081,
      "lower_95": 0.4643,
      "upper_95": 0.74
    }
  }
}
```