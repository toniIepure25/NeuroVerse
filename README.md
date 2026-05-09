# NeuroVerse: Multimodal Biosensing and Adaptive Neuroadaptive Interface Platform

**NeuroVerse** is a closed-loop neuroadaptive system that estimates cognitive proxies from simulated or dataset-derived multimodal biosignals and adapts an immersive 3D environment in real time. 

> **Status: NeuroVerse v1.1.0-rc1**
> Research prototype — simulated biosignals, local dataset replay, learned baselines, heuristic default, safety-gated adaptation. Not clinically validated.
>
> The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.
>
> Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.
>
> Hardware validation confirms stream quality and software integration; it does not validate clinical or unrestricted mental-state inference.
>
> Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present.

**Reviewers & Recruiters:** Please read [`REVIEWER_START_HERE.md`](./REVIEWER_START_HERE.md) for the best 5-minute technical review path.

---

## What It Is
NeuroVerse is a reproducible research platform for engineering and evaluating Brain-Computer Interface (BCI) pipelines. It integrates robust streaming (LSL, BrainFlow), dataset-driven offline baselines (PhysioNet EEGBCI), classical BCI machine learning models (CSP, Filter Bank CSP), and a responsive React Three Fiber visualizer, all behind a strict safety gate.

## What It Is Not
- **Not a medical device:** It is not for clinical diagnosis or therapy.
- **Not "mind reading":** It does not decode thoughts, detect consciousness, or reconstruct visual images. 
- **Not emotion ground truth:** Any emotion metrics are proxy representations of physiological states.

## Why It Matters for BCI/Neurotech
Translating offline EEG machine learning to a real-time, closed-loop interface is fraught with risk. NeuroVerse demonstrates how to safely bridge this gap. By focusing on explicit shadow inference, stringent LSL timestamp validation, explicit data-leakage guards in tabular data, and separated training/inference paths, NeuroVerse functions as a production-grade template for scaling BCI technologies from dataset to hardware.

---

## Architecture Overview
The system relies on an asynchronous Python backend and a React/TypeScript frontend connected via WebSockets.

```
Simulated Biosignals / Dataset Replay / LSL Stream
       ↓
Preprocessing (Bandpass, CSP filtering, epoching)
       ↓
Feature Extraction & Signal Quality Index (SQI)
       ↓
State Estimation (Heuristic or Classical ML)
       ↓
Safety Gate (Blocks uncertain or poor quality signals)
       ↓
Adaptation Policy (Translates state into UI parameters)
       ↓
WebSocket Session Recorder
       ↓
Immersive 3D Frontend
```

## Core Capabilities
- **Real-Time Neuroadaptive Loop:** WebSocket-driven state integration for continuous adaptation.
- **LSL Streaming Validation:** Timestamps, jitter, and stream mapping explicitly validated.
- **PhysioNet EEGBCI ML Benchmark:** Evaluates generalized classifiers against standardized datasets.
- **CSP / FBCSP Raw Epoch Benchmark:** Employs optimal spatial filtering on binary motor-imagery tasks.
- **Hardware Validation Protocol:** Rigorous checks prior to physical engagement.
- **BrainFlow / OpenBCI Readiness:** Native paths for Synthetic Boards, Cyton, and Ganglion.
- **Shadow-Only Safety Mode:** Model runs live over streamed data without triggering actual state adaptations.
- **Evidence Pack Generation:** Automatically collates benchmark reports and LSL validation data.

---

## Screenshots & Demo

> **TODO:** Add screenshots before public launch. (See `docs/SCREENSHOT_AND_DEMO_ASSETS.md`)
>
> Expected assets to capture:
> - `assets/screenshots/01_landing.png`
> - `assets/screenshots/02_evidence_center.png`
> - `assets/screenshots/03_dream_corridor.png`
> - `assets/screenshots/04_research_panel.png`
> - `assets/screenshots/05_hiring_page.png`

---

## Quickstart

Run the standard checks, launch the development environment, and compile the evidence pack.

```bash
# 1. Run environment pre-checks
make preflight

# 2. Launch FastAPI backend and Vite frontend
make dev

# 3. Generate the centralized evidence pack (in another terminal)
make generate-evidence-pack
```

Open `http://localhost:5173`. You will be greeted by the new **Product Landing Page** and **Evidence Center**, which guide you through the validated workflows and safety protocols before entering the live simulated dashboard.

