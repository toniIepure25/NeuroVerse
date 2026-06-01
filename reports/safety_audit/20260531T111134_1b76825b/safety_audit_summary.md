# NeuroVerse Safety Audit Report

**Run ID:** `20260531T111134_1b76825b`  
**Generated:** 2026-05-31T11:11:34.802814+00:00

> Closed-loop from real EEG is disabled by default. Hardware validation confirms stream quality and software integration; it does not validate clinical or unrestricted mental-state inference. The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

---

## 1. Current Safety State

- **State:** `NO_DATA`  
- **Label:** No Data  
- **Severity:** `info`  
- **Description:** No biosignal data is available.

**Allowed actions:**
- `configure`
- `connect_hardware`
- `start_simulator`

**Blocked actions:**
- `adapt`
- `calibrate`
- `shadow_inference`

---

## 2. Closed-Loop Governance

**Closed-loop allowed:** `False`

**Lock reasons:**
- Real EEG closed-loop adaptation is disabled by default.
- Signal quality is insufficient.
- Calibration has not been completed.
- Shadow inference has not been completed.
- Timing validation has not been completed.

**Required unlock conditions:**
- Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.
- Achieve sustained signal quality above safety thresholds.
- Complete calibration procedure.
- Complete shadow inference with acceptable results.
- Complete timing validation with acceptable jitter and drift.

---

## 3. Artifact Status

| Artifact | Found | Passed/Status |
| --- | --- | --- |
| hardware_validation | yes | False |
| calibration | yes | None |
| shadow | yes | True |
| physical_eeg_trial | yes | — |
| lsl_live_validation | yes | False |
| raw_bci_benchmark | yes | — |

---

## 4. Issues
- Hardware validation has not passed.

---

## 5. Timeline Summary

- Transitions recorded: 1
- Blocked actions recorded: 0

---

## 6. Steps Required for Any Future Closed-Loop Experiment
1. Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.
1. Achieve sustained signal quality above safety thresholds.
1. Complete calibration procedure.
1. Complete shadow inference with acceptable results.
1. Complete timing validation with acceptable jitter and drift.