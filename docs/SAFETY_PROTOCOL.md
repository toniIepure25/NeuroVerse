# Safety Protocol

NeuroVerse prioritizes user control, signal reliability, and conservative adaptation.

> **Closed-loop from real EEG is disabled by default.**
>
> **Hardware validation confirms stream quality and software integration; it does not validate clinical or unrestricted mental-state inference.**
>
> **The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.**

---

## Safety State Machine

NeuroVerse implements a formal, deterministic safety state machine (`backend/app/safety/state_machine.py`). Every adaptation decision can be traced to a state, a reason code, and a timeline entry.

### States

| State | Severity | Description |
| --- | --- | --- |
| `NO_DATA` | info | No biosignal data available |
| `SIMULATED_ONLY` | info | Running on simulated biosignals |
| `DATA_REPLAY` | info | Replaying recorded or dataset EEG |
| `RECORD_ONLY` | info | Recording without adaptation |
| `VALIDATION_RUNNING` | info | Hardware/signal validation in progress |
| `VALIDATION_PASSED` | info | Validation passed |
| `VALIDATION_FAILED` | warning | Validation failed |
| `CALIBRATION_REQUIRED` | warning | Calibration required before shadow inference |
| `CALIBRATION_RUNNING` | info | Calibration in progress |
| `CALIBRATED` | info | Calibration complete |
| `SHADOW_READY` | info | Ready for shadow-only inference |
| `SHADOW_RUNNING` | info | Shadow inference running (no real adaptation) |
| `CLOSED_LOOP_LOCKED` | **blocked** | Default state — real EEG closed-loop disabled |
| `HARDWARE_UNVALIDATED` | warning | Physical hardware not validated |
| `SIGNAL_UNSAFE` | warning | Signal quality below safety thresholds |
| `SENSOR_DROPOUT` | warning | One or more sensors dropped out |
| `HIGH_UNCERTAINTY` | warning | Model prediction uncertainty too high |
| `ADAPTATION_FROZEN` | **blocked** | Adaptation frozen by operator or safety gate |
| `EMERGENCY_STOP` | **emergency** | All adaptation halted |

### Default startup state

The system starts in `CLOSED_LOOP_LOCKED` or `NO_DATA`, never in a state that allows real EEG adaptation.

---

## Reason Codes

Structured reason codes (`backend/app/safety/reason_codes.py`) provide machine-readable explanations for every safety decision:

| Code | Meaning |
| --- | --- |
| `low_sqi` | Signal quality index below safety threshold |
| `high_jitter` | Timing jitter exceeds acceptable bounds |
| `missing_calibration` | Calibration not completed |
| `no_validation_report` | No hardware validation report found |
| `validation_failed` | Hardware validation failed |
| `physical_hardware_unvalidated` | Physical device not validated |
| `model_incompatible` | Active model not valid for closed-loop |
| `confidence_low` | Model confidence below threshold |
| `high_uncertainty` | Prediction uncertainty too high |
| `missing_modality` | Required signal modality absent |
| `sensor_dropout` | Sensor connection lost |
| `state_oscillation` | Contradictory state transitions detected |
| `emergency_stop_active` | Emergency stop is active |
| `adaptation_frozen` | Adaptation frozen by operator |
| `shadow_only_mode` | Running in shadow-only mode |
| `closed_loop_env_disabled` | Environment flag not set |
| `real_eeg_closed_loop_disabled` | Real EEG closed-loop disabled for safety |
| `user_manual_override` | Operator manual action |
| `no_data` | No data available |
| `unknown` | Unclassified reason |

---

## Closed-Loop Governance

`backend/app/safety/closed_loop_governance.py` implements a single authoritative function that determines whether closed-loop adaptation is allowed:

```python
evaluate_closed_loop_governance(
    environment_flag=False,          # master switch
    hardware_validated=False,        # physical hardware validated
    signal_quality_ok=False,         # SQI above thresholds
    timing_validated=False,          # jitter/drift acceptable
    calibration_complete=False,      # calibration completed
    shadow_inference_passed=False,   # shadow inference passed
    emergency_stop_active=False,     # emergency stop clear
    adaptation_frozen=False,         # adaptation not frozen
    mode="simulated",                # current operating mode
) -> ClosedLoopGovernanceResult
```

**The default is LOCKED**. The function returns a result with:
- `closed_loop_allowed: false` (by default)
- `lock_reasons: [...]` (human-readable)
- `lock_reason_codes: [...]` (machine-readable)
- `required_unlock_conditions: [...]` (what would be needed)

### Lock conditions (always active by default)

