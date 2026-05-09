# Model Card: physionet_eegbci_medium_group_subject_csp_logreg_csp4

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
  "balanced_accuracy": 0.49208312716476993,
  "macro_f1": 0.4791666666666667,
  "weighted_f1": 0.48379629629629634,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5163934426229508,
      "recall": 0.6702127659574468,
      "f1-score": 0.5833333333333334,
      "support": 94.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.46551724137931033,
      "recall": 0.313953488372093,
      "f1-score": 0.375,
      "support": 86.0
    },
    "accuracy": 0.5,
    "macro avg": {
      "precision": 0.49095534200113056,
      "recall": 0.49208312716476993,
      "f1-score": 0.4791666666666667,
      "support": 180.0
    },
    "weighted avg": {
      "precision": 0.4920859242509893,
      "recall": 0.5,
      "f1-score": 0.48379629629629634,
      "support": 180.0
    }
  },
  "confusion_matrix": [
    [
      63,
      31
    ],
    [
      59,
      27
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.30952710453747,
    "mce": 0.38634628943080773,
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
        "count": 13,
        "accuracy": 0.46153846153846156,
        "confidence": 0.5296196947781802
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 17,
        "accuracy": 0.4117647058823529,
        "confidence": 0.6573200355127539
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 32,
        "accuracy": 0.5,
        "confidence": 0.7561284846238929
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 79,
        "accuracy": 0.5063291139240507,
        "confidence": 0.8530603213309541
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 39,
        "accuracy": 0.5384615384615384,
        "confidence": 0.9248078278923462
      }
    ],
    "brier_score": 0.35610405719646354
  },
  "auroc": 0.5076694705591291,
  "split_strategy": "group_subject",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.27313201670848586,
    "p95_inference_latency_ms": 0.31948165133144346,
    "p99_inference_latency_ms": 0.37693205062169,
    "throughput_samples_per_sec": 3661.233172335491
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.5333333333333333,
      "balanced_accuracy": 0.5227272727272727,
      "macro_f1": 0.3867618429591174,
      "weighted_f1": 0.39342418343067276,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5227272727272727,
          "recall": 1.0,
          "f1-score": 0.6865671641791045,
          "support": 23.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.045454545454545456,
          "f1-score": 0.08695652173913043,
          "support": 22.0
        },
        "accuracy": 0.5333333333333333,
        "macro avg": {
          "precision": 0.7613636363636364,
          "recall": 0.5227272727272727,
          "f1-score": 0.3867618429591174,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.7560606060606061,
          "recall": 0.5333333333333333,
          "f1-score": 0.39342418343067276,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          23,
          0
        ],
        [
          21,
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
      "balanced_accuracy": 0.4732142857142857,
      "macro_f1": 0.44976076555023925,
      "weighted_f1": 0.4595427963849016,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5151515151515151,
          "recall": 0.7083333333333334,
          "f1-score": 0.5964912280701754,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.23809523809523808,
          "f1-score": 0.30303030303030304,
          "support": 21.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.46590909090909094,
          "recall": 0.4732142857142857,
          "f1-score": 0.44976076555023925,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.46919191919191916,
          "recall": 0.4888888888888889,
          "f1-score": 0.4595427963849016,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          17,
          7
        ],
        [
          16,
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
    "S009": {
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
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4666666666666667,
          "recall": 1.0,
          "f1-score": 0.6363636363636364,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.23333333333333334,
          "recall": 0.5,
          "f1-score": 0.3181818181818182,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.2177777777777778,
          "recall": 0.4666666666666667,
          "f1-score": 0.29696969696969694,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          0,
          24
        ],
        [
          0,
          21
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
      "accuracy": 0.5,
      "balanced_accuracy": 0.49721913236929927,
      "macro_f1": 0.4949494949494949,
      "weighted_f1": 0.49663299663299654,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5142857142857142,
          "recall": 0.5806451612903226,
          "f1-score": 0.5454545454545454,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.48,
          "recall": 0.41379310344827586,
          "f1-score": 0.4444444444444444,
          "support": 29.0
        },
        "accuracy": 0.5,
        "macro avg": {
          "precision": 0.4971428571428571,
          "recall": 0.49721913236929927,
          "f1-score": 0.4949494949494949,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.49771428571428566,
          "recall": 0.5,
          "f1-score": 0.49663299663299654,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          18,
          13
        ],
        [
          17,
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
    "4": {
      "task_type": "classification",
      "accuracy": 0.48333333333333334,
      "balanced_accuracy": 0.4755283648498332,
      "macro_f1": 0.4488888888888889,
      "weighted_f1": 0.4534814814814815,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.7096774193548387,
          "f1-score": 0.5866666666666667,
          "support": 31.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4375,
          "recall": 0.2413793103448276,
          "f1-score": 0.3111111111111111,
          "support": 29.0
        },
        "accuracy": 0.48333333333333334,
        "macro avg": {
          "precision": 0.46875,
          "recall": 0.4755283648498332,
          "f1-score": 0.4488888888888889,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.46979166666666666,
          "recall": 0.48333333333333334,
          "f1-score": 0.4534814814814815,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          22,
          9
        ],
        [
          22,
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
      "accuracy": 0.5166666666666667,
      "balanced_accuracy": 0.5022321428571428,
      "macro_f1": 0.48444444444444446,
      "weighted_f1": 0.493037037037037,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5348837209302325,
          "recall": 0.71875,
          "f1-score": 0.6133333333333333,
          "support": 32.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.47058823529411764,
          "recall": 0.2857142857142857,
          "f1-score": 0.35555555555555557,
          "support": 28.0
        },
        "accuracy": 0.5166666666666667,
        "macro avg": {
          "precision": 0.5027359781121751,
          "recall": 0.5022321428571428,
          "f1-score": 0.48444444444444446,
          "support": 60.0
        },
        "weighted avg": {
          "precision": 0.5048791609667123,
          "recall": 0.5166666666666667,
          "f1-score": 0.493037037037037,
          "support": 60.0
        }
      },
      "confusion_matrix": [
        [
          23,
          9
        ],
        [
          20,
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.5001,
      "lower_95": 0.4278,
      "upper_95": 0.5778
    },
    "balanced_accuracy": {
      "mean": 0.4933,
      "lower_95": 0.4205,
      "upper_95": 0.5645
    },
    "macro_f1": {
      "mean": 0.4786,
      "lower_95": 0.4046,
      "upper_95": 0.5578
    }
  }
}
```