---

## Reproducible Evidence Commands

Run these to reproduce key platform capabilities. Results are output to the `reports/` and `evidence_pack/` directories.

**Public EEG Fixture (Simulated/MNE Replay):**
```bash
make public-eeg-fixture-suite
```

**Real PhysioNet Benchmark (Subset):**
```bash
make bci-benchmark-small
```

**Raw CSP/FBCSP Benchmark:**
```bash
make prepare-raw-epochs-small
make raw-bci-benchmark-small
make raw-bci-loso-small
```

**LSL Validation:**
```bash
make lsl-live-validation-suite
```

**BrainFlow Synthetic Validation:**
```bash
make validate-brainflow-synthetic
make calibration-brainflow-synthetic
```

**Physical EEG Trial Protocol (Synthetic mode):**
```bash
make physical-eeg-trial-synthetic
```

---

## Benchmark Highlights

We evaluated classical ML on the PhysioNet EEG Motor Movement/Imagery dataset (Medium subset: `S001-S010`, Runs `4,8,12`). Task labels: `LEFT_HAND_IMAGERY` vs `RIGHT_HAND_IMAGERY`.

- **Splits Evaluated:** `group_run`, `group_subject`, `leave_one_subject_out` (LOSO).
- **Best Pipeline:** Filter Bank CSP (FBCSP) + Logistic Regression.
- **Performance:** 
  - Group Run: ~0.576 Balanced Accuracy
  - Group Subject: ~0.509 Balanced Accuracy
  - LOSO: ~0.488 Balanced Accuracy
- **Limitations:** These proxy metrics underscore the difficulty of generalizing inter-subject BCI models. LOSO accuracy typically drops near chance, demonstrating the necessity of shadow-mode validation.

---

## Hardware Validation Highlights

- **LSL:** Live validation scripts check drift, jitter, and missing samples from continuous streams. 
- **BrainFlow SyntheticBoard:** Native integration verifies pipeline routing without requiring physical devices.
- **OpenBCI Path:** Support for 8-channel Cyton and 4-channel Ganglion profiles exists in `run_hardware_validation.py`.
- **Disclaimer:** Physical device operation is strictly marked as unvalidated unless a live report was generated and committed locally. **No real OpenBCI device was connected for the repository's baseline validation.**

---

## Safety and Privacy
- Adaptations are blocked via a hardcoded Safety Gate when signal quality drops or when running physical hardware.
- Real EEG inputs are processed in a "shadow-only mode" where predictions are logged but the 3D scene ignores them.
- All metrics are processed locally. No cloud inference is performed on dataset streams.

---

## Repository Structure

```
neuroverse/
  backend/          # FastAPI application
  frontend/         # React + Three.js application
  docs/             # API reference, roadmap, safety docs, application package
  scripts/          # Reproducibility tools (LSL streaming, benchmarks)
  evidence_pack/    # Centralized portfolio evidence inventory and readmes
  reports/          # Generated JSON/MD benchmarks
```

---

## Evidence Pack

An automated inventory mapping what the platform has proven and what it has *not* proven. 

```bash
make generate-evidence-pack
```
See `evidence_pack/README.md` and `evidence_pack/artifact_inventory.md` for a comprehensive list of validation reports.

---

## Interview Demo Flow

For full details, see `docs/DEMO_SCRIPT.md`.

1. **Dashboard:** Open the UI. Show the Dream Corridor rendering loop.
2. **Research Panel:** Demonstrate how real-time inference is simulated.
3. **Benchmarks:** Open the terminal. Run `make raw-bci-benchmark-small` to display CSP metrics in action.
4. **LSL Shadow Mode:** Run `make lsl-live-validation-suite` to prove the backend can absorb and align incoming streams while maintaining a safety lock.
5. **Evidence Pack:** Open `evidence_pack/README.md` to prove documentation and reproducibility standards.

---

## Limitations
- **Hardware:** Simulated biosignals run by default.
- **Labels:** Models train strictly on proxy experimental labels (e.g., "Left hand imagery"), not ground truth cognitive states.
- **Performance:** CSP/FBCSP models perform modestly on unseen subjects (LOSO).

---

## Roadmap
See `docs/ROADMAP.md` for planned expansions into real-time XDF streaming and multi-modal synchronization.

---

## Project Status

**Version:** NeuroVerse v1.1.0-rc1
**License:** Research Prototype. See individual files.
