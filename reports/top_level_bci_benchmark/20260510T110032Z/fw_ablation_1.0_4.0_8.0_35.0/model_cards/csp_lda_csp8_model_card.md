# Model Card: fw_ablation_1.0_4.0_8.0_35.0_csp_lda_csp8

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
  "accuracy": 0.5515151515151515,
  "balanced_accuracy": 0.5506171025565678,
  "macro_f1": 0.5409774436090226,
  "weighted_f1": 0.5413989519252678,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5420560747663551,
      "recall": 0.6987951807228916,
      "f1-score": 0.6105263157894737,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5689655172413793,
      "recall": 0.4024390243902439,
      "f1-score": 0.4714285714285714,
      "support": 82.0
    },
    "accuracy": 0.5515151515151515,
    "macro avg": {
      "precision": 0.5555107960038672,
      "recall": 0.5506171025565678,
      "f1-score": 0.5409774436090226,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5554292522387914,
      "recall": 0.5515151515151515,
      "f1-score": 0.5413989519252678,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      58,
      25
    ],
    [
      49,
      33
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.1657951613653556,
    "mce": 0.35553989683244724,
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
        "count": 48,
        "accuracy": 0.4791666666666667,
        "confidence": 0.5460829975489631
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 33,
        "accuracy": 0.6060606060606061,
        "confidence": 0.6453872126708066
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 31,
        "accuracy": 0.5483870967741935,
        "confidence": 0.7480767541959042
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 28,
        "accuracy": 0.5714285714285714,
        "confidence": 0.8488415329968791
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 25,
        "accuracy": 0.6,
        "confidence": 0.9555398968324472
      }
    ],
    "brier_score": 0.28492949224963215
  },
  "auroc": 0.5830149867763739,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.32088990909401083,
    "p95_inference_latency_ms": 0.43897080013266526,
    "p99_inference_latency_ms": 0.5133134402785796,
    "throughput_samples_per_sec": 3116.333582515463
  },
  "per_subject": {
    "S001": {
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.875,
      "macro_f1": 0.8660714285714286,
      "weighted_f1": 0.8654761904761905,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7777777777777778,
          "recall": 1.0,
          "f1-score": 0.875,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.75,
          "f1-score": 0.8571428571428571,
          "support": 8.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.8888888888888888,
          "recall": 0.875,
          "f1-score": 0.8660714285714286,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8962962962962963,
          "recall": 0.8666666666666667,
          "f1-score": 0.8654761904761905,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
        ],
        [
          2,
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
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3214285714285714,
      "macro_f1": 0.3055555555555555,
      "weighted_f1": 0.31481481481481477,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.2,
          "recall": 0.14285714285714285,
          "f1-score": 0.16666666666666666,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.5,
          "f1-score": 0.4444444444444444,
          "support": 8.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.30000000000000004,
          "recall": 0.3214285714285714,
          "f1-score": 0.3055555555555555,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3066666666666667,
          "recall": 0.3333333333333333,
          "f1-score": 0.31481481481481477,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          1,
          6
        ],
        [
          4,
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6607142857142857,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6636500754147813,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.75,
          "f1-score": 0.7058823529411765,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5714285714285714,
          "f1-score": 0.6153846153846154,
          "support": 7.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6666666666666666,
          "recall": 0.6607142857142857,
          "f1-score": 0.660633484162896,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6666666666666666,
          "recall": 0.6666666666666666,
          "f1-score": 0.6636500754147813,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
    "S005": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.34782608695652173,
      "weighted_f1": 0.3710144927536232,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 1.0,
          "f1-score": 0.6956521739130435,
          "support": 8.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.26666666666666666,
          "recall": 0.5,
          "f1-score": 0.34782608695652173,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.28444444444444444,
          "recall": 0.5333333333333333,
          "f1-score": 0.3710144927536232,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7
        ],
        [
          0,
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
    "S006": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.34782608695652173,
      "weighted_f1": 0.3710144927536232,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 1.0,
          "f1-score": 0.6956521739130435,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.26666666666666666,
          "recall": 0.5,
          "f1-score": 0.34782608695652173,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.28444444444444444,
          "recall": 0.5333333333333333,
          "f1-score": 0.3710144927536232,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          16,
          0
        ],
        [
          14,
          0
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
    "S008": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.41964285714285715,
      "macro_f1": 0.354066985645933,
      "weighted_f1": 0.34258373205741627,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.7142857142857143,
          "f1-score": 0.5263157894736842,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.125,
          "f1-score": 0.18181818181818182,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.375,
          "recall": 0.41964285714285715,
          "f1-score": 0.354066985645933,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3722222222222223,
          "recall": 0.4,
          "f1-score": 0.34258373205741627,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5892857142857143,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5888888888888888,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.75,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.42857142857142855,
          "f1-score": 0.5,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6,
          "recall": 0.5892857142857143,
          "f1-score": 0.5833333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.5888888888888888,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
    "S010": {
      "task_type": "classification",
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5580357142857143,
      "macro_f1": 0.5542857142857143,
      "weighted_f1": 0.5592380952380952,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5789473684210527,
          "recall": 0.6875,
          "f1-score": 0.6285714285714286,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.42857142857142855,
          "f1-score": 0.48,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.562200956937799,
          "recall": 0.5580357142857143,
          "f1-score": 0.5542857142857143,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.563317384370016,
          "recall": 0.5666666666666667,
          "f1-score": 0.5592380952380952,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          5
        ],
        [
          8,
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
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5555555555555556,
      "balanced_accuracy": 0.5533596837944664,
      "macro_f1": 0.55,
      "weighted_f1": 0.551111111111111,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.6521739130434783,
          "f1-score": 0.6,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.45454545454545453,
          "f1-score": 0.5,
          "support": 44.0
        },
        "accuracy": 0.5555555555555556,
        "macro avg": {
          "precision": 0.5555555555555556,
          "recall": 0.5533596837944664,
          "f1-score": 0.55,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5555555555555556,
          "recall": 0.5555555555555556,
          "f1-score": 0.551111111111111,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          30,
          16
        ],
        [
          24,
          20
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7333333333333334,
      "macro_f1": 0.7222222222222222,
      "weighted_f1": 0.7222222222222221,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.9333333333333333,
          "f1-score": 0.7777777777777778,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8888888888888888,
          "recall": 0.5333333333333333,
          "f1-score": 0.6666666666666666,
          "support": 15.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.7777777777777777,
          "recall": 0.7333333333333334,
          "f1-score": 0.7222222222222222,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7777777777777778,
          "recall": 0.7333333333333333,
          "f1-score": 0.7222222222222221,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          1
        ],
        [
          7,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.4222222222222222,
      "balanced_accuracy": 0.4268774703557312,
      "macro_f1": 0.39814814814814814,
      "weighted_f1": 0.3954732510288066,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4375,
          "recall": 0.6363636363636364,
          "f1-score": 0.5185185185185185,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.38461538461538464,
          "recall": 0.21739130434782608,
          "f1-score": 0.2777777777777778,
          "support": 23.0
        },
        "accuracy": 0.4222222222222222,
        "macro avg": {
          "precision": 0.4110576923076923,
          "recall": 0.4268774703557312,
          "f1-score": 0.39814814814814814,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.41047008547008546,
          "recall": 0.4222222222222222,
          "f1-score": 0.3954732510288066,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          14,
          8
        ],
        [
          18,
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5526,
      "lower_95": 0.4848,
      "upper_95": 0.6214
    },
    "balanced_accuracy": {
      "mean": 0.5521,
      "lower_95": 0.4877,
      "upper_95": 0.6223
    },
    "macro_f1": {
      "mean": 0.5404,
      "lower_95": 0.4718,
      "upper_95": 0.6114
    }
  }
}
```