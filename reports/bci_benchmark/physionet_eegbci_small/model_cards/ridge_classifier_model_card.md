# Model Card: physionet_eegbci_small_ridge_classifier

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
  "accuracy": 0.4166666666666667,
  "balanced_accuracy": 0.35572858731924356,
  "macro_f1": 0.3546262626262626,
  "weighted_f1": 0.40979292929292926,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.2413793103448276,
      "recall": 0.22580645161290322,
      "f1-score": 0.23333333333333334,
      "support": 31.0
    },
    "REST": {
      "precision": 0.5538461538461539,
      "recall": 0.6,
      "f1-score": 0.576,
      "support": 60.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.2692307692307692,
      "recall": 0.2413793103448276,
      "f1-score": 0.2545454545454545,
      "support": 29.0
    },
    "accuracy": 0.4166666666666667,
    "macro avg": {
      "precision": 0.35481874447391687,
      "recall": 0.35572858731924356,
      "f1-score": 0.3546262626262626,
      "support": 120.0
    },
    "weighted avg": {
      "precision": 0.40434350132626,
      "recall": 0.4166666666666667,
      "f1-score": 0.40979292929292926,
      "support": 120.0
    }
  },
  "confusion_matrix": [
    [
      7,
      15,
      9
    ],
    [
      14,
      36,
      10
    ],
    [
      8,
      14,
      7
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "REST",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.21488936669908063,
    "mce": 0.4179867566363116,
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
        "count": 8,
        "accuracy": 0.25,
        "confidence": 0.38301678666888106
      },
      {
        "lo": 0.4,
        "hi": 0.5,
        "count": 29,
        "accuracy": 0.3103448275862069,
        "confidence": 0.44537495427980756
      },
      {
        "lo": 0.5,
        "hi": 0.6,
        "count": 26,
        "accuracy": 0.23076923076923078,
        "confidence": 0.5514258841651228
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 21,
        "accuracy": 0.42857142857142855,
        "confidence": 0.6435563083548281
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 16,
        "accuracy": 0.6875,
        "confidence": 0.7530188318612253
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 5,
        "accuracy": 1.0,
        "confidence": 0.8726284173289309
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 15,
        "accuracy": 0.5333333333333333,
        "confidence": 0.9513200899696449
      }
    ]
  },
  "auroc_ovr_macro": 0.5684175449558023,
  "latency": {
    "mean_inference_latency_ms": 0.36420796670123917,
    "p95_inference_latency_ms": 0.40545099959672365,
    "p99_inference_latency_ms": 0.4755389394904342,
    "throughput_samples_per_sec": 2745.6840361218756
  },
  "split_strategy": "group_run",
  "split_warnings": [],
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.35555555555555557,
      "macro_f1": 0.35648934163365403,
      "weighted_f1": 0.40771788341822296,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.26666666666666666,
          "f1-score": 0.25806451612903225,
          "support": 15.0
        },
        "REST": {
          "precision": 0.5925925925925926,
          "recall": 0.5333333333333333,
          "f1-score": 0.5614035087719298,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.23529411764705882,
          "recall": 0.26666666666666666,
          "f1-score": 0.25,
          "support": 15.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.35929557007988383,
          "recall": 0.35555555555555557,
          "f1-score": 0.35648934163365403,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.41761982570806105,
          "recall": 0.4,
          "f1-score": 0.40771788341822296,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          4,
          5,
          6
        ],
        [
          7,
          16,
          7
        ],
        [
          5,
          6,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.46468253968253964,
      "macro_f1": 0.4650641025641025,
      "weighted_f1": 0.5222115384615384,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.375,
          "f1-score": 0.4,
          "support": 8.0
        },
        "REST": {
          "precision": 0.6470588235294118,
          "recall": 0.7333333333333333,
          "f1-score": 0.6875,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.2857142857142857,
          "f1-score": 0.3076923076923077,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.46965452847805783,
          "recall": 0.46468253968253964,
          "f1-score": 0.4650641025641025,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.515592903828198,
          "recall": 0.5333333333333333,
          "f1-score": 0.5222115384615384,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          3,
          2
        ],
        [
          2,
          11,
          2
        ],
        [
          2,
          3,
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
    },
    "S003": {
      "task_type": "classification",
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.24761904761904763,
      "macro_f1": 0.2333333333333333,
      "weighted_f1": 0.2966666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "REST": {
          "precision": 0.42857142857142855,
          "recall": 0.6,
          "f1-score": 0.5,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.14285714285714285,
          "f1-score": 0.2,
          "support": 7.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.25396825396825395,
          "recall": 0.24761904761904763,
          "f1-score": 0.2333333333333333,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.292063492063492,
          "recall": 0.3333333333333333,
          "f1-score": 0.2966666666666667,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7,
          1
        ],
        [
          5,
          9,
          1
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
      "accuracy": 0.26666666666666666,
      "balanced_accuracy": 0.21666666666666667,
      "macro_f1": 0.2222222222222222,
      "weighted_f1": 0.28148148148148144,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "REST": {
          "precision": 0.5,
          "recall": 0.4,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2,
          "recall": 0.25,
          "f1-score": 0.2222222222222222,
          "support": 8.0
        },
        "accuracy": 0.26666666666666666,
        "macro avg": {
          "precision": 0.2333333333333333,
          "recall": 0.21666666666666667,
          "f1-score": 0.2222222222222222,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.30333333333333334,
          "recall": 0.26666666666666666,
          "f1-score": 0.28148148148148144,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          0,
          3,
          4
        ],
        [
          5,
          6,
          4
        ],
        [
          3,
          3,
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
    },
    "4": {
      "task_type": "classification",
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.36587301587301585,
      "macro_f1": 0.36414141414141415,
      "weighted_f1": 0.4173232323232323,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.2857142857142857,
          "recall": 0.25,
          "f1-score": 0.26666666666666666,
          "support": 16.0
        },
        "REST": {
          "precision": 0.5277777777777778,
          "recall": 0.6333333333333333,
          "f1-score": 0.5757575757575758,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3,
          "recall": 0.21428571428571427,
          "f1-score": 0.25,
          "support": 14.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.3711640211640212,
          "recall": 0.36587301587301585,
          "f1-score": 0.36414141414141415,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4100793650793651,
          "recall": 0.43333333333333335,
          "f1-score": 0.4173232323232323,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          4,
          9,
          3
        ],
        [
          7,
          19,
          4
        ],
        [
          3,
          8,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.46468253968253964,
      "macro_f1": 0.4650641025641025,
      "weighted_f1": 0.5222115384615384,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.375,
          "f1-score": 0.4,
          "support": 8.0
        },
        "REST": {
          "precision": 0.6470588235294118,
          "recall": 0.7333333333333333,
          "f1-score": 0.6875,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.2857142857142857,
          "f1-score": 0.3076923076923077,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.46965452847805783,
          "recall": 0.46468253968253964,
          "f1-score": 0.4650641025641025,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.515592903828198,
          "recall": 0.5333333333333333,
          "f1-score": 0.5222115384615384,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          3,
          2
        ],
        [
          2,
          11,
          2
        ],
        [
          2,
          3,
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
  }
}
```