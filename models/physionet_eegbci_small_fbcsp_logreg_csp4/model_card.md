# Model Card: physionet_eegbci_small_fbcsp_logreg_csp4

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
  "accuracy": 0.4,
  "balanced_accuracy": 0.40155728587319245,
  "macro_f1": 0.3993325917686318,
  "weighted_f1": 0.39866518353726366,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.4074074074074074,
      "recall": 0.3548387096774194,
      "f1-score": 0.3793103448275862,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.3939393939393939,
      "recall": 0.4482758620689655,
      "f1-score": 0.41935483870967744,
      "support": 29.0
    },
    "accuracy": 0.4,
    "macro avg": {
      "precision": 0.4006734006734006,
      "recall": 0.40155728587319245,
      "f1-score": 0.3993325917686318,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.40089786756453427,
      "recall": 0.4,
      "f1-score": 0.39866518353726366,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      11,
      20
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
    "ece": 0.3720878399689249,
    "mce": 0.46733597277899247,
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
        "count": 12,
        "accuracy": 0.08333333333333333,
        "confidence": 0.538159161578264
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 7,
        "accuracy": 0.42857142857142855,
        "confidence": 0.6209552842162527
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 11,
        "accuracy": 0.45454545454545453,
        "confidence": 0.7584579046667794
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 13,
        "accuracy": 0.38461538461538464,
        "confidence": 0.8519513573943771
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 17,
        "accuracy": 0.5882352941176471,
        "confidence": 0.9471922866012401
      }
    ],
    "brier_score": 0.35826398372107726
  },
  "auroc": 0.48720800889877647,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.949150966647721,
    "p95_inference_latency_ms": 7.569090451215743,
    "p99_inference_latency_ms": 7.681647919598618,
    "throughput_samples_per_sec": 143.90247165437552
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.3,
      "balanced_accuracy": 0.3,
      "macro_f1": 0.28,
      "weighted_f1": 0.28,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.35,
          "recall": 0.4666666666666667,
          "f1-score": 0.4,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2,
          "recall": 0.13333333333333333,
          "f1-score": 0.16,
          "support": 15.0
        },
        "accuracy": 0.3,
        "macro avg": {
          "precision": 0.275,
          "recall": 0.3,
          "f1-score": 0.28,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.275,
          "recall": 0.3,
          "f1-score": 0.28,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          8
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5625,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4296296296296296,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.125,
          "f1-score": 0.2222222222222222,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 1.0,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.75,
          "recall": 0.5625,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7666666666666667,
          "recall": 0.5333333333333333,
          "f1-score": 0.4296296296296296,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          1,
          7
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
      "balanced_accuracy": 0.41964285714285715,
      "macro_f1": 0.354066985645933,
      "weighted_f1": 0.34258373205741627,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.7142857142857143,
          "f1-score": 0.5263157894736842,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.125,
          "f1-score": 0.18181818181818182,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.375,
          "recall": 0.41964285714285715,
          "f1-score": 0.354066985645933,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3722222222222223,
          "recall": 0.4,
          "f1-score": 0.34258373205741627,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
        ],
        [
          7,
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.36666666666666664,
      "balanced_accuracy": 0.3794642857142857,
      "macro_f1": 0.34857142857142853,
      "weighted_f1": 0.34133333333333327,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.1875,
          "f1-score": 0.24,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.38095238095238093,
          "recall": 0.5714285714285714,
          "f1-score": 0.45714285714285713,
          "support": 14.0
        },
        "accuracy": 0.36666666666666664,
        "macro avg": {
          "precision": 0.3571428571428571,
          "recall": 0.3794642857142857,
          "f1-score": 0.34857142857142853,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.3555555555555555,
          "recall": 0.36666666666666664,
          "f1-score": 0.34133333333333327,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          13
        ],
        [
          6,
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
      "mean": 0.3962,
      "lower_95": 0.2833,
      "upper_95": 0.5333
    },
    "balanced_accuracy": {
      "mean": 0.3978,
      "lower_95": 0.2816,
      "upper_95": 0.533
    },
    "macro_f1": {
      "mean": 0.3916,
      "lower_95": 0.2758,
      "upper_95": 0.53
    }
  }
}
```