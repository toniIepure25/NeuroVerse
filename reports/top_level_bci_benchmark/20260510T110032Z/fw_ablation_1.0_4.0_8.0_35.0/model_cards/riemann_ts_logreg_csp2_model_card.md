# Model Card: fw_ablation_1.0_4.0_8.0_35.0_riemann_ts_logreg_csp2

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
  "accuracy": 0.5878787878787879,
  "balanced_accuracy": 0.5880840434910373,
  "macro_f1": 0.5874999999999999,
  "weighted_f1": 0.5874242424242423,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5974025974025974,
      "recall": 0.5542168674698795,
      "f1-score": 0.575,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5795454545454546,
      "recall": 0.6219512195121951,
      "f1-score": 0.6,
      "support": 82.0
    },
    "accuracy": 0.5878787878787879,
    "macro avg": {
      "precision": 0.588474025974026,
      "recall": 0.5880840434910373,
      "f1-score": 0.5874999999999999,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5885281385281386,
      "recall": 0.5878787878787879,
      "f1-score": 0.5874242424242423,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      46,
      37
    ],
    [
      31,
      51
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.10778708384310902,
    "mce": 0.2509455619888611,
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
        "count": 45,
        "accuracy": 0.4888888888888889,
        "confidence": 0.5414801257103126
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 45,
        "accuracy": 0.6,
        "confidence": 0.6485994482648776
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 32,
        "accuracy": 0.625,
        "confidence": 0.750474475521357
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 35,
        "accuracy": 0.6,
        "confidence": 0.8509455619888611
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 8,
        "accuracy": 0.875,
        "confidence": 0.9291262648669836
      }
    ],
    "brier_score": 0.2540264707805918
  },
  "auroc": 0.6235674404936821,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 1.776556115135353,
    "p95_inference_latency_ms": 2.5004675993841365,
    "p99_inference_latency_ms": 3.0516577197340666,
    "throughput_samples_per_sec": 562.8868075038606
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6875,
      "macro_f1": 0.6411483253588517,
      "weighted_f1": 0.634768740031898,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 1.0,
          "f1-score": 0.7368421052631579,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.375,
          "f1-score": 0.5454545454545454,
          "support": 8.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.7916666666666667,
          "recall": 0.6875,
          "f1-score": 0.6411483253588517,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8055555555555556,
          "recall": 0.6666666666666666,
          "f1-score": 0.634768740031898,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
        ],
        [
          5,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.9333333333333333,
      "balanced_accuracy": 0.9375,
      "macro_f1": 0.9333333333333333,
      "weighted_f1": 0.9333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.875,
          "recall": 1.0,
          "f1-score": 0.9333333333333333,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.875,
          "f1-score": 0.9333333333333333,
          "support": 8.0
        },
        "accuracy": 0.9333333333333333,
        "macro avg": {
          "precision": 0.9375,
          "recall": 0.9375,
          "f1-score": 0.9333333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.9416666666666667,
          "recall": 0.9333333333333333,
          "f1-score": 0.9333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
        ],
        [
          1,
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.75,
      "macro_f1": 0.7222222222222222,
      "weighted_f1": 0.7185185185185186,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.5,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6363636363636364,
          "recall": 1.0,
          "f1-score": 0.7777777777777778,
          "support": 7.0
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
          4,
          4
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
    "S005": {
      "task_type": "classification",
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3125,
      "macro_f1": 0.25,
      "weighted_f1": 0.26666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.625,
          "f1-score": 0.5,
          "support": 8.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.20833333333333334,
          "recall": 0.3125,
          "f1-score": 0.25,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.22222222222222224,
          "recall": 0.3333333333333333,
          "f1-score": 0.26666666666666666,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7
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
    "S006": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5401785714285714,
      "macro_f1": 0.53125,
      "weighted_f1": 0.5291666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 0.4375,
          "f1-score": 0.5,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6428571428571429,
          "f1-score": 0.5625,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5416666666666667,
          "recall": 0.5401785714285714,
          "f1-score": 0.53125,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5444444444444445,
          "recall": 0.5333333333333333,
          "f1-score": 0.5291666666666667,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          9
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
    },
    "S008": {
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5982142857142857,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.6,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.625,
          "f1-score": 0.625,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5714285714285714,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5982142857142857,
          "recall": 0.5982142857142857,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.6,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
    "S010": {
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
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5714285714285714,
          "f1-score": 0.6153846153846154,
          "support": 14.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6666666666666666,
          "recall": 0.6607142857142857,
          "f1-score": 0.660633484162896,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6666666666666666,
          "recall": 0.6666666666666666,
          "f1-score": 0.6636500754147813,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          12,
          4
        ],
        [
          6,
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
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5777777777777777,
      "balanced_accuracy": 0.5800395256916996,
      "macro_f1": 0.5744151319064211,
      "weighted_f1": 0.573574470438582,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6111111111111112,
          "recall": 0.4782608695652174,
          "f1-score": 0.5365853658536586,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.6818181818181818,
          "f1-score": 0.6122448979591837,
          "support": 44.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5833333333333334,
          "recall": 0.5800395256916996,
          "f1-score": 0.5744151319064211,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5839506172839506,
          "recall": 0.5777777777777777,
          "f1-score": 0.573574470438582,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          22,
          24
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
      "accuracy": 0.7666666666666667,
      "balanced_accuracy": 0.7666666666666666,
      "macro_f1": 0.7643097643097643,
      "weighted_f1": 0.7643097643097643,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7222222222222222,
          "recall": 0.8666666666666667,
          "f1-score": 0.7878787878787878,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.6666666666666666,
          "f1-score": 0.7407407407407407,
          "support": 15.0
        },
        "accuracy": 0.7666666666666667,
        "macro avg": {
          "precision": 0.7777777777777778,
          "recall": 0.7666666666666666,
          "f1-score": 0.7643097643097643,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7777777777777779,
          "recall": 0.7666666666666667,
          "f1-score": 0.7643097643097643,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          2
        ],
        [
          5,
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
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.4891304347826087,
      "macro_f1": 0.4888888888888889,
      "weighted_f1": 0.4888888888888889,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4782608695652174,
          "recall": 0.5,
          "f1-score": 0.4888888888888889,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.4782608695652174,
          "f1-score": 0.4888888888888889,
          "support": 23.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.4891304347826087,
          "recall": 0.4891304347826087,
          "f1-score": 0.4888888888888889,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4893719806763285,
          "recall": 0.4888888888888889,
          "f1-score": 0.4888888888888889,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          11,
          11
        ],
        [
          12,
          11
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
      "mean": 0.5887,
      "lower_95": 0.512,
      "upper_95": 0.6698
    },
    "balanced_accuracy": {
      "mean": 0.5889,
      "lower_95": 0.5116,
      "upper_95": 0.6702
    },
    "macro_f1": {
      "mean": 0.5868,
      "lower_95": 0.5077,
      "upper_95": 0.6686
    }
  }
}
```