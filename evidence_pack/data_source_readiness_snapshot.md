# Data Source Readiness Snapshot

**Generated:** 2026-06-01T22:59:40.683681+00:00

Static evidence is a baked snapshot, not live runtime evidence.
Closed-loop from real EEG is disabled by default.
BrainFlow SyntheticBoard is not real OpenBCI physical validation.
OpenBCI/Galea physical validation remains unperformed unless a real device report exists.

| Source | Availability | Recommended Protocol | Missing Requirements |
| --- | --- | --- | --- |
| Built-in Simulator | `available` | `synthetic_demo_protocol` | None |
| PhysioNet EEGBCI EDF Replay | `available` | `eeg_lsl_replay_shadow_protocol` | Start LSL replay stream before protocol execution. |
| LSL Stream | `partially_available` | `eeg_lsl_replay_shadow_protocol` | No EEG LSL stream detected. |
| BrainFlow SyntheticBoard | `available` | `brainflow_synthetic_shadow_protocol` | None |
| OpenBCI Cyton | `unavailable` | `physical_openbci_trial_protocol` | No serial OpenBCI device detected.; Explicit PORT input required.; Operator confirmation required. |
| OpenBCI Ganglion | `unavailable` | `physical_openbci_trial_protocol` | No serial OpenBCI device detected.; Explicit PORT input required.; Operator confirmation required. |
