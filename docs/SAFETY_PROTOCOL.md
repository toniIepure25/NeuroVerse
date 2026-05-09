# Safety Protocol

NeuroVerse prioritizes user control, signal reliability, and conservative adaptation.

## Runtime Controls

- Emergency stop: `POST /api/v1/runtime/emergency-stop`
- Freeze adaptation: `POST /api/v1/runtime/freeze`
- Unfreeze adaptation: `POST /api/v1/runtime/unfreeze`

Emergency stop freezes adaptation and logs an auditable runtime event. Unfreeze is blocked while an emergency stop is active or when the latest safety decision blocks adaptation.

## Hardware Closed-Loop Lock

Hardware closed-loop mode is disabled by default. Record-only validation and shadow inference are the safe intermediate modes.

For LSL streams, discovery, validation, calibration, and shadow inference are allowed. Direct LSL-driven corridor adaptation remains locked unless validation passes and explicit configuration enables it.

For EEG replay over LSL, marker labels are treated as task annotations for validation reports. They are not interpreted as direct mental-state labels, and shadow mode emits zero real adaptation actions.

Event-locked EEG classifiers predict dataset task labels under controlled conditions; they should not be interpreted as general mind-reading models. They remain shadow-only unless a future safety-reviewed protocol explicitly allows more.

For BrainFlow/OpenBCI hardware, only diagnostics, record-only validation,
calibration, and shadow inference are allowed by default. Physical EEG must not
control the Dream Corridor in this phase, even when validation passes.

Hardware validation confirms stream quality and software integration; it does
not validate clinical or unrestricted mental-state inference.

Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal
behavior, not a medical test. It may support first-pass hardware sanity review,
but it must not be treated as a diagnosis or a general mental-state decoder.

## Noisy Signal Behavior

Low signal quality or confidence should block or freeze adaptation. Hardware validation reports should still be saved when validation fails so the failure is auditable.

## Data Lifecycle

Sessions are stored locally as JSONL. Export bundles include session events, summaries, and a disclaimer. Deletion requires explicit confirmation and is restricted to the configured session directory.

## Scientific Limits

NeuroVerse estimates cognitive proxies. It is a research prototype, not clinically validated, not a medical device, and not a thought decoder.


## Real Public EEG Validation

PhysioNet EEGBCI support is local-first. Use `make physionet-eegbci-config` to create a config for local EDF files, then `make inspect-physionet-eegbci`, `make prepare-physionet-eegbci-events`, and `make train-physionet-eegbci-classifier` when files are present. Downloads happen only with `make physionet-eegbci-download`.

Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Closed-loop adaptation remains disabled by default.
