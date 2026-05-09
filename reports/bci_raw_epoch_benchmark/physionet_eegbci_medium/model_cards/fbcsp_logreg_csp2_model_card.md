# Model Card: physionet_eegbci_medium_fbcsp_logreg_csp2

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
  "accuracy": 0.5757575757575758,
  "balanced_accuracy": 0.5759623861298854,
  "macro_f1": 0.5753676470588236,
  "weighted_f1": 0.5752896613190731,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5844155844155844,
      "recall": 0.5421686746987951,
      "f1-score": 0.5625,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5681818181818182,
      "recall": 0.6097560975609756,
      "f1-score": 0.5882352941176471,
      "support": 82.0
    },
    "accuracy": 0.5757575757575758,
    "macro avg": {
      "precision": 0.5762987012987013,
      "recall": 0.5759623861298854,
      "f1-score": 0.5753676470588236,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5763478945297128,
      "recall": 0.5757575757575758,
      "f1-score": 0.5752896613190731,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      45,
      38
    ],
    [
      32,
      50
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.19677282003588809,
    "mce": 0.3186307890564055,
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
        "count": 15,
        "accuracy": 0.5333333333333333,
        "confidence": 0.5551737473486403
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 38,
        "accuracy": 0.5263157894736842,
        "confidence": 0.6448025344395751
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 41,
        "accuracy": 0.6097560975609756,
        "confidence": 0.7556272163286297
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 34,
        "accuracy": 0.5588235294117647,
        "confidence": 0.8490399330125661
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 37,
        "accuracy": 0.6216216216216216,
        "confidence": 0.9402524106780271
      }
    ],
    "brier_score": 0.292768836932009
  },
  "auroc": 0.5868351454598884,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 6.716821084685789,
    "p95_inference_latency_ms": 6.974583400369737,
    "p99_inference_latency_ms": 7.287732199620219,
    "throughput_samples_per_sec": 148.87995189867107
  },
  "per_subject": {
    "S001": {
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
    "S002": {
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3482142857142857,
      "macro_f1": 0.3055555555555555,
      "weighted_f1": 0.2962962962962962,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.36363636363636365,
          "recall": 0.5714285714285714,
          "f1-score": 0.4444444444444444,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.125,
          "f1-score": 0.16666666666666666,
          "support": 8.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.3068181818181818,
          "recall": 0.3482142857142857,
          "f1-score": 0.3055555555555555,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.303030303030303,
          "recall": 0.3333333333333333,
          "f1-score": 0.2962962962962962,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          3
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.9333333333333333,
      "balanced_accuracy": 0.9375,
      "macro_f1": 0.9333333333333333,
      "weighted_f1": 0.9333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.875,
          "f1-score": 0.9333333333333333,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.875,
          "recall": 1.0,
          "f1-score": 0.9333333333333333,
          "support": 7.0
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
          1
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.5089285714285714,
      "macro_f1": 0.4949494949494949,
      "weighted_f1": 0.49158249158249157,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.375,
          "f1-score": 0.4444444444444444,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.47368421052631576,
          "recall": 0.6428571428571429,
          "f1-score": 0.5454545454545454,
          "support": 14.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.5095693779904306,
          "recall": 0.5089285714285714,
          "f1-score": 0.4949494949494949,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5119617224880383,
          "recall": 0.5,
          "f1-score": 0.49158249158249157,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          6,
          10
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
      "balanced_accuracy": 0.5089285714285714,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4592592592592592,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.875,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.14285714285714285,
          "f1-score": 0.2222222222222222,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5192307692307692,
          "recall": 0.5089285714285714,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5205128205128206,
          "recall": 0.5333333333333333,
          "f1-score": 0.4592592592592592,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.4419642857142857,
      "macro_f1": 0.4276094276094276,
      "weighted_f1": 0.4237934904601571,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.3125,
          "f1-score": 0.37037037037037035,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.42105263157894735,
          "recall": 0.5714285714285714,
          "f1-score": 0.48484848484848486,
          "support": 14.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.43779904306220097,
          "recall": 0.4419642857142857,
          "f1-score": 0.4276094276094276,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.43891547049441787,
          "recall": 0.43333333333333335,
          "f1-score": 0.4237934904601571,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          5,
          11
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.6022727272727273,
      "macro_f1": 0.5968143354902937,
      "weighted_f1": 0.5960179193628671,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6388888888888888,
          "recall": 0.5,
          "f1-score": 0.5609756097560976,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5740740740740741,
          "recall": 0.7045454545454546,
          "f1-score": 0.6326530612244898,
          "support": 44.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6064814814814814,
          "recall": 0.6022727272727273,
          "f1-score": 0.5968143354902937,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.607201646090535,
          "recall": 0.6,
          "f1-score": 0.5960179193628671,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          23,
          23
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
      "accuracy": 0.7,
      "balanced_accuracy": 0.7,
      "macro_f1": 0.699666295884316,
      "weighted_f1": 0.6996662958843161,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6875,
          "recall": 0.7333333333333333,
          "f1-score": 0.7096774193548387,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.6666666666666666,
          "f1-score": 0.6896551724137931,
          "support": 15.0
        },
        "accuracy": 0.7,
        "macro avg": {
          "precision": 0.7008928571428572,
          "recall": 0.7,
          "f1-score": 0.699666295884316,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7008928571428572,
          "recall": 0.7,
          "f1-score": 0.6996662958843161,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          4
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
      "accuracy": 0.4444444444444444,
      "balanced_accuracy": 0.44565217391304346,
      "macro_f1": 0.44334487877288475,
      "weighted_f1": 0.44279509593710487,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.44,
          "recall": 0.5,
          "f1-score": 0.46808510638297873,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45,
          "recall": 0.391304347826087,
          "f1-score": 0.4186046511627907,
          "support": 23.0
        },
        "accuracy": 0.4444444444444444,
        "macro avg": {
          "precision": 0.445,
          "recall": 0.44565217391304346,
          "f1-score": 0.44334487877288475,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4451111111111111,
          "recall": 0.4444444444444444,
          "f1-score": 0.44279509593710487,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          11,
          11
        ],
        [
          14,
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5787,
      "lower_95": 0.5091,
      "upper_95": 0.6545
    },
    "balanced_accuracy": {
      "mean": 0.579,
      "lower_95": 0.5107,
      "upper_95": 0.6542
    },
    "macro_f1": {
      "mean": 0.5769,
      "lower_95": 0.5089,
      "upper_95": 0.6527
    }
  }
}
```