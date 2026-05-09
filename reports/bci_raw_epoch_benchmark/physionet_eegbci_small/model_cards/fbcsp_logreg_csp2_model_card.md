# Model Card: physionet_eegbci_small_fbcsp_logreg_csp2

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
  "accuracy": 0.48333333333333334,
  "balanced_accuracy": 0.482202447163515,
  "macro_f1": 0.48203842940685043,
  "weighted_f1": 0.4829016986911724,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.5161290322580645,
      "f1-score": 0.5079365079365079,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4642857142857143,
      "recall": 0.4482758620689655,
      "f1-score": 0.45614035087719296,
      "support": 29.0
    },
    "accuracy": 0.48333333333333334,
    "macro avg": {
      "precision": 0.48214285714285715,
      "recall": 0.482202447163515,
      "f1-score": 0.48203842940685043,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.48273809523809524,
      "recall": 0.48333333333333334,
      "f1-score": 0.4829016986911724,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      16,
      15
    ],
    [
      16,
      13
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.27862053384211494,
    "mce": 0.5012971991241748,
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
        "count": 13,
        "accuracy": 0.46153846153846156,
        "confidence": 0.5489490197194473
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 8,
        "accuracy": 0.625,
        "confidence": 0.6532448731745959
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 11,
        "accuracy": 0.5454545454545454,
        "confidence": 0.7547419444933372
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 17,
        "accuracy": 0.4117647058823529,
        "confidence": 0.8552061887638048
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 11,
        "accuracy": 0.45454545454545453,
        "confidence": 0.9558426536696293
      }
    ],
    "brier_score": 0.35667412324750825
  },
  "auroc": 0.45494994438264735,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.750768216564514,
    "p95_inference_latency_ms": 6.912295648908184,
    "p99_inference_latency_ms": 7.01072157073213,
    "throughput_samples_per_sec": 148.1312893466372
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.4333333333333333,
      "macro_f1": 0.3772893772893773,
      "weighted_f1": 0.3772893772893772,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4583333333333333,
          "recall": 0.7333333333333333,
          "f1-score": 0.5641025641025641,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.13333333333333333,
          "f1-score": 0.19047619047619047,
          "support": 15.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.3958333333333333,
          "recall": 0.4333333333333333,
          "f1-score": 0.3772893772893773,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.3958333333333333,
          "recall": 0.43333333333333335,
          "f1-score": 0.3772893772893772,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          4
        ],
        [
          13,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4732142857142857,
      "macro_f1": 0.4642857142857143,
      "weighted_f1": 0.46190476190476193,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.375,
          "f1-score": 0.42857142857142855,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5714285714285714,
          "f1-score": 0.5,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4722222222222222,
          "recall": 0.4732142857142857,
          "f1-score": 0.4642857142857143,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.47407407407407404,
          "recall": 0.4666666666666667,
          "f1-score": 0.46190476190476193,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
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
    "S003": {
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
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.42857142857142855,
      "macro_f1": 0.2857142857142857,
      "weighted_f1": 0.26666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.8571428571428571,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
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
          6,
          1
        ],
        [
          8,
          0
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
      "balanced_accuracy": 0.5401785714285714,
      "macro_f1": 0.53125,
      "weighted_f1": 0.5291666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 0.4375,
          "f1-score": 0.5,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6428571428571429,
          "f1-score": 0.5625,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5416666666666667,
          "recall": 0.5401785714285714,
          "f1-score": 0.53125,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5444444444444445,
          "recall": 0.5333333333333333,
          "f1-score": 0.5291666666666667,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          9
        ],
        [
          5,
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
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4732142857142857,
      "macro_f1": 0.4642857142857143,
      "weighted_f1": 0.46190476190476193,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.375,
          "f1-score": 0.42857142857142855,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5714285714285714,
          "f1-score": 0.5,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4722222222222222,
          "recall": 0.4732142857142857,
          "f1-score": 0.4642857142857143,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.47407407407407404,
          "recall": 0.4666666666666667,
          "f1-score": 0.46190476190476193,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
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
      "mean": 0.4792,
      "lower_95": 0.35,
      "upper_95": 0.6167
    },
    "balanced_accuracy": {
      "mean": 0.4781,
      "lower_95": 0.3387,
      "upper_95": 0.6094
    },
    "macro_f1": {
      "mean": 0.4736,
      "lower_95": 0.3366,
      "upper_95": 0.6078
    }
  }
}
```