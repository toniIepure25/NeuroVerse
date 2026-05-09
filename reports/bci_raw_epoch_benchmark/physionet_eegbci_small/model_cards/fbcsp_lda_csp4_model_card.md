# Model Card: physionet_eegbci_small_fbcsp_lda_csp4

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
  "accuracy": 0.45,
  "balanced_accuracy": 0.4555061179087876,
  "macro_f1": 0.4373401534526854,
  "weighted_f1": 0.43452685421994885,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.45,
      "recall": 0.2903225806451613,
      "f1-score": 0.35294117647058826,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.45,
      "recall": 0.6206896551724138,
      "f1-score": 0.5217391304347826,
      "support": 29.0
    },
    "accuracy": 0.45,
    "macro avg": {
      "precision": 0.45,
      "recall": 0.4555061179087876,
      "f1-score": 0.4373401534526854,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.45,
      "recall": 0.45,
      "f1-score": 0.43452685421994885,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      9,
      22
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
    "ece": 0.5139521611548108,
    "mce": 0.5507734390524173,
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
        "count": 5,
        "accuracy": 0.8,
        "confidence": 0.5657625065380079
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 4,
        "accuracy": 0.25,
        "confidence": 0.759798967212176
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 5,
        "accuracy": 0.4,
        "confidence": 0.8582336273437579
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 46,
        "accuracy": 0.43478260869565216,
        "confidence": 0.9855560477480694
      }
    ],
    "brier_score": 0.5031364443447581
  },
  "auroc": 0.5061179087875417,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.787991599837066,
    "p95_inference_latency_ms": 7.047282700659707,
    "p99_inference_latency_ms": 7.855580838768213,
    "throughput_samples_per_sec": 147.318980186128
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.4,
      "macro_f1": 0.3973214285714286,
      "weighted_f1": 0.3973214285714286,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4117647058823529,
          "recall": 0.4666666666666667,
          "f1-score": 0.4375,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.38461538461538464,
          "recall": 0.3333333333333333,
          "f1-score": 0.35714285714285715,
          "support": 15.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.3981900452488688,
          "recall": 0.4,
          "f1-score": 0.3973214285714286,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.3981900452488688,
          "recall": 0.4,
          "f1-score": 0.3973214285714286,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          8
        ],
        [
          10,
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
    "S002": {
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5446428571428572,
      "macro_f1": 0.5248868778280543,
      "weighted_f1": 0.5206636500754148,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.7142857142857143,
          "f1-score": 0.5882352941176471,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.375,
          "f1-score": 0.46153846153846156,
          "support": 8.0
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
          5,
          2
        ],
        [
          5,
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.41517857142857145,
      "macro_f1": 0.375,
      "weighted_f1": 0.36666666666666664,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.375,
          "recall": 0.1875,
          "f1-score": 0.25,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4090909090909091,
          "recall": 0.6428571428571429,
          "f1-score": 0.5,
          "support": 14.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.3920454545454546,
          "recall": 0.41517857142857145,
          "f1-score": 0.375,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.3909090909090909,
          "recall": 0.4,
          "f1-score": 0.36666666666666664,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          13
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.4452,
      "lower_95": 0.3167,
      "upper_95": 0.5667
    },
    "balanced_accuracy": {
      "mean": 0.4511,
      "lower_95": 0.3275,
      "upper_95": 0.5744
    },
    "macro_f1": {
      "mean": 0.4295,
      "lower_95": 0.3031,
      "upper_95": 0.5526
    }
  }
}
```