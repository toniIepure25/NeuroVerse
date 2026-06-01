# Model Card: fw_ablation_1.0_4.0_8.0_35.0_csp_lda_csp4

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
  "accuracy": 0.5212121212121212,
  "balanced_accuracy": 0.519761974728181,
  "macro_f1": 0.4913170731707317,
  "weighted_f1": 0.49206444937176647,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5163934426229508,
      "recall": 0.7590361445783133,
      "f1-score": 0.6146341463414634,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5348837209302325,
      "recall": 0.2804878048780488,
      "f1-score": 0.368,
      "support": 82.0
    },
    "accuracy": 0.5212121212121212,
    "macro avg": {
      "precision": 0.5256385817765916,
      "recall": 0.519761974728181,
      "f1-score": 0.4913170731707317,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.525582550630206,
      "recall": 0.5212121212121212,
      "f1-score": 0.49206444937176647,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      63,
      20
    ],
    [
      59,
      23
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.14796561618120488,
    "mce": 0.25889660535087256,
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
        "count": 46,
        "accuracy": 0.5434782608695652,
        "confidence": 0.5525232916678597
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 57,
        "accuracy": 0.42105263157894735,
        "confidence": 0.643424176822469
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 42,
        "accuracy": 0.5952380952380952,
        "confidence": 0.7458208654972719
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 17,
        "accuracy": 0.5882352941176471,
        "confidence": 0.836583000432852
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 3,
        "accuracy": 0.6666666666666666,
        "confidence": 0.9255632720175392
      }
    ],
    "brier_score": 0.27514370994985415
  },
  "auroc": 0.5411401704378489,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.32334626665749855,
    "p95_inference_latency_ms": 0.4325309997511793,
    "p99_inference_latency_ms": 0.47514852009044234,
    "throughput_samples_per_sec": 3092.6597988503777
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
      "accuracy": 0.26666666666666666,
      "balanced_accuracy": 0.2857142857142857,
      "macro_f1": 0.21052631578947367,
      "weighted_f1": 0.19649122807017544,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.5714285714285714,
          "f1-score": 0.42105263157894735,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "accuracy": 0.26666666666666666,
        "macro avg": {
          "precision": 0.16666666666666666,
          "recall": 0.2857142857142857,
          "f1-score": 0.21052631578947367,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.15555555555555553,
          "recall": 0.26666666666666666,
          "f1-score": 0.19649122807017544,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          3
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5625,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4296296296296296,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.125,
          "f1-score": 0.2222222222222222,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 1.0,
          "f1-score": 0.6666666666666666,
          "support": 7.0
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
          1,
          7
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5446428571428571,
      "macro_f1": 0.4993581514762516,
      "weighted_f1": 0.5115960633290544,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.56,
          "recall": 0.875,
          "f1-score": 0.6829268292682927,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.21428571428571427,
          "f1-score": 0.3157894736842105,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5800000000000001,
          "recall": 0.5446428571428571,
          "f1-score": 0.4993581514762516,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5786666666666667,
          "recall": 0.5666666666666667,
          "f1-score": 0.5115960633290544,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          2
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
      "accuracy": 0.5222222222222223,
      "balanced_accuracy": 0.5192687747035574,
      "macro_f1": 0.5120413567015508,
      "weighted_f1": 0.5136076437047311,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5263157894736842,
          "recall": 0.6521739130434783,
          "f1-score": 0.5825242718446602,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5151515151515151,
          "recall": 0.38636363636363635,
          "f1-score": 0.44155844155844154,
          "support": 44.0
        },
        "accuracy": 0.5222222222222223,
        "macro avg": {
          "precision": 0.5207336523125996,
          "recall": 0.5192687747035574,
          "f1-score": 0.5120413567015508,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5208576998050682,
          "recall": 0.5222222222222223,
          "f1-score": 0.5136076437047311,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          30,
          16
        ],
        [
          27,
          17
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
      "balanced_accuracy": 0.49604743083003955,
      "macro_f1": 0.434117003827228,
      "weighted_f1": 0.4302047263228237,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4864864864864865,
          "recall": 0.8181818181818182,
          "f1-score": 0.6101694915254238,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.17391304347826086,
          "f1-score": 0.25806451612903225,
          "support": 23.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.49324324324324326,
          "recall": 0.49604743083003955,
          "f1-score": 0.434117003827228,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4933933933933934,
          "recall": 0.4888888888888889,
          "f1-score": 0.4302047263228237,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          18,
          4
        ],
        [
          19,
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5209,
      "lower_95": 0.4453,
      "upper_95": 0.5939
    },
    "balanced_accuracy": {
      "mean": 0.52,
      "lower_95": 0.4538,
      "upper_95": 0.5826
    },
    "macro_f1": {
      "mean": 0.4898,
      "lower_95": 0.4147,
      "upper_95": 0.5635
    }
  }
}
```