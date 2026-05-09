# Neurotech Interview Q&A

This document prepares you for technical deep-dives into the NeuroVerse architecture and methodology.

### What is the core architecture?
NeuroVerse is a real-time, closed-loop system built with a FastAPI backend and a React Three Fiber frontend. The backend runs an asynchronous event loop that ingests data from acquisition adapters (Simulator, BrainFlow, LSL), applies preprocessing and feature extraction (e.g., CSP), computes a Signal Quality Index (SQI), and passes the features to a state estimator. A strict safety gate reviews the SQI and estimation confidence before allowing the adaptation policy to issue UI changes over WebSockets.

### Why use Lab Streaming Layer (LSL)?
LSL is the gold standard in neurotech for synchronizing multiple data streams (e.g., EEG, markers, eye tracking) across networks with sub-millisecond precision. By building an LSL adapter, NeuroVerse can natively ingest data from almost any research-grade hardware or interface with other experiment control software, while automatically handling timestamp alignment and jitter.

### Why BrainFlow?
BrainFlow provides a unified, hardware-agnostic API for acquiring data from consumer and research BCI devices (like OpenBCI Cyton/Ganglion). Using BrainFlow allows the system to switch between simulated boards and physical hardware with just a configuration change, without rewriting the low-level serial communication code.

### What exactly is real and what is simulated?
- **Simulated:** The default acquisition stream, the Dream Corridor environment adaptations, and the LSL live demo stream are mathematically simulated.
- **Real:** The FastAPI/React architecture, the signal processing pipelines, the benchmark evaluation scripts, and the model artifacts are real. When running the PhysioNet or raw epoch benchmarks, the system processes real, public human EEG data.

### What dataset did you use?
I used the PhysioNet EEG Motor Movement/Imagery Dataset (EEGBCI). Specifically, I evaluated models on a subset of subjects (e.g., S001-S010) performing left vs. right hand motor imagery (runs 4, 8, 12).

### What are CSP and FBCSP?
- **CSP (Common Spatial Pattern):** A mathematical technique used to project multi-channel EEG data into a lower-dimensional space that maximizes the variance for one class while minimizing it for another. It's highly effective for extracting motor imagery features.
- **FBCSP (Filter Bank CSP):** An extension of CSP where the EEG signal is first bandpass-filtered into multiple overlapping frequency bands. CSP is applied to each band independently, and a feature selection algorithm (or classifier) decides which frequency/spatial components are most discriminative.

### Why are LOSO (Leave-One-Subject-Out) metrics lower?
EEG signals are highly non-stationary and vary drastically between individuals due to differences in skull thickness, brain folding, and cognitive strategies. A model trained on a group of subjects will often overfit to subject-specific features. LOSO forces the model to predict on a completely unseen brain, resulting in a significant performance drop, which accurately reflects real-world, zero-shot BCI deployment challenges.

### How do you avoid data leakage?
In the raw-epoch benchmark, the dataset is split into training and testing sets *before* any data-dependent transformations (like CSP or standard scaling) are fitted. If CSP spatial filters were calculated on the entire dataset prior to splitting, the test set's spatial distribution would "leak" into the training phase, artificially inflating the accuracy.

### How do you prevent unsafe closed-loop behavior?
The system utilizes a hardcoded "Safety Gate." It requires:
1. Signal Quality Index (SQI) to be above a specific threshold.
2. The model's prediction confidence to be sufficiently high.
3. If running physical hardware, an explicit override flag must be passed. Otherwise, the system operates in "Shadow Mode," where predictions are logged but the 3D UI remains completely locked.

### How would you integrate an OpenBCI Cyton?
The integration is already built into the `run_hardware_validation.py` script via BrainFlow. I would connect the Cyton dongle, specify the serial port (e.g., `PORT=/dev/ttyUSB0`), and run the hardware validation target to check impedance and drop rate. If stable, I'd run the physical trial protocol to establish an eyes-open/closed alpha baseline, calibrate the system, and then proceed to shadow inference.

### What are the project’s scientific limitations?
The system relies on "proxy metrics"—event-locked classifiers trained on controlled experimental task labels. These models predict whether the EEG signal matches the statistical pattern of the training data (e.g., the subject was instructed to imagine moving their left hand). They do not decode actual thoughts, semantic meaning, or absolute emotional ground truth. Furthermore, without clinical validation, the system cannot be used for diagnostic purposes.

### What would be the next production step?
The next step would be deploying the application in a tightly controlled physical user study to gather real-world, closed-loop telemetry. I would focus on improving the online, adaptive calibration of the CSP models to handle intra-subject non-stationarity (e.g., the signal drifting over a 30-minute session).
