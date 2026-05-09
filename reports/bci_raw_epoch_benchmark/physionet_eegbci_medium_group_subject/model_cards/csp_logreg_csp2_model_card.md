# Model Card: physionet_eegbci_medium_group_subject_csp_logreg_csp2

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
  "accuracy": 0.5111111111111111,
  "balanced_accuracy": 0.5007422068283028,
  "macro_f1": 0.4769515255580504,
  "weighted_f1": 0.48289232304553925,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5227272727272727,
      "recall": 0.7340425531914894,
      "f1-score": 0.6106194690265486,
      "support": 94.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4791666666666667,
      "recall": 0.26744186046511625,
      "f1-score": 0.34328358208955223,
      "support": 86.0
    },
    "accuracy": 0.5111111111111111,
    "macro avg": {
      "precision": 0.5009469696969697,
      "recall": 0.5007422068283028,
      "f1-score": 0.4769515255580504,
      "support": 180.0
    },
    "weighted avg": {
      "precision": 0.5019149831649832,
      "recall": 0.5111111111111111,
      "f1-score": 0.48289232304553925,
      "support": 180.0
    }
  },
  "confusion_matrix": [
    [
      69,
      25
    ],
    [
      63,
      23
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.18704679388424794,
    "mce": 0.727090092842019,
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
        "accuracy": 0.5652173913043478,
        "confidence": 0.5470189923330427
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 53,
        "accuracy": 0.41509433962264153,
        "confidence": 0.6506480777326673
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 44,
        "accuracy": 0.5681818181818182,
        "confidence": 0.7509265207472033
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 32,
        "accuracy": 0.5625,
        "confidence": 0.8334603452989435
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 5,
        "accuracy": 0.2,
        "confidence": 0.9270900928420189
      }
    ],
    "brier_score": 0.2953621146836642
  },
  "auroc": 0.4965363681345868,
  "split_strategy": "group_subject",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.2931525889936084,
    "p95_inference_latency_ms": 0.37190530165389646,
    "p99_inference_latency_ms": 0.4555235698171609,
    "throughput_samples_per_sec": 3411.19279701058
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5909090909090909,
      "macro_f1": 0.5132211538461539,
      "weighted_f1": 0.5177884615384616,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5609756097560976,
          "recall": 1.0,
          "f1-score": 0.71875,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.18181818181818182,
          "f1-score": 0.3076923076923077,
          "support": 22.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.7804878048780488,
          "recall": 0.5909090909090909,
          "f1-score": 0.5132211538461539,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.775609756097561,
          "recall": 0.6,
          "f1-score": 0.5177884615384616,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          23,
          0
        ],
        [
          18,
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4464285714285714,
      "macro_f1": 0.4,
      "weighted_f1": 0.4133333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.75,
          "f1-score": 0.6,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.14285714285714285,
          "f1-score": 0.2,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.41666666666666663,
          "recall": 0.4464285714285714,
          "f1-score": 0.4,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4222222222222222,
          "recall": 0.4666666666666667,
          "f1-score": 0.4133333333333333,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          18,
          6
        ],
        [
          18,
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4851190476190476,
      "macro_f1": 0.4327731092436975,
      "weighted_f1": 0.4235294117647059,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.20833333333333334,
          "f1-score": 0.29411764705882354,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45714285714285713,
          "recall": 0.7619047619047619,
          "f1-score": 0.5714285714285714,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.47857142857142854,
          "recall": 0.4851190476190476,
          "f1-score": 0.4327731092436975,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.48000000000000004,
          "recall": 0.4666666666666667,
          "f1-score": 0.4235294117647059,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          5,
          19
        ],
        [
          5,
          16
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
      "balanced_accuracy": 0.4788654060066741,
      "macro_f1": 0.4714407502131287,
      "weighted_f1": 0.4740835464620631,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.6129032258064516,
          "f1-score": 0.5507246376811594,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.3448275862068966,
          "f1-score": 0.39215686274509803,
          "support": 29.0
        },
        "accuracy": 0.48333333333333334,
        "macro avg": {
          "precision": 0.4772727272727273,
          "recall": 0.4788654060066741,
          "f1-score": 0.4714407502131287,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.47803030303030297,
          "recall": 0.48333333333333334,
          "f1-score": 0.4740835464620631,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          19,
          12
        ],
        [
          19,
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.5,
      "balanced_accuracy": 0.4872080088987764,
      "macro_f1": 0.40476190476190477,
      "weighted_f1": 0.41269841269841273,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5094339622641509,
          "recall": 0.8709677419354839,
          "f1-score": 0.6428571428571429,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.42857142857142855,
          "recall": 0.10344827586206896,
          "f1-score": 0.16666666666666666,
          "support": 29.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.4690026954177897,
          "recall": 0.4872080088987764,
          "f1-score": 0.40476190476190477,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.47035040431266845,
          "recall": 0.5,
          "f1-score": 0.41269841269841273,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          27,
          4
        ],
        [
          26,
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
      "accuracy": 0.55,
      "balanced_accuracy": 0.5379464285714286,
      "macro_f1": 0.5278344505974935,
      "weighted_f1": 0.5346546196444185,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5609756097560976,
          "recall": 0.71875,
          "f1-score": 0.6301369863013698,
          "support": 32.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5263157894736842,
          "recall": 0.35714285714285715,
          "f1-score": 0.425531914893617,
          "support": 28.0
        },
        "accuracy": 0.55,
        "macro avg": {
          "precision": 0.5436456996148908,
          "recall": 0.5379464285714286,
          "f1-score": 0.5278344505974935,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.544801026957638,
          "recall": 0.55,
          "f1-score": 0.5346546196444185,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          23,
          9
        ],
        [
          18,
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
      "mean": 0.5114,
      "lower_95": 0.4304,
      "upper_95": 0.5807
    },
    "balanced_accuracy": {
      "mean": 0.5027,
      "lower_95": 0.434,
      "upper_95": 0.5649
    },
    "macro_f1": {
      "mean": 0.4768,
      "lower_95": 0.4015,
      "upper_95": 0.5488
    }
  }
}
```