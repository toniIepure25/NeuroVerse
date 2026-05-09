# NeuroVerse Demo Scripts

This document outlines tailored workflows for demonstrating the platform.

**Disclaimer**: Emphasize during all demos that the system runs in a safety-locked "shadow mode" using simulated data or recorded offline datasets. It does not read thoughts or decode medical conditions.

---

## A. 90-Second Recruiter Demo
**Goal**: Show that the architecture exists, looks professional, and has an evidence pack.

1. **Start**: `make dev`
2. **Open UI**: Go to `http://localhost:5173`.
3. **Show the 3D Engine**: Point out the React Three Fiber visualizer.
4. **Show Research Panel**: Click "Start Session" and demonstrate the real-time websocket feed in the right sidebar. Point out the "NeuroVerse v1.0-rc" badge and "Simulated" status.
5. **Close**: "The system uses classical ML to estimate cognitive proxy states from simulated hardware or datasets, gating all adaptation for safety. It's fully reproducible. Here is the generated Evidence Pack (`evidence_pack/README.md`) proving the validation."

---

## B. 3-Minute Technical Demo
**Goal**: Prove ML integration and data processing capabilities.

1. **Start UI**: `make dev`. Open the Research Panel.
2. **Run Benchmark**: Open a new terminal and run `make raw-bci-benchmark-small`.
3. **Explain Output**: Explain that this command is epoched a real EEG dataset (PhysioNet EEGBCI), filtering it, fitting Common Spatial Pattern (CSP) filters, and training a Logistic Regression model on a binary motor imagery task.
4. **Show Results**: Point out the Balanced Accuracy metrics in the terminal and mention how the system explicitly prevents data leakage via strict splitting.
5. **Show Live Inference**: Run `make live-shadow-best-raw-bci-model`. Show the system processing simulated marker streams and logging shadow predictions without risking unsafe 3D UI changes.

---

## C. 7-Minute Neurotech Interview Demo
**Goal**: Prove LSL stream engineering, hardware readiness, and safety concepts.

1. **Background**: "Neurotech engineering requires safely bridging offline ML into a live, asynchronous environment. Here is how NeuroVerse handles it."
2. **Start LSL**: In Terminal 1, run `make lsl-stream-demo`.
3. **Validate LSL**: In Terminal 2, run `make lsl-live-validation-suite`.
4. **Explain**: "The backend is now ingesting a continuous stream over the Lab Streaming Layer. We calculate stream jitter, clock drift, and sample drops. If signal quality (SQI) drops below a threshold, the system immediately disables adaptation."
5. **Show Hardware Readiness**: Open the Research Panel in the UI. Point out the LSL streams detected and the validation report.
6. **OpenBCI Explanation**: "If I had a physical OpenBCI Cyton right now, I would run `make physical-eeg-trial-openbci-cyton` instead. It uses BrainFlow to run an identical record-only safety protocol."

---

## D. 15-Minute Deep-Dive Demo
**Goal**: Comprehensive walkthrough of the codebase, BCI theory, and production integration.

1. **UI & Data Flow (3 mins)**: Run `make dev`. Start a session. Trace the WebSocket messages in the browser dev tools to show how state proxy messages arrive from FastAPI.
2. **Signal Processing Code (4 mins)**: Open `backend/app/features/eeg_features.py`. Show how CSP filtering and epoching work. Explain why Filter Bank CSP (FBCSP) is used to capture multiple frequency bands (e.g., mu and beta rhythms) for motor imagery.
3. **Safety Gate Code (3 mins)**: Open `backend/app/safety/gate.py`. Walk through the hardcoded thresholding logic. Emphasize that BCI algorithms generalize poorly to new subjects (LOSO metrics are low), making the shadow-mode gate essential.
4. **LSL Replay (3 mins)**: Run `make eeg-lsl-replay-demo`. Show how an offline `.edf` file is injected into a live network stream with event markers, proving the system can align real-time timestamps with cognitive events.
5. **Evidence Pack (2 mins)**: Run `make generate-evidence-pack`. Show how the JSON artifacts map directly to the recruiter summary and inventory files.

## Single Best Demo Flow
This is the recommended sequence to demonstrate the entire platform's capabilities quickly and honestly:

1. **Open frontend**: Run `make dev`, go to `http://localhost:5173`.
2. **Show Dream Corridor**: Point out the React Three Fiber environment.
3. **Show Research Panel evidence status**: Highlight the `v1.0.0-rc1` status and explicit "safety-locked" badge.
4. **Show PhysioNet medium benchmark**: Run `make bci-benchmark-small` and point out the real dataset processing.
5. **Show CSP/FBCSP benchmark**: Run `make raw-bci-benchmark-small` to highlight advanced spatial filtering.
6. **Show LOSO difficulty**: Point out that LOSO (Leave-One-Subject-Out) metrics are lower, proving scientific honesty over dataset overfitting.
7. **Show live LSL shadow evidence**: Run `make lsl-live-validation-suite` and show the shadow logs with zero real UI adaptation.
8. **Show BrainFlow SyntheticBoard validation**: Explain how it tests the hardware acquisition layer without requiring an actual headset.
9. **Show physical trial protocol**: Run `make physical-eeg-trial-synthetic` to show the eyes-open/closed recording sequence.
10. **Show evidence pack**: Open `evidence_pack/README.md` and `artifact_inventory.md` to prove all metrics are versioned.
11. **Emphasize closed-loop locked**: Reiterate that because this is a responsible neurotech project, actual 3D adaptation remains locked by the safety gate.

---

## Common Q&A During Demos

- **Is this reading thoughts?** No, it predicts controlled dataset task labels (like "imagine left hand movement") under experimental conditions.
- **Is this real EEG?** The LSL stream in the demo is simulated. The raw epoch benchmark uses real public EEG (PhysioNet).
- **Did you validate physical hardware?** The platform supports BrainFlow SyntheticBoards and OpenBCI. Physical hardware is not validated in this repository snapshot unless a local report exists.
- **Why are the LOSO metrics modest?** Inter-subject generalization is an unsolved problem in non-invasive BCI. Modest metrics are scientifically honest.
- **How does LSL fit?** LSL aligns timestamps across devices. NeuroVerse acts as an LSL receiver.
