# Hardware Integration

NeuroVerse is local-first and simulator-first by default. Hardware adapters are designed as an upgrade path for real biosignal acquisition, not as a claim that hardware is connected or validated today.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.

## Supported Modes

- `simulator`: deterministic multimodal synthetic EEG, physiology, and gaze-like signals for demos and CI.
- `brainflow`: BrainFlow/OpenBCI adapter with SyntheticBoard validation and explicit physical-board configuration.
- `lsl`: Lab Streaming Layer adapter shell for timestamped streams when `pylsl` is installed.
- `csv_replay`: local CSV replay for fixture and dataset-derived windows.
- `xdf_replay`: optional XDF replay path when `pyxdf` is installed and stream mapping is configured.

## Diagnostics

```bash
curl http://localhost:8000/api/v1/acquisition/status
```

The response reports the active adapter, optional dependency availability, adapter capabilities, and the latest recoverable error.

## Validation Before Closed Loop

Run record-only validation before any real hardware experiment:

```bash
make validate-synthetic-hardware
```

For real BrainFlow or LSL sources, use the same staged protocol: diagnostics, record-only validation, channel mapping validation, timestamp/SQI report, calibration, shadow inference, and only then explicitly enabled closed-loop mode. Hardware closed-loop adaptation is disabled by default.

## BrainFlow / OpenBCI

Example configs live in:

- `configs/hardware/openbci_cyton.example.yaml`
- `configs/hardware/openbci_ganglion.example.yaml`

These files intentionally avoid user-specific serial ports. To use a real device, install BrainFlow in your local environment, copy an example config, set the board and transport fields, and test the adapter before starting an adaptive session.

NeuroVerse does not auto-connect to OpenBCI hardware. That is a safety choice:
the project should fail clearly when dependencies or device configuration are
missing. Start with the synthetic BrainFlow board:

```bash
make validate-brainflow-synthetic
make calibration-brainflow-synthetic
make shadow-brainflow-synthetic
```

Then use a physical board only with an explicit port:

```bash
make discover-brainflow-devices
make validate-openbci-cyton PORT=/dev/ttyUSB0
make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0
```

Hardware validation confirms stream quality and software integration; it does
not validate clinical or unrestricted mental-state inference.

The physical EEG trial protocol records eyes-open and eyes-closed segments,
compares alpha-band power as a signal sanity check, generates calibration and
shadow-only reports, and emits zero real adaptation actions.

## Lab Streaming Layer

The LSL adapter checks for `pylsl` and exposes stream selection fields. Real deployment should pin stream name/type, channel order, sampling rate expectations, and timestamp handling before feeding data into closed-loop adaptation.

For a local streaming validation demo, run `make lsl-stream-demo` in one terminal and
`make validate-lsl-demo` in another. The demo stream is simulated and validates LSL
transport, timestamps, metadata, channel mapping, and reports without claiming real EEG.

For real EEG replay over LSL, run `make eeg-lsl-replay-demo` or provide a local
MNE-compatible file to `scripts/eeg_lsl_replay_streamer.py --input-file`. This
streams EEG samples and marker annotations through LSL for event-locked
record-only validation, calibration, and shadow inference.

## XDF Replay

XDF replay is optional. Real XDF files may contain multiple streams with different clocks and channel layouts. Configure stream-to-modality mapping before treating replayed data as NeuroVerse input.

## Signal Quality And Safety

Real EEG quality depends on electrode contact, impedance, motion artifacts, environment, and participant comfort. NeuroVerse safety gates should block or freeze adaptation when signal quality or model confidence is low.

## Privacy

Raw biosignals can be sensitive biometric data. Keep datasets local, avoid cloud upload by default, and document retention/deletion practices for each study or demo.

## Scientific Limits

NeuroVerse estimates cognitive proxies from simulated or dataset-derived biosignals. It is a research prototype, not clinically validated, not a medical device, and not a thought decoder.
