# Neurotech Application Package

## One-Paragraph Project Summary
NeuroVerse is a fully integrated, real-time closed-loop Brain-Computer Interface (BCI) research platform built to validate the entire neuroadaptive pipeline—from signal acquisition and classical ML modeling to a React Three Fiber visual interface. It acts as an executable portfolio piece demonstrating rigorous software engineering, machine learning validation (including raw-epoch CSP/FBCSP models on public datasets), LSL streaming architecture, and a stringent safety-first approach to physical hardware integration. NeuroVerse is engineered to highlight the difference between offline dataset accuracy and live online shadow-inference capabilities.

## Technical Bullet Points for CV
- **End-to-End System Design:** Developed a real-time neuroadaptive BCI loop using Python (FastAPI) and TypeScript (React Three Fiber), synchronizing hardware acquisition, feature extraction, ML inference, and 3D UI updates via WebSockets.
- **Command Center Architecture:** Engineered a high-fidelity 8-sector system health console with client-side static snapshot fallbacks, a 7-step guided reviewer tour, and an interactive ProvenanceGraph showcasing research-modeling to safety-gated runtime boundaries.
- **Machine Learning & Signal Processing:** Benchmarked classical BCI pipelines (CSP, Filter Bank CSP, SVM, Random Forest) on the PhysioNet EEG Motor Movement dataset, establishing realistic baselines with group-run, group-subject, and leave-one-subject-out (LOSO) splits.
- **Data Streaming & Hardware Integration:** Built robust streaming adapters for Lab Streaming Layer (LSL) and BrainFlow, incorporating live jitter/drift validation and timestamp synchronization.
- **Safety Engineering:** Implemented a hardcoded "shadow mode" and Signal Quality Index (SQI) safety gate that prevents unsafe closed-loop adaptation when hardware inputs are noisy or unvalidated.
- **Reproducible Evidence & QA Hardening:** Automated the generation of a comprehensive evidence pack and a suite of 3 dedicated QA verification scripts to ensure 100% route integrity, safety state invariance, and static portfolio synchronization prior to release.

## GitHub Repository Description
NeuroVerse is a local-first, safety-gated BCI/neuroadaptive runtime with an interactive CommandCenter dashboard, public EEG benchmarking, LSL validation, BrainFlow/OpenBCI readiness, and shadow-only inference.

### GitHub Topics Suggestion
`bci`, `eeg`, `neurotechnology`, `brain-computer-interface`, `lsl`, `brainflow`, `openbci`, `mne`, `csp`, `fbcsp`, `fastapi`, `react`, `machine-learning`, `neuroadaptive-interfaces`, `command-center`

## How to Review This Repo in 5 Minutes
1. Start the UI (`make dev`) and open `http://localhost:5173`.
2. Navigate to the **Command Center** page and click through the interactive 7-step **5-Minute Guided Reviewer Tour**.
3. Inspect the **ProvenanceGraph** showing model separation, and review the **Shadow Explainability** metrics card.
4. Open the **Evidence Center** tab to see exactly what workflows have been technically validated, including real CSP/FBCSP signal processing outputs on public datasets.
5. Click into the **Dream Corridor** tab and open the Research Panel to see how the React frontend interfaces with the real-time websocket state while enforcing the safety gate.
6. Review `backend/app/safety/gate.py` to see the hardcoded rules preventing unsafe adaptation.

Also open the **Data Sources** tab. It is a setup assistant that checks simulator,
PhysioNet replay, LSL stream, BrainFlow SyntheticBoard, and OpenBCI Cyton/Ganglion
readiness. In static portfolio mode it displays a baked snapshot or conservative
fallback metadata; with the backend running it calls `GET /api/v1/data-sources`
for live dependency/resource checks and protocol preflight.

