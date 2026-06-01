# Model Card: fw_ablation_1.0_3.0_8.0_30.0_fbcsp_logreg_csp8

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
  "balanced_accuracy": 0.5694975022039377,
  "macro_f1": 0.5691272205671412,
  "weighted_f1": 0.5692221787554459,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5681818181818182,
      "recall": 0.6024096385542169,
      "f1-score": 0.5847953216374269,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5714285714285714,
      "recall": 0.5365853658536586,
      "f1-score": 0.5534591194968553,
      "support": 82.0
    },
    "accuracy": 0.5696969696969697,
    "macro avg": {
      "precision": 0.5698051948051948,
      "recall": 0.5694975022039377,
      "f1-score": 0.5691272205671412,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5697953561589926,
      "recall": 0.5696969696969697,
      "f1-score": 0.5692221787554459,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      50,
      33
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
    "ece": 0.2641671217502656,
    "mce": 0.3695242922391702,
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
        "count": 23,
        "accuracy": 0.4782608695652174,
        "confidence": 0.5445168570972734
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 19,
        "accuracy": 0.47368421052631576,
        "confidence": 0.6565290434820547
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 12,
        "accuracy": 0.6666666666666666,
        "confidence": 0.7529905621883314
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 29,
        "accuracy": 0.4827586206896552,
        "confidence": 0.8522829129288254
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 82,
        "accuracy": 0.6341463414634146,
        "confidence": 0.9614334674170926
      }
    ],
    "brier_score": 0.3268585775687235
  },
  "auroc": 0.5931531002057007,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.914921915173843,
    "p95_inference_latency_ms": 9.116958399681607,
    "p99_inference_latency_ms": 11.067848679776944,
    "throughput_samples_per_sec": 126.34363430457621
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.8035714285714286,
      "macro_f1": 0.8,
      "weighted_f1": 0.8,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.8571428571428571,
          "f1-score": 0.8,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8571428571428571,
          "recall": 0.75,
          "f1-score": 0.8,
          "support": 8.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.8035714285714286,
          "recall": 0.8035714285714286,
          "f1-score": 0.8,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8071428571428572,
          "recall": 0.8,
          "f1-score": 0.8,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3181818181818182,
      "weighted_f1": 0.29696969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 1.0,
          "f1-score": 0.6363636363636364,
          "support": 7.0
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
          0,
          8
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
      "balanced_accuracy": 0.59375,
      "macro_f1": 0.5927601809954751,
      "weighted_f1": 0.5963800904977375,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6111111111111112,
          "recall": 0.6875,
          "f1-score": 0.6470588235294118,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5833333333333334,
          "recall": 0.5,
          "f1-score": 0.5384615384615384,
          "support": 14.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5972222222222223,
          "recall": 0.59375,
          "f1-score": 0.5927601809954751,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5981481481481482,
          "recall": 0.6,
          "f1-score": 0.5963800904977375,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          5
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4732142857142857,
      "macro_f1": 0.4642857142857143,
      "weighted_f1": 0.46190476190476193,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5714285714285714,
          "f1-score": 0.5,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.375,
          "f1-score": 0.42857142857142855,
          "support": 8.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4722222222222222,
          "recall": 0.4732142857142857,
          "f1-score": 0.4642857142857143,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.47407407407407404,
          "recall": 0.4666666666666667,
          "f1-score": 0.46190476190476193,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          3
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
      "accuracy": 0.6111111111111112,
      "balanced_accuracy": 0.6121541501976284,
      "macro_f1": 0.610678531701891,
      "weighted_f1": 0.6103901454290777,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6341463414634146,
          "recall": 0.5652173913043478,
          "f1-score": 0.5977011494252874,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5918367346938775,
          "recall": 0.6590909090909091,
          "f1-score": 0.6236559139784946,
          "support": 44.0
        },
        "accuracy": 0.6111111111111112,
        "macro avg": {
          "precision": 0.6129915380786461,
          "recall": 0.6121541501976284,
          "f1-score": 0.610678531701891,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.6134616448205298,
          "recall": 0.6111111111111112,
          "f1-score": 0.6103901454290777,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          26,
          20
        ],
        [
          15,
          29
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5666666666666667,
      "macro_f1": 0.466484268125855,
      "weighted_f1": 0.46648426812585503,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5357142857142857,
          "recall": 1.0,
          "f1-score": 0.6976744186046512,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.13333333333333333,
          "f1-score": 0.23529411764705882,
          "support": 15.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.7678571428571428,
          "recall": 0.5666666666666667,
          "f1-score": 0.466484268125855,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7678571428571428,
          "recall": 0.5666666666666667,
          "f1-score": 0.46648426812585503,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          15,
          0
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
      "mean": 0.5697,
      "lower_95": 0.497,
      "upper_95": 0.6424
    },
    "balanced_accuracy": {
      "mean": 0.5695,
      "lower_95": 0.4977,
      "upper_95": 0.6437
    },
    "macro_f1": {
      "mean": 0.5677,
      "lower_95": 0.4954,
      "upper_95": 0.6417
    }
  }
}
```