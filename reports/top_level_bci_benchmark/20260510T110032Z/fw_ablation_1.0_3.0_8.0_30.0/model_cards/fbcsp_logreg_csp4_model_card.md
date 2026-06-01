# Model Card: fw_ablation_1.0_3.0_8.0_30.0_fbcsp_logreg_csp4

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
  "accuracy": 0.6121212121212121,
  "balanced_accuracy": 0.6123273582133412,
  "macro_f1": 0.611764705882353,
  "weighted_f1": 0.6116934046345811,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.6233766233766234,
      "recall": 0.5783132530120482,
      "f1-score": 0.6,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6022727272727273,
      "recall": 0.6463414634146342,
      "f1-score": 0.6235294117647059,
      "support": 82.0
    },
    "accuracy": 0.6121212121212121,
    "macro avg": {
      "precision": 0.6128246753246753,
      "recall": 0.6123273582133412,
      "f1-score": 0.611764705882353,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.6128886265249901,
      "recall": 0.6121212121212121,
      "f1-score": 0.6116934046345811,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      48,
      35
    ],
    [
      29,
      53
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.18633032315206927,
    "mce": 0.3642612161141674,
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
        "count": 18,
        "accuracy": 0.5555555555555556,
        "confidence": 0.5468131230970701
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 29,
        "accuracy": 0.6206896551724138,
        "confidence": 0.6481287892279659
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 29,
        "accuracy": 0.6896551724137931,
        "confidence": 0.7523398888352612
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 36,
        "accuracy": 0.6111111111111112,
        "confidence": 0.8518806504987289
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 53,
        "accuracy": 0.5849056603773585,
        "confidence": 0.9491668764915259
      }
    ],
    "brier_score": 0.2895848429548944
  },
  "auroc": 0.6103438142815163,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.438917260630908,
    "p95_inference_latency_ms": 8.229650999601288,
    "p99_inference_latency_ms": 8.945305640008879,
    "throughput_samples_per_sec": 134.42816541223206
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
      "balanced_accuracy": 0.7321428571428572,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.7142857142857143,
          "f1-score": 0.7142857142857143,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.75,
          "f1-score": 0.75,
          "support": 8.0
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
          5,
          2
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.6026785714285714,
      "macro_f1": 0.6,
      "weighted_f1": 0.6,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6428571428571429,
          "recall": 0.5625,
          "f1-score": 0.6,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5625,
          "recall": 0.6428571428571429,
          "f1-score": 0.6,
          "support": 14.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6026785714285714,
          "recall": 0.6026785714285714,
          "f1-score": 0.6,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6053571428571428,
          "recall": 0.6,
          "f1-score": 0.6,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          9,
          7
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6607142857142857,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6636500754147813,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5714285714285714,
          "f1-score": 0.6153846153846154,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.75,
          "f1-score": 0.7058823529411765,
          "support": 8.0
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
          4,
          3
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.5848214285714286,
      "macro_f1": 0.569377990430622,
      "weighted_f1": 0.5770334928229666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5909090909090909,
          "recall": 0.8125,
          "f1-score": 0.6842105263157895,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.35714285714285715,
          "f1-score": 0.45454545454545453,
          "support": 14.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6079545454545454,
          "recall": 0.5848214285714286,
          "f1-score": 0.569377990430622,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6068181818181818,
          "recall": 0.6,
          "f1-score": 0.5770334928229666,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          3
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.6555555555555556,
      "balanced_accuracy": 0.6566205533596838,
      "macro_f1": 0.6551724137931034,
      "weighted_f1": 0.6549169859514686,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6829268292682927,
          "recall": 0.6086956521739131,
          "f1-score": 0.6436781609195402,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6326530612244898,
          "recall": 0.7045454545454546,
          "f1-score": 0.6666666666666666,
          "support": 44.0
        },
        "accuracy": 0.6555555555555556,
        "macro avg": {
          "precision": 0.6577899452463913,
          "recall": 0.6566205533596838,
          "f1-score": 0.6551724137931034,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.6583485426691001,
          "recall": 0.6555555555555556,
          "f1-score": 0.6549169859514686,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          28,
          18
        ],
        [
          13,
          31
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
      "balanced_accuracy": 0.6666666666666667,
      "macro_f1": 0.6527777777777778,
      "weighted_f1": 0.6527777777777779,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6190476190476191,
          "recall": 0.8666666666666667,
          "f1-score": 0.7222222222222222,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7777777777777778,
          "recall": 0.4666666666666667,
          "f1-score": 0.5833333333333334,
          "support": 15.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6984126984126984,
          "recall": 0.6666666666666667,
          "f1-score": 0.6527777777777778,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6984126984126984,
          "recall": 0.6666666666666666,
          "f1-score": 0.6527777777777779,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          2
        ],
        [
          8,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.4851778656126482,
      "macro_f1": 0.4722080571137175,
      "weighted_f1": 0.47429316108561387,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 0.3181818181818182,
          "f1-score": 0.3783783783783784,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6521739130434783,
          "f1-score": 0.5660377358490566,
          "support": 23.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.48333333333333334,
          "recall": 0.4851778656126482,
          "f1-score": 0.4722080571137175,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4837037037037037,
          "recall": 0.4888888888888889,
          "f1-score": 0.47429316108561387,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          7,
          15
        ],
        [
          8,
          15
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
      "mean": 0.6115,
      "lower_95": 0.5394,
      "upper_95": 0.682
    },
    "balanced_accuracy": {
      "mean": 0.6115,
      "lower_95": 0.5407,
      "upper_95": 0.6834
    },
    "macro_f1": {
      "mean": 0.6095,
      "lower_95": 0.5376,
      "upper_95": 0.682
    }
  }
}
```