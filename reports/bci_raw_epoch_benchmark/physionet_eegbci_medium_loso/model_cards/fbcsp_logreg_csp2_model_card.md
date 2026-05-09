# Model Card: physionet_eegbci_medium_loso_fbcsp_logreg_csp2

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
  "accuracy": 0.5777777777777777,
  "balanced_accuracy": 0.5863095238095238,
  "macro_f1": 0.5744151319064211,
  "weighted_f1": 0.5718931475029037,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6470588235294118,
      "recall": 0.4583333333333333,
      "f1-score": 0.5365853658536586,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5357142857142857,
      "recall": 0.7142857142857143,
      "f1-score": 0.6122448979591837,
      "support": 21.0
    },
    "accuracy": 0.5777777777777777,
    "macro avg": {
      "precision": 0.5913865546218487,
      "recall": 0.5863095238095238,
      "f1-score": 0.5744151319064211,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5950980392156863,
      "recall": 0.5777777777777777,
      "f1-score": 0.5718931475029037,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      11,
      13
    ],
    [
      6,
      15
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.2064372464294823,
    "mce": 0.350056432889681,
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
        "confidence": 0.5560925214814826
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 7,
        "accuracy": 0.42857142857142855,
        "confidence": 0.6419397323691368
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 10,
        "accuracy": 0.4,
        "confidence": 0.750056432889681
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 9,
        "accuracy": 1.0,
        "confidence": 0.836181496216943
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 6,
        "accuracy": 0.6666666666666666,
        "confidence": 0.9319940534231915
      }
    ],
    "brier_score": 0.2429402546757906
  },
  "auroc": 0.6785714285714286,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.421424444530405,
    "p95_inference_latency_ms": 8.315953399869613,
    "p99_inference_latency_ms": 8.430042278996552,
    "throughput_samples_per_sec": 134.74502199331837
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5777777777777777,
      "balanced_accuracy": 0.5863095238095238,
      "macro_f1": 0.5744151319064211,
      "weighted_f1": 0.5718931475029037,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6470588235294118,
          "recall": 0.4583333333333333,
          "f1-score": 0.5365853658536586,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5357142857142857,
          "recall": 0.7142857142857143,
          "f1-score": 0.6122448979591837,
          "support": 21.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5913865546218487,
          "recall": 0.5863095238095238,
          "f1-score": 0.5744151319064211,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5950980392156863,
          "recall": 0.5777777777777777,
          "f1-score": 0.5718931475029037,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          11,
          13
        ],
        [
          6,
          15
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
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.8035714285714286,
      "macro_f1": 0.8,
      "weighted_f1": 0.8,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8571428571428571,
          "recall": 0.75,
          "f1-score": 0.8,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.8571428571428571,
          "f1-score": 0.8,
          "support": 7.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.8035714285714286,
          "recall": 0.8035714285714286,
          "f1-score": 0.8,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8071428571428572,
          "recall": 0.8,
          "f1-score": 0.8,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
      "mean": 0.582,
      "lower_95": 0.4444,
      "upper_95": 0.745
    },
    "balanced_accuracy": {
      "mean": 0.5898,
      "lower_95": 0.4476,
      "upper_95": 0.7492
    },
    "macro_f1": {
      "mean": 0.5727,
      "lower_95": 0.4263,
      "upper_95": 0.7321
    }
  }
}
```