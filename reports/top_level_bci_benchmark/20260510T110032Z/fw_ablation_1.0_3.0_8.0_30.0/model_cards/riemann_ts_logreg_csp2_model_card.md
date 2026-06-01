# Model Card: fw_ablation_1.0_3.0_8.0_30.0_riemann_ts_logreg_csp2

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
  "accuracy": 0.5696969696969697,
  "balanced_accuracy": 0.5697178959741405,
  "macro_f1": 0.5696969696969697,
  "weighted_f1": 0.5696969696969697,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.573170731707317,
      "recall": 0.5662650602409639,
      "f1-score": 0.5696969696969697,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5662650602409639,
      "recall": 0.573170731707317,
      "f1-score": 0.5696969696969697,
      "support": 82.0
    },
    "accuracy": 0.5696969696969697,
    "macro avg": {
      "precision": 0.5697178959741405,
      "recall": 0.5697178959741405,
      "f1-score": 0.5696969696969697,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5697388222513112,
      "recall": 0.5696969696969697,
      "f1-score": 0.5696969696969697,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      47,
      36
    ],
    [
      35,
      47
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.17216511153803407,
    "mce": 0.2997835832794209,
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
        "count": 42,
        "accuracy": 0.6428571428571429,
        "confidence": 0.5444024882704367
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 53,
        "accuracy": 0.4339622641509434,
        "confidence": 0.6452951753919985
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 34,
        "accuracy": 0.5882352941176471,
        "confidence": 0.7443272131878343
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 25,
        "accuracy": 0.56,
        "confidence": 0.859783583279421
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 11,
        "accuracy": 0.9090909090909091,
        "confidence": 0.9336171622714684
      }
    ],
    "brier_score": 0.2658814273122085
  },
  "auroc": 0.5865412870996181,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 1.701118812177976,
    "p95_inference_latency_ms": 1.9771279994529323,
    "p99_inference_latency_ms": 2.3880497602294772,
    "throughput_samples_per_sec": 587.8484164898983
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.8125,
      "macro_f1": 0.7963800904977376,
      "weighted_f1": 0.7945701357466064,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7,
          "recall": 1.0,
          "f1-score": 0.8235294117647058,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.625,
          "f1-score": 0.7692307692307693,
          "support": 8.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.85,
          "recall": 0.8125,
          "f1-score": 0.7963800904977376,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8599999999999999,
          "recall": 0.8,
          "f1-score": 0.7945701357466064,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
        ],
        [
          3,
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.75,
      "macro_f1": 0.7222222222222222,
      "weighted_f1": 0.7185185185185186,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6363636363636364,
          "recall": 1.0,
          "f1-score": 0.7777777777777778,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.5,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.8181818181818181,
          "recall": 0.75,
          "f1-score": 0.7222222222222222,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8303030303030302,
          "recall": 0.7333333333333333,
          "f1-score": 0.7185185185185186,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.4107142857142857,
      "macro_f1": 0.3891402714932127,
      "weighted_f1": 0.38371040723981903,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.5714285714285714,
          "f1-score": 0.47058823529411764,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.25,
          "f1-score": 0.3076923076923077,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.4,
          "recall": 0.4107142857142857,
          "f1-score": 0.3891402714932127,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.4,
          "recall": 0.4,
          "f1-score": 0.38371040723981903,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          3
        ],
        [
          6,
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5777777777777777,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.375,
          "f1-score": 0.5,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.8571428571428571,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6477272727272727,
          "recall": 0.6160714285714286,
          "f1-score": 0.5833333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6545454545454545,
          "recall": 0.6,
          "f1-score": 0.5777777777777777,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          5
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
    "S005": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.375,
      "macro_f1": 0.2857142857142857,
      "weighted_f1": 0.30476190476190473,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.75,
          "f1-score": 0.5714285714285714,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.23076923076923078,
          "recall": 0.375,
          "f1-score": 0.2857142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.24615384615384617,
          "recall": 0.4,
          "f1-score": 0.30476190476190473,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7
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
    "S006": {
      "task_type": "classification",
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.4285714285714286,
      "macro_f1": 0.4276094276094276,
      "weighted_f1": 0.4314253647586981,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.47058823529411764,
          "recall": 0.5,
          "f1-score": 0.48484848484848486,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.38461538461538464,
          "recall": 0.35714285714285715,
          "f1-score": 0.37037037037037035,
          "support": 14.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.42760180995475117,
          "recall": 0.4285714285714286,
          "f1-score": 0.4276094276094276,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.43046757164404226,
          "recall": 0.43333333333333335,
          "f1-score": 0.4314253647586981,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          8,
          8
        ],
        [
          9,
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
    "S008": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.45535714285714285,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.45185185185185184,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.2857142857142857,
          "f1-score": 0.3333333333333333,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.625,
          "f1-score": 0.5555555555555556,
          "support": 8.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.45,
          "recall": 0.45535714285714285,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.45333333333333337,
          "recall": 0.4666666666666667,
          "f1-score": 0.45185185185185184,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          5
        ],
        [
          3,
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7321428571428572,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.75,
          "f1-score": 0.75,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.7142857142857143,
          "f1-score": 0.7142857142857143,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.7321428571428572,
          "recall": 0.7321428571428572,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7333333333333333,
          "recall": 0.7333333333333333,
          "f1-score": 0.7333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
        ],
        [
          2,
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
    "S010": {
      "task_type": "classification",
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.6339285714285714,
      "macro_f1": 0.6329254727474972,
      "weighted_f1": 0.6337411939191694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.625,
          "f1-score": 0.6451612903225806,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.6428571428571429,
          "f1-score": 0.6206896551724138,
          "support": 14.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6333333333333333,
          "recall": 0.6339285714285714,
          "f1-score": 0.6329254727474972,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6355555555555555,
          "recall": 0.6333333333333333,
          "f1-score": 0.6337411939191694,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          10,
          6
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5888888888888889,
      "balanced_accuracy": 0.5909090909090908,
      "macro_f1": 0.5863867842504037,
      "weighted_f1": 0.5856718972108365,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6216216216216216,
          "recall": 0.5,
          "f1-score": 0.5542168674698795,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5660377358490566,
          "recall": 0.6818181818181818,
          "f1-score": 0.6185567010309279,
          "support": 44.0
        },
        "accuracy": 0.5888888888888889,
        "macro avg": {
          "precision": 0.5938296787353391,
          "recall": 0.5909090909090908,
          "f1-score": 0.5863867842504037,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5944472774661453,
          "recall": 0.5888888888888889,
          "f1-score": 0.5856718972108365,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          23,
          23
        ],
        [
          14,
          30
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
      "balanced_accuracy": 0.6666666666666666,
      "macro_f1": 0.6651785714285714,
      "weighted_f1": 0.6651785714285715,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6470588235294118,
          "recall": 0.7333333333333333,
          "f1-score": 0.6875,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6923076923076923,
          "recall": 0.6,
          "f1-score": 0.6428571428571429,
          "support": 15.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6696832579185521,
          "recall": 0.6666666666666666,
          "f1-score": 0.6651785714285714,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.669683257918552,
          "recall": 0.6666666666666666,
          "f1-score": 0.6651785714285715,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          4
        ],
        [
          6,
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
      "balanced_accuracy": 0.46936758893280633,
      "macro_f1": 0.46,
      "weighted_f1": 0.45866666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4642857142857143,
          "recall": 0.5909090909090909,
          "f1-score": 0.52,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.47058823529411764,
          "recall": 0.34782608695652173,
          "f1-score": 0.4,
          "support": 23.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.46743697478991597,
          "recall": 0.46936758893280633,
          "f1-score": 0.46,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4675070028011205,
          "recall": 0.4666666666666667,
          "f1-score": 0.45866666666666667,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          13,
          9
        ],
        [
          15,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5716,
      "lower_95": 0.503,
      "upper_95": 0.6424
    },
    "balanced_accuracy": {
      "mean": 0.5716,
      "lower_95": 0.5025,
      "upper_95": 0.6446
    },
    "macro_f1": {
      "mean": 0.5702,
      "lower_95": 0.5023,
      "upper_95": 0.6424
    }
  }
}
```