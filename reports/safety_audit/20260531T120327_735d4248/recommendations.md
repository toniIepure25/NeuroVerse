# Safety Governance Recommendations

Based on the current runtime evidence:

- **Run LSL validation:** `make lsl-live-validation-suite` to validate streaming quality.

- **Do not enable real EEG closed-loop** without completing all validation, calibration, and shadow inference steps with a physically validated device.

- Physical OpenBCI/Galea hardware remains unvalidated unless a real device report exists in `reports/hardware_validation/` with physical_device_detected=True.