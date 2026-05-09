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
  "accuracy": 0.5083333333333333,
  "balanced_accuracy": 0.47845754542083796,
  "macro_f1": 0.47947993216506496,
  "weighted_f1": 0.5067486338797814,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.41379310344827586,
      "recall": 0.3870967741935484,
      "f1-score": 0.4,
      "support": 31.0
    },
    "REST": {
      "precision": 0.5806451612903226,
      "recall": 0.6,
      "f1-score": 0.5901639344262295,
      "support": 60.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4482758620689655,
      "recall": 0.4482758620689655,
      "f1-score": 0.4482758620689655,
      "support": 29.0
    },
    "accuracy": 0.5083333333333333,
    "macro avg": {
      "precision": 0.4809047089358547,
      "recall": 0.47845754542083796,
      "f1-score": 0.47947993216506496,
      "support": 120.0
    },
    "weighted avg": {
      "precision": 0.5055524657026326,
      "recall": 0.5083333333333333,
      "f1-score": 0.5067486338797814,
      "support": 120.0
    }
  },
  "confusion_matrix": [
    [
      12,
      13,
      6
    ],
    [
      14,
      36,
      10
    ],
    [
      3,
      13,
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
    "ece": 0.2970258174203062,
    "mce": 0.4831187483092238,
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
        "confidence": 0.35712981411749534
      },
      {
        "lo": 0.4,
        "hi": 0.5,
        "count": 3,
        "accuracy": 0.0,
        "confidence": 0.4831187483092238
      },
      {
        "lo": 0.5,
        "hi": 0.6,
        "count": 12,
        "accuracy": 0.4166666666666667,
        "confidence": 0.548398169205312
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 20,
        "accuracy": 0.5,
        "confidence": 0.6518502336976775
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 18,
        "accuracy": 0.4444444444444444,
        "confidence": 0.7396662135318609
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 15,
        "accuracy": 0.6,
        "confidence": 0.8440683829100556
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 51,
        "accuracy": 0.5686274509803921,
        "confidence": 0.9655649360735284
      }
    ]
  },
  "auroc_ovr_macro": 0.6547949319158278,
  "latency": {
    "mean_inference_latency_ms": 0.3486869086070025,
    "p95_inference_latency_ms": 0.3624702960223658,
    "p99_inference_latency_ms": 0.3984187906462467,
    "throughput_samples_per_sec": 2867.902336783967
  },
  "split_strategy": "group_run",
  "split_warnings": [],
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4777777777777778,
      "macro_f1": 0.46352413019079686,
      "weighted_f1": 0.468013468013468,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3888888888888889,
          "recall": 0.4666666666666667,
          "f1-score": 0.42424242424242425,
          "support": 15.0
        },
        "REST": {
          "precision": 0.5416666666666666,
          "recall": 0.43333333333333335,
          "f1-score": 0.48148148148148145,
          "support": 30.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5333333333333333,
          "f1-score": 0.48484848484848486,
          "support": 15.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4583333333333333,
          "recall": 0.4777777777777778,
          "f1-score": 0.46352413019079686,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4791666666666667,
          "recall": 0.4666666666666667,
          "f1-score": 0.468013468013468,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          7,
          6,
          2
        ],
        [
          9,
          13,
          8
        ],
        [
          2,
          5,
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
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.5626984126984127,
      "macro_f1": 0.5549019607843136,
      "weighted_f1": 0.6056862745098038,
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
          "precision": 0.4444444444444444,
          "recall": 0.5714285714285714,
          "f1-score": 0.5,
          "support": 7.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.709551656920078,
          "recall": 0.5626984126984127,
          "f1-score": 0.5549019607843136,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7124756335282652,
          "recall": 0.6333333333333333,
          "f1-score": 0.6056862745098038,
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
          0,
          13,
          2
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
      "macro_f1": 0.42782446311858074,
      "weighted_f1": 0.43337068160597575,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.2857142857142857,
          "f1-score": 0.26666666666666666,
          "support": 7.0
        },
        "REST": {
          "precision": 0.46153846153846156,
          "recall": 0.4,
          "f1-score": 0.42857142857142855,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.625,
          "f1-score": 0.5882352941176471,
          "support": 8.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.42236467236467234,
          "recall": 0.4369047619047619,
          "f1-score": 0.42782446311858074,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.43725071225071227,
          "recall": 0.43333333333333335,
          "f1-score": 0.43337068160597575,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          5,
          0
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
      "macro_f1": 0.4479365079365079,
      "weighted_f1": 0.4799047619047619,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42105263157894735,
          "recall": 0.5,
          "f1-score": 0.45714285714285713,
          "support": 16.0
        },
        "REST": {
          "precision": 0.5666666666666667,
          "recall": 0.5666666666666667,
          "f1-score": 0.5666666666666667,
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
          "precision": 0.4504518872939925,
          "recall": 0.4507936507936508,
          "f1-score": 0.4479365079365079,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.48046251993620415,
          "recall": 0.48333333333333334,
          "f1-score": 0.4799047619047619,
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
          2,
          8,
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
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.5626984126984127,
      "macro_f1": 0.5549019607843136,
      "weighted_f1": 0.6056862745098038,
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
          "precision": 0.4444444444444444,
          "recall": 0.5714285714285714,
          "f1-score": 0.5,
          "support": 7.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.709551656920078,
          "recall": 0.5626984126984127,
          "f1-score": 0.5549019607843136,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7124756335282652,
          "recall": 0.6333333333333333,
          "f1-score": 0.6056862745098038,
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
          0,
          13,
          2
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