# Model Card: physionet_eegbci_small_csp_svm_linear_csp4

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
  "accuracy": 0.5666666666666667,
  "balanced_accuracy": 0.5617352614015573,
  "macro_f1": 0.5542857142857143,
  "weighted_f1": 0.5567619047619047,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5641025641025641,
      "recall": 0.7096774193548387,
      "f1-score": 0.6285714285714286,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5714285714285714,
      "recall": 0.41379310344827586,
      "f1-score": 0.48,
      "support": 29.0
    },
    "accuracy": 0.5666666666666667,
    "macro avg": {
      "precision": 0.5677655677655677,
      "recall": 0.5617352614015573,
      "f1-score": 0.5542857142857143,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.5676434676434676,
      "recall": 0.5666666666666667,
      "f1-score": 0.5567619047619047,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      22,
      9
    ],
    [
      17,
      12
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.017395780713841652,
    "mce": 0.019715229242880605,
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
        "count": 46,
        "accuracy": 0.5652173913043478,
        "confidence": 0.5455021620614672
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 14,
        "accuracy": 0.6428571428571429,
        "confidence": 0.6330824073101435
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
    "brier_score": 0.252505018523497
  },
  "auroc": 0.5361512791991101,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3687310996610904,
    "p95_inference_latency_ms": 0.45722464856225997,
    "p99_inference_latency_ms": 0.5315025500385673,
    "throughput_samples_per_sec": 2712.003410938551
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.5,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3333333333333333,
      "weighted_f1": 0.3333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 1.0,
          "f1-score": 0.6666666666666666,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 15.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.25,
          "recall": 0.5,
          "f1-score": 0.3333333333333333,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.25,
          "recall": 0.5,
          "f1-score": 0.3333333333333333,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          15,
          0
        ],
        [
          15,
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
    "S002": {
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
    },
    "S003": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7321428571428572,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.75,
          "f1-score": 0.75,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.7142857142857143,
          "f1-score": 0.7142857142857143,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.7321428571428572,
          "recall": 0.7321428571428572,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7333333333333333,
          "recall": 0.7333333333333333,
          "f1-score": 0.7333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.5970695970695971,
      "weighted_f1": 0.6051282051282051,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6086956521739131,
          "recall": 0.875,
          "f1-score": 0.717948717948718,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.35714285714285715,
          "f1-score": 0.47619047619047616,
          "support": 14.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6614906832298137,
          "recall": 0.6160714285714286,
          "f1-score": 0.5970695970695971,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6579710144927536,
          "recall": 0.6333333333333333,
          "f1-score": 0.6051282051282051,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          2
        ],
        [
          9,
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
    "8": {
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.567,
      "lower_95": 0.4333,
      "upper_95": 0.6833
    },
    "balanced_accuracy": {
      "mean": 0.5614,
      "lower_95": 0.4293,
      "upper_95": 0.6722
    },
    "macro_f1": {
      "mean": 0.5499,
      "lower_95": 0.4158,
      "upper_95": 0.6665
    }
  }
}
```