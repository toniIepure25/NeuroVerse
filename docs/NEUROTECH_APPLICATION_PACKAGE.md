# Neurotech Application Package

## One-Paragraph Project Summary
NeuroVerse is a fully integrated, real-time closed-loop Brain-Computer Interface (BCI) research platform built to validate the entire neuroadaptive pipeline—from signal acquisition and classical ML modeling to a React Three Fiber visual interface. It acts as an executable portfolio piece demonstrating rigorous software engineering, machine learning validation (including raw-epoch CSP/FBCSP models on public datasets), LSL streaming architecture, and a stringent safety-first approach to physical hardware integration. NeuroVerse is engineered to highlight the difference between offline dataset accuracy and live online shadow-inference capabilities.

## Technical Bullet Points for CV
- **End-to-End System Design:** Developed a real-time neuroadaptive BCI loop using Python (FastAPI) and TypeScript (React Three Fiber), synchronizing hardware acquisition, feature extraction, ML inference, and 3D UI updates via WebSockets.
- **Machine Learning & Signal Processing:** Benchmarked classical BCI pipelines (CSP, Filter Bank CSP, SVM, Random Forest) on the PhysioNet EEG Motor Movement dataset, establishing realistic baselines with group-run, group-subject, and leave-one-subject-out (LOSO) splits.
- **Data Streaming & Hardware Integration:** Built robust streaming adapters for Lab Streaming Layer (LSL) and BrainFlow, incorporating live jitter/drift validation and timestamp synchronization.
- **Safety Engineering:** Implemented a hardcoded "shadow mode" and Signal Quality Index (SQI) safety gate that prevents unsafe closed-loop adaptation when hardware inputs are noisy or unvalidated.
- **Reproducible Evidence:** Automated the generation of a comprehensive evidence pack, ensuring all offline evaluations and live streaming validations are recorded, timestamped, and structured for portfolio review.

## GitHub Repository Description
NeuroVerse is an open-source, reproducible BCI research prototype that translates offline EEG ML baselines into a real-time closed-loop neuroadaptive interface using LSL, BrainFlow, FastAPI, and React. Built to demonstrate safe, shadow-only evaluation of classical algorithms (e.g. CSP/FBCSP) within a high-performance modern web stack.

### GitHub Topics Suggestion
`bci`, `neurotech`, `eeg`, `brain-computer-interface`, `machine-learning`, `fastapi`, `react-three-fiber`, `lsl`, `brainflow`, `signal-processing`

## How to Review This Repo in 5 Minutes
1. Read the **README.md** to understand the architecture and strict safety philosophy.
2. Open `evidence_pack/README.md` to see exactly what workflows have been technically validated.
3. Check `reports/bci_raw_epoch_benchmark/physionet_eegbci_medium/benchmark_summary.json` to see real CSP/FBCSP signal processing outputs on public datasets.
4. Check `frontend/src/components/Dashboard/ResearchPanel.tsx` to see how the React frontend interfaces with the real-time websocket state while enforcing the safety gate.
5. Review `backend/app/safety/gate.py` to see the hardcoded rules preventing unsafe adaptation.

## Screenshot & Demo Video Outline
**Screenshots to capture (if desired):**
- Dream Corridor 3D scene running.
- The React Research Panel showing the "Simulated" badge and active proxy metrics.
- Terminal output of `make raw-bci-benchmark-small` showing the dataset split and training metrics.
- Terminal output of `make lsl-live-validation-suite` showing jitter and clock offset diagnostics.

**Demo Video Outline (2 mins):**
- Show UI: "This is the NeuroVerse corridor, currently locked by the safety gate."
- Show Terminal 1: Run `make raw-bci-benchmark-small` to prove real EEG dataset processing.
- Show Terminal 2: Run `make lsl-live-validation-suite` to prove real streaming ingestion capabilities.
- Back to UI: Show the Research panel updating with real-time shadow predictions from the stream.

## LinkedIn Project Post
Excited to share **NeuroVerse v1.0**, a real-time Brain-Computer Interface research prototype I’ve been building! 🧠💻 

Taking EEG machine learning models from offline datasets (like PhysioNet) and deploying them in a live, closed-loop 3D environment is incredibly challenging due to signal noise and hardware unpredictability. To solve this, NeuroVerse implements a strict "shadow mode" and Signal Quality Index (SQI) gate, allowing for the rigorous evaluation of classical pipelines (like Filter Bank CSP) using LSL and BrainFlow streams without risking unsafe UI adaptations.

This isn't "mind reading"—it's a reproducible engineering framework for building safer, more transparent neuroadaptive interfaces. Check out the automated evidence pack and the architecture overview in the repo! 🚀 #Neurotech #BCI #MachineLearning #Python #React #BrainFlow

## Interview Talking Points
- **The Gap Between Offline and Online BCI:** Emphasize how easy it is to overfit on offline datasets (especially due to data leakage), and how NeuroVerse forces you to evaluate models in a live streaming context (LSL shadow mode) before trusting them.
- **Why Classical ML over Deep Learning:** Explain the choice of CSP and FBCSP for motor imagery. In many low-channel or standard BCI applications, classical models provide better interpretability, require less data, and run exceptionally fast during live inference.
- **Safety First:** Detail the "safety gate" architecture. If SQI drops or variance is too high, the system locks out adaptation.
- **Reproducibility:** Highlight the `make generate-evidence-pack` and benchmarking scripts. Good ML engineering requires trackable, reproducible results.

## Skills Demonstrated
- BCI signal processing (Filtering, Epoching, Spatial Filtering)
- EEG Machine Learning (CSP, FBCSP, Logistic Regression)
- Real-time systems (FastAPI, WebSockets, Asyncio)
- Data Streaming (LSL, pyxdf, BrainFlow)
- Safety engineering (Shadow mode, SQI gating)
- Model evaluation (LOSO, Data leakage prevention)
- Frontend visualization (React, Three.js)
- Reproducible research (Makefile, automated reporting)

## "What I would do with physical hardware"
"While NeuroVerse currently relies on simulated data, public datasets, and LSL replays, the architecture is ready for physical hardware (like an OpenBCI Cyton). If provided with physical hardware, my immediate next steps would be:
1. Run the existing `make validate-openbci-cyton` to verify live stream quality (jitter, drop rate).
2. Execute the physical EEG trial protocol (`make physical-eeg-trial-openbci-cyton`) to record a baseline eyes-open/eyes-closed session and generate an alpha-reactivity report.
3. Use the system's calibration API to establish personalized baseline thresholds for the user.
4. Run live LSL shadow mode with the physical device to observe online inference behavior before ever unlocking the closed-loop visualization."
