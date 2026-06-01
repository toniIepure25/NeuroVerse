# Evidence Pack Artifact Inventory

## A. Real Public EEG Evidence

### bci_benchmark_summary.json
- **Type**: Benchmark
- **Created At**: 2026-06-01T22:50:21.659533+00:00
- **What it proves**: Classical models can decode controlled proxy tasks (e.g. motor imagery) from the PhysioNet subset.
- **What it does not prove**: Does not prove high accuracy on unseen subjects (LOSO is lower) or general mind-reading.

### raw_bci_benchmark_summary.json
- **Type**: Benchmark
- **Created At**: 2026-06-01T22:50:21.661059+00:00
- **What it proves**: Raw epoch CSP/FBCSP baseline works and avoids data leakage.
- **What it does not prove**: Does not prove clinical utility.

### raw_bci_loso_summary.json
- **Type**: Benchmark
- **Created At**: 2026-06-01T22:50:21.662183+00:00
- **What it proves**: Provides realistic cross-subject (LOSO) metrics.
- **What it does not prove**: Does not prove zero-shot reliability.

## B. Streaming Evidence

### lsl_live_validation_summary.json
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:21.655257+00:00
- **What it proves**: Platform streams LSL continuously with low jitter/drift and maintains a safety lock.
- **What it does not prove**: Does not prove the LSL stream contains real human EEG unless physically attached.

### eeg_lsl_validation_summary.json
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:21.656343+00:00
- **What it proves**: Platform can replay EDF datasets dynamically over LSL and align markers correctly.
- **What it does not prove**: Does not prove real-time closed-loop control or mind-reading.

### raw_bci_shadow_report.md
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:21.663826+00:00
- **What it proves**: Live shadow inference processes streaming markers and builds epochs.
- **What it does not prove**: Does not prove closed-loop control.

## C. Hardware Readiness Evidence

### brainflow_hardware_validation.md
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:21.645848+00:00
- **What it proves**: BrainFlow SyntheticBoard integration works properly through the system's acquisition layer.
- **What it does not prove**: Does not prove real OpenBCI Cyton/Ganglion performance. Physical OpenBCI path is prepared but not yet physically validated.

### physical_eeg_trial_summary.json
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:21.653146+00:00
- **What it proves**: Physical trial protocol executes properly and computes eyes-open/closed alpha reactivity.
- **What it does not prove**: Does not prove clinical results; it is an offline sanity check.

## D. Safety Evidence

### shadow_report.json
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:21.651197+00:00
- **What it proves**: System runs in shadow-only inference and produces zero real adaptation actions while locked.
- **What it does not prove**: Does not prove safety under un-gated physical conditions.

## E. Multimodal Fusion / IMAGINA Proxy Evidence

### latest_fusion_report.json
- **Type**: Proxy Report
- **Created At**: 2026-06-01T22:50:22.186479+00:00
- **What it proves**: Simulated/optional modalities can be fused into safety-gated proxy estimates with uncertainty and proposed shadow visual mapping.
- **What it does not prove**: Does not prove clinical inference, unrestricted mental-state measurement, thoughts, dreams, or real EEG closed-loop control.

### latest_fusion_calibration_profile.json
- **Type**: Calibration
- **Created At**: 2026-06-01T22:50:22.187430+00:00
- **What it proves**: Subject-specific modal baselines are recorded, serialized, and safely applied to normalize features.
- **What it does not prove**: Does not prove absolute physical calibration against gold-standard laboratory instruments.

### latest_fusion_validation_summary.json
- **Type**: Validation
- **Created At**: 2026-06-01T22:50:22.188341+00:00
- **What it proves**: Behavioral validation shows robustness to missing modalities, expected uncertainty behavior, and conservative safety recommendations.
- **What it does not prove**: Does not prove decoding accuracy under un-simulated real-world noise.

