# Model Card: channel_ablation_all_channels_fbcsp_logreg_csp4

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
  "accuracy": 0.6444444444444445,
  "balanced_accuracy": 0.6398809523809523,
  "macro_f1": 0.64,
  "weighted_f1": 0.6426666666666667,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6538461538461539,
      "recall": 0.7083333333333334,
      "f1-score": 0.68,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.631578947368421,
      "recall": 0.5714285714285714,
      "f1-score": 0.6,
      "support": 21.0
    },
    "accuracy": 0.6444444444444445,
    "macro avg": {
      "precision": 0.6427125506072875,
      "recall": 0.6398809523809523,
      "f1-score": 0.64,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.6434547908232119,
      "recall": 0.6444444444444445,
      "f1-score": 0.6426666666666667,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      17,
      7
    ],
    [
      9,
      12
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.2392255253324061,
    "mce": 0.3559683041030962,
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
        "count": 10,
        "accuracy": 0.8,
        "confidence": 0.5413381373888667
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 7,
        "accuracy": 0.7142857142857143,
        "confidence": 0.6671899510959722
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 7,
        "accuracy": 0.5714285714285714,
        "confidence": 0.7644682004702678
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 14,
        "accuracy": 0.5,
        "confidence": 0.8559683041030962
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 7,
        "accuracy": 0.7142857142857143,
        "confidence": 0.9305751443976467
      }
    ],
    "brier_score": 0.28308200418597773
  },
  "auroc": 0.5992063492063492,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.855742422137862,
    "p95_inference_latency_ms": 7.527864399526152,
    "p99_inference_latency_ms": 7.752601719985251,
    "throughput_samples_per_sec": 145.8631229742387
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.6444444444444445,
      "balanced_accuracy": 0.6398809523809523,
      "macro_f1": 0.64,
      "weighted_f1": 0.6426666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6538461538461539,
          "recall": 0.7083333333333334,
          "f1-score": 0.68,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.631578947368421,
          "recall": 0.5714285714285714,
          "f1-score": 0.6,
          "support": 21.0
        },
        "accuracy": 0.6444444444444445,
        "macro avg": {
          "precision": 0.6427125506072875,
          "recall": 0.6398809523809523,
          "f1-score": 0.64,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.6434547908232119,
          "recall": 0.6444444444444445,
          "f1-score": 0.6426666666666667,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          17,
          7
        ],
        [
          9,
          12
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
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.8571428571428572,
      "macro_f1": 0.8611111111111112,
      "weighted_f1": 0.8629629629629629,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 1.0,
          "f1-score": 0.8888888888888888,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.7142857142857143,
          "f1-score": 0.8333333333333334,
          "support": 7.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.9,
          "recall": 0.8571428571428572,
          "f1-score": 0.8611111111111112,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8933333333333333,
          "recall": 0.8666666666666667,
          "f1-score": 0.8629629629629629,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          8,
          0
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.6414,
      "lower_95": 0.5111,
      "upper_95": 0.7778
    },
    "balanced_accuracy": {
      "mean": 0.6363,
      "lower_95": 0.4995,
      "upper_95": 0.7752
    },
    "macro_f1": {
      "mean": 0.6311,
      "lower_95": 0.4879,
      "upper_95": 0.7737
    }
  }
}
```