# Model Card: physionet_eegbci_medium_fbcsp_lda_csp4

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
  "balanced_accuracy": 0.5634734058183956,
  "macro_f1": 0.5632352941176471,
  "weighted_f1": 0.5633155080213903,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5632183908045977,
      "recall": 0.5903614457831325,
      "f1-score": 0.5764705882352941,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5641025641025641,
      "recall": 0.5365853658536586,
      "f1-score": 0.55,
      "support": 82.0
    },
    "accuracy": 0.5636363636363636,
    "macro avg": {
      "precision": 0.5636604774535809,
      "recall": 0.5634734058183956,
      "f1-score": 0.5632352941176471,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5636577981405567,
      "recall": 0.5636363636363636,
      "f1-score": 0.5633155080213903,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      49,
      34
    ],
    [
      38,
      44
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.23616636810129038,
    "mce": 0.39057655918144185,
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
        "count": 22,
        "accuracy": 0.5454545454545454,
        "confidence": 0.5603750001890678
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 14,
        "accuracy": 0.5,
        "confidence": 0.6547657366414903
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 42,
        "accuracy": 0.5952380952380952,
        "confidence": 0.7457263754716772
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 39,
        "accuracy": 0.5641025641025641,
        "confidence": 0.8565204566423822
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 48,
        "accuracy": 0.5625,
        "confidence": 0.9530765591814419
      }
    ],
    "brier_score": 0.3182481529240894
  },
  "auroc": 0.5686159271231266,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.3941958910312895,
    "p95_inference_latency_ms": 8.882972399442222,
    "p99_inference_latency_ms": 9.611538360477423,
    "throughput_samples_per_sec": 135.24121009736018
  },
  "per_subject": {
    "S001": {
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
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5446428571428572,
      "macro_f1": 0.5248868778280543,
      "weighted_f1": 0.5206636500754148,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.7142857142857143,
          "f1-score": 0.5882352941176471,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.375,
          "f1-score": 0.46153846153846156,
          "support": 8.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.55,
          "recall": 0.5446428571428572,
          "f1-score": 0.5248868778280543,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5533333333333333,
          "recall": 0.5333333333333333,
          "f1-score": 0.5206636500754148,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.6666666666666666,
      "balanced_accuracy": 0.6696428571428572,
      "macro_f1": 0.6666666666666666,
      "weighted_f1": 0.6666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.625,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.7142857142857143,
          "f1-score": 0.6666666666666666,
          "support": 7.0
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
          3
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
      "balanced_accuracy": 0.5758928571428572,
      "macro_f1": 0.5622895622895623,
      "weighted_f1": 0.5593714927048261,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6363636363636364,
          "recall": 0.4375,
          "f1-score": 0.5185185185185185,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5263157894736842,
          "recall": 0.7142857142857143,
          "f1-score": 0.6060606060606061,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5813397129186603,
          "recall": 0.5758928571428572,
          "f1-score": 0.5622895622895623,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5850079744816588,
          "recall": 0.5666666666666667,
          "f1-score": 0.5593714927048261,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          9
        ],
        [
          4,
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.45535714285714285,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.45185185185185184,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.625,
          "f1-score": 0.5555555555555556,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.2857142857142857,
          "f1-score": 0.3333333333333333,
          "support": 14.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.45,
          "recall": 0.45535714285714285,
          "f1-score": 0.4444444444444444,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.45333333333333337,
          "recall": 0.4666666666666667,
          "f1-score": 0.45185185185185184,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          10,
          6
        ],
        [
          10,
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5350790513833992,
      "macro_f1": 0.53125,
      "weighted_f1": 0.5305555555555556,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5526315789473685,
          "recall": 0.45652173913043476,
          "f1-score": 0.5,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5192307692307693,
          "recall": 0.6136363636363636,
          "f1-score": 0.5625,
          "support": 44.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5359311740890689,
          "recall": 0.5350790513833992,
          "f1-score": 0.53125,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5363022941970311,
          "recall": 0.5333333333333333,
          "f1-score": 0.5305555555555556,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          21,
          25
        ],
        [
          17,
          27
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
      "macro_f1": 0.5970695970695971,
      "weighted_f1": 0.5970695970695971,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 0.9333333333333333,
          "f1-score": 0.717948717948718,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.3333333333333333,
          "f1-score": 0.47619047619047616,
          "support": 15.0
        },
        "accuracy": 0.6333333333333333,
        "macro avg": {
          "precision": 0.7083333333333334,
          "recall": 0.6333333333333333,
          "f1-score": 0.5970695970695971,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7083333333333334,
          "recall": 0.6333333333333333,
          "f1-score": 0.5970695970695971,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          1
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
      "accuracy": 0.5777777777777777,
      "balanced_accuracy": 0.5790513833992095,
      "macro_f1": 0.5769421078673924,
      "weighted_f1": 0.5765242729121997,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.6363636363636364,
          "f1-score": 0.5957446808510638,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.5217391304347826,
          "f1-score": 0.5581395348837209,
          "support": 23.0
        },
        "accuracy": 0.5777777777777777,
        "macro avg": {
          "precision": 0.5800000000000001,
          "recall": 0.5790513833992095,
          "f1-score": 0.5769421078673924,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5804444444444444,
          "recall": 0.5777777777777777,
          "f1-score": 0.5765242729121997,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          14,
          8
        ],
        [
          11,
          12
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
      "mean": 0.5652,
      "lower_95": 0.4909,
      "upper_95": 0.6364
    },
    "balanced_accuracy": {
      "mean": 0.5652,
      "lower_95": 0.4905,
      "upper_95": 0.6364
    },
    "macro_f1": {
      "mean": 0.5634,
      "lower_95": 0.4899,
      "upper_95": 0.6337
    }
  }
}
```