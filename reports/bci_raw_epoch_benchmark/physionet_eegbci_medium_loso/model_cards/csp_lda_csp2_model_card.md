# Model Card: physionet_eegbci_medium_loso_csp_lda_csp2

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
  "accuracy": 0.4666666666666667,
  "balanced_accuracy": 0.49404761904761907,
  "macro_f1": 0.37788018433179726,
  "weighted_f1": 0.3622119815668202,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.5,
      "recall": 0.08333333333333333,
      "f1-score": 0.14285714285714285,
      "support": 24.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.4634146341463415,
      "recall": 0.9047619047619048,
      "f1-score": 0.6129032258064516,
      "support": 21.0
    },
    "accuracy": 0.4666666666666667,
    "macro avg": {
      "precision": 0.4817073170731707,
      "recall": 0.49404761904761907,
      "f1-score": 0.37788018433179726,
      "support": 45.0
    },
    "weighted avg": {
      "precision": 0.4829268292682927,
      "recall": 0.4666666666666667,
      "f1-score": 0.3622119815668202,
      "support": 45.0
    }
  },
  "confusion_matrix": [
    [
      2,
      22
    ],
    [
      2,
      19
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.0932542884899508,
    "mce": 0.1963697757832304,
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
        "count": 38,
        "accuracy": 0.47368421052631576,
        "confidence": 0.5479435408306624
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 7,
        "accuracy": 0.42857142857142855,
        "confidence": 0.6249412043546589
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
    "brier_score": 0.2567711942444624
  },
  "auroc": 0.5456349206349207,
  "split_strategy": "leave_one_subject_out",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 0.3450920222449996,
    "p95_inference_latency_ms": 0.3820491994702024,
    "p99_inference_latency_ms": 0.48180875965044867,
    "throughput_samples_per_sec": 2897.7777970481325
  },
  "per_subject": {
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.49404761904761907,
      "macro_f1": 0.37788018433179726,
      "weighted_f1": 0.3622119815668202,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.08333333333333333,
          "f1-score": 0.14285714285714285,
          "support": 24.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4634146341463415,
          "recall": 0.9047619047619048,
          "f1-score": 0.6129032258064516,
          "support": 21.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4817073170731707,
          "recall": 0.49404761904761907,
          "f1-score": 0.37788018433179726,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4829268292682927,
          "recall": 0.4666666666666667,
          "f1-score": 0.3622119815668202,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          2,
          22
        ],
        [
          2,
          19
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
          "precision": 0.5,
          "recall": 0.25,
          "f1-score": 0.3333333333333333,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.7142857142857143,
          "f1-score": 0.5555555555555556,
          "support": 7.0
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
          2,
          6
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
    "4": {
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
    "8": {
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
    }
  },
  "bootstrap_confidence_intervals": {
    "available": true,
    "n_bootstrap": 500,
    "seed": 42,
    "accuracy": {
      "mean": 0.4668,
      "lower_95": 0.3333,
      "upper_95": 0.6
    },
    "balanced_accuracy": {
      "mean": 0.494,
      "lower_95": 0.4216,
      "upper_95": 0.5728
    },
    "macro_f1": {
      "mean": 0.3701,
      "lower_95": 0.2623,
      "upper_95": 0.5019
    }
  }
}
```