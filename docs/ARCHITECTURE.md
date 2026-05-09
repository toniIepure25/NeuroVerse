# NeuroVerse Architecture

## Overview

NeuroVerse is a closed-loop neuroadaptive platform that estimates cognitive state from multimodal biosignals and adapts a 3D environment in real time, with a safety gate preventing unreliable adaptations.

The current implementation uses simulated biosignals with clean upgrade paths to real hardware (OpenBCI, BrainFlow, LSL).

## System Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Acquisition │────▶│ Preprocessing│────▶│   Feature    │
│  (Simulator) │     │  (Filters)   │     │  Extraction  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                    ┌─────────────┼──────────────┐
                                    ▼             ▼              ▼
                              ┌──────────┐ ┌──────────┐  ┌──────────┐
                              │ EEG SQI  │ │Physio SQI│  │ Gaze SQI │
                              └────┬─────┘ └────┬─────┘  └────┬─────┘
                                   └─────────────┼─────────────┘
                                                 ▼
                              ┌───────────────────────────────────┐
                              │     State Estimation (Heuristic)  │
                              │   focus | relaxation | workload   │
                              │   stress | fatigue | imagery      │
                              └───────────────┬───────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────────┐
                              │          Safety Gate              │
                              │  ALLOWED | WAIT | BLOCKED | ASK   │
                              └───────────────┬───────────────────┘
                                              │
                                              ▼
                              ┌───────────────────────────────────┐
                              │      Adaptation Policy            │
                              │  Behavior tree + smoothing        │
                              └───────────┬───────────┬───────────┘
                                          │           │
                                          ▼           ▼
                              ┌──────────────┐  ┌──────────────┐
                              │   Session    │  │  WebSocket   │
                              │   Recorder   │  │  Broadcast   │
                              │   (JSONL)    │  │  (clients)   │
                              └──────────────┘  └──────┬───────┘
                                                       │
                                                       ▼
                                              ┌──────────────┐
                                              │   Frontend   │
                                              │  React + R3F │
                                              └──────────────┘
```

## Backend Modules

### Core (`app/core/`)
- **config.py**: Pydantic Settings loaded from environment variables
- **logging.py**: Structured logging
- **clock.py**: Session-relative monotonic clock with replay override
- **engine.py**: `NeuroVerseEngine` orchestrates the full pipeline loop
- **exceptions.py**: Custom exception hierarchy

### Schemas (`app/schemas/`)
Strongly typed Pydantic models for all event payloads. See [EVENT_SCHEMAS.md](EVENT_SCHEMAS.md).

### Acquisition (`app/acquisition/`)
- **simulator.py**: Phase-driven synthetic biosignal generator (7 phases, 180s default)
- **brainflow_adapter.py**: Stub for BrainFlow hardware
- **lsl_adapter.py**: Stub for Lab Streaming Layer

### Signal Processing (`app/preprocessing/`, `app/features/`, `app/signal_quality/`)
- Bandpass/notch filter proxies, artifact rejection, windowing
- Per-modality feature extraction (EEG bands, physio metrics, gaze metrics)
- Signal Quality Index (SQI) per modality and multimodal fusion

### Inference (`app/inference/`)
- **HeuristicStateEstimator**: Weighted formula-based estimator (MVP)
- **LearnedModelEstimator**: Phase 2 wrapper for local sklearn baselines with explicit prediction semantics
- **ClassicalStateEstimator**: Legacy placeholder for sklearn models
- **TransformerFusionEstimator**: Placeholder for deep learning models
- **ONNXStateEstimator**: Placeholder for ONNX runtime models

### Datasets And Evaluation (`app/datasets/`, `app/ml/`, `app/experiments/`)
- Dataset adapters expose synthetic, CSV, CLARE-like, and PhysioNet-MI-style local data as `WindowedSample` objects
- Feature dataset generation reuses existing feature extractors and preserves modality prefixes
- Baseline training uses sklearn models and stores local joblib artifacts under `models/`
- Metrics include classification, calibration, latency, and replay-oriented summaries
- Dataset labels are treated as research proxies, not direct measurements of mental state

### Fusion (`app/fusion/`)
- **Late fusion**: Static weight combination
- **Bayesian fusion**: SQI-weighted combination (default)
- **Attention fusion**: Placeholder for learned cross-modal attention

### Safety (`app/safety/`)
- Threshold-based safety gate with configurable rules
- Decisions: ALLOWED, WAIT, BLOCKED, ASK
- Conformal prediction stub for future uncertainty quantification

### Policy (`app/policy/`)
- Behavior tree with priority-ordered rule evaluation
- Smoothing: max intensity delta, cooldown timers, oscillation detection

### Sessions (`app/sessions/`)
- JSONL recording of all events
- Replay at original or accelerated speed
- Session storage and retrieval

### API (`app/api/`)
- REST endpoints for health, config, sessions
- WebSocket for live streaming and replay

## Frontend Modules

### Store (`src/store/`)
- Zustand store managing cognitive state, safety, adaptation, environment, timeline

### Scene (`src/components/Scene/`)
- React Three Fiber canvas with fog, lighting, particles, symbolic objects
- Environment adapts based on adaptation actions from backend

### Dashboard (`src/components/Dashboard/`)
- Cognitive radar chart, SQI bars, safety panel, event timeline, session controls

## Key Design Decisions

1. **Engine pattern**: Pipeline logic lives in `NeuroVerseEngine`, not in API route handlers
2. **Event-driven architecture**: All pipeline stages emit typed `BaseEvent` objects
3. **SQI-weighted fusion**: Bayesian fusion automatically degrades gracefully when sensor quality drops
4. **Dual smoothing**: Backend (rolling average + max delta) and frontend (lerp interpolation)
5. **Deterministic replay**: Events recorded to JSONL can be replayed through safety + policy for verification
