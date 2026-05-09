# First Physical EEG Trial

NeuroVerse supports a conservative first-headset protocol for BrainFlow/OpenBCI
boards: serial discovery, explicit device selection, record-only eyes-open and
eyes-closed recording, alpha-band sanity reporting, calibration, and shadow-only
inference.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics.

Hardware validation confirms stream quality and software integration; it does
not validate clinical or unrestricted mental-state inference.

Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal
behavior, not a medical test.

## Device Discovery

```bash
make discover-brainflow-devices
```

If `pyserial` is installed, the report includes serial descriptions,
manufacturer, VID/PID, and likely OpenBCI hints. Without `pyserial`, NeuroVerse
falls back to path-only discovery using `/dev/ttyUSB*`, `/dev/ttyACM*`,
`/dev/cu.*`, and `/dev/rfcomm*`.

## Synthetic Protocol Smoke Test

```bash
make physical-eeg-trial-synthetic
```

This exercises the protocol machinery with BrainFlow SyntheticBoard. It is not
real EEG and should not be presented as physiological alpha evidence.

## OpenBCI Cyton

```bash
make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0
```

Before recording, verify participant comfort, electrode placement, reference,
ground, cable strain relief, and board battery/USB/Bluetooth state. Keep the
first trial short and record-only.

## OpenBCI Ganglion

```bash
make physical-eeg-trial-openbci-ganglion PORT=/dev/ttyUSB0
```

Ganglion has fewer channels, so posterior alpha interpretation depends heavily
on actual electrode placement.

## Protocol

1. Setup and safety check.
2. Device connection test through BrainFlow.
3. Eyes-open record-only segment.
4. Eyes-closed record-only segment.
5. Optional shadow-only segment.
6. Reports and evidence pack generation.

Reports are written under `reports/hardware_trials/{trial_id}/`:

- `physical_eeg_trial_summary.json/md`
- `raw_validation_report.json`
- `alpha_reactivity_report.json/md`
- `calibration_report.json`
- `shadow_report.json`

## Interpreting Alpha Reactivity

The alpha report compares 8-12 Hz power in eyes-closed versus eyes-open phases.
It reports aggregate and posterior-channel ratios when channels such as O1, O2,
Oz, Pz, P3, P4, PO7, or PO8 are available.

Statuses use modest engineering language:

- `visible_reactivity`: alpha ratio is clearly higher in eyes-closed data.
- `weak_reactivity`: a small increase is present.
- `inconclusive`: the expected pattern is not clear.
- `noisy_signal`: artifacts dominate the report.
- `insufficient_data`: required phases or samples are missing.

These statuses are not normal/abnormal clinical labels.

## Safety

The trial emits zero real adaptation actions. Closed-loop remains disabled even
when validation passes. Any future physical closed-loop experiment requires a
separate safety-reviewed protocol, explicit environment flags, operator
confirmation, and emergency controls.
