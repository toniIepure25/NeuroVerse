# Model Card: fw_ablation_1.0_4.0_8.0_35.0_riemann_mdm_csp8

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
  "balanced_accuracy": 0.5204231560387893,
  "macro_f1": 0.5125462772521596,
  "weighted_f1": 0.5129401792503396,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5192307692307693,
      "recall": 0.6506024096385542,
      "f1-score": 0.5775401069518716,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5245901639344263,
      "recall": 0.3902439024390244,
      "f1-score": 0.44755244755244755,
      "support": 82.0
    },
    "accuracy": 0.5212121212121212,
    "macro avg": {
      "precision": 0.5219104665825978,
      "recall": 0.5204231560387893,
      "f1-score": 0.5125462772521596,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5218942259925866,
      "recall": 0.5212121212121212,
      "f1-score": 0.5129401792503396,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      54,
      29
    ],
    [
      50,
      32
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.19565719531040324,
    "mce": 0.37831291957165625,
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
        "count": 49,
        "accuracy": 0.4489795918367347,
        "confidence": 0.5476074418549781
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 35,
        "accuracy": 0.6571428571428571,
        "confidence": 0.6502310417061499
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 29,
        "accuracy": 0.4827586206896552,
        "confidence": 0.7486632359357464
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 25,
        "accuracy": 0.48,
        "confidence": 0.8583129195716562
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 27,
        "accuracy": 0.5555555555555556,
        "confidence": 0.927396377911474
      }
    ],
    "brier_score": 0.30486014971885156
  },
  "auroc": 0.5279165442256832,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 1.1867769030273352,
    "p95_inference_latency_ms": 1.3291624001794842,
    "p99_inference_latency_ms": 1.5487789201142688,
    "throughput_samples_per_sec": 842.6183534993913
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
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5580357142857143,
      "macro_f1": 0.5542857142857143,
      "weighted_f1": 0.5592380952380952,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5789473684210527,
          "recall": 0.6875,
          "f1-score": 0.6285714285714286,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5454545454545454,
          "recall": 0.42857142857142855,
          "f1-score": 0.48,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.562200956937799,
          "recall": 0.5580357142857143,
          "f1-score": 0.5542857142857143,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.563317384370016,
          "recall": 0.5666666666666667,
          "f1-score": 0.5592380952380952,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          11,
          5
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
    },
    "S008": {
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
    "S009": {
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
    "S010": {
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5326086956521738,
      "macro_f1": 0.5324096981692232,
      "weighted_f1": 0.5328715157512783,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5416666666666666,
          "recall": 0.5652173913043478,
          "f1-score": 0.5531914893617021,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5238095238095238,
          "recall": 0.5,
          "f1-score": 0.5116279069767442,
          "support": 44.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5327380952380952,
          "recall": 0.5326086956521738,
          "f1-score": 0.5324096981692232,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5329365079365078,
          "recall": 0.5333333333333333,
          "f1-score": 0.5328715157512783,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          26,
          20
        ],
        [
          22,
          22
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3333333333333333,
      "weighted_f1": 0.3333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 1.0,
          "f1-score": 0.6666666666666666,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 15.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.25,
          "recall": 0.5,
          "f1-score": 0.3333333333333333,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.25,
          "recall": 0.5,
          "f1-score": 0.3333333333333333,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          15,
          0
        ],
        [
          15,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.5111111111111111,
      "balanced_accuracy": 0.5128458498023716,
      "macro_f1": 0.5089285714285714,
      "weighted_f1": 0.5082010582010582,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.5909090909090909,
          "f1-score": 0.5416666666666666,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5263157894736842,
          "recall": 0.43478260869565216,
          "f1-score": 0.47619047619047616,
          "support": 23.0
        },
        "accuracy": 0.5111111111111111,
        "macro avg": {
          "precision": 0.513157894736842,
          "recall": 0.5128458498023716,
          "f1-score": 0.5089285714285714,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5134502923976608,
          "recall": 0.5111111111111111,
          "f1-score": 0.5082010582010582,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          13,
          9
        ],
        [
          13,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5211,
      "lower_95": 0.4424,
      "upper_95": 0.5971
    },
    "balanced_accuracy": {
      "mean": 0.5205,
      "lower_95": 0.4451,
      "upper_95": 0.5909
    },
    "macro_f1": {
      "mean": 0.5112,
      "lower_95": 0.4327,
      "upper_95": 0.5816
    }
  }
}
```