## Screenshot & Demo Video Outline
**Screenshots to capture (if desired):**
- **CommandCenter_Full_Dashboard.png**: Showing all 8 health sectors in green (Safe/Operating) status.
- **Reviewer_Guided_Tour_Banner.png**: Displaying the active step and step description of the tour.
- **ProvenanceGraph_Visualization.png**: Showing the strict visual boundary separating external IMAGINA research and the safety-gated NeuroVerse runtime.
- **Shadow_Explainability_Indicators.png**: Showing the real-time cosine similarity and late-fusion weight metrics.
- **Dream Corridor 3D scene** running with the React Research Panel showing the "Simulated" badge and active proxy metrics.
- Terminal output of `make reviewer-ready-check` showing all launch QA verifiers passing.

**Demo Video Outline (2 mins):**
- **0:00 - 0:30 (Command Center Introduction)**: Show the new CommandCenter. "Welcome to CommandCenter. Let's start our guided 5-minute reviewer tour." Step through the safety and LSL validation sectors.
- **0:30 - 1:00 (Research Separation)**: Hover over the ProvenanceGraph nodes showing how we ingest external IMAGINA research without compromising safety locks.
- **1:00 - 1:30 (Terminal Verification)**: Run `make reviewer-ready-fast` to show our dynamic QA verifiers checking routes, assets, and safety invariants.
- **1:30 - 2:00 (Offline Fallback & Dream Corridor)**: Shut down the backend, show the UI switching seamlessly to `Baked Snapshot Fallback` while remaining fully interactive, and show the shadow explainability card.

## LinkedIn Project Post
Excited to share **NeuroVerse v1.2**, featuring our new **Command Center Dashboard**! 🧠💻

Building a closed-loop Brain-Computer Interface (BCI) requires strict systems observability. In this release, I've implemented a comprehensive CommandCenter health console that displays 8 live sectors, maps external research integrations via an interactive ProvenanceGraph, and provides a 7-step guided tour for auditors.

To ensure release readiness, I also built a suite of automated QA checkers that statically and dynamically validate route wiring, safety states, and static fallbacks, proving that both our live FastAPI server and static baked portfolio modes maintain a strict `closed_loop_allowed=false` safety lock.

This isn't "mind reading"—it's a robust engineering template for scaling neuroadaptive interfaces from model research to safe, auditable real-time runtimes. Check out the automated evidence pack and the architecture overview in the repo! 🚀 #Neurotech #BCI #MachineLearning #Python #React #FastAPI #SystemsEngineering #SoftwareQA #TypeScript

## Interview Talking Points
- **The Gap Between Offline and Online BCI:** Emphasize how easy it is to overfit on offline datasets (especially due to data leakage), and how NeuroVerse forces you to evaluate models in a live streaming context (LSL shadow mode) before trusting them.
- **Why Classical ML over Deep Learning:** Explain the choice of CSP and FBCSP for motor imagery. In many low-channel or standard BCI applications, classical models provide better interpretability, require less data, and run exceptionally fast during live inference.
- **Safety First:** Detail the "safety gate" architecture. If SQI drops or variance is too high, the system locks out adaptation.
- **Reproducibility:** Highlight the `make generate-evidence-pack` and benchmarking scripts. Good ML engineering requires trackable, reproducible results.
- **Data Source Setup:** Explain how the Data Source Wizard separates simulator,
  public replay, LSL, BrainFlow SyntheticBoard, and physical OpenBCI readiness
  without fabricating hardware claims.

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

BrainFlow SyntheticBoard is not real OpenBCI physical validation. OpenBCI/Galea
physical validation remains unperformed unless a real device report exists.
Closed-loop from real EEG is disabled by default.

## Multimodal Fusion v1 / IMAGINA Foundation

NeuroVerse now includes a safe simulated Multimodal Fusion v1 pathway. It
accepts EEG, gaze, physiology, behavior, self-report, and IMAGINA proxy packets,
handles missing modalities, estimates uncertainty, and writes
`reports/fusion/*/fusion_report.json`.

This demonstrates research software architecture for multimodal neuroadaptive
systems, not validated mind reading. Multimodal fusion outputs are experimental
proxy estimates, not clinical or unrestricted mental-state measurements. The
corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics. IMAGINA plugin outputs are experimental
imagery-quality proxies, not decoded thoughts or dreams.
