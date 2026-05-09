# Evidence Pack Artifact Inventory

## A. Real Public EEG Evidence

### bci_benchmark_summary.json
- **Type**: Benchmark
- **Created At**: 2026-05-08T22:48:29.267330+00:00
- **What it proves**: Classical models can decode controlled proxy tasks (e.g. motor imagery) from the PhysioNet subset.
- **What it does not prove**: Does not prove high accuracy on unseen subjects (LOSO is lower) or general mind-reading.

### raw_bci_benchmark_summary.json
- **Type**: Benchmark
- **Created At**: 2026-05-08T22:48:29.268258+00:00
- **What it proves**: Raw epoch CSP/FBCSP baseline works and avoids data leakage.
- **What it does not prove**: Does not prove clinical utility.

### raw_bci_loso_summary.json
- **Type**: Benchmark
- **Created At**: 2026-05-08T22:48:29.268779+00:00
- **What it proves**: Provides realistic cross-subject (LOSO) metrics.
- **What it does not prove**: Does not prove zero-shot reliability.

## B. Streaming Evidence

### lsl_live_validation_summary.json
- **Type**: Validation
- **Created At**: 2026-05-08T22:48:29.264860+00:00
- **What it proves**: Platform streams LSL continuously with low jitter/drift and maintains a safety lock.
- **What it does not prove**: Does not prove the LSL stream contains real human EEG unless physically attached.

### eeg_lsl_validation_summary.json
- **Type**: Validation
- **Created At**: 2026-05-08T22:48:29.265299+00:00
- **What it proves**: Platform can replay EDF datasets dynamically over LSL and align markers correctly.
- **What it does not prove**: Does not prove real-time closed-loop control or mind-reading.

### raw_bci_shadow_report.md
- **Type**: Validation
- **Created At**: 2026-05-08T22:48:29.270223+00:00
- **What it proves**: Live shadow inference processes streaming markers and builds epochs.
- **What it does not prove**: Does not prove closed-loop control.

## C. Hardware Readiness Evidence

### brainflow_hardware_validation.md
- **Type**: Validation
- **Created At**: 2026-05-08T22:48:29.261054+00:00
- **What it proves**: BrainFlow SyntheticBoard integration works properly through the system's acquisition layer.
- **What it does not prove**: Does not prove real OpenBCI Cyton/Ganglion performance. Physical OpenBCI path is prepared but not yet physically validated.

### physical_eeg_trial_summary.json
- **Type**: Validation
- **Created At**: 2026-05-08T22:48:29.264102+00:00
- **What it proves**: Physical trial protocol executes properly and computes eyes-open/closed alpha reactivity.
- **What it does not prove**: Does not prove clinical results; it is an offline sanity check.

## D. Safety Evidence

### shadow_report.json
- **Type**: Validation
- **Created At**: 2026-05-08T22:48:29.263263+00:00
- **What it proves**: System runs in shadow-only inference and produces zero real adaptation actions while locked.
- **What it does not prove**: Does not prove safety under un-gated physical conditions.
