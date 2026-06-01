# Model Card: fw_ablation_1.0_3.0_8.0_30.0_csp_lda_csp4

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
  "accuracy": 0.5272727272727272,
  "balanced_accuracy": 0.5260799294739935,
  "macro_f1": 0.5075757575757576,
  "weighted_f1": 0.5081726354453627,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5217391304347826,
      "recall": 0.7228915662650602,
      "f1-score": 0.6060606060606061,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.54,
      "recall": 0.32926829268292684,
      "f1-score": 0.4090909090909091,
      "support": 82.0
    },
    "accuracy": 0.5272727272727272,
    "macro avg": {
      "precision": 0.5308695652173914,
      "recall": 0.5260799294739935,
      "f1-score": 0.5075757575757576,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5308142292490119,
      "recall": 0.5272727272727272,
      "f1-score": 0.5081726354453627,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      60,
      23
    ],
    [
      55,
      27
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.14623558356853755,
    "mce": 0.27977888643791715,
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
        "confidence": 0.5511912051364649
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 55,
        "accuracy": 0.6181818181818182,
        "confidence": 0.6464261039396406
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 51,
        "accuracy": 0.47058823529411764,
        "confidence": 0.7503671217320348
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 10,
        "accuracy": 0.6,
        "confidence": 0.844158589527473
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 5,
        "accuracy": 0.8,
        "confidence": 0.9225426885030998
      }
    ],
    "brier_score": 0.2736180859713736
  },
  "auroc": 0.5503967087863649,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.35931212726912537,
    "p95_inference_latency_ms": 0.496101200042176,
    "p99_inference_latency_ms": 0.7022076802240916,
    "throughput_samples_per_sec": 2783.095598805098
  },
  "per_subject": {
    "S001": {
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.625,
      "macro_f1": 0.55,
      "weighted_f1": 0.5399999999999999,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 1.0,
          "f1-score": 0.7,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.25,
          "f1-score": 0.4,
          "support": 8.0
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
          7,
          0
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7410714285714286,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.730952380952381,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.8333333333333334,
          "recall": 0.625,
          "f1-score": 0.7142857142857143,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.8571428571428571,
          "f1-score": 0.75,
          "support": 7.0
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
          5,
          3
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.46875,
      "macro_f1": 0.3333333333333333,
      "weighted_f1": 0.3555555555555555,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5172413793103449,
          "recall": 0.9375,
          "f1-score": 0.6666666666666666,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 14.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.25862068965517243,
          "recall": 0.46875,
          "f1-score": 0.3333333333333333,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.27586206896551724,
          "recall": 0.5,
          "f1-score": 0.3555555555555555,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          15,
          1
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.48660714285714285,
      "macro_f1": 0.4712103407755582,
      "weighted_f1": 0.4794359576968273,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5238095238095238,
          "recall": 0.6875,
          "f1-score": 0.5945945945945946,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.2857142857142857,
          "f1-score": 0.34782608695652173,
          "support": 14.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.48412698412698413,
          "recall": 0.48660714285714285,
          "f1-score": 0.4712103407755582,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.48677248677248675,
          "recall": 0.5,
          "f1-score": 0.4794359576968273,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          5
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
      "accuracy": 0.5444444444444444,
      "balanced_accuracy": 0.541501976284585,
      "macro_f1": 0.5347371075526415,
      "weighted_f1": 0.5362305439975342,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.543859649122807,
          "recall": 0.6739130434782609,
          "f1-score": 0.6019417475728155,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.4090909090909091,
          "f1-score": 0.4675324675324675,
          "support": 44.0
        },
        "accuracy": 0.5444444444444444,
        "macro avg": {
          "precision": 0.5446570972886762,
          "recall": 0.541501976284585,
          "f1-score": 0.5347371075526415,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5446393762183236,
          "recall": 0.5444444444444444,
          "f1-score": 0.5362305439975342,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          31,
          15
        ],
        [
          26,
          18
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
      "macro_f1": 0.55,
      "weighted_f1": 0.55,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.9333333333333333,
          "f1-score": 0.7,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.8,
          "recall": 0.26666666666666666,
          "f1-score": 0.4,
          "support": 15.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.68,
          "recall": 0.6,
          "f1-score": 0.55,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6799999999999999,
          "recall": 0.6,
          "f1-score": 0.55,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          1
        ],
        [
          11,
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
      "mean": 0.5266,
      "lower_95": 0.4453,
      "upper_95": 0.5939
    },
    "balanced_accuracy": {
      "mean": 0.5259,
      "lower_95": 0.45,
      "upper_95": 0.5917
    },
    "macro_f1": {
      "mean": 0.5054,
      "lower_95": 0.43,
      "upper_95": 0.5781
    }
  }
}
```