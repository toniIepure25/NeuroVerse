# NeuroVerse Recruiter Technical Summary

NeuroVerse / Dream Corridor is a local-first neuroadaptive interface prototype for experimenting with simulated or dataset-derived biosignal workflows, cognitive proxy estimation, safety-gated adaptation, deterministic replay, model evaluation, and professional reporting.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

## Why It Is Relevant To BCI / ML Roles

- Real-time backend pipeline: acquisition, features, signal quality, inference, safety, policy, recording, WebSocket broadcast.
- BCI/ML workflow: dataset adapters, feature dataset generation, leakage-aware splits, learned baselines, calibration metrics, model registry, model cards.
- Safety engineering: confidence/SQI gating, conservative learned-model activation, replay auditability, scientific limitation language.
- Product engineering: cinematic interactive frontend, Research Panel, runtime metrics, evaluation visibility, docs, Docker, Makefile workflows.
- Hardware readiness: simulator-first architecture with BrainFlow/OpenBCI, LSL, CSV replay, and XDF replay adapter boundaries and diagnostics.

## Technical Stack

- Backend: FastAPI, Pydantic, NumPy, SciPy, pandas, scikit-learn, joblib, PyYAML.
- Frontend: React, TypeScript, Three.js / React Three Fiber, Zustand.
- Workflow: Docker Compose, pytest, ruff, npm lint/build, Makefile automation.

## What Is Real Today

- Synthetic closed-loop neuroadaptive session.
- JSONL session recording and replay.
- Safety-gated adaptation policy.
- Dataset preparation, validation, training, evaluation, and registry artifacts.
- Runtime health, latency, metrics, and acquisition diagnostics.
- Local evidence pack generation.

## What Is Simulated Or Prototype-Only

- Default biosignals are simulated.
- Learned models estimate dataset-derived proxies, not mental states.
- Hardware adapters are readiness layers and diagnostics unless optional dependencies and local hardware are configured.
- The system is not clinically validated and is not a medical device.

## Next Step With Real Hardware

The next engineering phase would connect a configured BrainFlow/OpenBCI or LSL stream, validate channel mapping and timestamps, collect calibration baselines, quantify signal quality, and run offline replay before allowing any closed-loop learned-model use.

## Hardware Validation Path

NeuroVerse now models the safe path expected in serious BCI prototyping:

1. Simulator remains the default.
2. Adapter diagnostics report dependency and configuration readiness.
3. Hardware validation runs in record-only mode.
4. Timestamp jitter, sampling drift, channel mapping, and SQI are summarized in a report.
5. Calibration creates session-local proxy baselines.
6. Shadow inference computes would-be state/safety/action outputs without adapting the corridor.
7. Hardware closed-loop mode remains locked unless validation passes and explicit configuration enables it.

This matters for BCI/ML roles because it shows the difference between a demo and a safety-conscious acquisition pipeline.

## Real LSL Validation Layer

NeuroVerse uses LSL before direct hardware trials because it is a common interoperability layer for BCI tools. The synthetic LSL streamer proves the platform can discover streams, inspect metadata, preserve timestamps, validate channel profiles, compute SQI, calibrate baselines, and run shadow inference through the same backend path used for real streams.

Closed-loop adaptation remains locked by default. That is intentional: the engineering artifact demonstrates a safer BCI workflow rather than an uncontrolled hardware demo.

## Live LSL Runtime Validation

The live validation suite starts a local simulated LSL stream, discovers it, runs
record-only timing/channel/SQI validation, computes an LSL calibration profile,
runs shadow inference, and packages the artifacts into the evidence pack. This
validates real-time streaming infrastructure and auditability; it does not claim
that the synthetic stream is real EEG or clinically meaningful.

## Real EEG Replay Over LSL

The EEG replay layer uses MNE-compatible data and LSL to stream EEG samples plus
task markers through the same validation pipeline. Fixture mode creates a small
10-channel RawArray with 10-20-style channel labels for deterministic demos; local
EDF/BDF/FIF/GDF files can be replayed without committing datasets to the repo.

Reports include stream metadata, channel mapping, timing and jitter diagnostics,
marker alignment, SQI/artifact proxy summaries, calibration, and shadow
inference. Closed-loop adaptation remains disabled by default. This demonstrates
how the platform would handle public EEG recordings or OpenBCI/Galea LSL streams
before any safety-reviewed closed-loop trial.

