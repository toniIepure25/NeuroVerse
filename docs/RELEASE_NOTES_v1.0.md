# Release Notes: NeuroVerse v1.0.0-rc1

## Overview
NeuroVerse v1.0.0-rc1 is the first major release candidate of the Dream Corridor neuroadaptive platform. This release formalizes the transition from ad-hoc scripts to a structured, reproducible neurotechnology portfolio piece, emphasizing rigorous ML baselines, live hardware/LSL streaming paths, and explicit scientific honesty.

## Features
- **Real-Time Neuroadaptive Loop**: Full integration of FastAPI backend, WebSockets, and React Three Fiber frontend.
- **LSL Live Streaming Validation**: Architecture to ingest continuous Lab Streaming Layer streams, handle sub-millisecond timestamps, and validate jitter/drift without breaking the event loop.
- **Hardware Integration Paths**: BrainFlow adapters for OpenBCI Cyton (8-channel) and Ganglion (4-channel), plus a native SyntheticBoard capability for continuous integration.
- **Safety-First "Shadow Mode"**: Default behavior strictly gates UI adaptations. Real signals run through the pipeline to generate performance metrics without influencing the visual state.
- **Physical Trial Protocol**: Offline eyes-open/eyes-closed data collection workflow allowing alpha reactivity sanity checking prior to full ML engagement.
- **Automated Evidence Pack**: Single-command generation (`make generate-evidence-pack`) of the `evidence_pack/` folder, collating artifacts, JSON reports, and Markdown indices.

## Validated Workflows
- Simulated biosignal closed-loop.
- LSL continuous replay and live stream simulation.
- MNE EDF file replay over LSL with event markers.
- BrainFlow SyntheticBoard integration.
- (Physical OpenBCI validation is structurally complete but remains strictly marked as unvalidated unless local hardware is supplied.)

## Benchmark Results
- **PhysioNet EEGBCI (S001-S010, Medium Subset):**
  - **Task:** Left vs. Right hand motor imagery (Binary).
  - **Best Model:** Filter Bank CSP (FBCSP) + Logistic Regression.
  - **Group Run Split:** ~0.576 Balanced Accuracy.
  - **Group Subject Split:** ~0.509 Balanced Accuracy.
  - **LOSO Split:** ~0.488 Balanced Accuracy.
- These results reflect realistic classical algorithm performance on public datasets, deliberately emphasizing the inter-subject generalization challenge.

## Limitations
- **Simulated by Default**: The default runtime is simulated to allow reproducibility without specialized hardware.
- **No Ground Truth**: The system relies on experimental task labels ("proxy metrics") and does not claim to decode internal cognitive state or read thoughts.
- **Not a Medical Device**: This is a research prototype.

## Known Issues
- Optional dependencies (`pylsl`, `mne`, `brainflow`) are not installed by default. Hardware commands will exit with graceful error messages unless dependencies are met.
- The `export-api-docs` Makefile command requires a full python environment. If executed in a broken state, it outputs a partial placeholder.

## Next Milestones
- Native real-time XDF file parsing for synchronized multi-stream playback.
- Enhanced online artifact rejection algorithms for physical OpenBCI data.
- UI improvements for the Data / Research panels to support multi-modal visualizations.
