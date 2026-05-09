# Real EEG Replay Over LSL

This workflow replays an MNE-compatible EEG recording through Lab Streaming Layer (LSL), emits task markers on a separate marker stream, and runs NeuroVerse's record-only validation, calibration, and shadow inference pipeline.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

## Purpose

Real EEG replay over LSL is a bridge between synthetic streaming tests and physical hardware trials. It validates:

- stream discovery and metadata inspection;
- EEG channel mapping;
- event marker streaming and alignment;
- sample-rate, jitter, gap, and duplicate timestamp diagnostics;
- SQI and artifact proxy summaries;
- baseline calibration from streamed data;
- shadow inference with zero real adaptation actions.

It is not clinical validation, a motor-imagery decoder, or a medical signal-quality assessment.

## Dependencies

Install optional hardware extras:

```bash
make install-hardware-extra
make check-hardware-extra
```

This enables `pylsl` and MNE in local development. CI does not require a live LSL stream.

## Fixture Mode

Fixture mode creates a small deterministic MNE `RawArray` with 10 EEG-like channels:

```text
Fp1 Fp2 F3 F4 C3 C4 P3 P4 O1 O2
```

It also emits markers:

```text
BASELINE
LEFT_HAND_IMAGERY
RIGHT_HAND_IMAGERY
REST
NOISY_SEGMENT
END
```

Terminal 1:

```bash
make eeg-lsl-replay-demo
```

Terminal 2:

```bash
make validate-eeg-lsl-demo
make calibration-eeg-lsl-demo
make shadow-eeg-lsl-demo
make generate-evidence-pack
```

One-shot suite:

```bash
make eeg-lsl-live-suite
```

Reports are written under:

```text
reports/eeg_lsl_validation/<run_id>/
reports/hardware_validation/
reports/calibration/
reports/shadow/
```

## Local Real File Mode

NeuroVerse can replay local MNE-compatible files without committing datasets to Git:

```bash
python3 scripts/eeg_lsl_replay_streamer.py \
  --input-file /path/to/local_file.edf \
  --stream-name NeuroVerseReplayEEG \
  --marker-stream-name NeuroVerseReplayMarkers \
  --duration 60 \
  --markers
```

Supported formats follow MNE reader support, including EDF/BDF/FIF/GDF where available. If annotations exist, they are replayed as marker labels. If annotations are absent, fixture-style labels are used only as a local demo scaffold.

For PhysioNet Motor Imagery, use a local EDF file:

```bash
make physionet-mi-lsl-replay FILE=/path/to/local_physionet_file.edf
```

NeuroVerse does not auto-download public EEG datasets.

For the full local-first PhysioNet EEGBCI validation workflow, see
`docs/REAL_PUBLIC_EEG_VALIDATION.md`. That path adds dataset inspection,
run-aware `T0`/`T1`/`T2` event mapping, event-locked classifier training, LSL
replay, shadow inference, and evidence reporting while keeping closed-loop
adaptation locked by default.

## Marker Alignment

The validation pipeline attempts to discover `NeuroVerseReplayMarkers`, pull marker samples, and align them to EEG windows by timestamp. Reports include:

- marker stream found;
- marker count;
- marker labels;
- markers per label;
- aligned and unaligned marker counts;
- alignment warnings.

Markers are task labels or fixture labels. They are not decoded mental states.

## SQI And Artifact Summary

EEG replay reports include software diagnostics:

- NaN/Inf counts;
- amplitude range per channel;
- flatline or dropout candidates;
- high-amplitude candidates;
- SQI mean/min/max.

SQI is a software diagnostic proxy, not a clinical quality assessment.

## Closed-Loop Safety

EEG/LSL closed-loop adaptation remains disabled by default. The safe path is:

1. record-only EEG LSL validation;
2. calibration;
3. shadow inference;
4. human review;
5. explicit environment flag only after validation passes.

Shadow inference computes would-be actions and emits zero real adaptation actions.

## Physical Hardware Mapping

A real OpenBCI, Galea, or other BCI device would publish an LSL EEG stream and marker stream using vendor or lab tooling. NeuroVerse would then use the same profile, timing, marker, SQI, calibration, and shadow pipeline before any closed-loop experiment is considered.
