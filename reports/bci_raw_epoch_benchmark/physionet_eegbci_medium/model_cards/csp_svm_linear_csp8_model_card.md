# Model Card: physionet_eegbci_medium_csp_svm_linear_csp8

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
  "accuracy": 0.5636363636363636,
  "balanced_accuracy": 0.5628122245077872,
  "macro_f1": 0.5549895115373089,
  "weighted_f1": 0.5553654616285723,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5523809523809524,
      "recall": 0.6987951807228916,
      "f1-score": 0.6170212765957447,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5833333333333334,
      "recall": 0.4268292682926829,
      "f1-score": 0.49295774647887325,
      "support": 82.0
    },
    "accuracy": 0.5636363636363636,
    "macro avg": {
      "precision": 0.5678571428571428,
      "recall": 0.5628122245077872,
      "f1-score": 0.5549895115373089,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5677633477633478,
      "recall": 0.5636363636363636,
      "f1-score": 0.5553654616285723,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      58,
      25
    ],
    [
      47,
      35
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.15791173925649118,
    "mce": 0.38047717663432284,
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
        "count": 44,
        "accuracy": 0.4318181818181818,
        "confidence": 0.5460943057063408
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 51,
        "accuracy": 0.45098039215686275,
        "confidence": 0.6502291978058641
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 37,
        "accuracy": 0.7567567567567568,
        "confidence": 0.7465529700779474
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 24,
        "accuracy": 0.4583333333333333,
        "confidence": 0.8388105099676562
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 9,
        "accuracy": 0.7777777777777778,
        "confidence": 0.9285117879781435
      }
    ],
    "brier_score": 0.26384322306919983
  },
  "auroc": 0.5969732588892154,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.2856907756998253,
    "p95_inference_latency_ms": 0.3089805988565785,
    "p99_inference_latency_ms": 0.31828040038817557,
    "throughput_samples_per_sec": 3500.2880213769936
  },
  "per_subject": {
    "S001": {
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.8571428571428572,
      "macro_f1": 0.8611111111111112,
      "weighted_f1": 0.8629629629629629,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.7142857142857143,
          "f1-score": 0.8333333333333334,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 1.0,
          "f1-score": 0.8888888888888888,
          "support": 8.0
        },
        "accuracy": 0.8666666666666667,
        "macro avg": {
          "precision": 0.9,
          "recall": 0.8571428571428572,
          "f1-score": 0.8611111111111112,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8933333333333333,
          "recall": 0.8666666666666667,
          "f1-score": 0.8629629629629629,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.3839285714285714,
      "macro_f1": 0.354066985645933,
      "weighted_f1": 0.36555023923444974,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.14285714285714285,
          "f1-score": 0.18181818181818182,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.625,
          "f1-score": 0.5263157894736842,
          "support": 8.0
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
          1,
          6
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
    "S004": {
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
    "S005": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4375,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.3393939393939394,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.875,
          "f1-score": 0.6363636363636364,
          "support": 8.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.25,
          "recall": 0.4375,
          "f1-score": 0.3181818181818182,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.26666666666666666,
          "recall": 0.4666666666666667,
          "f1-score": 0.3393939393939394,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7
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
      "accuracy": 0.6,
      "balanced_accuracy": 0.6071428571428572,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.5964285714285714,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.7142857142857143,
          "f1-score": 0.625,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.5,
          "f1-score": 0.5714285714285714,
          "support": 8.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.6111111111111112,
          "recall": 0.6071428571428572,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6148148148148148,
          "recall": 0.6,
          "f1-score": 0.5964285714285714,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.7857142857142857,
      "macro_f1": 0.784688995215311,
      "weighted_f1": 0.7885167464114832,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7272727272727273,
          "recall": 1.0,
          "f1-score": 0.8421052631578947,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.5714285714285714,
          "f1-score": 0.7272727272727273,
          "support": 7.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.8636363636363636,
          "recall": 0.7857142857142857,
          "f1-score": 0.784688995215311,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8545454545454546,
          "recall": 0.8,
          "f1-score": 0.7885167464114832,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          8,
          0
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.48214285714285715,
      "macro_f1": 0.45054945054945056,
      "weighted_f1": 0.46153846153846156,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5217391304347826,
          "recall": 0.75,
          "f1-score": 0.6153846153846154,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.21428571428571427,
          "f1-score": 0.2857142857142857,
          "support": 14.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.47515527950310554,
          "recall": 0.48214285714285715,
          "f1-score": 0.45054945054945056,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.4782608695652174,
          "recall": 0.5,
          "f1-score": 0.46153846153846156,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          12,
          4
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5622529644268774,
      "macro_f1": 0.546453030107249,
      "weighted_f1": 0.5485807813240299,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.7608695652173914,
          "f1-score": 0.6422018348623854,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5925925925925926,
          "recall": 0.36363636363636365,
          "f1-score": 0.4507042253521127,
          "support": 44.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5740740740740741,
          "recall": 0.5622529644268774,
          "f1-score": 0.546453030107249,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5736625514403293,
          "recall": 0.5666666666666667,
          "f1-score": 0.5485807813240299,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          35,
          11
        ],
        [
          28,
          16
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
      "accuracy": 0.6333333333333333,
      "balanced_accuracy": 0.6333333333333333,
      "macro_f1": 0.6329254727474972,
      "weighted_f1": 0.6329254727474972,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6428571428571429,
          "recall": 0.6,
          "f1-score": 0.6206896551724138,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.6666666666666666,
          "f1-score": 0.6451612903225806,
          "support": 15.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6339285714285714,
          "recall": 0.6333333333333333,
          "f1-score": 0.6329254727474972,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6339285714285715,
          "recall": 0.6333333333333333,
          "f1-score": 0.6329254727474972,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          9,
          6
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
      "accuracy": 0.5111111111111111,
      "balanced_accuracy": 0.5138339920948617,
      "macro_f1": 0.505,
      "weighted_f1": 0.5037777777777778,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6363636363636364,
          "f1-score": 0.56,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5294117647058824,
          "recall": 0.391304347826087,
          "f1-score": 0.45,
          "support": 23.0
        },
        "accuracy": 0.5111111111111111,
        "macro avg": {
          "precision": 0.5147058823529411,
          "recall": 0.5138339920948617,
          "f1-score": 0.505,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.515032679738562,
          "recall": 0.5111111111111111,
          "f1-score": 0.5037777777777778,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          14,
          8
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
      "mean": 0.5625,
      "lower_95": 0.4788,
      "upper_95": 0.6364
    },
    "balanced_accuracy": {
      "mean": 0.5619,
      "lower_95": 0.4834,
      "upper_95": 0.6348
    },
    "macro_f1": {
      "mean": 0.5524,
      "lower_95": 0.4706,
      "upper_95": 0.6267
    }
  }
}
```