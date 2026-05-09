# NeuroVerse Event Schemas

## Event Envelope

All events use a common `BaseEvent` envelope:

```json
{
  "event_id": "a1b2c3d4-...",
  "session_id": "abc123",
  "event_type": "neuroverse.state.predicted",
  "timestamp": 45.123,
  "source": "engine",
  "correlation_id": null,
  "payload": { ... },
  "metadata": null
}
```

## Event Types

| Event Type | Description |
|---|---|
| `neuroverse.signal.raw_window` | Raw biosignal data window |
| `neuroverse.signal.window_processed` | Preprocessed signal window |
| `neuroverse.features.extracted` | Extracted features across modalities |
| `neuroverse.state.predicted` | Cognitive state estimation |
| `neuroverse.safety.decision` | Safety gate decision |
| `neuroverse.adaptation.action` | Environment adaptation action |
| `neuroverse.session.started` | Session start marker |
| `neuroverse.session.stopped` | Session end marker |
| `neuroverse.replay.started` | Replay session start |
| `neuroverse.replay.completed` | Replay session complete |
| `neuroverse.error` | Error event |

## Payload Schemas

### StatePredictionPayload

```json
{
  "focus": 0.72,
  "relaxation": 0.45,
  "workload": 0.38,
  "stress": 0.22,
  "fatigue": 0.15,
  "imagery_engagement": 0.31,
  "confidence": 0.84,
  "model_version": "heuristic-v1",
  "feature_window_ms": 500
}
```

All numeric scores are clamped to [0, 1].
For Phase 2 learned baselines, `model_version` may use a `learned:<model_id>` prefix. The scores
remain estimated proxies whose interpretation depends on model metadata such as `prediction_semantics`.

### SafetyDecisionPayload

```json
{
  "decision": "ALLOWED",
  "reason": "No safety issue",
  "sqi_scores": {"eeg": 0.92, "physio": 0.87, "gaze": 0.91, "multimodal": 0.90},
  "confidence": 0.84,
  "blocked_actions": [],
  "safety_level": "normal"
}
```

Decision values: `ALLOWED`, `WAIT`, `BLOCKED`, `ASK`.
Safety levels: `normal`, `caution`, `freeze`.

### AdaptationActionPayload

```json
{
  "action": "IncreaseSceneClarity",
  "intensity": 0.65,
  "duration_ms": 2000,
  "source_state": "high_focus",
  "reason": "Focus high (0.82), confidence adequate",
  "parameters": {"reduce_fog": true, "increase_light": true}
}
```

Possible actions: `IncreaseSceneClarity`, `SmoothEnvironmentMotion`, `SimplifyEnvironment`, `StabilizeVisualField`, `GenerateSymbolicObject`, `ReduceVisualComplexity`, `MaintainBaseline`, `FreezeAdaptation`.

### FeaturePayload

```json
{
  "eeg": {"alpha_power": 0.62, "beta_power": 0.51, "theta_power": 0.34, ...},
  "physio": {"heart_rate": 0.45, "rmssd_proxy": 0.68, "stress_index": 0.29, ...},
  "gaze": {"fixation_stability": 0.81, "blink_rate": 0.12, ...},
  "multimodal": {"cognitive_zone_score": 0.67, "modality_agreement": 0.74, ...},
  "sqi_scores": {"eeg": 0.92, "physio": 0.87, "gaze": 0.91, "multimodal": 0.90}
}
```

### RawSignalPayload

```json
{
  "modality": "multimodal",
  "sampling_rate": 250.0,
  "channel_names": ["Fp1", "Fp2", "F3", ..., "HR", "HRV_RMSSD", ..., "gaze_x", "blink"],
  "data": [[0.12, -0.34, ...], ...],
  "window_size_ms": 500,
  "signal_quality_hint": 0.91
}
```

## Versioning

Schemas are versioned implicitly through `model_version` in state predictions. Event types use dotted namespaces for future evolution. Breaking changes will use new event type suffixes (e.g., `neuroverse.state.predicted.v2`).
