# Model Card: physionet_eegbci_medium_group_subject_fbcsp_logreg_csp6

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
  "accuracy": 0.5166666666666667,
  "balanced_accuracy": 0.5090301830776843,
  "macro_f1": 0.49767441860465117,
  "weighted_f1": 0.502015503875969,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5289256198347108,
      "recall": 0.6808510638297872,
      "f1-score": 0.5953488372093023,
      "support": 94.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4915254237288136,
      "recall": 0.3372093023255814,
      "f1-score": 0.4,
      "support": 86.0
    },
    "accuracy": 0.5166666666666667,
    "macro avg": {
      "precision": 0.5102255217817622,
      "recall": 0.5090301830776843,
      "f1-score": 0.49767441860465117,
      "support": 180.0
    },
    "weighted avg": {
      "precision": 0.5110566372507821,
      "recall": 0.5166666666666667,
      "f1-score": 0.502015503875969,
      "support": 180.0
    }
  },
  "confusion_matrix": [
    [
      64,
      30
    ],
    [
      57,
      29
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.2808008483849648,
    "mce": 0.4336924449318883,
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
        "count": 29,
        "accuracy": 0.5517241379310345,
        "confidence": 0.5442034299407496
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 28,
        "accuracy": 0.35714285714285715,
        "confidence": 0.6458902421628316
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 29,
        "accuracy": 0.4827586206896552,
        "confidence": 0.7463762311928089
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 28,
        "accuracy": 0.6428571428571429,
        "confidence": 0.8561611902471438
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 66,
        "accuracy": 0.5303030303030303,
        "confidence": 0.9639954752349186
      }
    ],
    "brier_score": 0.3423041538040075
  },
  "auroc": 0.5383473527956457,
  "split_strategy": "group_subject",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.855617872194368,
    "p95_inference_latency_ms": 7.3863192501448784,
    "p99_inference_latency_ms": 7.6007744088019535,
    "throughput_samples_per_sec": 145.86577295328698
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5296442687747036,
      "macro_f1": 0.5181030086690463,
      "weighted_f1": 0.5200067992520823,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 0.6956521739130435,
          "f1-score": 0.6037735849056604,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 0.36363636363636365,
          "f1-score": 0.43243243243243246,
          "support": 22.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5333333333333333,
          "recall": 0.5296442687747036,
          "f1-score": 0.5181030086690463,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5333333333333333,
          "recall": 0.5333333333333333,
          "f1-score": 0.5200067992520823,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          16,
          7
        ],
        [
          14,
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
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.48023715415019763,
      "macro_f1": 0.3915343915343915,
      "weighted_f1": 0.39694297472075246,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8695652173913043,
          "f1-score": 0.6349206349206349,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.09090909090909091,
          "f1-score": 0.14814814814814814,
          "support": 22.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.45,
          "recall": 0.48023715415019763,
          "f1-score": 0.3915343915343915,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.45111111111111113,
          "recall": 0.4888888888888889,
          "f1-score": 0.39694297472075246,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          20,
          3
        ],
        [
          20,
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
    "S006": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.48511904761904756,
      "macro_f1": 0.48481831757093086,
      "weighted_f1": 0.48787124605939935,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.52,
          "recall": 0.5416666666666666,
          "f1-score": 0.5306122448979592,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45,
          "recall": 0.42857142857142855,
          "f1-score": 0.43902439024390244,
          "support": 21.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.485,
          "recall": 0.48511904761904756,
          "f1-score": 0.48481831757093086,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.48733333333333334,
          "recall": 0.4888888888888889,
          "f1-score": 0.48787124605939935,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          13,
          11
        ],
        [
          12,
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.5555555555555556,
      "balanced_accuracy": 0.5505952380952381,
      "macro_f1": 0.55,
      "weighted_f1": 0.5533333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5769230769230769,
          "recall": 0.625,
          "f1-score": 0.6,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5263157894736842,
          "recall": 0.47619047619047616,
          "f1-score": 0.5,
          "support": 21.0
        },
        "accuracy": 0.5555555555555556,
        "macro avg": {
          "precision": 0.5516194331983806,
          "recall": 0.5505952380952381,
          "f1-score": 0.55,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.553306342780027,
          "recall": 0.5555555555555556,
          "f1-score": 0.5533333333333333,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          15,
          9
        ],
        [
          11,
          10
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.4949944382647386,
      "macro_f1": 0.4857142857142857,
      "weighted_f1": 0.48857142857142855,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5128205128205128,
          "recall": 0.6451612903225806,
          "f1-score": 0.5714285714285714,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.47619047619047616,
          "recall": 0.3448275862068966,
          "f1-score": 0.4,
          "support": 29.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.49450549450549447,
          "recall": 0.4949944382647386,
          "f1-score": 0.4857142857142857,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4951159951159951,
          "recall": 0.5,
          "f1-score": 0.48857142857142855,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          20,
          11
        ],
        [
          19,
          10
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
      "balanced_accuracy": 0.5272525027808677,
      "macro_f1": 0.513888888888889,
      "weighted_f1": 0.5171296296296296,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5365853658536586,
          "recall": 0.7096774193548387,
          "f1-score": 0.6111111111111112,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5263157894736842,
          "recall": 0.3448275862068966,
          "f1-score": 0.4166666666666667,
          "support": 29.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5314505776636713,
          "recall": 0.5272525027808677,
          "f1-score": 0.513888888888889,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.5316217372700043,
          "recall": 0.5333333333333333,
          "f1-score": 0.5171296296296296,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          22,
          9
        ],
        [
          19,
          10
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
      "accuracy": 0.5166666666666667,
      "balanced_accuracy": 0.5044642857142857,
      "macro_f1": 0.49285922471582627,
      "weighted_f1": 0.500184591469931,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5365853658536586,
          "recall": 0.6875,
          "f1-score": 0.6027397260273972,
          "support": 32.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.47368421052631576,
          "recall": 0.32142857142857145,
          "f1-score": 0.3829787234042553,
          "support": 28.0
        },
        "accuracy": 0.5166666666666667,
        "macro avg": {
          "precision": 0.5051347881899871,
          "recall": 0.5044642857142857,
          "f1-score": 0.49285922471582627,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.5072314933675652,
          "recall": 0.5166666666666667,
          "f1-score": 0.500184591469931,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          22,
          10
        ],
        [
          19,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.515,
      "lower_95": 0.4471,
      "upper_95": 0.5862
    },
    "balanced_accuracy": {
      "mean": 0.5087,
      "lower_95": 0.4455,
      "upper_95": 0.5706
    },
    "macro_f1": {
      "mean": 0.4957,
      "lower_95": 0.4289,
      "upper_95": 0.5634
    }
  }
}
```