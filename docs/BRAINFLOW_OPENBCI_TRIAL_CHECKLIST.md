# BrainFlow / OpenBCI Trial Checklist

Use this only after the LSL live validation path is working locally.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics.

## Preflight

- Install optional hardware dependencies with `make install-hardware-extra`.
- Confirm `make check-hardware-extra` reports BrainFlow availability.
- Confirm `NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=false`.
- Use record-only validation first; do not start physical closed-loop adaptation.

## Hardware Setup

- Verify board model: Cyton, Ganglion, or another BrainFlow-supported board.
- Confirm serial/Bluetooth permissions and port names.
- Use a local config based on `configs/hardware/openbci_cyton_eeg.example.yaml`
  or `configs/hardware/openbci_ganglion_eeg.example.yaml`.
- Document channel order, reference, sample rate, and disabled channels.

## Validation Protocol

1. Adapter diagnostics.
2. Record-only stream validation.
3. Timestamp jitter and sampling-rate report.
4. Channel mapping validation.
5. SQI summary and artifact review.
6. Baseline calibration.
7. Shadow inference.
8. Human review.
9. Explicit closed-loop enablement only after validation passes.

## Stop Criteria

- Dropped/gapped samples.
- Unexpected channel count or order.
- Low SQI or unstable electrodes.
- Participant discomfort.
- Any uncertainty about whether the stream is mapped correctly.

NeuroVerse is a research prototype, not clinically validated, not a medical
device, and not a thought decoder.
