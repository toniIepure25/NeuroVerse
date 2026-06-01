# Fusion Validation Report

Run ID: `20260601T135441_8ca8f527`
Generated: `2026-06-01T13:54:42.464197+00:00`

> Multimodal fusion outputs are experimental proxy estimates, not clinical or unrestricted mental-state measurements.
> Fusion validation is behavioral testing under simulated conditions. It does not prove accuracy against ground-truth cognitive states.
> Closed-loop from real EEG is disabled by default.

## Summary

- Scenarios tested: 7
- All uncertainty checks passed: ✅
- All safety checks passed: ✅

## Scenario Results

| Scenario | Uncertainty | Confidence | Safety | Missing |
| --- | --- | --- | --- | --- |
| all_modalities | 0.280 | 0.720 | allow_shadow | imagina |
| eeg_only | 0.600 | 0.400 | wait | gaze, physiology, behavior, self_report, imagina |
| no_eeg | 0.360 | 0.640 | allow_shadow | eeg, imagina |
| self_report_only | 0.600 | 0.400 | wait | eeg, gaze, physiology, behavior, imagina |
| low_quality_eeg | 0.302 | 0.698 | wait | imagina |
| contradictory_modalities | 0.280 | 0.720 | allow_shadow | imagina |
| no_imagery_task | 0.280 | 0.720 | allow_shadow | imagina |

## Uncertainty Checks

- ✅ Uncertainty should increase when modalities are missing
- ✅ Low quality EEG should increase uncertainty
- ✅ Confidence should be capped below 0.80 in all_modalities
- ✅ Confidence should be capped below 0.80 in eeg_only
- ✅ Confidence should be capped below 0.80 in no_eeg
- ✅ Confidence should be capped below 0.80 in self_report_only
- ✅ Confidence should be capped below 0.80 in low_quality_eeg
- ✅ Confidence should be capped below 0.80 in contradictory_modalities
- ✅ Confidence should be capped below 0.80 in no_imagery_task
- ✅ No imagery task should not reduce uncertainty compared to all modalities

## Safety Checks

- ✅ All modalities present should allow shadow
- ✅ Self-report only should be conservative (wait or block)
- ✅ EEG only with 4+ missing modalities should be conservative
- ✅ proxy_only_estimate should be in reason codes for all_modalities
- ✅ proxy_only_estimate should be in reason codes for eeg_only
- ✅ proxy_only_estimate should be in reason codes for no_eeg
- ✅ proxy_only_estimate should be in reason codes for self_report_only
- ✅ proxy_only_estimate should be in reason codes for low_quality_eeg
- ✅ proxy_only_estimate should be in reason codes for contradictory_modalities
- ✅ proxy_only_estimate should be in reason codes for no_imagery_task
