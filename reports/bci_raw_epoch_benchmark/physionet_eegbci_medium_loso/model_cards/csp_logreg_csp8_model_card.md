# Model Card: physionet_eegbci_medium_loso_csp_logreg_csp8

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
  "accuracy": 0.4666666666666667,
  "balanced_accuracy": 0.48214285714285715,
  "macro_f1": 0.4444444444444444,
  "weighted_f1": 0.43703703703703706,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.25,
      "f1-score": 0.3333333333333333,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.45454545454545453,
      "recall": 0.7142857142857143,
      "f1-score": 0.5555555555555556,
      "support": 21.0
    },
    "accuracy": 0.4666666666666667,
    "macro avg": {
      "precision": 0.4772727272727273,
      "recall": 0.48214285714285715,
      "f1-score": 0.4444444444444444,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.4787878787878788,
      "recall": 0.4666666666666667,
      "f1-score": 0.43703703703703706,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      6,
      18
    ],
    [
      6,
      15
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.15773158795253162,
    "mce": 0.26062661425869504,
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
        "count": 24,
        "accuracy": 0.4166666666666667,
        "confidence": 0.5513130973013364
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 13,
        "accuracy": 0.46153846153846156,
        "confidence": 0.647235646109392
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 4,
        "accuracy": 0.5,
        "confidence": 0.760626614258695
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 4,
        "accuracy": 0.75,
        "confidence": 0.8524593165437434
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.2681572041267743
  },
  "auroc": 0.5277777777777777,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.348030199893401,
    "p95_inference_latency_ms": 0.46844420030538453,
    "p99_inference_latency_ms": 0.5581431603786771,
    "throughput_samples_per_sec": 2873.313868469726
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.48214285714285715,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.43703703703703706,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.25,
          "f1-score": 0.3333333333333333,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.7142857142857143,
          "f1-score": 0.5555555555555556,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4772727272727273,
          "recall": 0.48214285714285715,
          "f1-score": 0.4444444444444444,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4787878787878788,
          "recall": 0.4666666666666667,
          "f1-score": 0.43703703703703706,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          6,
          18
        ],
        [
          6,
          15
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.49107142857142855,
      "macro_f1": 0.4,
      "weighted_f1": 0.3866666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.125,
          "f1-score": 0.2,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.8571428571428571,
          "f1-score": 0.6,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4807692307692308,
          "recall": 0.49107142857142855,
          "f1-score": 0.4,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.48205128205128206,
          "recall": 0.4666666666666667,
          "f1-score": 0.3866666666666667,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          1,
          7
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
      "mean": 0.4704,
      "lower_95": 0.3111,
      "upper_95": 0.6222
    },
    "balanced_accuracy": {
      "mean": 0.4855,
      "lower_95": 0.3515,
      "upper_95": 0.6197
    },
    "macro_f1": {
      "mean": 0.4419,
      "lower_95": 0.2897,
      "upper_95": 0.5942
    }
  }
}
```