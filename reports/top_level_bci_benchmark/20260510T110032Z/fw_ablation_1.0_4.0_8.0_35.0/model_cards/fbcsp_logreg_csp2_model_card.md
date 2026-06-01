# Model Card: fw_ablation_1.0_4.0_8.0_35.0_fbcsp_logreg_csp2

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
  "accuracy": 0.5575757575757576,
  "balanced_accuracy": 0.5575962386129886,
  "macro_f1": 0.5575757575757576,
  "weighted_f1": 0.5575757575757576,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5609756097560976,
      "recall": 0.5542168674698795,
      "f1-score": 0.5575757575757576,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5542168674698795,
      "recall": 0.5609756097560976,
      "f1-score": 0.5575757575757576,
      "support": 82.0
    },
    "accuracy": 0.5575757575757576,
    "macro avg": {
      "precision": 0.5575962386129886,
      "recall": 0.5575962386129886,
      "f1-score": 0.5575757575757576,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5576167196502195,
      "recall": 0.5575757575757576,
      "f1-score": 0.5575757575757576,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      46,
      37
    ],
    [
      36,
      46
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.14779402709054706,
    "mce": 0.30123853199517925,
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
        "accuracy": 0.5106382978723404,
        "confidence": 0.5518936737983225
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 33,
        "accuracy": 0.5757575757575758,
        "confidence": 0.6474358013937862
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 40,
        "accuracy": 0.5,
        "confidence": 0.7487188709209016
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 33,
        "accuracy": 0.5454545454545454,
        "confidence": 0.8466930774497247
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 12,
        "accuracy": 0.9166666666666666,
        "confidence": 0.9326669968955986
      }
    ],
    "brier_score": 0.2698978769690377
  },
  "auroc": 0.5868351454598885,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 8.011441436401308,
    "p95_inference_latency_ms": 8.85234199995466,
    "p99_inference_latency_ms": 9.192865599943614,
    "throughput_samples_per_sec": 124.82148286778143
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7410714285714286,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.730952380952381,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.8571428571428571,
          "f1-score": 0.75,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.625,
          "f1-score": 0.7142857142857143,
          "support": 8.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.75,
          "recall": 0.7410714285714286,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7555555555555554,
          "recall": 0.7333333333333333,
          "f1-score": 0.730952380952381,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6428571428571428,
      "macro_f1": 0.6031746031746031,
      "weighted_f1": 0.6137566137566137,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.2857142857142857,
          "f1-score": 0.4444444444444444,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6153846153846154,
          "recall": 1.0,
          "f1-score": 0.7619047619047619,
          "support": 8.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.8076923076923077,
          "recall": 0.6428571428571428,
          "f1-score": 0.6031746031746031,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7948717948717949,
          "recall": 0.6666666666666666,
          "f1-score": 0.6137566137566137,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          5
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6785714285714286,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6576168929110106,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 0.5,
          "f1-score": 0.6153846153846154,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.8571428571428571,
          "f1-score": 0.7058823529411765,
          "support": 7.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.7,
          "recall": 0.6785714285714286,
          "f1-score": 0.660633484162896,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7066666666666668,
          "recall": 0.6666666666666666,
          "f1-score": 0.6576168929110106,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          4
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
      "balanced_accuracy": 0.5357142857142857,
      "macro_f1": 0.5333333333333333,
      "weighted_f1": 0.5333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5,
          "f1-score": 0.5333333333333333,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5714285714285714,
          "f1-score": 0.5333333333333333,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5357142857142857,
          "recall": 0.5357142857142857,
          "f1-score": 0.5333333333333333,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5380952380952381,
          "recall": 0.5333333333333333,
          "f1-score": 0.5333333333333333,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          8,
          8
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
    },
    "S008": {
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.3839285714285714,
      "macro_f1": 0.354066985645933,
      "weighted_f1": 0.36555023923444974,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.625,
          "f1-score": 0.5263157894736842,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.14285714285714285,
          "f1-score": 0.18181818181818182,
          "support": 7.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.3522727272727273,
          "recall": 0.3839285714285714,
          "f1-score": 0.354066985645933,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3590909090909091,
          "recall": 0.4,
          "f1-score": 0.36555023923444974,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
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
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.6294642857142857,
      "macro_f1": 0.6296296296296295,
      "weighted_f1": 0.6320987654320988,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6470588235294118,
          "recall": 0.6875,
          "f1-score": 0.6666666666666666,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6153846153846154,
          "recall": 0.5714285714285714,
          "f1-score": 0.5925925925925926,
          "support": 14.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6312217194570136,
          "recall": 0.6294642857142857,
          "f1-score": 0.6296296296296295,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6322775263951735,
          "recall": 0.6333333333333333,
          "f1-score": 0.6320987654320988,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          5
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
      "balanced_accuracy": 0.5790513833992095,
      "macro_f1": 0.5769421078673924,
      "weighted_f1": 0.5765242729121997,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.5217391304347826,
          "f1-score": 0.5581395348837209,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.6363636363636364,
          "f1-score": 0.5957446808510638,
          "support": 44.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5800000000000001,
          "recall": 0.5790513833992095,
          "f1-score": 0.5769421078673924,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5804444444444444,
          "recall": 0.5777777777777777,
          "f1-score": 0.5765242729121997,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          24,
          22
        ],
        [
          16,
          28
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.6,
      "macro_f1": 0.569377990430622,
      "weighted_f1": 0.5693779904306221,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5652173913043478,
          "recall": 0.8666666666666667,
          "f1-score": 0.6842105263157895,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.3333333333333333,
          "f1-score": 0.45454545454545453,
          "support": 15.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.639751552795031,
          "recall": 0.6,
          "f1-score": 0.569377990430622,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6397515527950312,
          "recall": 0.6,
          "f1-score": 0.5693779904306221,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          2
        ],
        [
          10,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.4871541501976284,
      "macro_f1": 0.48481831757093086,
      "weighted_f1": 0.4858359604004204,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.47368421052631576,
          "recall": 0.4090909090909091,
          "f1-score": 0.43902439024390244,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5652173913043478,
          "f1-score": 0.5306122448979592,
          "support": 23.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.48684210526315785,
          "recall": 0.4871541501976284,
          "f1-score": 0.48481831757093086,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.48713450292397653,
          "recall": 0.4888888888888889,
          "f1-score": 0.4858359604004204,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          9,
          13
        ],
        [
          10,
          13
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
      "mean": 0.558,
      "lower_95": 0.4788,
      "upper_95": 0.6274
    },
    "balanced_accuracy": {
      "mean": 0.5582,
      "lower_95": 0.4811,
      "upper_95": 0.6273
    },
    "macro_f1": {
      "mean": 0.5565,
      "lower_95": 0.4785,
      "upper_95": 0.626
    }
  }
}
```