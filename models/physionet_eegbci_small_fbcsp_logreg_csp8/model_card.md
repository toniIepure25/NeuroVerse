# Model Card: physionet_eegbci_small_fbcsp_logreg_csp8

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
  "accuracy": 0.6166666666666667,
  "balanced_accuracy": 0.6145717463848721,
  "macro_f1": 0.613986013986014,
  "weighted_f1": 0.6150582750582749,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6176470588235294,
      "recall": 0.6774193548387096,
      "f1-score": 0.6461538461538462,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6153846153846154,
      "recall": 0.5517241379310345,
      "f1-score": 0.5818181818181818,
      "support": 29.0
    },
    "accuracy": 0.6166666666666667,
    "macro avg": {
      "precision": 0.6165158371040724,
      "recall": 0.6145717463848721,
      "f1-score": 0.613986013986014,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.616553544494721,
      "recall": 0.6166666666666667,
      "f1-score": 0.6150582750582749,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      21,
      10
    ],
    [
      13,
      16
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.1937081807698645,
    "mce": 0.35519742185897496,
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
        "accuracy": 0.7,
        "confidence": 0.5384788981942306
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 16,
        "accuracy": 0.5625,
        "confidence": 0.6586599266234379
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 7,
        "accuracy": 0.5714285714285714,
        "confidence": 0.7689956253349088
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 16,
        "accuracy": 0.5,
        "confidence": 0.855197421858975
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 11,
        "accuracy": 0.8181818181818182,
        "confidence": 0.9456902613701099
      }
    ],
    "brier_score": 0.2687554298527509
  },
  "auroc": 0.6184649610678532,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.68651105012638,
    "p95_inference_latency_ms": 6.84685344749596,
    "p99_inference_latency_ms": 6.906069910473889,
    "throughput_samples_per_sec": 149.5548265011989
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.5,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.42233632862644416,
      "weighted_f1": 0.42233632862644416,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8666666666666667,
          "f1-score": 0.6341463414634146,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.13333333333333333,
          "f1-score": 0.21052631578947367,
          "support": 15.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.5,
          "recall": 0.5,
          "f1-score": 0.42233632862644416,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5,
          "recall": 0.5,
          "f1-score": 0.42233632862644416,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          2
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
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.875,
      "macro_f1": 0.8660714285714286,
      "weighted_f1": 0.8654761904761905,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.75,
          "f1-score": 0.8571428571428571,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7777777777777778,
          "recall": 1.0,
          "f1-score": 0.875,
          "support": 7.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.8888888888888888,
          "recall": 0.875,
          "f1-score": 0.8660714285714286,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8962962962962963,
          "recall": 0.8666666666666667,
          "f1-score": 0.8654761904761905,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.29696969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 1.0,
          "f1-score": 0.6363636363636364,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
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
          7,
          0
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5714285714285714,
      "macro_f1": 0.5661846496106786,
      "weighted_f1": 0.5652206154987023,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6153846153846154,
          "recall": 0.5,
          "f1-score": 0.5517241379310345,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5294117647058824,
          "recall": 0.6428571428571429,
          "f1-score": 0.5806451612903226,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5723981900452488,
          "recall": 0.5714285714285714,
          "f1-score": 0.5661846496106786,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.57526395173454,
          "recall": 0.5666666666666667,
          "f1-score": 0.5652206154987023,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          8,
          8
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
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.875,
      "macro_f1": 0.8660714285714286,
      "weighted_f1": 0.8654761904761905,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.75,
          "f1-score": 0.8571428571428571,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7777777777777778,
          "recall": 1.0,
          "f1-score": 0.875,
          "support": 7.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.8888888888888888,
          "recall": 0.875,
          "f1-score": 0.8660714285714286,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8962962962962963,
          "recall": 0.8666666666666667,
          "f1-score": 0.8654761904761905,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
      "mean": 0.6117,
      "lower_95": 0.4913,
      "upper_95": 0.7333
    },
    "balanced_accuracy": {
      "mean": 0.6094,
      "lower_95": 0.4833,
      "upper_95": 0.73
    },
    "macro_f1": {
      "mean": 0.6047,
      "lower_95": 0.4762,
      "upper_95": 0.7255
    }
  }
}
```