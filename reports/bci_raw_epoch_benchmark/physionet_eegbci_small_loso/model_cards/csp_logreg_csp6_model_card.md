# Model Card: physionet_eegbci_small_loso_csp_logreg_csp6

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
  "accuracy": 0.4888888888888889,
  "balanced_accuracy": 0.5,
  "macro_f1": 0.3283582089552239,
  "weighted_f1": 0.32106135986733003,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.0,
      "recall": 0.0,
      "f1-score": 0.0,
      "support": 23.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4888888888888889,
      "recall": 1.0,
      "f1-score": 0.6567164179104478,
      "support": 22.0
    },
    "accuracy": 0.4888888888888889,
    "macro avg": {
      "precision": 0.24444444444444444,
      "recall": 0.5,
      "f1-score": 0.3283582089552239,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.23901234567901233,
      "recall": 0.4888888888888889,
      "f1-score": 0.32106135986733003,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      0,
      23
    ],
    [
      0,
      22
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.298316277636714,
    "mce": 0.5901021255023402,
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
        "accuracy": 0.3333333333333333,
        "confidence": 0.5430209283340254
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 6,
        "accuracy": 0.5,
        "confidence": 0.6606745394842247
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 14,
        "accuracy": 0.7142857142857143,
        "confidence": 0.7489197361472747
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 13,
        "accuracy": 0.38461538461538464,
        "confidence": 0.8488713104739843
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 9,
        "accuracy": 0.3333333333333333,
        "confidence": 0.9234354588356735
      }
    ],
    "brier_score": 0.3724517106728865
  },
  "auroc": 0.36363636363636365,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.4380973997791039,
    "p95_inference_latency_ms": 0.558568598353304,
    "p99_inference_latency_ms": 0.6027699222613592,
    "throughput_samples_per_sec": 2282.5974326809906
  },
  "per_subject": {
    "S003": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3283582089552239,
      "weighted_f1": 0.32106135986733003,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4888888888888889,
          "recall": 1.0,
          "f1-score": 0.6567164179104478,
          "support": 22.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.24444444444444444,
          "recall": 0.5,
          "f1-score": 0.3283582089552239,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.23901234567901233,
          "recall": 0.4888888888888889,
          "f1-score": 0.32106135986733003,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          0,
          23
        ],
        [
          0,
          22
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
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.29696969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 1.0,
          "f1-score": 0.6363636363636364,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.23333333333333334,
          "recall": 0.5,
          "f1-score": 0.3181818181818182,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.21777777777777776,
          "recall": 0.4666666666666667,
          "f1-score": 0.29696969696969694,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          8
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
    },
    "4": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.29696969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 1.0,
          "f1-score": 0.6363636363636364,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.23333333333333334,
          "recall": 0.5,
          "f1-score": 0.3181818181818182,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.21777777777777776,
          "recall": 0.4666666666666667,
          "f1-score": 0.29696969696969694,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          8
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
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.34782608695652173,
      "weighted_f1": 0.3710144927536232,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 1.0,
          "f1-score": 0.6956521739130435,
          "support": 8.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.26666666666666666,
          "recall": 0.5,
          "f1-score": 0.34782608695652173,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.28444444444444444,
          "recall": 0.5333333333333333,
          "f1-score": 0.3710144927536232,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7
        ],
        [
          0,
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.4922,
      "lower_95": 0.3439,
      "upper_95": 0.6222
    },
    "balanced_accuracy": {
      "mean": 0.5,
      "lower_95": 0.5,
      "upper_95": 0.5
    },
    "macro_f1": {
      "mean": 0.3282,
      "lower_95": 0.2558,
      "upper_95": 0.3836
    }
  }
}
```