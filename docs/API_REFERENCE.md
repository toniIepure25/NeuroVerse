# NeuroVerse API Reference

This document summarizes the available REST and WebSocket endpoints.

## Acquisition

### `GET /api/v1/acquisition/status`
**Purpose**: Api Acquisition Status

---

### `POST /api/v1/acquisition/test`
**Purpose**: Api Acquisition Test

---

### `POST /api/v1/acquisition/select`
**Purpose**: Api Acquisition Select

---

### `GET /api/v1/acquisition/lsl/status`
**Purpose**: Api Lsl Status

---

### `GET /api/v1/acquisition/lsl/streams`
**Purpose**: Api Lsl Streams

---

### `GET /api/v1/acquisition/lsl/streams/{stream_id}/metadata`
**Purpose**: Api Lsl Stream Metadata

---

### `GET /api/v1/acquisition/brainflow/status`
**Purpose**: Api Brainflow Status

---

### `GET /api/v1/acquisition/brainflow/profiles`
**Purpose**: Api Brainflow Profiles

---

### `GET /api/v1/acquisition/brainflow/devices`
**Purpose**: Api Brainflow Devices

---

### `POST /api/v1/acquisition/brainflow/test`
**Purpose**: Api Brainflow Test

---

### `POST /api/v1/acquisition/brainflow/select`
**Purpose**: Api Brainflow Select

---

### `POST /api/v1/acquisition/brainflow/start`
**Purpose**: Api Brainflow Start

---

### `POST /api/v1/acquisition/brainflow/stop`
**Purpose**: Api Brainflow Stop

---

### `POST /api/v1/acquisition/lsl/select`
**Purpose**: Api Lsl Select

---

### `GET /api/v1/acquisition/profiles`
**Purpose**: Api Acquisition Profiles

---

### `GET /api/v1/acquisition/profiles/{profile_id}`
**Purpose**: Api Acquisition Profile

---

### `POST /api/v1/acquisition/profiles/validate`
**Purpose**: Api Validate Profile

---

### `POST /api/v1/acquisition/validation/start`
**Purpose**: Api Validation Start

---

### `POST /api/v1/acquisition/validation/stop`
**Purpose**: Api Validation Stop

---

### `GET /api/v1/acquisition/validation/status`
**Purpose**: Api Validation Status

---

### `GET /api/v1/acquisition/validation/reports`
**Purpose**: Api Validation Reports

---

### `GET /api/v1/acquisition/validation/reports/{report_id}`
**Purpose**: Api Validation Report

---

### `POST /api/v1/acquisition/shadow/start`
**Purpose**: Start Shadow Mode

---

### `GET /api/v1/acquisition/shadow/{report_id}`
**Purpose**: Get Shadow Report

---

## Calibration

### `POST /api/v1/calibration/start`
**Purpose**: Start Calibration

---

### `GET /api/v1/calibration/{calibration_id}`
**Purpose**: Get Calibration

---

## Hardware Trials

### `GET /api/v1/hardware-trials`
**Purpose**: List Hardware Trials

---

### `GET /api/v1/hardware-trials/latest`
**Purpose**: Latest Hardware Trial

---

### `GET /api/v1/hardware-trials/{trial_id}`
**Purpose**: Get Hardware Trial

---

## Health & Runtime

### `GET /api/v1/health`
**Purpose**: Api V1 Health

---

### `GET /api/v1/health/deep`
**Purpose**: Deep Health

---

### `GET /api/v1/runtime/status`
**Purpose**: Api Runtime Status

---

### `GET /api/v1/runtime/latency`
**Purpose**: Api Runtime Latency

---

### `GET /api/v1/runtime/metrics`
**Purpose**: Api Runtime Metrics

---

### `POST /api/v1/runtime/emergency-stop`
**Purpose**: Api Emergency Stop

---

### `POST /api/v1/runtime/freeze`
**Purpose**: Api Freeze

---

### `POST /api/v1/runtime/unfreeze`
**Purpose**: Api Unfreeze

---

## Models & Evaluation

### `GET /api/datasets`
**Purpose**: List Datasets

---

### `GET /api/datasets/{dataset_id}/metadata`
**Purpose**: Dataset Metadata

---

### `POST /api/datasets/validate`
**Purpose**: Validate Dataset

---

### `GET /api/models`
**Purpose**: Api List Models

---

### `GET /api/models/active`
**Purpose**: Api Get Active Model

---

### `POST /api/models/deactivate`
**Purpose**: Api Deactivate Model

---

### `GET /api/models/{model_id}`
**Purpose**: Api Get Model

---

### `POST /api/models/{model_id}/activate`
**Purpose**: Api Activate Model

