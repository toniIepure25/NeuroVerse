# NeuroVerse Safety Audit Report

**Run ID:** `20260601T134815_73442219`  
**Generated:** 2026-06-01T13:48:15.964600+00:00

> Closed-loop from real EEG is disabled by default. Hardware validation confirms stream quality and software integration; it does not validate clinical or unrestricted mental-state inference. The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

---

## 1. Current Safety State

- **State:** `NO_DATA`
- **Label:** No Data
- **Severity:** `info`
- **Description:** No biosignal data is available.

---

## 2. Closed-Loop Governance

**Closed-loop allowed:** `False`

**Lock reasons:**
- Real EEG closed-loop adaptation is disabled by default.

**Required unlock conditions:**
- Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.

---

## 3. Runtime Evidence Summary

| Field | Value |
| --- | --- |
| validation_report_present | True |
| validation_passed | True |
| adapter | brainflow |
| brainflow_synthetic_validated | True |
| lsl_synthetic_validated | False |
| lsl_replay_validated | False |
| physical_hardware_validated | False |
| signal_quality_ok | True |
| signal_quality_source | hardware_validation |
| latest_sqi_mean | None |
| best_sqi_mean | 0.9312 |
| timing_ok | True |
| latest_jitter_p95_ms | None |
| best_jitter_p95_ms | 0.0 |
| calibration_complete | True |
| shadow_inference_passed | True |
| shadow_real_actions_emitted | 0 |
| lsl_live_validation_passed | False |

**Evidence sources:**
- `brainflow_synthetic:20260601T130224Z_brainflow_validation.json`
- `simulator:20260601T130224Z_simulator_validation.json`
- `brainflow_synthetic:20260601T122151Z_brainflow_validation.json`
- `simulator:20260601T122150Z_simulator_validation.json`
- `brainflow_synthetic:20260601T114843Z_brainflow_validation.json`
- `calibration:20260601T130225Z_brainflow_calibration.json`
- `shadow:20260601T130226Z_shadow.json`

**Evidence warnings:**
- ⚠ Latest hardware validation report failed; using older valid report for evidence. Failed: 20260601T130235Z_brainflow_validation.json

**Report paths:**
- `latest_validation_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/hardware_validation/20260601T130235Z_brainflow_validation.json`
- `latest_valid_validation_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/hardware_validation/20260601T130224Z_brainflow_validation.json`
- `latest_failed_validation_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/hardware_validation/20260601T130235Z_brainflow_validation.json`
- `latest_calibration_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/calibration/20260601T130225Z_brainflow_calibration.json`
- `latest_shadow_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/shadow/20260601T130226Z_shadow.json`
- `latest_physical_trial_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/hardware_trials/20260508T202435Z_physical_eeg_trial/physical_eeg_trial_summary.json`
- `safety_audit_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/safety_audit/20260601T130239_eb3bfc21/safety_audit_summary.json`

---

## 4. Issues
- No LSL live validation report found or validation failed.

---

## 5. Timeline Summary

- Transitions recorded: 1
- Blocked actions recorded: 0

---

## 6. Steps Required for Any Future Closed-Loop Experiment
1. Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.