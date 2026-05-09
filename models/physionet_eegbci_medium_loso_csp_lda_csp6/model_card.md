# Model Card: physionet_eegbci_medium_loso_csp_lda_csp6

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
  "accuracy": 0.5111111111111111,
  "balanced_accuracy": 0.5297619047619048,
  "macro_f1": 0.48004201680672265,
  "weighted_f1": 0.4715686274509804,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6,
      "recall": 0.25,
      "f1-score": 0.35294117647058826,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4857142857142857,
      "recall": 0.8095238095238095,
      "f1-score": 0.6071428571428571,
      "support": 21.0
    },
    "accuracy": 0.5111111111111111,
    "macro avg": {
      "precision": 0.5428571428571428,
      "recall": 0.5297619047619048,
      "f1-score": 0.48004201680672265,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.5466666666666666,
      "recall": 0.5111111111111111,
      "f1-score": 0.4715686274509804,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      6,
      18
    ],
    [
      4,
      17
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.11895803139293236,
    "mce": 0.4198844144488551,
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
        "count": 23,
        "accuracy": 0.4782608695652174,
        "confidence": 0.5528022336621611
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 12,
        "accuracy": 0.5833333333333334,
        "confidence": 0.6369128044236506
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 6,
        "accuracy": 0.3333333333333333,
        "confidence": 0.7532177477821884
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 4,
        "accuracy": 0.75,
        "confidence": 0.8690999746688286
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.2672879435106136
  },
  "auroc": 0.5555555555555556,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3257737112208916,
    "p95_inference_latency_ms": 0.4236048000166192,
    "p99_inference_latency_ms": 0.584104919835227,
    "throughput_samples_per_sec": 3069.615397302417
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5111111111111111,
      "balanced_accuracy": 0.5297619047619048,
      "macro_f1": 0.48004201680672265,
      "weighted_f1": 0.4715686274509804,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.25,
          "f1-score": 0.35294117647058826,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4857142857142857,
          "recall": 0.8095238095238095,
          "f1-score": 0.6071428571428571,
          "support": 21.0
        },
        "accuracy": 0.5111111111111111,
        "macro avg": {
          "precision": 0.5428571428571428,
          "recall": 0.5297619047619048,
          "f1-score": 0.48004201680672265,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5466666666666666,
          "recall": 0.5111111111111111,
          "f1-score": 0.4715686274509804,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          6,
          18
        ],
        [
          4,
          17
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
    "4": {
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
    "8": {
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5145,
      "lower_95": 0.3556,
      "upper_95": 0.6667
    },
    "balanced_accuracy": {
      "mean": 0.5326,
      "lower_95": 0.3993,
      "upper_95": 0.659
    },
    "macro_f1": {
      "mean": 0.4769,
      "lower_95": 0.3351,
      "upper_95": 0.6334
    }
  }
}
```