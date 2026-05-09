# Model Card: physionet_eegbci_medium_group_subject_csp_lda_csp6

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
  "accuracy": 0.4888888888888889,
  "balanced_accuracy": 0.4784760019792182,
  "macro_f1": 0.45317659490159823,
  "weighted_f1": 0.4593874286385184,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5075757575757576,
      "recall": 0.7127659574468085,
      "f1-score": 0.5929203539823009,
      "support": 94.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4375,
      "recall": 0.2441860465116279,
      "f1-score": 0.31343283582089554,
      "support": 86.0
    },
    "accuracy": 0.4888888888888889,
    "macro avg": {
      "precision": 0.4725378787878788,
      "recall": 0.4784760019792182,
      "f1-score": 0.45317659490159823,
      "support": 180.0
    },
    "weighted avg": {
      "precision": 0.4740951178451179,
      "recall": 0.4888888888888889,
      "f1-score": 0.4593874286385184,
      "support": 180.0
    }
  },
  "confusion_matrix": [
    [
      67,
      27
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
    "ece": 0.33658661590190797,
    "mce": 0.4254366934537724,
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
        "count": 7,
        "accuracy": 0.2857142857142857,
        "confidence": 0.5451680801350525
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 18,
        "accuracy": 0.6111111111111112,
        "confidence": 0.6480899120833166
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 42,
        "accuracy": 0.3333333333333333,
        "confidence": 0.7587700267871057
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 51,
        "accuracy": 0.5294117647058824,
        "confidence": 0.8482993507695467
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 62,
        "accuracy": 0.5483870967741935,
        "confidence": 0.9350352882192426
      }
    ],
    "brier_score": 0.3620425650046864
  },
  "auroc": 0.52894606630381,
  "split_strategy": "group_subject",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3076129388824079,
    "p95_inference_latency_ms": 0.38932665038373665,
    "p99_inference_latency_ms": 0.4513691688407563,
    "throughput_samples_per_sec": 3250.838549357226
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
    "S006": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.46130952380952384,
      "macro_f1": 0.3630769230769231,
      "weighted_f1": 0.381948717948718,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5121951219512195,
          "recall": 0.875,
          "f1-score": 0.6461538461538462,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.25,
          "recall": 0.047619047619047616,
          "f1-score": 0.08,
          "support": 21.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.38109756097560976,
          "recall": 0.46130952380952384,
          "f1-score": 0.3630769230769231,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.38983739837398373,
          "recall": 0.4888888888888889,
          "f1-score": 0.381948717948718,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          21,
          3
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
      "accuracy": 0.4444444444444444,
      "balanced_accuracy": 0.47619047619047616,
      "macro_f1": 0.3076923076923077,
      "weighted_f1": 0.28717948717948716,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.0,
          "recall": 0.0,
          "f1-score": 0.0,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.9523809523809523,
          "f1-score": 0.6153846153846154,
          "support": 21.0
        },
        "accuracy": 0.4444444444444444,
        "macro avg": {
          "precision": 0.22727272727272727,
          "recall": 0.47619047619047616,
          "f1-score": 0.3076923076923077,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.2121212121212121,
          "recall": 0.4444444444444444,
          "f1-score": 0.28717948717948716,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          0,
          24
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4582869855394883,
      "macro_f1": 0.4258373205741627,
      "weighted_f1": 0.43094098883572574,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4888888888888889,
          "recall": 0.7096774193548387,
          "f1-score": 0.5789473684210527,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.20689655172413793,
          "f1-score": 0.2727272727272727,
          "support": 29.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4444444444444444,
          "recall": 0.4582869855394883,
          "f1-score": 0.4258373205741627,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.44592592592592595,
          "recall": 0.4666666666666667,
          "f1-score": 0.43094098883572574,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          22,
          9
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
      "mean": 0.4881,
      "lower_95": 0.4111,
      "upper_95": 0.5667
    },
    "balanced_accuracy": {
      "mean": 0.4792,
      "lower_95": 0.4124,
      "upper_95": 0.5483
    },
    "macro_f1": {
      "mean": 0.4517,
      "lower_95": 0.3811,
      "upper_95": 0.5295
    }
  }
}
```