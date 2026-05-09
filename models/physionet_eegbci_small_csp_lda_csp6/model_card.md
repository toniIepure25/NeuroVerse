# Model Card: physionet_eegbci_small_csp_lda_csp6

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
  "accuracy": 0.55,
  "balanced_accuracy": 0.5389321468298109,
  "macro_f1": 0.48717948717948717,
  "weighted_f1": 0.49316239316239313,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.54,
      "recall": 0.8709677419354839,
      "f1-score": 0.6666666666666666,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.6,
      "recall": 0.20689655172413793,
      "f1-score": 0.3076923076923077,
      "support": 29.0
    },
    "accuracy": 0.55,
    "macro avg": {
      "precision": 0.5700000000000001,
      "recall": 0.5389321468298109,
      "f1-score": 0.48717948717948717,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.5690000000000001,
      "recall": 0.55,
      "f1-score": 0.49316239316239313,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      27,
      4
    ],
    [
      23,
      6
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.23150323843470444,
    "mce": 0.3801050866700848,
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
        "count": 9,
        "accuracy": 0.5555555555555556,
        "confidence": 0.5583578173258792
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 12,
        "accuracy": 0.3333333333333333,
        "confidence": 0.6410662953787637
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 6,
        "accuracy": 0.5,
        "confidence": 0.7407429179978798
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 15,
        "accuracy": 0.4666666666666667,
        "confidence": 0.8467717533367515
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 18,
        "accuracy": 0.7777777777777778,
        "confidence": 0.9458969220869798
      }
    ],
    "brier_score": 0.2866885650320453
  },
  "auroc": 0.6518353726362625,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3567880667105783,
    "p95_inference_latency_ms": 0.44153840117360227,
    "p99_inference_latency_ms": 0.5734503807252616,
    "throughput_samples_per_sec": 2802.784322972289
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.43333333333333335,
      "balanced_accuracy": 0.43333333333333335,
      "macro_f1": 0.3023255813953488,
      "weighted_f1": 0.3023255813953488,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4642857142857143,
          "recall": 0.8666666666666667,
          "f1-score": 0.6046511627906976,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 15.0
        },
        "accuracy": 0.43333333333333335,
        "macro avg": {
          "precision": 0.23214285714285715,
          "recall": 0.43333333333333335,
          "f1-score": 0.3023255813953488,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.23214285714285715,
          "recall": 0.43333333333333335,
          "f1-score": 0.3023255813953488,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          13,
          2
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7321428571428572,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.75,
          "f1-score": 0.75,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.7142857142857143,
          "f1-score": 0.7142857142857143,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.7321428571428572,
          "recall": 0.7321428571428572,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7333333333333333,
          "recall": 0.7333333333333333,
          "f1-score": 0.7333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
    "S003": {
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.4,
      "balanced_accuracy": 0.42857142857142855,
      "macro_f1": 0.2857142857142857,
      "weighted_f1": 0.26666666666666666,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.8571428571428571,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.21428571428571427,
          "recall": 0.42857142857142855,
          "f1-score": 0.2857142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.2,
          "recall": 0.4,
          "f1-score": 0.26666666666666666,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          1
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5044642857142857,
      "macro_f1": 0.4034090909090909,
      "weighted_f1": 0.42196969696969694,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5357142857142857,
          "recall": 0.9375,
          "f1-score": 0.6818181818181818,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.07142857142857142,
          "f1-score": 0.125,
          "support": 14.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5178571428571428,
          "recall": 0.5044642857142857,
          "f1-score": 0.4034090909090909,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.5190476190476191,
          "recall": 0.5333333333333333,
          "f1-score": 0.42196969696969694,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          15,
          1
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
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7321428571428572,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.75,
          "f1-score": 0.75,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.7142857142857143,
          "f1-score": 0.7142857142857143,
          "support": 7.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.7321428571428572,
          "recall": 0.7321428571428572,
          "f1-score": 0.7321428571428572,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.7333333333333333,
          "recall": 0.7333333333333333,
          "f1-score": 0.7333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          6,
          2
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5526,
      "lower_95": 0.4333,
      "upper_95": 0.6833
    },
    "balanced_accuracy": {
      "mean": 0.5399,
      "lower_95": 0.4381,
      "upper_95": 0.6455
    },
    "macro_f1": {
      "mean": 0.4853,
      "lower_95": 0.3625,
      "upper_95": 0.6241
    }
  }
}
```