# Hardware Safety Protocol

NeuroVerse uses a staged path: simulator, adapter diagnostics, record-only
hardware validation, timestamp/channel/SQI report, baseline calibration, shadow
inference, and only then explicitly enabled closed-loop mode.

Hardware closed-loop adaptation is disabled by default.
