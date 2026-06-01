# Model Card: fw_ablation_1.0_3.0_8.0_30.0_csp_lda_csp2

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
  "accuracy": 0.5212121212121212,
  "balanced_accuracy": 0.5202027622685865,
  "macro_f1": 0.5070156196815552,
  "weighted_f1": 0.507522637593361,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5181818181818182,
      "recall": 0.6867469879518072,
      "f1-score": 0.5906735751295337,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5272727272727272,
      "recall": 0.35365853658536583,
      "f1-score": 0.4233576642335766,
      "support": 82.0
    },
    "accuracy": 0.5212121212121212,
    "macro avg": {
      "precision": 0.5227272727272727,
      "recall": 0.5202027622685865,
      "f1-score": 0.5070156196815552,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5226997245179064,
      "recall": 0.5212121212121212,
      "f1-score": 0.507522637593361,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      57,
      26
    ],
    [
      53,
      29
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.13850284965512655,
    "mce": 0.23019172825897083,
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
        "count": 55,
        "accuracy": 0.509090909090909,
        "confidence": 0.5502853630738099
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 52,
        "accuracy": 0.4807692307692308,
        "confidence": 0.6555224483570293
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 44,
        "accuracy": 0.5454545454545454,
        "confidence": 0.7394097439350904
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 10,
        "accuracy": 0.6,
        "confidence": 0.8301917282589708
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 4,
        "accuracy": 0.75,
        "confidence": 0.9160404734342814
      }
    ],
    "brier_score": 0.2707841773471064
  },
  "auroc": 0.534528357331766,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.2945424242584109,
    "p95_inference_latency_ms": 0.3404655995836946,
    "p99_inference_latency_ms": 0.3869523198227396,
    "throughput_samples_per_sec": 3395.0966571887457
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5625,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4296296296296296,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 1.0,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.125,
          "f1-score": 0.2222222222222222,
          "support": 8.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.75,
          "recall": 0.5625,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7666666666666667,
          "recall": 0.5333333333333333,
          "f1-score": 0.4296296296296296,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.2,
      "balanced_accuracy": 0.19642857142857142,
      "macro_f1": 0.19642857142857142,
      "weighted_f1": 0.2,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.14285714285714285,
          "recall": 0.14285714285714285,
          "f1-score": 0.14285714285714285,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.25,
          "f1-score": 0.25,
          "support": 8.0
        },
        "accuracy": 0.2,
        "macro avg": {
          "precision": 0.19642857142857142,
          "recall": 0.19642857142857142,
          "f1-score": 0.19642857142857142,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.2,
          "recall": 0.2,
          "f1-score": 0.2,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          1,
          6
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
      "balanced_accuracy": 0.5044642857142857,
      "macro_f1": 0.4034090909090909,
      "weighted_f1": 0.42196969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5357142857142857,
          "recall": 0.9375,
          "f1-score": 0.6818181818181818,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.07142857142857142,
          "f1-score": 0.125,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5178571428571428,
          "recall": 0.5044642857142857,
          "f1-score": 0.4034090909090909,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5190476190476191,
          "recall": 0.5333333333333333,
          "f1-score": 0.42196969696969694,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          15,
          1
        ],
        [
          13,
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
    "S008": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5777777777777777,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.8571428571428571,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.375,
          "f1-score": 0.5,
          "support": 8.0
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
          6,
          1
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5714285714285714,
      "macro_f1": 0.48863636363636365,
      "weighted_f1": 0.5045454545454545,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 1.0,
          "f1-score": 0.7272727272727273,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.14285714285714285,
          "f1-score": 0.25,
          "support": 7.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.7857142857142857,
          "recall": 0.5714285714285714,
          "f1-score": 0.48863636363636365,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7714285714285715,
          "recall": 0.6,
          "f1-score": 0.5045454545454545,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          8,
          0
        ],
        [
          6,
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
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.45089285714285715,
      "macro_f1": 0.4258373205741627,
      "weighted_f1": 0.4360446570972887,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6875,
          "f1-score": 0.5789473684210527,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.375,
          "recall": 0.21428571428571427,
          "f1-score": 0.2727272727272727,
          "support": 14.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4375,
          "recall": 0.45089285714285715,
          "f1-score": 0.4258373205741627,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.44166666666666665,
          "recall": 0.4666666666666667,
          "f1-score": 0.4360446570972887,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          5
        ],
        [
          11,
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5555555555555556,
      "balanced_accuracy": 0.5543478260869565,
      "macro_f1": 0.5535714285714286,
      "weighted_f1": 0.5542328042328042,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.6086956521739131,
          "f1-score": 0.5833333333333334,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.55,
          "recall": 0.5,
          "f1-score": 0.5238095238095238,
          "support": 44.0
        },
        "accuracy": 0.5555555555555556,
        "macro avg": {
          "precision": 0.555,
          "recall": 0.5543478260869565,
          "f1-score": 0.5535714285714286,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5551111111111112,
          "recall": 0.5555555555555556,
          "f1-score": 0.5542328042328042,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          28,
          18
        ],
        [
          22,
          22
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
      "balanced_accuracy": 0.5333333333333333,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4444444444444444,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5185185185185185,
          "recall": 0.9333333333333333,
          "f1-score": 0.6666666666666666,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.13333333333333333,
          "f1-score": 0.2222222222222222,
          "support": 15.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5925925925925926,
          "recall": 0.5333333333333333,
          "f1-score": 0.4444444444444444,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5925925925925927,
          "recall": 0.5333333333333333,
          "f1-score": 0.4444444444444444,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          1
        ],
        [
          13,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.4444444444444444,
      "balanced_accuracy": 0.4496047430830039,
      "macro_f1": 0.41558441558441556,
      "weighted_f1": 0.4126984126984127,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.6818181818181818,
          "f1-score": 0.5454545454545454,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.21739130434782608,
          "f1-score": 0.2857142857142857,
          "support": 23.0
        },
        "accuracy": 0.4444444444444444,
        "macro avg": {
          "precision": 0.4356060606060606,
          "recall": 0.4496047430830039,
          "f1-score": 0.41558441558441556,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.43518518518518523,
          "recall": 0.4444444444444444,
          "f1-score": 0.4126984126984127,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          15,
          7
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
      "mean": 0.5205,
      "lower_95": 0.4424,
      "upper_95": 0.5939
    },
    "balanced_accuracy": {
      "mean": 0.52,
      "lower_95": 0.4449,
      "upper_95": 0.5948
    },
    "macro_f1": {
      "mean": 0.5049,
      "lower_95": 0.4266,
      "upper_95": 0.5805
    }
  }
}
```