## Event-Locked BCI Classifier Evidence

The public EEG validation suite inspects an MNE-compatible fixture or local EEG
file, extracts event-locked features, trains a simple classifier, registers a
model card, replays EEG over LSL, and compares learned event-label predictions
against heuristic proxy summaries. This is the BCI ML evidence path: controlled
task-label classification, shadow-only integration, and explicit safety locks.


## Real Public EEG Validation

PhysioNet EEGBCI support is local-first. Use `make physionet-eegbci-config` to create a config for local EDF files, then `make inspect-physionet-eegbci`, `make prepare-physionet-eegbci-events`, and `make train-physionet-eegbci-classifier` when files are present. Downloads happen only with `make physionet-eegbci-download`.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Closed-loop adaptation remains disabled by default.

First real public EEG evidence run:

- PhysioNet EEGBCI subjects `S001-S003`, motor imagery runs `4/8/12`.
- 9 EDF files, 64 channels, 160 Hz, 270 event annotations.
- Event-locked logistic-regression baseline with `group_run` split.
- Metrics: accuracy 0.508, balanced accuracy 0.478, macro F1 0.479.
- Representative EDF replayed over LSL with observed rate 159.798 Hz, jitter p95 0.085 ms, zero gaps, and zero duplicate timestamps.
- Calibration and shadow inference reports generated; real adaptation actions emitted = 0.

The value here is not high accuracy. It is the reproducible end-to-end path from
public EEG files to leakage-aware evaluation, LSL replay validation, marker/SQI
reporting, shadow inference, and a safety-locked product surface.

## BCI Model Benchmark Evidence

The benchmark layer compares several classical baselines on the same
event-locked PhysioNet feature dataset, using group-aware splits, confidence
intervals, model cards, and a best-model artifact. It records failed or deferred
models instead of hiding them. CSP/FBCSP are handled in the raw-epoch benchmark,
which is the scientifically correct boundary for those methods.

This demonstrates ML evaluation maturity: honest metrics, leakage prevention,
uncertainty estimates, reproducible artifacts, and shadow-only governance.

## Raw-Epoch CSP Benchmark Evidence

NeuroVerse now includes a raw-epoch benchmark path for motor imagery EEG. It
exports PhysioNet EEGBCI epochs as `n_epochs x n_channels x n_times` tensors,
then evaluates CSP + LDA, CSP + logistic regression, and CSP + linear SVM with
group-aware splits and bootstrap intervals.

The latest small benchmark selected Filter Bank CSP + logistic regression with
8 CSP components per band by balanced accuracy. It outperformed the
flattened-feature baseline on this subset, while LOSO remained much harder.
Medium-cohort subjects 1-10 are now supported as an opt-in local run. The latest
medium artifact used 30 EDF files for runs 4/8/12 and produced:

- group-run best: `fbcsp_lda`, balanced accuracy approximately 0.576.
- group-subject best: `fbcsp_logreg`, balanced accuracy approximately 0.509.
- LOSO fold mean balanced accuracy approximately 0.488.

The project also includes a true live LSL raw-shadow path: replayed EDF samples
and markers are streamed over LSL, buffered by timestamp, converted into raw
epochs around marker events, and passed through the selected CSP/FBCSP model.
The report records marker counts, epochs built, missed epochs, predictions, and
zero real adaptation actions.

## Physical Hardware Validation Evidence

BrainFlow/OpenBCI integration now has a record-only validation path. The
BrainFlow SyntheticBoard can be opened locally, streamed into NeuroVerse,
validated for timing/channel/SQI/artifact proxies, calibrated, and run through
shadow inference while emitting zero real adaptation actions. Physical OpenBCI
Cyton and Ganglion profiles are present, but require explicit serial-port
configuration and remain locked by default.

Hardware validation confirms stream quality and software integration; it does
not validate clinical or unrestricted mental-state inference.

The first physical EEG trial protocol adds an eyes-open / eyes-closed
alpha-reactivity sanity check with timing, SQI, artifact, calibration, and
shadow-only reports. If no headset is connected, NeuroVerse reports device
readiness and exact commands instead of fabricating physical evidence.

This is exactly the kind of honest result a BCI ML prototype should show: model
improvement where appropriate, uncertainty where needed, and no closed-loop
activation from real EEG.
