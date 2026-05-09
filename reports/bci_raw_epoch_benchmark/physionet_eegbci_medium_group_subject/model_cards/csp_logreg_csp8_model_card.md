# Model Card: physionet_eegbci_medium_group_subject_csp_logreg_csp8

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
  "accuracy": 0.5,
  "balanced_accuracy": 0.48911429985155863,
  "macro_f1": 0.46172248803827753,
  "weighted_f1": 0.46810207336523124,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5149253731343284,
      "recall": 0.7340425531914894,
      "f1-score": 0.6052631578947368,
      "support": 94.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.45652173913043476,
      "recall": 0.2441860465116279,
      "f1-score": 0.3181818181818182,
      "support": 86.0
    },
    "accuracy": 0.5,
    "macro avg": {
      "precision": 0.4857235561323816,
      "recall": 0.48911429985155863,
      "f1-score": 0.46172248803827753,
      "support": 180.0
    },
    "weighted avg": {
      "precision": 0.48702141466580146,
      "recall": 0.5,
      "f1-score": 0.46810207336523124,
      "support": 180.0
    }
  },
  "confusion_matrix": [
    [
      69,
      25
    ],
    [
      65,
      21
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.2953924742819012,
    "mce": 0.36980287527502886,
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
        "accuracy": 0.6086956521739131,
        "confidence": 0.5592741472915003
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 28,
        "accuracy": 0.2857142857142857,
        "confidence": 0.655003140609548
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 36,
        "accuracy": 0.4722222222222222,
        "confidence": 0.7525106093860753
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 50,
        "accuracy": 0.54,
        "confidence": 0.8540391449330884
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 43,
        "accuracy": 0.5581395348837209,
        "confidence": 0.9279424101587498
      }
    ],
    "brier_score": 0.3380635275461129
  },
  "auroc": 0.5204106877783277,
  "split_strategy": "group_subject",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.2976236611377519,
    "p95_inference_latency_ms": 0.3305792992250644,
    "p99_inference_latency_ms": 0.3412757406658784,
    "throughput_samples_per_sec": 3359.947916026612
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.5111111111111111,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.3382352941176471,
      "weighted_f1": 0.34575163398692815,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5111111111111111,
          "recall": 1.0,
          "f1-score": 0.6764705882352942,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 22.0
        },
        "accuracy": 0.5111111111111111,
        "macro avg": {
          "precision": 0.25555555555555554,
          "recall": 0.5,
          "f1-score": 0.3382352941176471,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.26123456790123456,
          "recall": 0.5111111111111111,
          "f1-score": 0.34575163398692815,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          23,
          0
        ],
        [
          22,
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
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.4782608695652174,
      "macro_f1": 0.3283582089552239,
      "weighted_f1": 0.33565505804311774,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.9565217391304348,
          "f1-score": 0.6567164179104478,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 22.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.25,
          "recall": 0.4782608695652174,
          "f1-score": 0.3283582089552239,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.25555555555555554,
          "recall": 0.4888888888888889,
          "f1-score": 0.33565505804311774,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          22,
          1
        ],
        [
          22,
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
    "S006": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5029761904761905,
      "macro_f1": 0.3867618429591174,
      "weighted_f1": 0.40674886437378327,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5348837209302325,
          "recall": 0.9583333333333334,
          "f1-score": 0.6865671641791045,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.047619047619047616,
          "f1-score": 0.08695652173913043,
          "support": 21.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5174418604651163,
          "recall": 0.5029761904761905,
          "f1-score": 0.3867618429591174,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.5186046511627906,
          "recall": 0.5333333333333333,
          "f1-score": 0.40674886437378327,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          23,
          1
        ],
        [
          20,
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4970238095238095,
      "macro_f1": 0.35096153846153844,
      "weighted_f1": 0.33269230769230773,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.041666666666666664,
          "f1-score": 0.07692307692307693,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46511627906976744,
          "recall": 0.9523809523809523,
          "f1-score": 0.625,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4825581395348837,
          "recall": 0.4970238095238095,
          "f1-score": 0.35096153846153844,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.48372093023255813,
          "recall": 0.4666666666666667,
          "f1-score": 0.33269230769230773,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          1,
          23
        ],
        [
          1,
          20
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
      "accuracy": 0.48333333333333334,
      "balanced_accuracy": 0.47664071190211343,
      "macro_f1": 0.4578839988341591,
      "weighted_f1": 0.46179928106480134,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6774193548387096,
          "f1-score": 0.5753424657534246,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.27586206896551724,
          "f1-score": 0.3404255319148936,
          "support": 29.0
        },
        "accuracy": 0.48333333333333334,
        "macro avg": {
          "precision": 0.4722222222222222,
          "recall": 0.47664071190211343,
          "f1-score": 0.4578839988341591,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4731481481481481,
          "recall": 0.48333333333333334,
          "f1-score": 0.46179928106480134,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          21,
          10
        ],
        [
          21,
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.5,
      "balanced_accuracy": 0.4905450500556173,
      "macro_f1": 0.45054945054945056,
      "weighted_f1": 0.45604395604395603,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5106382978723404,
          "recall": 0.7741935483870968,
          "f1-score": 0.6153846153846154,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.46153846153846156,
          "recall": 0.20689655172413793,
          "f1-score": 0.2857142857142857,
          "support": 29.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.486088379705401,
          "recall": 0.4905450500556173,
          "f1-score": 0.45054945054945056,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.4869067103109656,
          "recall": 0.5,
          "f1-score": 0.45604395604395603,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          24,
          7
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
        "available": false
      }
    },
    "8": {
      "task_type": "classification",
      "accuracy": 0.5166666666666667,
      "balanced_accuracy": 0.5,
      "macro_f1": 0.4744790093627303,
      "weighted_f1": 0.4844055169636565,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5333333333333333,
          "recall": 0.75,
          "f1-score": 0.6233766233766234,
          "support": 32.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 0.25,
          "f1-score": 0.32558139534883723,
          "support": 28.0
        },
        "accuracy": 0.5166666666666667,
        "macro avg": {
          "precision": 0.5,
          "recall": 0.5,
          "f1-score": 0.4744790093627303,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.5022222222222222,
          "recall": 0.5166666666666667,
          "f1-score": 0.4844055169636565,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          24,
          8
        ],
        [
          21,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.4996,
      "lower_95": 0.4222,
      "upper_95": 0.5778
    },
    "balanced_accuracy": {
      "mean": 0.4902,
      "lower_95": 0.4222,
      "upper_95": 0.5551
    },
    "macro_f1": {
      "mean": 0.4605,
      "lower_95": 0.3876,
      "upper_95": 0.5358
    }
  }
}
```