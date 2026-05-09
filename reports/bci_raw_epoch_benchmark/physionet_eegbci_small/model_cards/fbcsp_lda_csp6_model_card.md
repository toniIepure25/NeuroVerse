# Model Card: physionet_eegbci_small_fbcsp_lda_csp6

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
  "accuracy": 0.5833333333333334,
  "balanced_accuracy": 0.5834260289210234,
  "macro_f1": 0.5832175604334537,
  "weighted_f1": 0.5834491062332129,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6,
      "recall": 0.5806451612903226,
      "f1-score": 0.5901639344262295,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5666666666666667,
      "recall": 0.5862068965517241,
      "f1-score": 0.576271186440678,
      "support": 29.0
    },
    "accuracy": 0.5833333333333334,
    "macro avg": {
      "precision": 0.5833333333333333,
      "recall": 0.5834260289210234,
      "f1-score": 0.5832175604334537,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.5838888888888889,
      "recall": 0.5833333333333334,
      "f1-score": 0.5834491062332129,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      18,
      13
    ],
    [
      12,
      17
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.40384247364633996,
    "mce": 0.8543292981952498,
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
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.5933580683194764
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.6636686597292372
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 2,
        "accuracy": 1.0,
        "confidence": 0.7217380414678508
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 2,
        "accuracy": 0.0,
        "confidence": 0.8543292981952498
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 54,
        "accuracy": 0.6111111111111112,
        "confidence": 0.9945988736532757
      }
    ],
    "brier_score": 0.38701893860305076
  },
  "auroc": 0.6206896551724138,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.725053450281848,
    "p95_inference_latency_ms": 6.866342696957872,
    "p99_inference_latency_ms": 7.063652541364717,
    "throughput_samples_per_sec": 148.69770290942296
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5666666666666667,
      "macro_f1": 0.5661846496106786,
      "weighted_f1": 0.5661846496106785,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5625,
          "recall": 0.6,
          "f1-score": 0.5806451612903226,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5333333333333333,
          "f1-score": 0.5517241379310345,
          "support": 15.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5669642857142857,
          "recall": 0.5666666666666667,
          "f1-score": 0.5661846496106786,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5669642857142857,
          "recall": 0.5666666666666667,
          "f1-score": 0.5661846496106785,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          9,
          6
        ],
        [
          7,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5982142857142857,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.6,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.625,
          "f1-score": 0.625,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5714285714285714,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5982142857142857,
          "recall": 0.5982142857142857,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.6,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "balanced_accuracy": 0.6071428571428572,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.5964285714285714,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5,
          "f1-score": 0.5714285714285714,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.7142857142857143,
          "f1-score": 0.625,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6111111111111112,
          "recall": 0.6071428571428572,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6148148148148148,
          "recall": 0.6,
          "f1-score": 0.5964285714285714,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5535714285714286,
      "macro_f1": 0.49760765550239233,
      "weighted_f1": 0.4886762360446571,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8571428571428571,
          "f1-score": 0.631578947368421,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.25,
          "f1-score": 0.36363636363636365,
          "support": 8.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5833333333333333,
          "recall": 0.5535714285714286,
          "f1-score": 0.49760765550239233,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5888888888888888,
          "recall": 0.5333333333333333,
          "f1-score": 0.4886762360446571,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
        ],
        [
          6,
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.6116071428571428,
      "macro_f1": 0.5927601809954751,
      "weighted_f1": 0.5891402714932127,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7,
          "recall": 0.4375,
          "f1-score": 0.5384615384615384,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.55,
          "recall": 0.7857142857142857,
          "f1-score": 0.6470588235294118,
          "support": 14.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.625,
          "recall": 0.6116071428571428,
          "f1-score": 0.5927601809954751,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.63,
          "recall": 0.6,
          "f1-score": 0.5891402714932127,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          9
        ],
        [
          3,
          11
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.5982142857142857,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.6,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.625,
          "f1-score": 0.625,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5714285714285714,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5982142857142857,
          "recall": 0.5982142857142857,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.6,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "mean": 0.5789,
      "lower_95": 0.45,
      "upper_95": 0.7
    },
    "balanced_accuracy": {
      "mean": 0.5788,
      "lower_95": 0.4506,
      "upper_95": 0.7022
    },
    "macro_f1": {
      "mean": 0.5745,
      "lower_95": 0.4462,
      "upper_95": 0.6987
    }
  }
}
```