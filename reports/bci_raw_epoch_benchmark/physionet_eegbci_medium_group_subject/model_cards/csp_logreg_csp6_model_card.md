# Model Card: physionet_eegbci_medium_group_subject_csp_logreg_csp6

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
  "accuracy": 0.4777777777777778,
  "balanced_accuracy": 0.4678377041068778,
  "macro_f1": 0.4445903361344538,
  "weighted_f1": 0.45062441643323997,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.6914893617021277,
      "f1-score": 0.5803571428571429,
      "support": 94.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.42,
      "recall": 0.2441860465116279,
      "f1-score": 0.3088235294117647,
      "support": 86.0
    },
    "accuracy": 0.4777777777777778,
    "macro avg": {
      "precision": 0.45999999999999996,
      "recall": 0.4678377041068778,
      "f1-score": 0.4445903361344538,
      "support": 180.0
    },
    "weighted avg": {
      "precision": 0.4617777777777778,
      "recall": 0.4777777777777778,
      "f1-score": 0.45062441643323997,
      "support": 180.0
    }
  },
  "confusion_matrix": [
    [
      65,
      29
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
    "ece": 0.3241807306483388,
    "mce": 0.4343311764371634,
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
        "accuracy": 0.1111111111111111,
        "confidence": 0.5454422875482745
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 24,
        "accuracy": 0.375,
        "confidence": 0.656157759281668
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 48,
        "accuracy": 0.4166666666666667,
        "confidence": 0.756250163261902
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 61,
        "accuracy": 0.5573770491803278,
        "confidence": 0.8547790434845999
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 38,
        "accuracy": 0.5789473684210527,
        "confidence": 0.9277430320230156
      }
    ],
    "brier_score": 0.3442050837018897
  },
  "auroc": 0.5285749628896586,
  "split_strategy": "group_subject",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.31384835004549433,
    "p95_inference_latency_ms": 0.4044651996082387,
    "p99_inference_latency_ms": 1.0629577091094697,
    "throughput_samples_per_sec": 3186.252213385999
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
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.44047619047619047,
      "macro_f1": 0.35096153846153844,
      "weighted_f1": 0.36923076923076925,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.8333333333333334,
          "f1-score": 0.625,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.2,
          "recall": 0.047619047619047616,
          "f1-score": 0.07692307692307693,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.35,
          "recall": 0.44047619047619047,
          "f1-score": 0.35096153846153844,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.36,
          "recall": 0.4666666666666667,
          "f1-score": 0.36923076923076925,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          20,
          4
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
      "accuracy": 0.45,
      "balanced_accuracy": 0.44438264738598443,
      "macro_f1": 0.4308709399252658,
      "weighted_f1": 0.43434895084794484,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.475,
          "recall": 0.6129032258064516,
          "f1-score": 0.5352112676056338,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.27586206896551724,
          "f1-score": 0.32653061224489793,
          "support": 29.0
        },
        "accuracy": 0.45,
        "macro avg": {
          "precision": 0.4375,
          "recall": 0.44438264738598443,
          "f1-score": 0.4308709399252658,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.43875000000000003,
          "recall": 0.45,
          "f1-score": 0.43434895084794484,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          19,
          12
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
      "mean": 0.4775,
      "lower_95": 0.3971,
      "upper_95": 0.5556
    },
    "balanced_accuracy": {
      "mean": 0.469,
      "lower_95": 0.3969,
      "upper_95": 0.5409
    },
    "macro_f1": {
      "mean": 0.4435,
      "lower_95": 0.3704,
      "upper_95": 0.5189
    }
  }
}
```