---

### `GET /api/evaluation/reports`
**Purpose**: Api List Reports

---

### `GET /api/evaluation/latest`
**Purpose**: Api Latest Report

---

### `GET /api/evaluation/reports/{report_id}`
**Purpose**: Api Get Report

---

## Other

### `GET /health`
**Purpose**: Health

---

### `GET /ready`
**Purpose**: Ready

---

### `GET /api/config`
**Purpose**: Get Config

---

### `POST /api/session/start`
**Purpose**: Start Session

---

### `POST /api/v1/session/start`
**Purpose**: Start Session

---

### `POST /api/session/stop`
**Purpose**: Stop Session

---

### `POST /api/v1/session/stop`
**Purpose**: Stop Session

---

### `GET /api/sessions`
**Purpose**: Get Sessions

---

### `GET /api/sessions/{session_id}/files`
**Purpose**: Get Files

---

### `GET /api/sessions/{session_id}/export`
**Purpose**: Export Session

---

### `DELETE /api/sessions/{session_id}/delete`
**Purpose**: Delete Session

---

### `GET /api/sessions/{session_id}`
**Purpose**: Get Session

---

### `GET /api/sessions/{session_id}/summary`
**Purpose**: Get Summary

---

### `GET /api/sessions/{session_id}/events`
**Purpose**: Get Events

---

### `POST /api/replay/{session_id}`
**Purpose**: Start Replay

---

### `GET /api/v1/datasets`
**Purpose**: List Datasets

---

### `GET /api/v1/datasets/{dataset_id}/metadata`
**Purpose**: Dataset Metadata

---

### `POST /api/v1/datasets/validate`
**Purpose**: Validate Dataset

---

### `GET /api/v1/models`
**Purpose**: Api List Models

---

### `GET /api/v1/models/active`
**Purpose**: Api Get Active Model

---

### `POST /api/v1/models/deactivate`
**Purpose**: Api Deactivate Model

---

### `GET /api/v1/models/{model_id}`
**Purpose**: Api Get Model

---

### `POST /api/v1/models/{model_id}/activate`
**Purpose**: Api Activate Model

---

### `GET /api/v1/evaluation/reports`
**Purpose**: Api List Reports

---

### `GET /api/v1/reports`
**Purpose**: Api List Reports

---

### `GET /api/v1/evaluation/latest`
**Purpose**: Api Latest Report

---

### `GET /api/v1/evaluation/reports/{report_id}`
**Purpose**: Api Get Report

---

### `GET /api/v1/reports/{report_id}`
**Purpose**: Api Get Report

---

### `GET /api/v1/eeg/public/latest`
**Purpose**: Api Latest Public Eeg Report

---

### `GET /api/v1/eeg/real-public/latest`
**Purpose**: Api Latest Real Public Eeg Report

---

### `GET /api/v1/eeg/bci-benchmark/latest`
**Purpose**: Api Latest Bci Benchmark Report

---

### `GET /api/v1/eeg/raw-bci-benchmark/latest`
**Purpose**: Api Latest Raw Bci Benchmark Report

---

### `GET /api/v1/eeg/bci-benchmark-comparison/latest`
**Purpose**: Api Latest Bci Benchmark Comparison

---

### `GET /api/v1/eeg/raw-bci-shadow/latest`
**Purpose**: Api Latest Raw Bci Shadow Report

---

### `GET /api/runtime/status`
**Purpose**: Api Runtime Status

---

### `GET /api/runtime/latency`
**Purpose**: Api Runtime Latency

---

### `GET /api/runtime/metrics`
**Purpose**: Api Runtime Metrics

---

## Replay

### `POST /api/v1/replay/{session_id}`
**Purpose**: Start Replay

---

### `POST /api/v1/replay/{session_id}/pause`
**Purpose**: Pause Replay

---

### `POST /api/v1/replay/{session_id}/resume`
**Purpose**: Resume Replay

---

### `POST /api/v1/replay/{session_id}/restart`
**Purpose**: Restart Replay

---

## Sessions

### `GET /api/v1/sessions`
**Purpose**: Get Sessions

---

### `GET /api/v1/sessions/{session_id}/files`
**Purpose**: Get Files

---

### `GET /api/v1/sessions/{session_id}/export`
**Purpose**: Export Session

---

### `DELETE /api/v1/sessions/{session_id}/delete`
**Purpose**: Delete Session

---

### `GET /api/v1/sessions/{session_id}`
**Purpose**: Get Session

---

### `GET /api/v1/sessions/{session_id}/summary`
**Purpose**: Get Summary

---

### `GET /api/v1/sessions/{session_id}/events`
**Purpose**: Get Events

---
