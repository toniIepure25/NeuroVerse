# NeuroVerse: A Safety-Gated Neuroadaptive Research Platform

## 1. Abstract
NeuroVerse is an open-source, local-first research platform designed to bridge the gap between offline EEG machine learning baselines and real-time closed-loop neuroadaptive interfaces. By integrating modern web technologies (React, Vite) with high-performance backend signal processing (FastAPI, LSL, BrainFlow, MNE-Python), NeuroVerse provides a reproducible environment for evaluating classical algorithms like CSP and FBCSP. Crucially, the platform enforces strict safety gating, ensuring that unpredictable physical hardware streams operate purely in "shadow mode," locking closed-loop adaptation until explicit validation and ethical criteria are met.

## 2. Introduction
Brain-Computer Interfaces (BCI) hold the potential to dynamically alter software environments based on cognitive proxies. However, transitioning from controlled, offline dataset evaluation to live, online closed-loop adaptation introduces severe safety, latency, and scientific validity risks. NeuroVerse was built to provide a structured, auditable "corridor" where offline models can be validated against asynchronous live streams before ever triggering a real environmental state change.

## 3. Motivation
Many BCI prototypes demonstrate high accuracy offline but fail when translated into online systems due to non-stationarity, latency jitter, and hardware artifacts. Furthermore, uncontrolled neuroadaptive loops can induce negative psychological feedback or simulator sickness if the system acts on low-confidence noise. NeuroVerse mitigates this by making the safety gate a first-class citizen of the architecture.

## 4. Related Work
- **BCI & EEG Motor Imagery:** The PhysioNet EEG Motor Movement/Imagery dataset remains a standard public benchmark.
- **CSP/FBCSP:** Common Spatial Pattern (CSP) and Filter Bank CSP (FBCSP) are established baselines for motor imagery decoding, though Riemannian geometry approaches are increasingly dominant.
- **LSL & BrainFlow:** The Lab Streaming Layer (LSL) provides precise time-synchronization for physiological data, while BrainFlow abstracts hardware connections (e.g., OpenBCI, Ganglion).
- **Neuroadaptive Interfaces:** Systems that alter their state based on cognitive load or intent are moving from passive monitoring to active, closed-loop manipulation.

## 5. System Architecture
NeuroVerse utilizes a decoupled architecture:
- **Frontend:** React + Vite + TypeScript for high-performance, WebGL-ready interfaces.
- **Backend:** FastAPI for asynchronous WebSocket streaming and API routes.
- **Engine:** A state machine managing data acquisition, signal quality indices (SQI), artifact detection, and model inference.
- **Safety Gate:** A strict boolean lock evaluating model confidence, SQI, and manual overrides before permitting UI transitions.

## 6. Data Sources
The platform currently supports and validates:
- **Synthetic Simulator:** A deterministic local generator for testing UI state logic.
- **PhysioNet EEGBCI:** Support for automated EDF downloading, event parsing, and baseline extraction.
- **LSL Replay:** Replaying PhysioNet data asynchronously over UDP via `pylsl`.
- **BrainFlow SyntheticBoard:** Native C++ bound synthetic data generation.
- **OpenBCI (Prepared):** Hardware profiles exist for Cyton and Ganglion, though physical validation remains pending.

## 7. Methods
- **Preprocessing:** Epoch extraction (e.g., 0.5–2.5s post-stimulus), bandpass filtering, and baseline correction.
- **Event Mapping:** Normalizing annotations into structured tasks (`LEFT_HAND_IMAGERY`, etc.).
- **Modeling:** Using `mne.decoding.CSP` and scikit-learn classifiers (`LogisticRegression`, `LDA`, `SVC`).
- **Shadow Inference:** The system executes inference on live streams and logs predictions, but intentionally drops the adaptation payload to the UI, guaranteeing zero false positives during testing.

## 8. Evaluation
NeuroVerse implements stringent cross-validation constraints to avoid data leakage:
- **Group Run:** Splitting by recording run to measure within-subject stability.
- **Group Subject:** Splitting by subject ID to estimate broad generalization.
- **LOSO (Leave-One-Subject-Out):** The strictest metric for cross-subject BCI.
- **Streaming Metrics:** Measuring inference latency, packet jitter, and throughput over LSL.

## 9. Results
Current benchmarks on the PhysioNet EEGBCI medium cohort (S001-S010, runs 4/8/12) demonstrate modest, honest offline baselines. 
- The best FBCSP + LogReg pipeline yields a group_run balanced accuracy of ~0.576 and a true LOSO accuracy of ~0.488. 
- These results reflect the inherent difficulty of zero-calibration, cross-subject motor imagery classification on raw EEG using classical methods.
- The LSL shadow mode operates successfully with sub-50ms inference latency.

**Limitations:** The system has not yet been validated with physical OpenBCI hardware or human-in-the-loop closed adaptation. 

## 10. Safety and Ethics
NeuroVerse does not claim to decode dreams or read thoughts. It classifies controlled experimental proxy markers (e.g., motor imagery lateralization). The "Dream Corridor" is an adaptive scaffold, not a literal representation of mental imagery. Unrestricted closed-loop control is disabled by default to prevent reckless biofeedback loops.

## 11. Product Interface
The platform includes a fully featured React dashboard (`ResearchPanel`) which renders real-time signal quality, hardware status, safety gate status, and prediction confidence alongside an interactive 3D environment.

## 12. Discussion
By exposing the difference between offline accuracy (often inflated by leakage) and online shadow inference (often degraded by jitter and noise), NeuroVerse serves as a critical stepping stone. The safety gate forces researchers to acknowledge when their signal quality is insufficient for closed-loop control.

## 13. Future Work
- **Physical Validation:** Acquiring an OpenBCI Cyton to validate the `PHYSICAL_OVERRIDE` path.
- **Subject Calibration:** Implementing within-session calibration workflows.
- **Riemannian Geometry:** Integrating `pyriemann` for covariance-based classification (MDM, Tangent Space).
- **MOABB Integration:** Aligning reporting schemas with the Mother of All BCI Benchmarks.
- **IRB Approval:** Proceeding to true closed-loop human trials only under strict ethical review.

## 14. Conclusion
NeuroVerse is a transparent, reproducible, and safety-conscious framework for BCI development. It successfully translates offline baselines into live streaming prototypes while strictly guarding against unvalidated closed-loop adaptation, serving as a model for responsible neurotechnology engineering.
