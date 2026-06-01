# Model Card: channel_ablation_all_channels_csp_lda_csp2

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
  "balanced_accuracy": 0.48511904761904756,
  "macro_f1": 0.48481831757093086,
  "weighted_f1": 0.48787124605939935,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.52,
      "recall": 0.5416666666666666,
      "f1-score": 0.5306122448979592,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.45,
      "recall": 0.42857142857142855,
      "f1-score": 0.43902439024390244,
      "support": 21.0
    },
    "accuracy": 0.4888888888888889,
    "macro avg": {
      "precision": 0.485,
      "recall": 0.48511904761904756,
      "f1-score": 0.48481831757093086,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.48733333333333334,
      "recall": 0.4888888888888889,
      "f1-score": 0.48787124605939935,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      13,
      11
    ],
    [
      12,
      9
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.13682490542059333,
    "mce": 0.2326698131111652,
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
        "count": 16,
        "accuracy": 0.5,
        "confidence": 0.5420490443348258
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 22,
        "accuracy": 0.45454545454545453,
        "confidence": 0.6401099068722188
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 4,
        "accuracy": 0.5,
        "confidence": 0.7326698131111652
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 3,
        "accuracy": 0.6666666666666666,
        "confidence": 0.8237462769786706
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.26690534953212663
  },
  "auroc": 0.4861111111111111,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.40102195552107234,
    "p95_inference_latency_ms": 0.5169559994101289,
    "p99_inference_latency_ms": 0.5509613598769648,
    "throughput_samples_per_sec": 2493.6290550492154
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.48511904761904756,
      "macro_f1": 0.48481831757093086,
      "weighted_f1": 0.48787124605939935,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.52,
          "recall": 0.5416666666666666,
          "f1-score": 0.5306122448979592,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45,
          "recall": 0.42857142857142855,
          "f1-score": 0.43902439024390244,
          "support": 21.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.485,
          "recall": 0.48511904761904756,
          "f1-score": 0.48481831757093086,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.48733333333333334,
          "recall": 0.4888888888888889,
          "f1-score": 0.48787124605939935,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          13,
          11
        ],
        [
          12,
          9
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4464285714285714,
      "macro_f1": 0.4,
      "weighted_f1": 0.41333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.75,
          "f1-score": 0.6,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.14285714285714285,
          "f1-score": 0.2,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.41666666666666663,
          "recall": 0.4464285714285714,
          "f1-score": 0.4,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.4222222222222222,
          "recall": 0.4666666666666667,
          "f1-score": 0.41333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
        ],
        [
          6,
          1
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6785714285714286,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6576168929110106,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 0.5,
          "f1-score": 0.6153846153846154,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.8571428571428571,
          "f1-score": 0.7058823529411765,
          "support": 7.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.7,
          "recall": 0.6785714285714286,
          "f1-score": 0.660633484162896,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7066666666666668,
          "recall": 0.6666666666666666,
          "f1-score": 0.6576168929110106,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
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
      "mean": 0.492,
      "lower_95": 0.3556,
      "upper_95": 0.6222
    },
    "balanced_accuracy": {
      "mean": 0.4889,
      "lower_95": 0.3443,
      "upper_95": 0.6293
    },
    "macro_f1": {
      "mean": 0.4823,
      "lower_95": 0.3382,
      "upper_95": 0.6215
    }
  }
}
```