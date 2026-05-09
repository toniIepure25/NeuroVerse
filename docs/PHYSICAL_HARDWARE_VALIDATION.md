# Physical Hardware Validation

NeuroVerse supports a staged hardware path for BrainFlow/OpenBCI and LSL-capable
EEG devices. The goal is record-only validation, calibration, and shadow
inference before any future safety-reviewed closed-loop experiment.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics.

Hardware validation confirms stream quality and software integration; it does
not validate clinical or unrestricted mental-state inference.

## Supported Modes

- BrainFlow SyntheticBoard: local adapter validation with generated data.
- OpenBCI Cyton: explicit serial-port trial through BrainFlow.
- OpenBCI Ganglion: explicit serial-port trial through BrainFlow.
- LSL EEG devices: validated through the existing LSL stream workflow.

## Synthetic BrainFlow Trial

```bash
make check-hardware-extra
make validate-brainflow-synthetic
make calibration-brainflow-synthetic
make shadow-brainflow-synthetic
make generate-evidence-pack
```

This proves that the BrainFlow adapter can open a board, read timestamped EEG
windows, compute timing/SQI/artifact diagnostics, write calibration baselines,
and run shadow inference with zero real adaptation actions. SyntheticBoard data
is generated data, not real EEG.

## OpenBCI Cyton Trial

1. Connect the board according to OpenBCI guidance.
2. Identify the serial port, for example `/dev/ttyUSB0` or `/dev/ttyACM0`.
3. Keep the participant at rest for the first trial.
4. Run:

```bash
make validate-openbci-cyton PORT=/dev/ttyUSB0
make calibration-openbci-cyton PORT=/dev/ttyUSB0
make shadow-openbci-cyton PORT=/dev/ttyUSB0
```

If no board is connected or the port is wrong, the commands should fail with a
structured BrainFlow error and still leave closed-loop disabled.

## OpenBCI Ganglion Trial

```bash
make validate-openbci-ganglion PORT=/dev/ttyUSB0
```

Ganglion support is configured as a record-only validation path. Verify the
montage, reference, and BrainFlow connection fields before interpreting reports.

## Reports

Validation reports are written to `reports/hardware_validation/` and include:

- board id and board name;
- synthetic vs physical status;
- serial port redacted/safely represented;
- expected and observed sampling rate;
- jitter p50/p95/p99;
- gaps and duplicate timestamps;
- channel mapping status;
- SQI and artifact proxy summaries;
- warnings, recommendations, and closed-loop lock status.

Calibration reports are written to `reports/calibration/`. Shadow reports are
written to `reports/shadow/`.

## First EEG Alpha Trial

For a modest first physiological sanity check, run the eyes-open / eyes-closed
protocol:

```bash
make discover-brainflow-devices
make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0
```

The protocol writes `reports/hardware_trials/{trial_id}/` with timing, SQI,
artifact, alpha reactivity, calibration, and shadow-only reports. A synthetic
workflow is available for software validation:

```bash
make physical-eeg-trial-synthetic
```

Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal
behavior, not a medical test.

## Safety Rules

- Physical EEG never controls the Dream Corridor by default.
- Emergency stop and freeze controls remain available in the frontend.
- SQI is a software diagnostic proxy, not clinical signal quality.
- Shadow mode may compute would-be actions, but emits zero real actions.
- Any future closed-loop hardware experiment requires validation, calibration,
  shadow review, explicit environment flags, and human operator approval.

## Troubleshooting

- `brainflow` missing: run `make install-hardware-extra`.
- No serial port: check USB/Bluetooth pairing and OS permissions.
- Timing gaps: reduce other system load, use a shorter USB path, and repeat
  record-only validation.
- Bad channels: check electrode contact, reference, impedance, and cable motion.
- Low SQI: treat the trial as unusable until the hardware setup is improved.