1. `closed_loop_env_disabled` — environment flag `NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED` not set
2. `real_eeg_closed_loop_disabled` — all live EEG modes (`physical_hardware`, `brainflow_physical`, `lsl_live`) are permanently locked in this phase
3. `missing_calibration` — calibration not completed
4. `shadow_only_mode` — shadow inference not passed
5. `low_sqi` — signal quality insufficient
6. `high_jitter` — timing not validated

---

## Safety API

Safety state, timeline, and controls are available via the API:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/v1/safety/state` | GET | Current safety state + governance |
| `/api/v1/safety/timeline` | GET | State transition history |
| `/api/v1/safety/blocked-actions` | GET | Blocked action log |
| `/api/v1/safety/closed-loop` | GET | Closed-loop governance decision |
| `/api/v1/safety/report/latest` | GET | Full audit snapshot |
| `/api/v1/safety/reset` | POST | Reset state machine |
| `/api/v1/safety/freeze` | POST | Freeze adaptation |
| `/api/v1/safety/unfreeze` | POST | Unfreeze adaptation |
| `/api/v1/safety/emergency-stop` | POST | Trigger emergency stop |
| `/api/v1/safety/clear-emergency` | POST | Clear emergency stop |

Legacy runtime control endpoints remain available:
- `POST /api/v1/runtime/emergency-stop`
- `POST /api/v1/runtime/freeze`
- `POST /api/v1/runtime/unfreeze`

---

## Safety Audit Report

```bash
make safety-audit
```

Generates a structured audit report in `reports/safety_audit/{run_id}/`:
- `safety_audit_summary.json` — full JSON audit
- `safety_audit_summary.md` — human-readable summary
- `closed_loop_lock_reasons.json` — governance decision
- `recommendations.md` — next steps
- `state_transitions.csv` — transition history (if runtime available)
- `blocked_actions.csv` — blocked action log (if runtime available)

---

## Hardware Closed-Loop Lock

Hardware closed-loop mode is disabled by default. Record-only validation and shadow inference are the safe intermediate modes.

For LSL streams, discovery, validation, calibration, and shadow inference are allowed. Direct LSL-driven corridor adaptation remains locked unless validation passes and explicit configuration enables it.

For EEG replay over LSL, marker labels are treated as task annotations for validation reports. They are not interpreted as direct mental-state labels, and shadow mode emits zero real adaptation actions.

Event-locked EEG classifiers predict dataset task labels under controlled conditions; they should not be interpreted as general mind-reading models. They remain shadow-only unless a future safety-reviewed protocol explicitly allows more.

For BrainFlow/OpenBCI hardware, only diagnostics, record-only validation, calibration, and shadow inference are allowed by default. Physical EEG must not control the Dream Corridor in this phase, even when validation passes.

**Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present in `reports/hardware_validation/`.**

---

## Noisy Signal Behavior

Low signal quality or confidence should block or freeze adaptation. Hardware validation reports should still be saved when validation fails so the failure is auditable.

---

## Data Lifecycle

Sessions are stored locally as JSONL. Export bundles include session events, summaries, and a disclaimer. Deletion requires explicit confirmation and is restricted to the configured session directory.

---

## Scientific Limits

NeuroVerse estimates cognitive proxies. It is a research prototype, not clinically validated, not a medical device, and not a thought decoder.

---

## Real Public EEG Validation

PhysioNet EEGBCI support is local-first. Use `make physionet-eegbci-config` to create a config for local EDF files, then `make inspect-physionet-eegbci`, `make prepare-physionet-eegbci-events`, and `make train-physionet-eegbci-classifier` when files are present. Downloads happen only with `make physionet-eegbci-download`.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Closed-loop adaptation remains disabled by default.

---

## Future Closed-Loop Requirements

Any future closed-loop experiment would require all of the following:

1. Validated physical hardware (committed real device validation report)
2. Signal quality sustained above safety thresholds
3. Completed calibration procedure
4. Completed shadow inference with acceptable results
5. Timing validation (jitter and drift within bounds)
6. Explicit operator confirmation
7. Environment flag `NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true`
8. Safety review and operator protocol sign-off

None of these conditions are met by default.

---

## Multimodal Fusion v1 Safety Notes

Fusion v1 combines optional EEG, gaze, physiology, behavior, self-report, and
IMAGINA proxy packets through a conservative late-fusion baseline. Multimodal
fusion outputs are experimental proxy estimates, not clinical or unrestricted
mental-state measurements.

Fusion outputs may include proposed Dream Corridor visual mappings, but those
mappings are shadow-only suggestions. They do not execute real EEG adaptation,
do not bypass the Safety Gate, and do not unlock physical hardware workflows.
If uncertainty is high, modality quality is low, or physical hardware evidence
is missing, the fusion safety recommendation is `wait` or `block`.

IMAGINA plugin outputs are experimental imagery-quality proxies, not decoded
thoughts or dreams. Closed-loop from real EEG is disabled by default.
