# NeuroVerse Roadmap

## Phase 0: Foundation (Complete)
- Project scaffold and directory structure
- Backend and frontend configuration
- Docker and development workflow
- CI-ready Makefile

## Phase 1: Simulated Closed-Loop MVP (Complete)
- Typed event schemas (Pydantic v2)
- 7-phase biosignal simulator
- Feature extraction (EEG, physio, gaze, multimodal)
- Signal Quality Index per modality
- Heuristic state estimator
- Safety gate with configurable thresholds
- Behavior-tree adaptation policy with smoothing
- JSONL session recording
- WebSocket streaming
- REST API endpoints
- 47 backend tests

## Phase 2: Frontend Demo (Complete)
- React + TypeScript + Vite scaffold
- React Three Fiber meditation chamber
- Adaptive fog, lighting, particles, symbolic objects
- Zustand state management
- Recharts cognitive radar chart
- SQI bars, safety panel, event timeline
- Session controls with WebSocket auto-reconnect

## Phase 3: Replay and Validation (Complete)
- JSONL session replay at variable speed
- Replay WebSocket endpoint
- Deterministic replay validation
- Export scripts

## Phase 4: Future-Ready Interfaces (Complete)
- BrainFlow adapter stub
- LSL adapter stub
- ONNX model loader stub
- Transformer fusion architecture documentation
- Attention fusion stub

## Phase 5: Polish and Documentation (Complete)
- Architecture documentation
- Event schema documentation
- Safety and ethics documentation
- Demo script
- Research notes

---

## Future Phases

### Phase 6: Classical ML Models
- Collect labeled feature vectors from calibration sessions
- Train RandomForest/GradientBoosting per cognitive dimension
- Evaluate against heuristic baseline
- Export as .joblib, integrate into ClassicalStateEstimator

### Phase 7: Real Hardware Integration
- BrainFlow adapter for OpenBCI Cyton/Ganglion
- LSL adapter for multi-device synchronization
- Real-time artifact rejection with MNE-Python
- Per-subject calibration protocol

### Phase 8: Transformer Fusion
- Implement PyTorch cross-modal attention model
- Train on public datasets (DEAP, SEED, or custom)
- Conformal prediction for uncertainty-aware safety
- ONNX export for production inference

### Phase 9: BCI Game / XR Integration
- Unity WebSocket bridge
- VR meditation environment
- Haptic feedback integration
- Eye tracker integration (Tobii, Pupil Labs)

### Phase 10: Evaluation and Publication
- Controlled user study protocol
- Statistical analysis pipeline
- IRB documentation templates
- Research paper draft structure
