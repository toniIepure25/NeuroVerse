# Model Card: fw_ablation_1.0_4.0_8.0_35.0_fbcsp_logreg_csp4

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
  "accuracy": 0.593939393939394,
  "balanced_accuracy": 0.5937408169262416,
  "macro_f1": 0.5934017433520908,
  "weighted_f1": 0.5934913517833081,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5909090909090909,
      "recall": 0.6265060240963856,
      "f1-score": 0.6081871345029239,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5974025974025974,
      "recall": 0.5609756097560976,
      "f1-score": 0.5786163522012578,
      "support": 82.0
    },
    "accuracy": 0.593939393939394,
    "macro avg": {
      "precision": 0.5941558441558441,
      "recall": 0.5937408169262416,
      "f1-score": 0.5934017433520908,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5941361668634396,
      "recall": 0.593939393939394,
      "f1-score": 0.5934913517833081,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      52,
      31
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
    "ece": 0.1857041641062847,
    "mce": 0.375128438421794,
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
        "count": 27,
        "accuracy": 0.5185185185185185,
        "confidence": 0.5493781865343942
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 21,
        "accuracy": 0.42857142857142855,
        "confidence": 0.6516647374075875
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 29,
        "accuracy": 0.6206896551724138,
        "confidence": 0.7449012269592215
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 49,
        "accuracy": 0.7142857142857143,
        "confidence": 0.8549157525567675
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 39,
        "accuracy": 0.5641025641025641,
        "confidence": 0.9392310025243581
      }
    ],
    "brier_score": 0.2795028201299206
  },
  "auroc": 0.6196003526300323,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 8.198184399985951,
    "p95_inference_latency_ms": 9.037478600112081,
    "p99_inference_latency_ms": 9.362944880012943,
    "throughput_samples_per_sec": 121.97822727697044
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6785714285714286,
      "macro_f1": 0.660633484162896,
      "weighted_f1": 0.6576168929110106,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.8571428571428571,
          "f1-score": 0.7058823529411765,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 0.5,
          "f1-score": 0.6153846153846154,
          "support": 8.0
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
          6,
          1
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5535714285714286,
      "macro_f1": 0.49760765550239233,
      "weighted_f1": 0.4886762360446571,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8571428571428571,
          "f1-score": 0.631578947368421,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.25,
          "f1-score": 0.36363636363636365,
          "support": 8.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5833333333333333,
          "recall": 0.5535714285714286,
          "f1-score": 0.49760765550239233,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5888888888888888,
          "recall": 0.5333333333333333,
          "f1-score": 0.4886762360446571,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
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
      "accuracy": 0.8666666666666667,
      "balanced_accuracy": 0.875,
      "macro_f1": 0.8660714285714286,
      "weighted_f1": 0.8654761904761905,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.75,
          "f1-score": 0.8571428571428571,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7777777777777778,
          "recall": 1.0,
          "f1-score": 0.875,
          "support": 7.0
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
          6,
          2
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5625,
      "macro_f1": 0.5622895622895623,
      "weighted_f1": 0.5652076318742985,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5882352941176471,
          "recall": 0.625,
          "f1-score": 0.6060606060606061,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.5,
          "f1-score": 0.5185185185185185,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5633484162895928,
          "recall": 0.5625,
          "f1-score": 0.5622895622895623,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5650075414781297,
          "recall": 0.5666666666666667,
          "f1-score": 0.5652076318742985,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          10,
          6
        ],
        [
          7,
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
    "S008": {
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4375,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.3393939393939394,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.875,
          "f1-score": 0.6363636363636364,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
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
          7,
          1
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
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6517857142857143,
      "macro_f1": 0.6411483253588517,
      "weighted_f1": 0.6475279106858054,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6363636363636364,
          "recall": 0.875,
          "f1-score": 0.7368421052631579,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.42857142857142855,
          "f1-score": 0.5454545454545454,
          "support": 14.0
        },
        "accuracy": 0.6666666666666666,
        "macro avg": {
          "precision": 0.6931818181818181,
          "recall": 0.6517857142857143,
          "f1-score": 0.6411483253588517,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6893939393939393,
          "recall": 0.6666666666666666,
          "f1-score": 0.6475279106858054,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          2
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
      "accuracy": 0.6222222222222222,
      "balanced_accuracy": 0.6210474308300395,
      "macro_f1": 0.6205357142857143,
      "weighted_f1": 0.6210978835978836,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.62,
          "recall": 0.6739130434782609,
          "f1-score": 0.6458333333333334,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.5681818181818182,
          "f1-score": 0.5952380952380952,
          "support": 44.0
        },
        "accuracy": 0.6222222222222222,
        "macro avg": {
          "precision": 0.6225,
          "recall": 0.6210474308300395,
          "f1-score": 0.6205357142857143,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.6224444444444444,
          "recall": 0.6222222222222222,
          "f1-score": 0.6210978835978836,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          31,
          15
        ],
        [
          19,
          25
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
      "macro_f1": 0.6122209165687427,
      "weighted_f1": 0.6122209165687427,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5909090909090909,
          "recall": 0.8666666666666667,
          "f1-score": 0.7027027027027027,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.4,
          "f1-score": 0.5217391304347826,
          "support": 15.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.6704545454545454,
          "recall": 0.6333333333333333,
          "f1-score": 0.6122209165687427,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6704545454545454,
          "recall": 0.6333333333333333,
          "f1-score": 0.6122209165687427,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          2
        ],
        [
          9,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.5111111111111111,
      "balanced_accuracy": 0.5079051383399209,
      "macro_f1": 0.4989878542510121,
      "weighted_f1": 0.5007197480881691,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.36363636363636365,
          "f1-score": 0.42105263157894735,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5172413793103449,
          "recall": 0.6521739130434783,
          "f1-score": 0.5769230769230769,
          "support": 23.0
        },
        "accuracy": 0.5111111111111111,
        "macro avg": {
          "precision": 0.5086206896551724,
          "recall": 0.5079051383399209,
          "f1-score": 0.4989878542510121,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5088122605363985,
          "recall": 0.5111111111111111,
          "f1-score": 0.5007197480881691,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          8,
          14
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
      "mean": 0.5949,
      "lower_95": 0.5241,
      "upper_95": 0.6667
    },
    "balanced_accuracy": {
      "mean": 0.5948,
      "lower_95": 0.5218,
      "upper_95": 0.669
    },
    "macro_f1": {
      "mean": 0.593,
      "lower_95": 0.521,
      "upper_95": 0.6665
    }
  }
}
```