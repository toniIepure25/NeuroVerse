# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

NeuroVerse is a closed-loop neuroadaptive BCI platform: a FastAPI backend streams/derives multimodal biosignals, estimates cognitive-proxy state, gates it through a safety layer, and drives a React Three Fiber 3D frontend over WebSockets. It is a research prototype (simulated signals + local dataset replay by default), explicitly **not** a medical device and **not** "mind reading" — keep that framing when touching docs, model cards, or UI copy.

Almost everything is driven through the root `Makefile` — prefer `make <target>` over invoking scripts directly, since targets encode the correct flags, config paths, and output locations.

## Common commands

```bash
make install              # backend (pip install -e ".[dev]") + frontend (npm install)
make install-hardware-extra   # adds the ".[hardware]" extra (brainflow, pylsl, mne, neurokit2)
# Riemannian models (pyriemann) live in the ".[bci]" extra: pip install -e ".[bci]"
make dev                  # backend on :8000 (uvicorn --reload) + frontend on :5173 (vite), in parallel
make backend / make frontend   # run one side only
make preflight            # environment pre-checks before doing anything

make test                 # cd backend && python3 -m pytest app/tests/ -v
make lint                 # ruff check --fix + ruff format on backend/app
make frontend-check       # npm run lint (frontend)
make build                # vite production build of the frontend
make smoke                # smoke-api + frontend-check
make release-check        # validate release artifacts (scripts/check_release_artifacts.py)
```

Run a single backend test:
```bash
cd backend && python3 -m pytest app/tests/test_<name>.py::test_<case> -v
```

`make smoke-api` boots the app via `create_app()` and asserts a fixed set of expected routes exist — if you add/rename/remove an API route, update the expected-paths set in the `smoke-api` target in the `Makefile`, or this will fail.

## BCI / evidence workflows

These produce artifacts under `reports/` and `evidence_pack/`. The common path:

```bash
make public-eeg-fixture-suite        # simulated/MNE replay end-to-end suite (no download)
make prepare-raw-epochs-small        # build epoch .npz from PhysioNet EEGBCI subset
make raw-bci-benchmark-small         # CSP/FBCSP benchmark (group_run split)
make raw-bci-loso-small              # leave-one-subject-out (strictest cross-subject evidence)
make lsl-live-validation-suite       # LSL drift/jitter/missing-sample validation
make validate-brainflow-synthetic    # BrainFlow SyntheticBoard path (no hardware)
make generate-evidence-pack          # regenerate evidence_pack/ inventory + reports
```

PhysioNet data is **not** downloaded implicitly — `*-medium` targets require an explicit `make physionet-eegbci-download-medium` / `-config-medium` first and will hard-fail otherwise. Hardware targets for real devices require a `PORT=` arg (e.g. `make validate-openbci-cyton PORT=/dev/ttyUSB0`).

**Provenance is strict:** benchmark leaderboard rows must carry `metric_source_file`, `metric_source_field`, and `benchmark_type` — never hardcode metric values. Keep the three evaluation contexts distinct and non-comparable: `subject_specific` (per-user calibrated), `channel_ablation` (LOSO), `frequency_window_ablation` (group_run).

## Architecture

The single most important distinction: **`backend/app/inference/` is the real-time online path** (models that run in the live closed loop) and **`backend/app/ml/` is the offline training/benchmark pipeline**. They are deliberately separate to prevent leakage between training and serving — keep them that way.

The live closed loop (orchestrated from `core/engine.py`) flows through one module per stage:

```
acquisition/ → preprocessing/ → features/ + signal_quality/(SQI) → inference/ → fusion/ → safety/(GATE) → policy/ → sessions/(recorder) → WebSocket → frontend
```

