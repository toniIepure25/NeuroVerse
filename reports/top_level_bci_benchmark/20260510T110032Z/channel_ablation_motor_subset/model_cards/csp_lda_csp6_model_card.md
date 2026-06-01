# Model Card: channel_ablation_motor_subset_csp_lda_csp6

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
    "ece": 0.07055728301561831,
    "mce": 0.27203132788104323,
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
        "count": 27,
        "accuracy": 0.48148148148148145,
        "confidence": 0.5546221699080149
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 14,
        "accuracy": 0.6428571428571429,
        "confidence": 0.6348461545241253
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 4,
        "accuracy": 1.0,
        "confidence": 0.7279686721189568
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
    "brier_score": 0.2309124832583691
  },
  "auroc": 0.6567460317460317,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3150895997856019,
    "p95_inference_latency_ms": 0.37165679968893517,
    "p99_inference_latency_ms": 0.4501252800400837,
    "throughput_samples_per_sec": 3173.700435306133
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
      "balanced_accuracy": 0.3392857142857143,
      "macro_f1": 0.33035714285714285,
      "weighted_f1": 0.3273809523809524,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.25,
          "f1-score": 0.2857142857142857,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.42857142857142855,
          "f1-score": 0.375,
          "support": 7.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3392857142857143,
          "f1-score": 0.33035714285714285,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3333333333333333,
          "f1-score": 0.3273809523809524,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          6
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
    "4": {
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
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7410714285714286,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.730952380952381,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.625,
          "f1-score": 0.7142857142857143,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.8571428571428571,
          "f1-score": 0.75,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.75,
          "recall": 0.7410714285714286,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7555555555555554,
          "recall": 0.7333333333333333,
          "f1-score": 0.730952380952381,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "mean": 0.5821,
      "lower_95": 0.4222,
      "upper_95": 0.7333
    },
    "balanced_accuracy": {
      "mean": 0.5911,
      "lower_95": 0.4414,
      "upper_95": 0.7355
    },
    "macro_f1": {
      "mean": 0.5731,
      "lower_95": 0.4175,
      "upper_95": 0.7327
    }
  }
}
```