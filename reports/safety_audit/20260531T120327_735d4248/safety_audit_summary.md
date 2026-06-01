# NeuroVerse Safety Audit Report

**Run ID:** `20260531T120327_735d4248`  
**Generated:** 2026-05-31T12:03:27.512659+00:00

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
- Timing validation has not been completed.

**Required unlock conditions:**
- Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.
- Complete timing validation with acceptable jitter and drift.

---

## 3. Runtime Evidence Summary

| Field | Value |
| --- | --- |
| validation_report_present | True |
| validation_passed | False |
| adapter | lsl |
| brainflow_synthetic_validated | False |
| lsl_synthetic_validated | False |
| physical_hardware_validated | False |
| signal_quality_ok | True |
| latest_sqi_mean | None |
| timing_ok | False |
| latest_jitter_p95_ms | None |
| calibration_complete | True |
| shadow_inference_passed | True |
| shadow_real_actions_emitted | 0 |
| lsl_live_validation_passed | False |

**Report paths:**
- `latest_validation_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/hardware_validation/20260531T120306Z_lsl_validation.json`
- `latest_calibration_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/calibration/20260531T120304Z_brainflow_calibration.json`
- `latest_shadow_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/shadow/20260531T120305Z_shadow.json`
- `latest_physical_trial_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/hardware_trials/20260508T202435Z_physical_eeg_trial/physical_eeg_trial_summary.json`
- `safety_audit_report_path`: `/home/tonystark/Desktop/NeuroVerse/reports/safety_audit/20260531T111134_1b76825b/safety_audit_summary.json`

---

## 4. Issues
- Hardware validation report found but did not pass.
- No LSL live validation report found or validation failed.

---

## 5. Timeline Summary

- Transitions recorded: 1
- Blocked actions recorded: 0

---

## 6. Steps Required for Any Future Closed-Loop Experiment
1. Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.
1. Complete timing validation with acceptable jitter and drift.