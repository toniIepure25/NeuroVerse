# Model Card: fw_ablation_1.0_3.0_8.0_30.0_riemann_mdm_csp6

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
  "accuracy": 0.509090909090909,
  "balanced_accuracy": 0.508742286218043,
  "macro_f1": 0.5072811059907834,
  "weighted_f1": 0.507462086300796,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5108695652173914,
      "recall": 0.5662650602409639,
      "f1-score": 0.5371428571428571,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5068493150684932,
      "recall": 0.45121951219512196,
      "f1-score": 0.4774193548387097,
      "support": 82.0
    },
    "accuracy": 0.509090909090909,
    "macro avg": {
      "precision": 0.5088594401429423,
      "recall": 0.508742286218043,
      "f1-score": 0.5072811059907834,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.508871622719151,
      "recall": 0.509090909090909,
      "f1-score": 0.507462086300796,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      47,
      36
    ],
    [
      45,
      37
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.20618897759913904,
    "mce": 0.44803029943927364,
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
        "accuracy": 0.45454545454545453,
        "confidence": 0.5499895660910018
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 33,
        "accuracy": 0.6060606060606061,
        "confidence": 0.6493838699386079
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 38,
        "accuracy": 0.39473684210526316,
        "confidence": 0.7462097098438377
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 29,
        "accuracy": 0.6551724137931034,
        "confidence": 0.8492195663996284
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 21,
        "accuracy": 0.47619047619047616,
        "confidence": 0.9242207756297498
      }
    ],
    "brier_score": 0.303132110866822
  },
  "auroc": 0.5245371730825742,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 1.1657103696989273,
    "p95_inference_latency_ms": 1.2963370001671135,
    "p99_inference_latency_ms": 1.3920143601353627,
    "throughput_samples_per_sec": 857.8460190401103
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.49107142857142855,
      "macro_f1": 0.4,
      "weighted_f1": 0.3866666666666667,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.125,
          "f1-score": 0.2,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.8571428571428571,
          "f1-score": 0.6,
          "support": 14.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4807692307692308,
          "recall": 0.49107142857142855,
          "f1-score": 0.4,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.48205128205128206,
          "recall": 0.4666666666666667,
          "f1-score": 0.3866666666666667,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          2,
          14
        ],
        [
          2,
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
      "balanced_accuracy": 0.5357142857142857,
      "macro_f1": 0.4222222222222222,
      "weighted_f1": 0.44148148148148153,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5517241379310345,
          "recall": 1.0,
          "f1-score": 0.7111111111111111,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.07142857142857142,
          "f1-score": 0.13333333333333333,
          "support": 14.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.7758620689655172,
          "recall": 0.5357142857142857,
          "f1-score": 0.4222222222222222,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7609195402298851,
          "recall": 0.5666666666666667,
          "f1-score": 0.44148148148148153,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          16,
          0
        ],
        [
          13,
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5222222222222223,
      "balanced_accuracy": 0.5222332015810276,
      "macro_f1": 0.5221632300283986,
      "weighted_f1": 0.5222812144160459,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 0.5217391304347826,
          "f1-score": 0.5274725274725275,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5111111111111111,
          "recall": 0.5227272727272727,
          "f1-score": 0.5168539325842697,
          "support": 44.0
        },
        "accuracy": 0.5222222222222223,
        "macro avg": {
          "precision": 0.5222222222222221,
          "recall": 0.5222332015810276,
          "f1-score": 0.5221632300283986,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5224691358024691,
          "recall": 0.5222222222222223,
          "f1-score": 0.5222812144160459,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          24,
          22
        ],
        [
          21,
          23
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
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.48616600790513836,
      "macro_f1": 0.4796380090497738,
      "weighted_f1": 0.481179822356293,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.47058823529411764,
          "recall": 0.36363636363636365,
          "f1-score": 0.41025641025641024,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6086956521739131,
          "f1-score": 0.5490196078431373,
          "support": 23.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.4852941176470588,
          "recall": 0.48616600790513836,
          "f1-score": 0.4796380090497738,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.48562091503267973,
          "recall": 0.4888888888888889,
          "f1-score": 0.481179822356293,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          8,
          14
        ],
        [
          9,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5081,
      "lower_95": 0.4364,
      "upper_95": 0.5758
    },
    "balanced_accuracy": {
      "mean": 0.5078,
      "lower_95": 0.4358,
      "upper_95": 0.5791
    },
    "macro_f1": {
      "mean": 0.5049,
      "lower_95": 0.4328,
      "upper_95": 0.5731
    }
  }
}
```