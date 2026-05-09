# Model Card: physionet_eegbci_medium_csp_lda_csp4

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
  "balanced_accuracy": 0.5684689979429915,
  "macro_f1": 0.5506156737887913,
  "weighted_f1": 0.5511768883743259,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5517241379310345,
      "recall": 0.7710843373493976,
      "f1-score": 0.6432160804020101,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6122448979591837,
      "recall": 0.36585365853658536,
      "f1-score": 0.4580152671755725,
      "support": 82.0
    },
    "accuracy": 0.5696969696969697,
    "macro avg": {
      "precision": 0.5819845179451091,
      "recall": 0.5684689979429915,
      "f1-score": 0.5506156737887913,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5818011217025996,
      "recall": 0.5696969696969697,
      "f1-score": 0.5511768883743259,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      64,
      19
    ],
    [
      52,
      30
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.14917845154949053,
    "mce": 0.3171170291543516,
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
        "count": 47,
        "accuracy": 0.5957446808510638,
        "confidence": 0.5482311508762814
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 37,
        "accuracy": 0.5135135135135135,
        "confidence": 0.6429110685978661
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 49,
        "accuracy": 0.5714285714285714,
        "confidence": 0.7509906244412524
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 26,
        "accuracy": 0.5384615384615384,
        "confidence": 0.85557856761589
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 6,
        "accuracy": 0.8333333333333334,
        "confidence": 0.9250026171826015
      }
    ],
    "brier_score": 0.2718377215136707
  },
  "auroc": 0.5838965618571849,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.2921551394000276,
    "p95_inference_latency_ms": 0.380303799465764,
    "p99_inference_latency_ms": 0.5085698802577087,
    "throughput_samples_per_sec": 3422.838982239399
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.29696969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 1.0,
          "f1-score": 0.6363636363636364,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.23333333333333334,
          "recall": 0.5,
          "f1-score": 0.3181818181818182,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.21777777777777776,
          "recall": 0.4666666666666667,
          "f1-score": 0.29696969696969694,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
        ],
        [
          8,
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
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3392857142857143,
      "macro_f1": 0.33035714285714285,
      "weighted_f1": 0.3273809523809524,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.42857142857142855,
          "f1-score": 0.375,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.25,
          "f1-score": 0.2857142857142857,
          "support": 8.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3392857142857143,
          "f1-score": 0.33035714285714285,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3333333333333333,
          "recall": 0.3333333333333333,
          "f1-score": 0.3273809523809524,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          4
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6696428571428572,
      "macro_f1": 0.6666666666666666,
      "weighted_f1": 0.6666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.7142857142857143,
          "f1-score": 0.6666666666666666,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.625,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6696428571428572,
          "recall": 0.6696428571428572,
          "f1-score": 0.6666666666666666,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6726190476190477,
          "recall": 0.6666666666666666,
          "f1-score": 0.6666666666666666,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.34782608695652173,
      "weighted_f1": 0.3710144927536232,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 1.0,
          "f1-score": 0.6956521739130435,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
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
          8,
          0
        ],
        [
          7,
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
    "S010": {
      "task_type": "classification",
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.6160714285714286,
      "macro_f1": 0.5970695970695971,
      "weighted_f1": 0.6051282051282051,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6086956521739131,
          "recall": 0.875,
          "f1-score": 0.717948717948718,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.35714285714285715,
          "f1-score": 0.47619047619047616,
          "support": 14.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6614906832298137,
          "recall": 0.6160714285714286,
          "f1-score": 0.5970695970695971,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6579710144927536,
          "recall": 0.6333333333333333,
          "f1-score": 0.6051282051282051,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          2
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5617588932806324,
      "macro_f1": 0.5417156286721504,
      "weighted_f1": 0.5440919180049615,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5538461538461539,
          "recall": 0.782608695652174,
          "f1-score": 0.6486486486486487,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.3409090909090909,
          "f1-score": 0.43478260869565216,
          "support": 44.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5769230769230769,
          "recall": 0.5617588932806324,
          "f1-score": 0.5417156286721504,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5764102564102564,
          "recall": 0.5666666666666667,
          "f1-score": 0.5440919180049615,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          36,
          10
        ],
        [
          29,
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
    },
    "4": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6666666666666667,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6606334841628959,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.631578947368421,
          "recall": 0.8,
          "f1-score": 0.7058823529411765,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7272727272727273,
          "recall": 0.5333333333333333,
          "f1-score": 0.6153846153846154,
          "support": 15.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6794258373205742,
          "recall": 0.6666666666666667,
          "f1-score": 0.660633484162896,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6794258373205742,
          "recall": 0.6666666666666666,
          "f1-score": 0.6606334841628959,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          12,
          3
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
      "accuracy": 0.5111111111111111,
      "balanced_accuracy": 0.5158102766798419,
      "macro_f1": 0.4907407407407407,
      "weighted_f1": 0.48847736625514404,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.7272727272727273,
          "f1-score": 0.5925925925925926,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.30434782608695654,
          "f1-score": 0.3888888888888889,
          "support": 23.0
        },
        "accuracy": 0.5111111111111111,
        "macro avg": {
          "precision": 0.5192307692307692,
          "recall": 0.5158102766798419,
          "f1-score": 0.4907407407407407,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5196581196581196,
          "recall": 0.5111111111111111,
          "f1-score": 0.48847736625514404,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          16,
          6
        ],
        [
          16,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5676,
      "lower_95": 0.497,
      "upper_95": 0.6424
    },
    "balanced_accuracy": {
      "mean": 0.5667,
      "lower_95": 0.4953,
      "upper_95": 0.6354
    },
    "macro_f1": {
      "mean": 0.5468,
      "lower_95": 0.4664,
      "upper_95": 0.6214
    }
  }
}
```