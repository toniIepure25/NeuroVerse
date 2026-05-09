# Model Card: physionet_eegbci_small_fbcsp_lda_csp8

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
  "accuracy": 0.6,
  "balanced_accuracy": 0.6006674082313682,
  "macro_f1": 0.6,
  "weighted_f1": 0.6,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6206896551724138,
      "recall": 0.5806451612903226,
      "f1-score": 0.6,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5806451612903226,
      "recall": 0.6206896551724138,
      "f1-score": 0.6,
      "support": 29.0
    },
    "accuracy": 0.6,
    "macro avg": {
      "precision": 0.6006674082313682,
      "recall": 0.6006674082313682,
      "f1-score": 0.6,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.6013348164627365,
      "recall": 0.6,
      "f1-score": 0.6,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      18,
      13
    ],
    [
      11,
      18
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.3412012620971817,
    "mce": 0.5506938466552436,
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
        "accuracy": 0.5,
        "confidence": 0.5886861925394835
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 2,
        "accuracy": 0.5,
        "confidence": 0.6701458145378077
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 5,
        "accuracy": 0.2,
        "confidence": 0.7506938466552436
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 3,
        "accuracy": 0.6666666666666666,
        "confidence": 0.8518092989347475
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 48,
        "accuracy": 0.6458333333333334,
        "confidence": 0.9926148871165804
      }
    ],
    "brier_score": 0.34781835180855997
  },
  "auroc": 0.6885428253615128,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.906494933597666,
    "p95_inference_latency_ms": 7.239113602008729,
    "p99_inference_latency_ms": 7.551464912321533,
    "throughput_samples_per_sec": 144.79124499684377
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.6,
      "macro_f1": 0.5927601809954751,
      "weighted_f1": 0.5927601809954751,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5789473684210527,
          "recall": 0.7333333333333333,
          "f1-score": 0.6470588235294118,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6363636363636364,
          "recall": 0.4666666666666667,
          "f1-score": 0.5384615384615384,
          "support": 15.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6076555023923444,
          "recall": 0.6,
          "f1-score": 0.5927601809954751,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6076555023923444,
          "recall": 0.6,
          "f1-score": 0.5927601809954751,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          4
        ],
        [
          8,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5777777777777777,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.375,
          "f1-score": 0.5,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.8571428571428571,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6477272727272727,
          "recall": 0.6160714285714286,
          "f1-score": 0.5833333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6545454545454545,
          "recall": 0.6,
          "f1-score": 0.5777777777777777,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.49107142857142855,
      "macro_f1": 0.4,
      "weighted_f1": 0.3866666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.8571428571428571,
          "f1-score": 0.6,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.125,
          "f1-score": 0.2,
          "support": 8.0
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
          6,
          1
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6741071428571428,
      "macro_f1": 0.6651785714285714,
      "weighted_f1": 0.6636904761904762,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.5625,
          "f1-score": 0.6428571428571429,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6111111111111112,
          "recall": 0.7857142857142857,
          "f1-score": 0.6875,
          "support": 14.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6805555555555556,
          "recall": 0.6741071428571428,
          "f1-score": 0.6651785714285714,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6851851851851852,
          "recall": 0.6666666666666666,
          "f1-score": 0.6636904761904762,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          9,
          7
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
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5777777777777777,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.375,
          "f1-score": 0.5,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.8571428571428571,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6477272727272727,
          "recall": 0.6160714285714286,
          "f1-score": 0.5833333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6545454545454545,
          "recall": 0.6,
          "f1-score": 0.5777777777777777,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
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
      "mean": 0.596,
      "lower_95": 0.4667,
      "upper_95": 0.7167
    },
    "balanced_accuracy": {
      "mean": 0.597,
      "lower_95": 0.4685,
      "upper_95": 0.716
    },
    "macro_f1": {
      "mean": 0.592,
      "lower_95": 0.4661,
      "upper_95": 0.7128
    }
  }
}
```