### latest_fusion_ablation_table.csv
- **Type**: Ablation Table
- **Created At**: 2026-06-01T22:50:22.189135+00:00
- **What it proves**: Controlled ablation testing reveals exactly how modality presence affects confidence and uncertainty.
- **What it does not prove**: Does not guarantee identical model response for out-of-distribution subject profiles.

## F. IMAGINA v1 Baseline Evidence

### latest_imagina_v1_metrics.json
- **Type**: Metrics
- **Created At**: 2026-06-01T22:50:22.189657+00:00
- **What it proves**: IMAGINA v1 manifest validates and a baseline model is successfully trained/evaluated.
- **What it does not prove**: Does not prove clinical utility, thought/dream reading, or direct closed-loop control.

### latest_imagina_v1_model_card.md
- **Type**: Model Card
- **Created At**: 2026-06-01T22:50:22.189861+00:00
- **What it proves**: Trained baseline models are registered with strict limitations and usage boundaries.
- **What it does not prove**: Does not prove real generalizable imagery reconstruction.

## G. IMAGINA Export Contract & Safety Compliance

### latest_contract_import_summary.json
- **Type**: Contract Import Summary
- **Created At**: Missing (Optional/Not Run)
- **What it proves**: Imagina v1 Export manifest validates perfectly, checking schema version, safety flags, and copying lightweight metadata.
- **What it does not prove**: Does not prove model performance or validity under real live BCI closed loop control.

### latest_contract_import_summary.md
- **Type**: Scientific Framing & Safety Audit
- **Created At**: Missing (Optional/Not Run)
- **What it proves**: Import processes strictly frame all metrics as experimental proxy estimates, enforcing closed_loop_allowed = false.
- **What it does not prove**: Does not prove the user has real active dream decoding capabilities.

## H. Launch & Reviewer Readiness Evidence

### reviewer_demo_flow_summary.json
- **Type**: QA Verification Summary
- **Created At**: 2026-06-01T22:50:22.288010+00:00
- **What it proves**: Statically and dynamically checks route wiring, safety states, and data schemas across live FastAPI endpoints and component structures.
- **What it does not prove**: Does not prove real physical EEG device streaming.

### static_portfolio_check.json
- **Type**: Portfolio Health Report
- **Created At**: 2026-06-01T22:50:22.288313+00:00
- **What it proves**: Checks presence of complete static assets and guarantees that closed_loop_allowed is uniformly locked to false in all configurations.
- **What it does not prove**: Does not represent physical trial success; it validates data synchronization.

### frontend_route_check.json
- **Type**: Frontend Structure Integrity
- **Created At**: 2026-06-01T22:50:22.288589+00:00
- **What it proves**: Verifies 100% routing integrity of App navigation header matching physical page files.
- **What it does not prove**: Does not represent automated browser click verification.

## I. Public Launch Readiness Evidence

### frontend_bundle_check.json
- **Type**: Bundle Performance Budget
- **Created At**: 2026-06-01T22:50:22.288885+00:00
- **What it proves**: Statically measures Vite production bundle assets size and validates against maximum budget of 2.5 MB.
- **What it does not prove**: Does not prove runtime rendering frame rates or client GPU limits.

### accessibility_check.json
- **Type**: A11y & Usability Compliance
- **Created At**: 2026-06-01T22:50:22.289182+00:00
- **What it proves**: Pragmatically audits component semantic heading tags, keyboard tabIndex elements, and ensures all core disclaimers are visibly present in static text.
- **What it does not prove**: Does not replace dynamic screen-reader test evaluations or WCAG compliance certificate.

### screenshot_assets_check.json
- **Type**: Visual Documentation Verification
- **Created At**: 2026-06-01T22:50:22.289447+00:00
- **What it proves**: Audits presence of 10 key high-resolution screenshots mapping out the entire system's walkthrough pathway.
- **What it does not prove**: Does not claim clinical or automated UI functionality validation.
