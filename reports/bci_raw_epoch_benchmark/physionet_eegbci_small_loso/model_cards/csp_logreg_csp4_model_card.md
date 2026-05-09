# Model Card: physionet_eegbci_small_loso_csp_logreg_csp4

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
  "balanced_accuracy": 0.4772727272727273,
  "macro_f1": 0.3181818181818182,
  "weighted_f1": 0.3111111111111111,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.0,
      "recall": 0.0,
      "f1-score": 0.0,
      "support": 23.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4772727272727273,
      "recall": 0.9545454545454546,
      "f1-score": 0.6363636363636364,
      "support": 22.0
    },
    "accuracy": 0.4666666666666667,
    "macro avg": {
      "precision": 0.23863636363636365,
      "recall": 0.4772727272727273,
      "f1-score": 0.3181818181818182,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.23333333333333334,
      "recall": 0.4666666666666667,
      "f1-score": 0.3111111111111111,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      0,
      23
    ],
    [
      1,
      21
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.3124957459962817,
    "mce": 0.9349678588521539,
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
        "confidence": 0.5382324801580706
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 5,
        "accuracy": 0.6,
        "confidence": 0.6769647130173337
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 16,
        "accuracy": 0.5,
        "confidence": 0.7615785797968717
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 19,
        "accuracy": 0.47368421052631576,
        "confidence": 0.8425049773588178
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 2,
        "accuracy": 0.0,
        "confidence": 0.9349678588521539
      }
    ],
    "brier_score": 0.3549659715210422
  },
  "auroc": 0.43478260869565216,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.47826284474770847,
    "p95_inference_latency_ms": 0.9086731988645611,
    "p99_inference_latency_ms": 3.227188439632301,
    "throughput_samples_per_sec": 2090.900455642789
  },
  "per_subject": {
    "S003": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4772727272727273,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.3111111111111111,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4772727272727273,
          "recall": 0.9545454545454546,
          "f1-score": 0.6363636363636364,
          "support": 22.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.23863636363636365,
          "recall": 0.4772727272727273,
          "f1-score": 0.3181818181818182,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.23333333333333334,
          "recall": 0.4666666666666667,
          "f1-score": 0.3111111111111111,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          0,
          23
        ],
        [
          1,
          21
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
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.8571428571428571,
          "f1-score": 0.5714285714285714,
          "support": 7.0
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
          0,
          8
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
      "mean": 0.4696,
      "lower_95": 0.3333,
      "upper_95": 0.6
    },
    "balanced_accuracy": {
      "mean": 0.477,
      "lower_95": 0.425,
      "upper_95": 0.5
    },
    "macro_f1": {
      "mean": 0.3178,
      "lower_95": 0.25,
      "upper_95": 0.375
    }
  }
}
```