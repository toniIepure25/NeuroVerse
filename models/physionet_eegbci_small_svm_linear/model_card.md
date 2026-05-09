# Model Card: physionet_eegbci_small_svm_linear

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
  "accuracy": 0.49166666666666664,
  "balanced_accuracy": 0.47254356692621435,
  "macro_f1": 0.4692250648869114,
  "weighted_f1": 0.4941601779755284,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.41935483870967744,
      "recall": 0.41935483870967744,
      "f1-score": 0.41935483870967744,
      "support": 31.0
    },
    "REST": {
      "precision": 0.5892857142857143,
      "recall": 0.55,
      "f1-score": 0.5689655172413793,
      "support": 60.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.3939393939393939,
      "recall": 0.4482758620689655,
      "f1-score": 0.41935483870967744,
      "support": 29.0
    },
    "accuracy": 0.49166666666666664,
    "macro avg": {
      "precision": 0.46752664897826185,
      "recall": 0.47254356692621435,
      "f1-score": 0.4692250648869114,
      "support": 120.0
    },
    "weighted avg": {
      "precision": 0.4981782106782107,
      "recall": 0.49166666666666664,
      "f1-score": 0.4941601779755284,
      "support": 120.0
    }
  },
  "confusion_matrix": [
    [
      13,
      9,
      9
    ],
    [
      16,
      33,
      11
    ],
    [
      2,
      14,
      13
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "REST",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.06304591480479577,
    "mce": 0.14998170476697154,
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
        "count": 7,
        "accuracy": 0.42857142857142855,
        "confidence": 0.3785303781118305
      },
      {
        "lo": 0.4,
        "hi": 0.5,
        "count": 29,
        "accuracy": 0.3103448275862069,
        "confidence": 0.46032653235317844
      },
      {
        "lo": 0.5,
        "hi": 0.6,
        "count": 49,
        "accuracy": 0.5510204081632653,
        "confidence": 0.5525201073718524
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 22,
        "accuracy": 0.6818181818181818,
        "confidence": 0.6341490475073773
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 13,
        "accuracy": 0.6153846153846154,
        "confidence": 0.7495035976198202
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
    ]
  },
  "auroc_ovr_macro": 0.6565549476466724,
  "latency": {
    "mean_inference_latency_ms": 0.34020207501725963,
    "p95_inference_latency_ms": 0.3809326498867449,
    "p99_inference_latency_ms": 0.45033632036393106,
    "throughput_samples_per_sec": 2939.4294551238895
  },
  "split_strategy": "group_run",
  "split_warnings": [],
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.45,
      "balanced_accuracy": 0.4666666666666666,
      "macro_f1": 0.44922028273859577,
      "weighted_f1": 0.4501227592237581,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42105263157894735,
          "recall": 0.5333333333333333,
          "f1-score": 0.47058823529411764,
          "support": 15.0
        },
        "REST": {
          "precision": 0.5217391304347826,
          "recall": 0.4,
          "f1-score": 0.4528301886792453,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3888888888888889,
          "recall": 0.4666666666666667,
          "f1-score": 0.42424242424242425,
          "support": 15.0
        },
        "accuracy": 0.45,
        "macro avg": {
          "precision": 0.44389355030087296,
          "recall": 0.4666666666666666,
          "f1-score": 0.44922028273859577,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.46335494533435034,
          "recall": 0.45,
          "f1-score": 0.4501227592237581,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          8,
          4,
          3
        ],
        [
          10,
          12,
          8
        ],
        [
          1,
          7,
          7
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
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.5626984126984127,
      "macro_f1": 0.5538918597742127,
      "weighted_f1": 0.603767082590612,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.25,
          "f1-score": 0.36363636363636365,
          "support": 8.0
        },
        "REST": {
          "precision": 0.6842105263157895,
          "recall": 0.8666666666666667,
          "f1-score": 0.7647058823529411,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5714285714285714,
          "f1-score": 0.5333333333333333,
          "support": 7.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6169590643274854,
          "recall": 0.5626984126984127,
          "f1-score": 0.5538918597742127,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6365497076023392,
          "recall": 0.6333333333333333,
          "f1-score": 0.603767082590612,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          3,
          3
        ],
        [
          1,
          13,
          1
        ],
        [
          0,
          3,
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.398015873015873,
      "macro_f1": 0.3967932000386362,
      "weighted_f1": 0.4366463826910075,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.375,
          "f1-score": 0.35294117647058826,
          "support": 8.0
        },
        "REST": {
          "precision": 0.5714285714285714,
          "recall": 0.5333333333333333,
          "f1-score": 0.5517241379310345,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2857142857142857,
          "recall": 0.2857142857142857,
          "f1-score": 0.2857142857142857,
          "support": 7.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.39682539682539675,
          "recall": 0.398015873015873,
          "f1-score": 0.3967932000386362,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.44126984126984126,
          "recall": 0.43333333333333335,
          "f1-score": 0.4366463826910075,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          2,
          3
        ],
        [
          5,
          8,
          2
        ],
        [
          1,
          4,
          2
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
      "balanced_accuracy": 0.44285714285714284,
      "macro_f1": 0.43246187363834426,
      "weighted_f1": 0.43790849673202614,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3,
          "recall": 0.42857142857142855,
          "f1-score": 0.35294117647058826,
          "support": 7.0
        },
        "REST": {
          "precision": 0.5,
          "recall": 0.4,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5,
          "f1-score": 0.5,
          "support": 8.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.43333333333333335,
          "recall": 0.44285714285714284,
          "f1-score": 0.43246187363834426,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.4533333333333333,
          "recall": 0.43333333333333335,
          "f1-score": 0.43790849673202614,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          3,
          1
        ],
        [
          6,
          6,
          3
        ],
        [
          1,
          3,
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.45,
      "balanced_accuracy": 0.44126984126984126,
      "macro_f1": 0.434086596515439,
      "weighted_f1": 0.45530446782818695,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5,
          "f1-score": 0.47058823529411764,
          "support": 16.0
        },
        "REST": {
          "precision": 0.56,
          "recall": 0.4666666666666667,
          "f1-score": 0.509090909090909,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.29411764705882354,
          "recall": 0.35714285714285715,
          "f1-score": 0.3225806451612903,
          "support": 14.0
        },
        "accuracy": 0.45,
        "macro avg": {
          "precision": 0.43285403050108934,
          "recall": 0.44126984126984126,
          "f1-score": 0.434086596515439,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4671459694989107,
          "recall": 0.45,
          "f1-score": 0.45530446782818695,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          8,
          3,
          5
        ],
        [
          9,
          14,
          7
        ],
        [
          1,
          8,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.5626984126984127,
      "macro_f1": 0.5538918597742127,
      "weighted_f1": 0.603767082590612,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.25,
          "f1-score": 0.36363636363636365,
          "support": 8.0
        },
        "REST": {
          "precision": 0.6842105263157895,
          "recall": 0.8666666666666667,
          "f1-score": 0.7647058823529411,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5714285714285714,
          "f1-score": 0.5333333333333333,
          "support": 7.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6169590643274854,
          "recall": 0.5626984126984127,
          "f1-score": 0.5538918597742127,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6365497076023392,
          "recall": 0.6333333333333333,
          "f1-score": 0.603767082590612,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          3,
          3
        ],
        [
          1,
          13,
          1
        ],
        [
          0,
          3,
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
    }
  }
}
```