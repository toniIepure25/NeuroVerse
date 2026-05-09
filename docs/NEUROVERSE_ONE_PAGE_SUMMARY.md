# NeuroVerse: One-Page Summary

**What is NeuroVerse?**
NeuroVerse is an open-source, local-first research platform designed to safely bridge the gap between offline EEG machine learning baselines and real-time closed-loop neuroadaptive interfaces. It provides a reproducible, end-to-end environment for developing Brain-Computer Interfaces (BCI).

**Core Philosophy**
- **Safety First:** Unpredictable physical hardware streams operate purely in "shadow mode" by default. A hardcoded Safety Gate locks closed-loop adaptation until explicit signal quality and confidence thresholds are met.
- **Scientific Honesty:** The system classifies controlled experimental proxies (like motor imagery lateralization), not general "thoughts" or "dreams". 
- **Reproducibility:** All offline baselines and streaming latency metrics are generated into a versioned evidence pack.

**Technical Stack**
- **Frontend:** React, Vite, TypeScript, WebGL (for the Dream Corridor UI).
- **Backend:** FastAPI, Python, WebSockets.
- **Signal Processing:** LSL (Lab Streaming Layer), BrainFlow, MNE-Python.
- **Machine Learning:** scikit-learn (CSP, FBCSP, LogReg, LDA).

**Current Capabilities & Validations**
- **Public EEG Benchmarks:** Automated downloading, parsing, and baseline extraction for the PhysioNet EEG Motor Movement/Imagery dataset.
- **Strict Leakage Prevention:** Built-in validation splits for `group_run`, `group_subject`, and true `Leave-One-Subject-Out` (LOSO) to prevent inflated cross-subject scores.
- **Asynchronous Streaming:** Successful LSL replay validation ensuring sub-50ms inference latency on live UDP streams.
- **Hardware Preparedness:** Integrated BrainFlow SyntheticBoard testing, with configurations ready for physical OpenBCI Cyton and Ganglion devices.

**Results**
Using the PhysioNet EEGBCI medium cohort (S001-S010), the platform achieves a modest, realistic LOSO balanced accuracy of ~0.488 with FBCSP + Logistic Regression on raw EEG epochs. This establishes a baseline for future improvements (e.g., Riemannian geometry, personalized calibration).

**Limitations**
The system has not yet been validated with physical OpenBCI hardware. It relies solely on simulated or pre-recorded (PhysioNet) data streams.

**Why It Matters**
NeuroVerse forces engineers to acknowledge the severe drop in reliability when moving from static CSV datasets to live, jittery, real-time streams. By making the safety lock a first-class feature, it models responsible neurotech development.

*[Read the full Technical Whitepaper](NEUROVERSE_WHITEPAPER.md)*
