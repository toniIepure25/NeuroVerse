# Model Card: fw_ablation_1.0_3.0_8.0_30.0_fbcsp_logreg_csp2

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
  "accuracy": 0.503030303030303,
  "balanced_accuracy": 0.5033059065530414,
  "macro_f1": 0.5021342360906682,
  "weighted_f1": 0.5020062265278634,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5066666666666667,
      "recall": 0.4578313253012048,
      "f1-score": 0.4810126582278481,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.5487804878048781,
      "f1-score": 0.5232558139534884,
      "support": 82.0
    },
    "accuracy": 0.503030303030303,
    "macro avg": {
      "precision": 0.5033333333333334,
      "recall": 0.5033059065530414,
      "f1-score": 0.5021342360906682,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5033535353535354,
      "recall": 0.503030303030303,
      "f1-score": 0.5020062265278634,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      38,
      45
    ],
    [
      37,
      45
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.2628927410334455,
    "mce": 0.3694425955343445,
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
        "count": 30,
        "accuracy": 0.36666666666666664,
        "confidence": 0.5463597759840081
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 25,
        "accuracy": 0.44,
        "confidence": 0.6450842274389741
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 31,
        "accuracy": 0.6129032258064516,
        "confidence": 0.750482536226813
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 47,
        "accuracy": 0.48936170212765956,
        "confidence": 0.8588042976620041
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 32,
        "accuracy": 0.59375,
        "confidence": 0.9447075841212037
      }
    ],
    "brier_score": 0.3189762377217628
  },
  "auroc": 0.5411401704378489,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.301681587832166,
    "p95_inference_latency_ms": 7.916912399559806,
    "p99_inference_latency_ms": 8.294766360086212,
    "throughput_samples_per_sec": 136.95475322649548
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5892857142857143,
      "macro_f1": 0.5833333333333333,
      "weighted_f1": 0.5888888888888888,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.42857142857142855,
          "f1-score": 0.5,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.6,
          "recall": 0.75,
          "f1-score": 0.6666666666666666,
          "support": 8.0
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
          3,
          4
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
    "S003": {
      "task_type": "classification",
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.3125,
      "macro_f1": 0.25,
      "weighted_f1": 0.26666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.625,
          "f1-score": 0.5,
          "support": 8.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.20833333333333334,
          "recall": 0.3125,
          "f1-score": 0.25,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.22222222222222224,
          "recall": 0.3333333333333333,
          "f1-score": 0.26666666666666666,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          0,
          7
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.49107142857142855,
      "macro_f1": 0.4,
      "weighted_f1": 0.3866666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.125,
          "f1-score": 0.2,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.8571428571428571,
          "f1-score": 0.6,
          "support": 7.0
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
          1,
          7
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5803571428571428,
      "macro_f1": 0.5542857142857143,
      "weighted_f1": 0.5493333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6666666666666666,
          "recall": 0.375,
          "f1-score": 0.48,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5238095238095238,
          "recall": 0.7857142857142857,
          "f1-score": 0.6285714285714286,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5952380952380952,
          "recall": 0.5803571428571428,
          "f1-score": 0.5542857142857143,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.5666666666666667,
          "f1-score": 0.5493333333333333,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          6,
          10
        ],
        [
          3,
          11
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
      "balanced_accuracy": 0.4642857142857143,
      "macro_f1": 0.4642857142857143,
      "weighted_f1": 0.4666666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.42857142857142855,
          "f1-score": 0.42857142857142855,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5,
          "f1-score": 0.5,
          "support": 8.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4642857142857143,
          "recall": 0.4642857142857143,
          "f1-score": 0.4642857142857143,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.4666666666666667,
          "recall": 0.4666666666666667,
          "f1-score": 0.4666666666666667,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          3,
          4
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
      "accuracy": 0.5222222222222223,
      "balanced_accuracy": 0.525197628458498,
      "macro_f1": 0.5149768141371098,
      "weighted_f1": 0.5136594672125441,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.391304347826087,
          "f1-score": 0.45569620253164556,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5087719298245614,
          "recall": 0.6590909090909091,
          "f1-score": 0.5742574257425742,
          "support": 44.0
        },
        "accuracy": 0.5222222222222223,
        "macro avg": {
          "precision": 0.5271132376395534,
          "recall": 0.525197628458498,
          "f1-score": 0.5149768141371098,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5275208222576644,
          "recall": 0.5222222222222223,
          "f1-score": 0.5136594672125441,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          18,
          28
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
      "macro_f1": 0.4993581514762516,
      "weighted_f1": 0.4993581514762516,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.9333333333333333,
          "f1-score": 0.6829268292682927,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.2,
          "f1-score": 0.3157894736842105,
          "support": 15.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.6442307692307692,
          "recall": 0.5666666666666667,
          "f1-score": 0.4993581514762516,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.6442307692307693,
          "recall": 0.5666666666666667,
          "f1-score": 0.4993581514762516,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          14,
          1
        ],
        [
          12,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.4222222222222222,
      "balanced_accuracy": 0.41897233201581024,
      "macro_f1": 0.40789473684210525,
      "weighted_f1": 0.4099415204678362,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.375,
          "recall": 0.2727272727272727,
          "f1-score": 0.3157894736842105,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4482758620689655,
          "recall": 0.5652173913043478,
          "f1-score": 0.5,
          "support": 23.0
        },
        "accuracy": 0.4222222222222222,
        "macro avg": {
          "precision": 0.41163793103448276,
          "recall": 0.41897233201581024,
          "f1-score": 0.40789473684210525,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4124521072796935,
          "recall": 0.4222222222222222,
          "f1-score": 0.4099415204678362,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          6,
          16
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
      "mean": 0.5013,
      "lower_95": 0.4242,
      "upper_95": 0.5729
    },
    "balanced_accuracy": {
      "mean": 0.5015,
      "lower_95": 0.4273,
      "upper_95": 0.5736
    },
    "macro_f1": {
      "mean": 0.4989,
      "lower_95": 0.4215,
      "upper_95": 0.5695
    }
  }
}
```