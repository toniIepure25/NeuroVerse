# Model Card: physionet_eegbci_medium_csp_svm_linear_csp6

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
  "balanced_accuracy": 0.550396708786365,
  "macro_f1": 0.5351050868108438,
  "weighted_f1": 0.5356344437367891,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5398230088495575,
      "recall": 0.7349397590361446,
      "f1-score": 0.6224489795918368,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5769230769230769,
      "recall": 0.36585365853658536,
      "f1-score": 0.44776119402985076,
      "support": 82.0
    },
    "accuracy": 0.5515151515151515,
    "macro avg": {
      "precision": 0.5583730428863172,
      "recall": 0.550396708786365,
      "f1-score": 0.5351050868108438,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5582606184376095,
      "recall": 0.5515151515151515,
      "f1-score": 0.5356344437367891,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      61,
      22
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
    "ece": 0.1212992934281122,
    "mce": 0.2563572333869769,
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
        "accuracy": 0.43636363636363634,
        "confidence": 0.5503024378716748
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 55,
        "accuracy": 0.5636363636363636,
        "confidence": 0.6531240902081474
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 32,
        "accuracy": 0.625,
        "confidence": 0.7458390761624943
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 17,
        "accuracy": 0.5882352941176471,
        "confidence": 0.844592527504624
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 6,
        "accuracy": 0.8333333333333334,
        "confidence": 0.9335001610783106
      }
    ],
    "brier_score": 0.2550762312880392
  },
  "auroc": 0.6215104319717896,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.30643007878759154,
    "p95_inference_latency_ms": 0.3690303990879328,
    "p99_inference_latency_ms": 0.42199643983622054,
    "throughput_samples_per_sec": 3263.387210408842
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
      "accuracy": 0.9333333333333333,
      "balanced_accuracy": 0.9285714285714286,
      "macro_f1": 0.9321266968325792,
      "weighted_f1": 0.9327300150829563,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.8571428571428571,
          "f1-score": 0.9230769230769231,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8888888888888888,
          "recall": 1.0,
          "f1-score": 0.9411764705882353,
          "support": 8.0
        },
        "accuracy": 0.9333333333333333,
        "macro avg": {
          "precision": 0.9444444444444444,
          "recall": 0.9285714285714286,
          "f1-score": 0.9321266968325792,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.9407407407407408,
          "recall": 0.9333333333333333,
          "f1-score": 0.9327300150829563,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
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
      "accuracy": 0.26666666666666666,
      "balanced_accuracy": 0.26785714285714285,
      "macro_f1": 0.26666666666666666,
      "weighted_f1": 0.26666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.2857142857142857,
          "f1-score": 0.26666666666666666,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2857142857142857,
          "recall": 0.25,
          "f1-score": 0.26666666666666666,
          "support": 8.0
        },
        "accuracy": 0.26666666666666666,
        "macro avg": {
          "precision": 0.26785714285714285,
          "recall": 0.26785714285714285,
          "f1-score": 0.26666666666666666,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.26904761904761904,
          "recall": 0.26666666666666666,
          "f1-score": 0.26666666666666666,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          2,
          5
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4464285714285714,
      "macro_f1": 0.4,
      "weighted_f1": 0.41333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.75,
          "f1-score": 0.6,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.14285714285714285,
          "f1-score": 0.2,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.41666666666666663,
          "recall": 0.4464285714285714,
          "f1-score": 0.4,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.4222222222222222,
          "recall": 0.4666666666666667,
          "f1-score": 0.41333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5535714285714286,
      "macro_f1": 0.5417156286721504,
      "weighted_f1": 0.5488444966705835,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.75,
          "f1-score": 0.6486486486486487,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5555555555555556,
          "recall": 0.35714285714285715,
          "f1-score": 0.43478260869565216,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5634920634920635,
          "recall": 0.5535714285714286,
          "f1-score": 0.5417156286721504,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.564021164021164,
          "recall": 0.5666666666666667,
          "f1-score": 0.5488444966705835,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          12,
          4
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
      "accuracy": 0.5444444444444444,
      "balanced_accuracy": 0.5395256916996047,
      "macro_f1": 0.518213866039953,
      "weighted_f1": 0.5207120163641903,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.7608695652173914,
          "f1-score": 0.6306306306306306,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.3181818181818182,
          "f1-score": 0.4057971014492754,
          "support": 44.0
        },
        "accuracy": 0.5444444444444444,
        "macro avg": {
          "precision": 0.5492307692307692,
          "recall": 0.5395256916996047,
          "f1-score": 0.518213866039953,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.548991452991453,
          "recall": 0.5444444444444444,
          "f1-score": 0.5207120163641903,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          35,
          11
        ],
        [
          30,
          14
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4713438735177865,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4419753086419753,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.46875,
          "recall": 0.6818181818181818,
          "f1-score": 0.5555555555555556,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.2608695652173913,
          "f1-score": 0.3333333333333333,
          "support": 23.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4651442307692308,
          "recall": 0.4713438735177865,
          "f1-score": 0.4444444444444444,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4650641025641026,
          "recall": 0.4666666666666667,
          "f1-score": 0.4419753086419753,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          15,
          7
        ],
        [
          17,
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.55,
      "lower_95": 0.4727,
      "upper_95": 0.6242
    },
    "balanced_accuracy": {
      "mean": 0.5492,
      "lower_95": 0.4745,
      "upper_95": 0.6188
    },
    "macro_f1": {
      "mean": 0.5321,
      "lower_95": 0.4566,
      "upper_95": 0.6078
    }
  }
}
```