- **`acquisition/`** — pluggable signal-source adapters over a common `base.py`: `simulator`, `csv_replay_adapter`, `lsl_adapter`, `brainflow_adapter` (SyntheticBoard / OpenBCI Cyton / Ganglion), `eeg_fixture` / EEG-LSL-replay. Scripts/routes pick one via `--source` / `--adapter` / `--profile-id`.
- **`preprocessing/`** (`filters`, `windowing`, `artifact`) and **`features/`** (`eeg_features`, `gaze_features`, `physio_features`, `multimodal_features`).
- **`signal_quality/`** — per-modality SQI (`eeg_sqi`, `gaze_sqi`, `physio_sqi`) feeding the safety gate.
- **`inference/`** — online estimators behind a common base: `heuristic_model` (the safe default), `classical_model`, `learned_model`, loaded via `model_loader` / `onnx_loader`, with per-user `calibration`.
- **`fusion/`** — multimodal combination (`late_fusion`, `bayesian_fusion`; attention/transformer variants are stubs).
- **`safety/`** — the gate. `safety_gate.py` + `rules.py` are the enforcement; `state_machine.py`, `closed_loop_governance.py`, and `reason_codes.py` add governed state transitions and machine-readable block reasons (not free-text). Adaptations are **blocked** on poor SQI or physical-hardware mode. Safety-critical — preserve gating semantics; `test_safety_gate.py` guards them.
- **`policy/`** — `adaptation_policy` / `behavior_tree` / `smoothing` translate gated state into UI parameters.
- **`sessions/`** — `recorder` / `storage` / `replay` / `summary` persist sessions as JSONL under `backend/data/sessions/`.
- **`core/`** — `config` (pydantic-settings), `engine` (loop orchestrator), `clock`, `runtime_status`, `telemetry`.

`schemas/` holds the pydantic contracts (`signals`, `state`, `adaptation`, `safety`, `events`, `session`) shared across stages and with the frontend.

API (`backend/app/main.py` → `create_app()`, entrypoint `uvicorn app.main:app`): routers are one-per-domain in `api/routes_*.py` (`health`, `config`, `sessions`, `stream`, `replay`, `datasets`, `models`, `evaluation`, `runtime`, `acquisition`, `hardware_trials`, `calibration`, `shadow`), plus `websocket_manager.py` for the live stream. Routes span legacy `/api/...` and versioned `/api/v1/...`.

The **offline `ml/` pipeline**: `feature_dataset` / `event_epochs` build datasets, `splits.py` enforces `group_run` / `group_subject` / `leave_one_subject_out` (the leakage guard), `trainer` + `baselines` + `raw_epoch_models` (CSP/FBCSP/Riemannian) train, `evaluator` + `metrics` score, `registry` + `serialization` + `reports` persist results.

Other top-level dirs:
- **`scripts/`** (~45 files) — all reproducibility tooling the `Makefile` targets call (streaming, benchmarks, hardware validation, dataset prep, evidence-pack generation).
- **`configs/datasets/*.yaml`, `configs/experiments/*.yaml`, `configs/hardware/*.example.yaml`** — passed via `--dataset-config` / `--experiment-config` / `--profile-id`.
- **`models/`** — trained-model registry (`registry.json`) plus per-model `metadata.json` / `metrics.json` / `model_card.md`.
- **`reports/`** — generated benchmark JSON/MD.
- **`evidence_pack/`** — curated portfolio inventory of what has / has **not** been proven; regenerated by `make generate-evidence-pack`.
- **`frontend/src/`** — React 18 + TS + Three.js (`@react-three/fiber`/`drei`), Zustand store, Vite. `components/` is split into `Pages` (landing, Evidence Center), `Dashboard`, `Scene` (the 3D "Dream Corridor"), `Layout`. Note: `npm run lint` is `tsc --noEmit` (type-check only, no ESLint).

## Safety / framing invariants

- Real EEG runs in **shadow-only mode**: predictions are logged but the 3D scene ignores them. Do not wire real-stream inference into adaptation output.
- Physical OpenBCI/Galea hardware is treated as **unvalidated** unless a committed real-device report exists. Don't claim hardware validation in docs/model cards without that report.
- All inference is local; no cloud inference on dataset streams.
