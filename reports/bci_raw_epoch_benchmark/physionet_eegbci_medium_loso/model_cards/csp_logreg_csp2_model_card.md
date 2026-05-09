# Model Card: physionet_eegbci_medium_loso_csp_logreg_csp2

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
  "balanced_accuracy": 0.5148809523809523,
  "macro_f1": 0.41492368569813454,
  "weighted_f1": 0.4010552100998681,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6,
      "recall": 0.125,
      "f1-score": 0.20689655172413793,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.475,
      "recall": 0.9047619047619048,
      "f1-score": 0.6229508196721312,
      "support": 21.0
    },
    "accuracy": 0.4888888888888889,
    "macro avg": {
      "precision": 0.5375,
      "recall": 0.5148809523809523,
      "f1-score": 0.41492368569813454,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5416666666666666,
      "recall": 0.4888888888888889,
      "f1-score": 0.4010552100998681,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      3,
      21
    ],
    [
      2,
      19
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.06997093001024508,
    "mce": 0.19399530610939103,
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
        "count": 38,
        "accuracy": 0.5,
        "confidence": 0.547124334413034
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 7,
        "accuracy": 0.42857142857142855,
        "confidence": 0.6225667346808196
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.2565464292323388
  },
  "auroc": 0.5436507936507936,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.2851614889449492,
    "p95_inference_latency_ms": 0.32431799882033374,
    "p99_inference_latency_ms": 0.4307986000640089,
    "throughput_samples_per_sec": 3506.7848877484694
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.5148809523809523,
      "macro_f1": 0.41492368569813454,
      "weighted_f1": 0.4010552100998681,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.125,
          "f1-score": 0.20689655172413793,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.475,
          "recall": 0.9047619047619048,
          "f1-score": 0.6229508196721312,
          "support": 21.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.5375,
          "recall": 0.5148809523809523,
          "f1-score": 0.41492368569813454,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5416666666666666,
          "recall": 0.4888888888888889,
          "f1-score": 0.4010552100998681,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          3,
          21
        ],
        [
          2,
          19
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.4901,
      "lower_95": 0.3556,
      "upper_95": 0.6222
    },
    "balanced_accuracy": {
      "mean": 0.5157,
      "lower_95": 0.435,
      "upper_95": 0.6001
    },
    "macro_f1": {
      "mean": 0.4084,
      "lower_95": 0.2865,
      "upper_95": 0.5503
    }
  }
}
```