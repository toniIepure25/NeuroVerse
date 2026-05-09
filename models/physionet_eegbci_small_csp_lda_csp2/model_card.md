# Model Card: physionet_eegbci_small_csp_lda_csp2

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
  "accuracy": 0.4166666666666667,
  "balanced_accuracy": 0.41434927697441604,
  "macro_f1": 0.4125874125874126,
  "weighted_f1": 0.4142191142191142,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.4411764705882353,
      "recall": 0.4838709677419355,
      "f1-score": 0.46153846153846156,
      "support": 31.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.38461538461538464,
      "recall": 0.3448275862068966,
      "f1-score": 0.36363636363636365,
      "support": 29.0
    },
    "accuracy": 0.4166666666666667,
    "macro avg": {
      "precision": 0.41289592760180993,
      "recall": 0.41434927697441604,
      "f1-score": 0.4125874125874126,
      "support": 60.0
    },
    "weighted avg": {
      "precision": 0.41383861236802416,
      "recall": 0.4166666666666667,
      "f1-score": 0.4142191142191142,
      "support": 60.0
    }
  },
  "confusion_matrix": [
    [
      15,
      16
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
    "available": true,
    "ece": 0.12940361729205924,
    "mce": 0.13046050681473892,
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
        "count": 54,
        "accuracy": 0.4074074074074074,
        "confidence": 0.5378679142221463
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 6,
        "accuracy": 0.5,
        "confidence": 0.6198916115879423
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 0,
        "accuracy": null,
        "confidence": null
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 0,
        "accuracy": null,
        "confidence": null
      }
    ],
    "brier_score": 0.26092407873779944
  },
  "auroc": 0.4160177975528365,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.48871158329954295,
    "p95_inference_latency_ms": 0.9001654520034179,
    "p99_inference_latency_ms": 3.2267636289543518,
    "throughput_samples_per_sec": 2046.19664066173
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.33333333333333337,
      "macro_f1": 0.3212669683257918,
      "weighted_f1": 0.3212669683257918,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3684210526315789,
          "recall": 0.4666666666666667,
          "f1-score": 0.4117647058823529,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2727272727272727,
          "recall": 0.2,
          "f1-score": 0.23076923076923078,
          "support": 15.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.32057416267942584,
          "recall": 0.33333333333333337,
          "f1-score": 0.3212669683257918,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.32057416267942584,
          "recall": 0.3333333333333333,
          "f1-score": 0.3212669683257918,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          7,
          8
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5089285714285714,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4592592592592592,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.875,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.14285714285714285,
          "f1-score": 0.2222222222222222,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5192307692307692,
          "recall": 0.5089285714285714,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5205128205128206,
          "recall": 0.5333333333333333,
          "f1-score": 0.4592592592592592,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
    "S003": {
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
    }
  },
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.48214285714285715,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.437037037037037,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.7142857142857143,
          "f1-score": 0.5555555555555556,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.25,
          "f1-score": 0.3333333333333333,
          "support": 8.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4772727272727273,
          "recall": 0.48214285714285715,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.47878787878787876,
          "recall": 0.4666666666666667,
          "f1-score": 0.437037037037037,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.3333333333333333,
      "balanced_accuracy": 0.34375,
      "macro_f1": 0.3212669683257918,
      "weighted_f1": 0.3152337858220211,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.3,
          "recall": 0.1875,
          "f1-score": 0.23076923076923078,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.35,
          "recall": 0.5,
          "f1-score": 0.4117647058823529,
          "support": 14.0
        },
        "accuracy": 0.3333333333333333,
        "macro avg": {
          "precision": 0.32499999999999996,
          "recall": 0.34375,
          "f1-score": 0.3212669683257918,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.3233333333333333,
          "recall": 0.3333333333333333,
          "f1-score": 0.3152337858220211,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          3,
          13
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5089285714285714,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.4592592592592592,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5384615384615384,
          "recall": 0.875,
          "f1-score": 0.6666666666666666,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.14285714285714285,
          "f1-score": 0.2222222222222222,
          "support": 7.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.5192307692307692,
          "recall": 0.5089285714285714,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.5205128205128206,
          "recall": 0.5333333333333333,
          "f1-score": 0.4592592592592592,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.4136,
      "lower_95": 0.3,
      "upper_95": 0.55
    },
    "balanced_accuracy": {
      "mean": 0.4107,
      "lower_95": 0.2997,
      "upper_95": 0.5525
    },
    "macro_f1": {
      "mean": 0.4049,
      "lower_95": 0.2969,
      "upper_95": 0.5489
    }
  }
}
```