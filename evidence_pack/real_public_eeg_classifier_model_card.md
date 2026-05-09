# Model Card: S001R04_event_classifier

## Intended Use
Event-locked controlled EEG task-label classification.

## Not Intended Use
Not for thought reading, clinical diagnosis, unrestricted mental-state inference, or direct closed-loop control.

## Limitations
Fixture or local dataset annotations define labels; performance is not clinical validation and may not generalize across subjects or hardware.

## Metrics
```json
{
  "task_type": "classification",
  "accuracy": 0.5,
  "balanced_accuracy": 0.4669632925472747,
  "macro_f1": 0.46616154658584746,
  "weighted_f1": 0.5008270193323231,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.4,
      "recall": 0.3870967741935484,
      "f1-score": 0.39344262295081966,
      "support": 31.0
    },
    "REST": {
      "precision": 0.6101694915254238,
      "recall": 0.6,
      "f1-score": 0.6050420168067226,
      "support": 60.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.3870967741935484,
      "recall": 0.41379310344827586,
      "f1-score": 0.4,
      "support": 29.0
    },
    "accuracy": 0.5,
    "macro avg": {
      "precision": 0.4657554219063241,
      "recall": 0.4669632925472747,
      "f1-score": 0.46616154658584746,
      "support": 120.0
    },
    "weighted avg": {
      "precision": 0.5019664661928194,
      "recall": 0.5,
      "f1-score": 0.5008270193323231,
      "support": 120.0
    }
  },
  "confusion_matrix": [
    [
      12,
      10,
      9
    ],
    [
      14,
      36,
      10
    ],
    [
      4,
      13,
      12
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "REST",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.30446297105077147,
    "mce": 0.3948415944808792,
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
        "count": 1,
        "accuracy": 0.0,
        "confidence": 0.3895837859850851
      },
      {
        "lo": 0.4,
        "hi": 0.5,
        "count": 4,
        "accuracy": 0.25,
        "confidence": 0.49351967083221776
      },
      {
        "lo": 0.5,
        "hi": 0.6,
        "count": 19,
        "accuracy": 0.3684210526315789,
        "confidence": 0.5497988121961114
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 15,
        "accuracy": 0.4666666666666667,
        "confidence": 0.6510903628348111
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 12,
        "accuracy": 0.5833333333333334,
        "confidence": 0.7482411171846001
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 17,
        "accuracy": 0.47058823529411764,
        "confidence": 0.849923815488789
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 52,
        "accuracy": 0.5769230769230769,
        "confidence": 0.9717646714039561
      }
    ]
  },
  "auroc_ovr_macro": 0.6551116698941685,
  "latency": {
    "mean_inference_latency_ms": 0.35797731666207255,
    "p95_inference_latency_ms": 0.37296300029083795,
    "p99_inference_latency_ms": 0.39273083997613867,
    "throughput_samples_per_sec": 2793.4730874135003
  },
  "split_strategy": "group_run",
  "split_warnings": [],
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4777777777777778,
      "macro_f1": 0.4595704948646125,
      "weighted_f1": 0.47212885154061623,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3684210526315789,
          "recall": 0.4666666666666667,
          "f1-score": 0.4117647058823529,
          "support": 15.0
        },
        "REST": {
          "precision": 0.6190476190476191,
          "recall": 0.43333333333333335,
          "f1-score": 0.5098039215686274,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.5333333333333333,
          "f1-score": 0.45714285714285713,
          "support": 15.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4624895572263994,
          "recall": 0.4777777777777778,
          "f1-score": 0.4595704948646125,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.5016290726817043,
          "recall": 0.4666666666666667,
          "f1-score": 0.47212885154061623,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          7,
          4,
          4
        ],
        [
          9,
          13,
          8
        ],
        [
          3,
          4,
          8
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    },
    "S002": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5150793650793651,
      "macro_f1": 0.513235294117647,
      "weighted_f1": 0.5765196078431372,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.25,
          "f1-score": 0.4,
          "support": 8.0
        },
        "REST": {
          "precision": 0.6842105263157895,
          "recall": 0.8666666666666667,
          "f1-score": 0.7647058823529411,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.42857142857142855,
          "f1-score": 0.375,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.672514619883041,
          "recall": 0.5150793650793651,
          "f1-score": 0.513235294117647,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6865497076023391,
          "recall": 0.6,
          "f1-score": 0.5765196078431372,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          2,
          4
        ],
        [
          0,
          13,
          2
        ],
        [
          0,
          4,
          3
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    },
    "S003": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.39484126984126977,
      "macro_f1": 0.38779956427015244,
      "weighted_f1": 0.44008714596949894,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.375,
          "f1-score": 0.35294117647058826,
          "support": 8.0
        },
        "REST": {
          "precision": 0.5263157894736842,
          "recall": 0.6666666666666666,
          "f1-score": 0.5882352941176471,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.14285714285714285,
          "f1-score": 0.2222222222222222,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.45321637426900585,
          "recall": 0.39484126984126977,
          "f1-score": 0.38779956427015244,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.46871345029239764,
          "recall": 0.4666666666666667,
          "f1-score": 0.44008714596949894,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          4,
          1
        ],
        [
          5,
          10,
          0
        ],
        [
          1,
          5,
          1
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "REST",
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
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.4369047619047619,
      "macro_f1": 0.41817363922627077,
      "weighted_f1": 0.4333423301844354,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.2857142857142857,
          "f1-score": 0.26666666666666666,
          "support": 7.0
        },
        "REST": {
          "precision": 0.5454545454545454,
          "recall": 0.4,
          "f1-score": 0.46153846153846156,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.625,
          "f1-score": 0.5263157894736842,
          "support": 8.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.4166666666666667,
          "recall": 0.4369047619047619,
          "f1-score": 0.41817363922627077,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.45227272727272727,
          "recall": 0.43333333333333335,
          "f1-score": 0.4333423301844354,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          3,
          2
        ],
        [
          5,
          6,
          4
        ],
        [
          1,
          2,
          5
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    },
    "4": {
      "task_type": "classification",
      "accuracy": 0.48333333333333334,
      "balanced_accuracy": 0.4507936507936508,
      "macro_f1": 0.4469052102950408,
      "weighted_f1": 0.4813207784055242,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.5,
          "f1-score": 0.4444444444444444,
          "support": 16.0
        },
        "REST": {
          "precision": 0.5862068965517241,
          "recall": 0.5666666666666667,
          "f1-score": 0.576271186440678,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.36363636363636365,
          "recall": 0.2857142857142857,
          "f1-score": 0.32,
          "support": 14.0
        },
        "accuracy": 0.48333333333333334,
        "macro avg": {
          "precision": 0.44994775339602927,
          "recall": 0.4507936507936508,
          "f1-score": 0.4469052102950408,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4846185997910135,
          "recall": 0.48333333333333334,
          "f1-score": 0.4813207784055242,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          8,
          5,
          3
        ],
        [
          9,
          17,
          4
        ],
        [
          3,
          7,
          4
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5150793650793651,
      "macro_f1": 0.513235294117647,
      "weighted_f1": 0.5765196078431372,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.25,
          "f1-score": 0.4,
          "support": 8.0
        },
        "REST": {
          "precision": 0.6842105263157895,
          "recall": 0.8666666666666667,
          "f1-score": 0.7647058823529411,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.42857142857142855,
          "f1-score": 0.375,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.672514619883041,
          "recall": 0.5150793650793651,
          "f1-score": 0.513235294117647,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6865497076023391,
          "recall": 0.6,
          "f1-score": 0.5765196078431372,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          2,
          4
        ],
        [
          0,
          13,
          2
        ],
        [
          0,
          4,
          3
        ]
      ],
      "class_labels": [
        "LEFT_HAND_IMAGERY",
        "REST",
        "RIGHT_HAND_IMAGERY"
      ],
      "calibration": {
        "available": false
      }
    }
  }
}
```