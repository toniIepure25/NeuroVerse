# Model Card: physionet_eegbci_medium_fbcsp_lda_csp2

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
  "accuracy": 0.5757575757575758,
  "balanced_accuracy": 0.5761093153100205,
  "macro_f1": 0.5744916003536693,
  "weighted_f1": 0.574350936419902,
  "per_class": {
    "LEFT_HAND_IMAGERY": {
      "precision": 0.589041095890411,
      "recall": 0.5180722891566265,
      "f1-score": 0.5512820512820513,
      "support": 83.0
    },
    "RIGHT_HAND_IMAGERY": {
      "precision": 0.5652173913043478,
      "recall": 0.6341463414634146,
      "f1-score": 0.5977011494252874,
      "support": 82.0
    },
    "accuracy": 0.5757575757575758,
    "macro avg": {
      "precision": 0.5771292435973794,
      "recall": 0.5761093153100205,
      "f1-score": 0.5744916003536693,
      "support": 165.0
    },
    "weighted avg": {
      "precision": 0.5772014366415795,
      "recall": 0.5757575757575758,
      "f1-score": 0.574350936419902,
      "support": 165.0
    }
  },
  "confusion_matrix": [
    [
      43,
      40
    ],
    [
      30,
      52
    ]
  ],
  "class_labels": [
    "LEFT_HAND_IMAGERY",
    "RIGHT_HAND_IMAGERY"
  ],
  "calibration": {
    "available": true,
    "ece": 0.22221660747919453,
    "mce": 0.3169244908456199,
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
        "count": 21,
        "accuracy": 0.6190476190476191,
        "confidence": 0.543810742309814
      },
      {
        "lo": 0.6000000000000001,
        "hi": 0.7000000000000001,
        "count": 29,
        "accuracy": 0.5517241379310345,
        "confidence": 0.6490466815399856
      },
      {
        "lo": 0.7000000000000001,
        "hi": 0.8,
        "count": 36,
        "accuracy": 0.5277777777777778,
        "confidence": 0.7496337311564562
      },
      {
        "lo": 0.8,
        "hi": 0.9,
        "count": 41,
        "accuracy": 0.5609756097560976,
        "confidence": 0.8593528557109179
      },
      {
        "lo": 0.9,
        "hi": 1.0,
        "count": 38,
        "accuracy": 0.631578947368421,
        "confidence": 0.9485034382140409
      }
    ],
    "brier_score": 0.30449819170926395
  },
  "auroc": 0.5755215985894798,
  "split_strategy": "group_run",
  "split_warnings": [],
  "latency": {
    "mean_inference_latency_ms": 7.246002375706501,
    "p95_inference_latency_ms": 8.153906200095662,
    "p99_inference_latency_ms": 8.597072959673822,
    "throughput_samples_per_sec": 138.007131125526
  },
  "per_subject": {
    "S001": {
      "task_type": "classification",
      "accuracy": 0.6,
      "balanced_accuracy": 0.5982142857142857,
      "macro_f1": 0.5982142857142857,
      "weighted_f1": 0.6,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5714285714285714,
          "recall": 0.5714285714285714,
          "f1-score": 0.5714285714285714,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.625,
          "recall": 0.625,
          "f1-score": 0.625,
          "support": 8.0
        },
        "accuracy": 0.6,
        "macro avg": {
          "precision": 0.5982142857142857,
          "recall": 0.5982142857142857,
          "f1-score": 0.5982142857142857,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.6,
          "recall": 0.6,
          "f1-score": 0.6,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          4,
          3
        ],
        [
          3,
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
    "S002": {
      "task_type": "classification",
      "accuracy": 0.8,
      "balanced_accuracy": 0.8125,
      "macro_f1": 0.7963800904977376,
      "weighted_f1": 0.7945701357466064,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7,
          "recall": 1.0,
          "f1-score": 0.8235294117647058,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.625,
          "f1-score": 0.7692307692307693,
          "support": 8.0
        },
        "accuracy": 0.8,
        "macro avg": {
          "precision": 0.85,
          "recall": 0.8125,
          "f1-score": 0.7963800904977376,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.8599999999999999,
          "recall": 0.8,
          "f1-score": 0.7945701357466064,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          0
        ],
        [
          3,
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
      "accuracy": 0.4,
      "balanced_accuracy": 0.41964285714285715,
      "macro_f1": 0.354066985645933,
      "weighted_f1": 0.34258373205741627,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4166666666666667,
          "recall": 0.7142857142857143,
          "f1-score": 0.5263157894736842,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.3333333333333333,
          "recall": 0.125,
          "f1-score": 0.18181818181818182,
          "support": 8.0
        },
        "accuracy": 0.4,
        "macro avg": {
          "precision": 0.375,
          "recall": 0.41964285714285715,
          "f1-score": 0.354066985645933,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.3722222222222223,
          "recall": 0.4,
          "f1-score": 0.34258373205741627,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          2
        ],
        [
          7,
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
    "S004": {
      "task_type": "classification",
      "accuracy": 0.9333333333333333,
      "balanced_accuracy": 0.9375,
      "macro_f1": 0.9333333333333333,
      "weighted_f1": 0.9333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 1.0,
          "recall": 0.875,
          "f1-score": 0.9333333333333333,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.875,
          "recall": 1.0,
          "f1-score": 0.9333333333333333,
          "support": 7.0
        },
        "accuracy": 0.9333333333333333,
        "macro avg": {
          "precision": 0.9375,
          "recall": 0.9375,
          "f1-score": 0.9333333333333333,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.9416666666666667,
          "recall": 0.9333333333333333,
          "f1-score": 0.9333333333333333,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          7,
          1
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
      "balanced_accuracy": 0.48214285714285715,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.437037037037037,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.25,
          "f1-score": 0.3333333333333333,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.45454545454545453,
          "recall": 0.7142857142857143,
          "f1-score": 0.5555555555555556,
          "support": 14.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4772727272727273,
          "recall": 0.48214285714285715,
          "f1-score": 0.4444444444444444,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.47878787878787876,
          "recall": 0.4666666666666667,
          "f1-score": 0.437037037037037,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          4,
          12
        ],
        [
          4,
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
    "S008": {
      "task_type": "classification",
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7321428571428572,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7333333333333333,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7142857142857143,
          "recall": 0.7142857142857143,
          "f1-score": 0.7142857142857143,
          "support": 7.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.75,
          "recall": 0.75,
          "f1-score": 0.75,
          "support": 8.0
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
          5,
          2
        ],
        [
          2,
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
    "S009": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.45535714285714285,
      "macro_f1": 0.4444444444444444,
      "weighted_f1": 0.45185185185185184,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.625,
          "f1-score": 0.5555555555555556,
          "support": 8.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4,
          "recall": 0.2857142857142857,
          "f1-score": 0.3333333333333333,
          "support": 7.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.45,
          "recall": 0.45535714285714285,
          "f1-score": 0.4444444444444444,
          "support": 15.0
        },
        "weighted avg": {
          "precision": 0.45333333333333337,
          "recall": 0.4666666666666667,
          "f1-score": 0.45185185185185184,
          "support": 15.0
        }
      },
      "confusion_matrix": [
        [
          5,
          3
        ],
        [
          5,
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
    "S010": {
      "task_type": "classification",
      "accuracy": 0.4666666666666667,
      "balanced_accuracy": 0.4732142857142857,
      "macro_f1": 0.4642857142857143,
      "weighted_f1": 0.46190476190476193,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.375,
          "f1-score": 0.42857142857142855,
          "support": 16.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.4444444444444444,
          "recall": 0.5714285714285714,
          "f1-score": 0.5,
          "support": 14.0
        },
        "accuracy": 0.4666666666666667,
        "macro avg": {
          "precision": 0.4722222222222222,
          "recall": 0.4732142857142857,
          "f1-score": 0.4642857142857143,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.47407407407407404,
          "recall": 0.4666666666666667,
          "f1-score": 0.46190476190476193,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          6,
          10
        ],
        [
          6,
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
  "per_run": {
    "12": {
      "task_type": "classification",
      "accuracy": 0.5666666666666667,
      "balanced_accuracy": 0.5696640316205533,
      "macro_f1": 0.5600952500313323,
      "weighted_f1": 0.558900447006726,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.6060606060606061,
          "recall": 0.43478260869565216,
          "f1-score": 0.5063291139240507,
          "support": 46.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.543859649122807,
          "recall": 0.7045454545454546,
          "f1-score": 0.6138613861386139,
          "support": 44.0
        },
        "accuracy": 0.5666666666666667,
        "macro avg": {
          "precision": 0.5749601275917066,
          "recall": 0.5696640316205533,
          "f1-score": 0.5600952500313323,
          "support": 90.0
        },
        "weighted avg": {
          "precision": 0.5756512493354599,
          "recall": 0.5666666666666667,
          "f1-score": 0.558900447006726,
          "support": 90.0
        }
      },
      "confusion_matrix": [
        [
          20,
          26
        ],
        [
          13,
          31
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
      "accuracy": 0.7333333333333333,
      "balanced_accuracy": 0.7333333333333334,
      "macro_f1": 0.7321428571428572,
      "weighted_f1": 0.7321428571428572,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.7058823529411765,
          "recall": 0.8,
          "f1-score": 0.75,
          "support": 15.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.7692307692307693,
          "recall": 0.6666666666666666,
          "f1-score": 0.7142857142857143,
          "support": 15.0
        },
        "accuracy": 0.7333333333333333,
        "macro avg": {
          "precision": 0.7375565610859729,
          "recall": 0.7333333333333334,
          "f1-score": 0.7321428571428572,
          "support": 30.0
        },
        "weighted avg": {
          "precision": 0.7375565610859728,
          "recall": 0.7333333333333333,
          "f1-score": 0.7321428571428572,
          "support": 30.0
        }
      },
      "confusion_matrix": [
        [
          12,
          3
        ],
        [
          5,
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
    "8": {
      "task_type": "classification",
      "accuracy": 0.4888888888888889,
      "balanced_accuracy": 0.4891304347826087,
      "macro_f1": 0.4888888888888889,
      "weighted_f1": 0.4888888888888889,
      "per_class": {
        "LEFT_HAND_IMAGERY": {
          "precision": 0.4782608695652174,
          "recall": 0.5,
          "f1-score": 0.4888888888888889,
          "support": 22.0
        },
        "RIGHT_HAND_IMAGERY": {
          "precision": 0.5,
          "recall": 0.4782608695652174,
          "f1-score": 0.4888888888888889,
          "support": 23.0
        },
        "accuracy": 0.4888888888888889,
        "macro avg": {
          "precision": 0.4891304347826087,
          "recall": 0.4891304347826087,
          "f1-score": 0.4888888888888889,
          "support": 45.0
        },
        "weighted avg": {
          "precision": 0.4893719806763285,
          "recall": 0.4888888888888889,
          "f1-score": 0.4888888888888889,
          "support": 45.0
        }
      },
      "confusion_matrix": [
        [
          11,
          11
        ],
        [
          12,
          11
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
      "mean": 0.5784,
      "lower_95": 0.5091,
      "upper_95": 0.6485
    },
    "balanced_accuracy": {
      "mean": 0.5787,
      "lower_95": 0.5101,
      "upper_95": 0.6524
    },
    "macro_f1": {
      "mean": 0.5757,
      "lower_95": 0.5083,
      "upper_95": 0.6484
    }
  }
}
```