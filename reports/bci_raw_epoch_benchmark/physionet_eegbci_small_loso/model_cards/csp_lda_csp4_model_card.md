# Model Card: physionet_eegbci_small_loso_csp_lda_csp4

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
  "balanced_accuracy": 0.4990118577075099,
  "macro_f1": 0.3630769230769231,
  "weighted_f1": 0.3567863247863248,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.043478260869565216,
      "f1-score": 0.08,
      "support": 23.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4883720930232558,
      "recall": 0.9545454545454546,
      "f1-score": 0.6461538461538462,
      "support": 22.0
    },
    "accuracy": 0.4888888888888889,
    "macro avg": {
      "precision": 0.4941860465116279,
      "recall": 0.4990118577075099,
      "f1-score": 0.3630769230769231,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.4943152454780362,
      "recall": 0.4888888888888889,
      "f1-score": 0.3567863247863248,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      1,
      22
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
    "ece": 0.4578747160533271,
    "mce": 0.6649206733340107,
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
        "count": 2,
        "accuracy": 1.0,
        "confidence": 0.5843005319642443
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 2,
        "accuracy": 0.0,
        "confidence": 0.6649206733340107
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 1,
        "accuracy": 1.0,
        "confidence": 0.7604503793154784
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 9,
        "accuracy": 0.6666666666666666,
        "confidence": 0.8552363294719166
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 31,
        "accuracy": 0.41935483870967744,
        "confidence": 0.951820817862207
      }
    ],
    "brier_score": 0.4392292051366476
  },
  "auroc": 0.450592885375494,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.35255173344113344,
    "p95_inference_latency_ms": 0.4157000010309275,
    "p99_inference_latency_ms": 0.5787134022102692,
    "throughput_samples_per_sec": 2836.463148938035
  },
  "per_subject": {
    "S003": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.4990118577075099,
      "macro_f1": 0.3630769230769231,
      "weighted_f1": 0.3567863247863248,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.043478260869565216,
          "f1-score": 0.08,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4883720930232558,
          "recall": 0.9545454545454546,
          "f1-score": 0.6461538461538462,
          "support": 22.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.4941860465116279,
          "recall": 0.4990118577075099,
          "f1-score": 0.3630769230769231,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4943152454780362,
          "recall": 0.4888888888888889,
          "f1-score": 0.3567863247863248,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          1,
          22
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
      "mean": 0.491,
      "lower_95": 0.3333,
      "upper_95": 0.6222
    },
    "balanced_accuracy": {
      "mean": 0.498,
      "lower_95": 0.4353,
      "upper_95": 0.5514
    },
    "macro_f1": {
      "mean": 0.36,
      "lower_95": 0.2672,
      "upper_95": 0.472
    }
  }
}
```