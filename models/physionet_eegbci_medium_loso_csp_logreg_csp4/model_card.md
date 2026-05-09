# Model Card: physionet_eegbci_medium_loso_csp_logreg_csp4

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
  "accuracy": 0.4444444444444444,
  "balanced_accuracy": 0.4494047619047619,
  "macro_f1": 0.44334487877288475,
  "weighted_f1": 0.4416955302655451,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.47368421052631576,
      "recall": 0.375,
      "f1-score": 0.4186046511627907,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4230769230769231,
      "recall": 0.5238095238095238,
      "f1-score": 0.46808510638297873,
      "support": 21.0
    },
    "accuracy": 0.4444444444444444,
    "macro avg": {
      "precision": 0.4483805668016194,
      "recall": 0.4494047619047619,
      "f1-score": 0.44334487877288475,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.45006747638326583,
      "recall": 0.4444444444444444,
      "f1-score": 0.4416955302655451,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      9,
      15
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
    "ece": 0.17509510204114598,
    "mce": 0.8144692372623686,
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
        "confidence": 0.5390517055742853
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 11,
        "accuracy": 0.2727272727272727,
        "confidence": 0.6314977583449779
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 6,
        "accuracy": 0.8333333333333334,
        "confidence": 0.7393435062852097
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.8144692372623686
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.2606793459012462
  },
  "auroc": 0.501984126984127,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3212511556032243,
    "p95_inference_latency_ms": 0.33419360079278704,
    "p99_inference_latency_ms": 0.43463499954668844,
    "throughput_samples_per_sec": 3112.829269430224
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4444444444444444,
      "balanced_accuracy": 0.4494047619047619,
      "macro_f1": 0.44334487877288475,
      "weighted_f1": 0.4416955302655451,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.47368421052631576,
          "recall": 0.375,
          "f1-score": 0.4186046511627907,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4230769230769231,
          "recall": 0.5238095238095238,
          "f1-score": 0.46808510638297873,
          "support": 21.0
        },
        "accuracy": 0.4444444444444444,
        "macro avg": {
          "precision": 0.4483805668016194,
          "recall": 0.4494047619047619,
          "f1-score": 0.44334487877288475,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.45006747638326583,
          "recall": 0.4444444444444444,
          "f1-score": 0.4416955302655451,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          9,
          15
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
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.33035714285714285,
      "macro_f1": 0.33035714285714285,
      "weighted_f1": 0.3333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.375,
          "recall": 0.375,
          "f1-score": 0.375,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2857142857142857,
          "recall": 0.2857142857142857,
          "f1-score": 0.2857142857142857,
          "support": 7.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.33035714285714285,
          "recall": 0.33035714285714285,
          "f1-score": 0.33035714285714285,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3333333333333333,
          "f1-score": 0.3333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5535714285714286,
      "macro_f1": 0.49760765550239233,
      "weighted_f1": 0.4886762360446571,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.25,
          "f1-score": 0.36363636363636365,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8571428571428571,
          "f1-score": 0.631578947368421,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5833333333333333,
          "recall": 0.5535714285714286,
          "f1-score": 0.49760765550239233,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5888888888888888,
          "recall": 0.5333333333333333,
          "f1-score": 0.4886762360446571,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          6
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
      "mean": 0.4483,
      "lower_95": 0.3111,
      "upper_95": 0.6
    },
    "balanced_accuracy": {
      "mean": 0.4532,
      "lower_95": 0.3026,
      "upper_95": 0.6036
    },
    "macro_f1": {
      "mean": 0.4412,
      "lower_95": 0.2946,
      "upper_95": 0.5942
    }
  }
}
```