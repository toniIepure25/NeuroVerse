# Model Card: physionet_eegbci_medium_loso_csp_logreg_csp6

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
  "balanced_accuracy": 0.5535714285714286,
  "macro_f1": 0.49760765550239233,
  "weighted_f1": 0.4886762360446571,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6666666666666666,
      "recall": 0.25,
      "f1-score": 0.36363636363636365,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.8571428571428571,
      "f1-score": 0.631578947368421,
      "support": 21.0
    },
    "accuracy": 0.5333333333333333,
    "macro avg": {
      "precision": 0.5833333333333333,
      "recall": 0.5535714285714286,
      "f1-score": 0.49760765550239233,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5888888888888889,
      "recall": 0.5333333333333333,
      "f1-score": 0.4886762360446571,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      6,
      18
    ],
    [
      3,
      18
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.11165800220982568,
    "mce": 0.5809156612352212,
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
        "count": 23,
        "accuracy": 0.5652173913043478,
        "confidence": 0.5552076187717986
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 11,
        "accuracy": 0.5454545454545454,
        "confidence": 0.6377089751011016
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 6,
        "accuracy": 0.16666666666666666,
        "confidence": 0.7475823279018878
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 5,
        "accuracy": 0.8,
        "confidence": 0.8588185275340159
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.27107082134579163
  },
  "auroc": 0.5456349206349207,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.410155333277847,
    "p95_inference_latency_ms": 0.5359388007491361,
    "p99_inference_latency_ms": 0.5432694801856996,
    "throughput_samples_per_sec": 2438.100687386603
  },
  "per_subject": {
    "S010": {
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
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8571428571428571,
          "f1-score": 0.631578947368421,
          "support": 21.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5833333333333333,
          "recall": 0.5535714285714286,
          "f1-score": 0.49760765550239233,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5888888888888889,
          "recall": 0.5333333333333333,
          "f1-score": 0.4886762360446571,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          6,
          18
        ],
        [
          3,
          18
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
      "balanced_accuracy": 0.5446428571428572,
      "macro_f1": 0.5248868778280543,
      "weighted_f1": 0.5206636500754148,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.375,
          "f1-score": 0.46153846153846156,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.7142857142857143,
          "f1-score": 0.5882352941176471,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.55,
          "recall": 0.5446428571428572,
          "f1-score": 0.5248868778280543,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5533333333333333,
          "recall": 0.5333333333333333,
          "f1-score": 0.5206636500754148,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
        ],
        [
          2,
          5
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.625,
      "macro_f1": 0.55,
      "weighted_f1": 0.5399999999999999,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.25,
          "f1-score": 0.4,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 1.0,
          "f1-score": 0.7,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.7692307692307692,
          "recall": 0.625,
          "f1-score": 0.55,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7846153846153847,
          "recall": 0.6,
          "f1-score": 0.5399999999999999,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          6
        ],
        [
          0,
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5368,
      "lower_95": 0.3778,
      "upper_95": 0.6889
    },
    "balanced_accuracy": {
      "mean": 0.5564,
      "lower_95": 0.4351,
      "upper_95": 0.6759
    },
    "macro_f1": {
      "mean": 0.4945,
      "lower_95": 0.3458,
      "upper_95": 0.65
    }
  }
}
```