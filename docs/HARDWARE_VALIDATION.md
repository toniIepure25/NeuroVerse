# Hardware Validation

NeuroVerse uses a staged hardware safety path:

1. Simulator mode.
2. Adapter diagnostics.
3. Record-only hardware validation.
4. Timestamp, channel, and SQI report.
5. Baseline calibration.
6. Shadow inference without corridor adaptation.
7. Closed-loop hardware mode only after validation passes and explicit configuration enables it.

Hardware closed-loop adaptation is disabled by default.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

## Record-Only Mode

Validation sessions record windows and compute diagnostics without sending adaptation actions to the Dream Corridor. This is the correct first step for BrainFlow/OpenBCI, LSL, CSV replay, or XDF replay sources.

## Timing Diagnostics

Validation reports include:

- expected and observed sampling rate;
- sampling drift percentage;
- timestamp jitter mean, p95, and max;
- gap count;
- duplicate timestamp count.

## Channel Mapping

Profiles live under `configs/hardware/` and define channel index, name, modality, semantic role, and required modalities. Duplicate indices, unknown modalities, and missing required modalities fail validation.

## Calibration

Calibration creates session-local proxy baselines. These are not clinical measurements and should not be generalized across participants or hardware setups.

## Shadow Mode

Shadow mode computes features, state proxy estimates, safety decisions, and would-be actions without adapting the corridor. Use it before real hardware closed-loop experiments.

## Closed-Loop Criteria

Closed-loop hardware adaptation should remain locked unless:

- dependency and adapter diagnostics pass;
- channel mapping validates;
- timing diagnostics pass;
- SQI is adequate;
- calibration exists;
- shadow inference is reviewed;
- `NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true` is set intentionally.

## Commands

```bash
make validate-synthetic-hardware
make calibration-synthetic
make shadow-synthetic
```

For LSL streaming validation:

```bash
make lsl-stream-demo
make discover-lsl
make validate-lsl-demo
make calibration-lsl-demo
make shadow-lsl-demo
```

For BrainFlow/OpenBCI validation:

```bash
make discover-brainflow-devices
make validate-brainflow-synthetic
make calibration-brainflow-synthetic
make shadow-brainflow-synthetic
make validate-openbci-cyton PORT=/dev/ttyUSB0
make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0
```

BrainFlow SyntheticBoard is generated data for adapter validation. Physical
OpenBCI trials require an explicit port and remain record-only. Hardware
validation confirms stream quality and software integration; it does not
validate clinical or unrestricted mental-state inference.

The first physical EEG protocol is an eyes-open / eyes-closed alpha-reactivity
sanity check. It is record-only and writes reports under
`reports/hardware_trials/`. Eyes-open / eyes-closed alpha reactivity is a sanity
check for EEG signal behavior, not a medical test.

For event-locked EEG replay over LSL:

```bash
make eeg-lsl-replay-demo
make eeg-lsl-live-suite
```

This uses an MNE-compatible fixture by default and can replay local EDF/BDF/FIF/GDF files when provided. Marker labels are task annotations or fixture events, not decoded mental content.

Real hardware should go through the same protocol with explicit local configuration.
