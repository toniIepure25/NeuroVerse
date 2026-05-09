# LSL Validation

Lab Streaming Layer (LSL) is NeuroVerse's safest first bridge to real streaming biosignal tools. This workflow validates stream discovery, metadata, timestamps, channel mapping, SQI, calibration, and shadow inference before any closed-loop adaptation is considered.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

## Install Optional Dependency

```bash
make check-hardware-extra
make install-hardware-extra
```

If `pylsl` is missing, all LSL scripts and endpoints fail gracefully with installation instructions.

## Local Synthetic LSL Demo

Terminal 1:

```bash
make lsl-stream-demo
```

Terminal 2:

```bash
make discover-lsl
make validate-lsl-demo
make calibration-lsl-demo
make shadow-lsl-demo
make generate-evidence-pack
make dev
```

Open the frontend Research Panel to inspect discovered streams, metadata, timing diagnostics, validation pass/fail, and the closed-loop safety lock.

## One-Command Live Runtime Suite

When `pylsl` is installed, run:

```bash
make lsl-live-validation-suite
```

The suite starts `scripts/lsl_synthetic_streamer.py` as a subprocess, waits for the
stream to become discoverable, runs record-only validation, calibration, shadow
inference, regenerates the evidence pack, and writes:

```text
reports/lsl_live_validation/<run_id>/
  discovery.json
  validation_report.json
  calibration_report.json
  shadow_report.json
  live_validation_summary.json
  live_validation_summary.md
  streamer.log
```

If `pylsl` is unavailable, the suite exits cleanly with the hardware-extra install hint.

## What The Synthetic Stream Is

`scripts/lsl_synthetic_streamer.py` creates a simulated EEG-like LSL stream named `NeuroVerseSyntheticEEG`. It is useful for validating real streaming infrastructure without claiming real EEG or clinical signal quality.

Optional marker output emits phase labels:

- `BASELINE`
- `FOCUS_RISE`
- `WORKLOAD`
- `RELAXATION`
- `IMAGERY`
- `NOISY`
- `RECOVERY`
- `END`

## Validation Reports

LSL validation writes reports under `reports/hardware_validation/` with:

- stream metadata;
- expected and observed sample rate;
- drift percent;
- jitter p50/p95/p99/max;
- timestamp monotonicity;
- gap and duplicate counts;
- optional clock offset estimate;
- timing quality classification: `excellent`, `acceptable`, `warning`, or `failed`;
- channel mapping status;
- marker stream summary;
- SQI summary;
- closed-loop allowed status.

Closed-loop remains locked by default.

## Real Hardware Path

OpenBCI, Galea, or other BCI hardware should first publish to LSL using their standard tooling. NeuroVerse then follows the same record-only protocol:

1. Discover stream.
2. Inspect metadata.
3. Validate channel profile.
4. Record-only timing/SQI validation.
5. Baseline calibration.
6. Shadow inference.
7. Human review.
8. Explicitly enabled closed-loop mode only after validation passes.

NeuroVerse is a research prototype, not clinically validated, not a medical device, and not a thought decoder.

## EEG Replay Over LSL

For event-locked EEG replay, use the MNE-backed streamer:

```bash
make eeg-lsl-replay-demo
make eeg-lsl-live-suite
```

The fixture mode emits a 10-channel EEG-like stream plus `Markers` labels such
as `BASELINE`, `LEFT_HAND_IMAGERY`, `RIGHT_HAND_IMAGERY`, `REST`, and
`NOISY_SEGMENT`. Reports include marker alignment, channel mapping, timing,
SQI, and artifact proxy summaries. See `docs/REAL_EEG_LSL_REPLAY.md`.
