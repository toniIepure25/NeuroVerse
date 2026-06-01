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
- **Command Center Dashboard:** An 8-sector live health monitoring console featuring a guided tour, provenance maps, and shadow explainability.
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
> - `assets/screenshots/02_command_center.png`
> - `assets/screenshots/03_evidence_center.png`
> - `assets/screenshots/04_dream_corridor.png`
> - `assets/screenshots/05_research_panel.png`
> - `assets/screenshots/06_hiring_page.png`

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

Open `http://localhost:5173`. You will be greeted by the new **Product Landing Page** and **Command Center** tour, which guides you through live runtime states, biosensing data pipelines, and safety parameters prior to dashboard operations.

### Static Portfolio Mode

For Vercel, Netlify, GitHub Pages, or reviewer-only frontend hosting, bake the latest generated evidence into `frontend/public/evidence/` and build the static app:

```bash
make protocol-run-demo
make generate-evidence-pack
make static-portfolio-build
```

The Command Center and Evidence Center automatically label whether they are showing live backend evidence or a static baked snapshot. Static evidence is copied from `evidence_pack/` only, preserves `closed_loop_allowed: false`, and is not live runtime evidence.

### Data Source Wizard

The **Data Sources** tab is a setup assistant for moving from safe demos toward
more demanding evidence paths:

- Simulator: default no-hardware protocol.
- PhysioNet EEGBCI replay: checks local dataset configuration and EDF files.
- LSL stream: checks `pylsl` and detected EEG streams when the backend is live.
- BrainFlow SyntheticBoard: checks BrainFlow availability while clearly marking
  the source as synthetic.
- OpenBCI Cyton/Ganglion: checks BrainFlow and serial-device hints, but remains
  record-only/manual with explicit `PORT` input.

BrainFlow SyntheticBoard is not real OpenBCI physical validation. OpenBCI/Galea
physical validation remains unperformed unless a real device report exists.
Closed-loop from real EEG is disabled by default.

---

## Reproducible Evidence Commands

Run these to reproduce key platform capabilities. Results are output to the `reports/` and `evidence_pack/` directories.

**Launch Readiness & QA Checklists (Unified Validation):**
```bash
# 1. Run full release readiness and QA verifiers
make reviewer-ready-check

# 2. Run non-expensive verification tests only (fast)
make reviewer-ready-fast

# 3. Run individual QA checks
make verify-reviewer-demo-flow
make check-static-portfolio
make check-frontend-routes
```

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

**Multimodal Fusion Validation & Calibration:**
```bash
make fusion-evidence-refresh  # runs validation scenarios, calibration profile, and manifest check
make fusion-validate          # runs behavioral ablation scenarios
make fusion-calibrate         # normalizes and bakes demo calibration profile
make imagina-validate-manifest # validates IMAGINA dataset bridge bridge manifest
```


---

## Benchmark Highlights

We evaluated classical ML and Riemannian geometry models on the PhysioNet EEG Motor Movement/Imagery dataset (Medium subset: `S001-S010`, Runs `4,8,12`). Task labels: `LEFT_HAND_IMAGERY` vs `RIGHT_HAND_IMAGERY`.

All benchmark results are provenance-strict: every leaderboard row includes `metric_source_file`, `metric_source_field`, and `benchmark_type`. No manually hardcoded values.

- **Evaluation Contexts:**
  - `subject_specific` (calibrated per-user): Riemannian MDM ~0.651 Balanced Accuracy (train runs 4/8, test run 12). This requires per-user calibration.
  - `channel_ablation` (LOSO): Best cross-subject generalization is Riemannian TS LogReg on motor_subset (7ch) at ~0.699 Balanced Accuracy.
  - `frequency_window_ablation` (group_run): Best run-level generalization is FBCSP LogReg at ~0.636 Balanced Accuracy.
- **Channel Ablation:** all_channels (64ch), motor_subset (7ch), minimal_motor (3ch). Channel counts verified to differ.
- **Limitations:** These are different evaluation contexts and should not be compared as equivalent. LOSO accuracy is the strictest cross-subject evidence.


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

## Multimodal Fusion v1 / IMAGINA Plugin Foundation

NeuroVerse now includes a conservative Fusion v1 layer for EEG, simulated or
optional gaze, simulated or optional physiology, behavior, self-report, and
IMAGINA-style imagery proxy packets. It uses a late-fusion baseline with
missing-modality handling, uncertainty, and safety recommendations.

Multimodal fusion outputs are experimental proxy estimates, not clinical or
unrestricted mental-state measurements. IMAGINA plugin outputs are experimental
imagery-quality proxies, not decoded thoughts or dreams. Proposed Dream
Corridor mappings are shadow-only suggestions; closed-loop from real EEG is
disabled by default.

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
