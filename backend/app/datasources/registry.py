"""Static data source definitions."""

from __future__ import annotations

from app.datasources.models import DataSourceDefinition

DATA_SOURCE_DEFINITIONS: list[DataSourceDefinition] = [
    DataSourceDefinition(
        source_id="simulator",
        title="Built-in Simulator",
        mode="simulator",
        description="No-hardware source for the default reviewer demo and protocol run.",
        recommended_protocol_id="synthetic_demo_protocol",
        commands=[
            "POST /api/v1/fusion/demo-sample",
            "make protocol-run-demo",
            "make generate-evidence-pack",
            "make static-evidence-bake",
        ],
        what_it_proves=[
            "End-to-end protocol orchestration, report generation, and safety locks work.",
            "The platform can be reviewed without hardware or external datasets.",
            "Multimodal Fusion v1 can generate simulated proxy evidence safely.",
        ],
        what_it_does_not_prove=[
            "Real EEG neural dynamics.",
            "Physical device integration or clinical performance.",
            "Decoded thoughts, dreams, or clinical mental-state measurements.",
        ],
        limitations=[
            "Signals are synthesized.",
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics.",
        ],
    ),
    DataSourceDefinition(
        source_id="physionet_eegbci_replay",
        title="PhysioNet EEGBCI EDF Replay",
        mode="public_eeg_replay",
        description="Local public EEG dataset files used for replay and benchmark workflows.",
        recommended_protocol_id="eeg_lsl_replay_shadow_protocol",
        commands=[
            "make physionet-eegbci-download",
            "make prepare-raw-epochs-small",
            "make raw-bci-benchmark-small",
        ],
        what_it_proves=[
            "Controlled public EEG task-label workflows can be prepared and benchmarked.",
            "Replay/shadow paths can operate on provenance-tracked dataset artifacts.",
        ],
        what_it_does_not_prove=[
            "Unrestricted mental-state inference.",
            "Online performance on a new live user.",
        ],
        limitations=[
            "PhysioNet task labels are controlled experimental proxy labels.",
            "Replay is not equivalent to live physical hardware validation.",
        ],
    ),
    DataSourceDefinition(
        source_id="lsl_stream",
        title="LSL Stream",
        mode="lsl_stream",
        description="Local Lab Streaming Layer EEG stream, usually from a replay streamer.",
        recommended_protocol_id="eeg_lsl_replay_shadow_protocol",
        commands=[
            "make eeg-lsl-replay-demo",
            "make validate-eeg-lsl-demo",
            "make shadow-eeg-lsl-demo",
        ],
        what_it_proves=[
            "Stream discovery, timing, jitter, marker alignment, and shadow ingestion "
            "can run locally.",
        ],
        what_it_does_not_prove=[
            "That a detected stream contains high-quality human EEG.",
            "Closed-loop control from real EEG.",
        ],
        limitations=[
            "Requires pylsl and a local stream; multicast discovery can fail in "
            "restricted networks.",
            "Closed-loop from real EEG is disabled by default.",
        ],
    ),
    DataSourceDefinition(
        source_id="brainflow_synthetic",
        title="BrainFlow SyntheticBoard",
        mode="brainflow_synthetic",
        description=(
            "BrainFlow synthetic board path for hardware-stack integration without a device."
        ),
        recommended_protocol_id="brainflow_synthetic_shadow_protocol",
        commands=[
            "make validate-brainflow-synthetic",
            "make calibration-brainflow-synthetic",
            "make shadow-brainflow-synthetic",
        ],
        what_it_proves=[
            "BrainFlow acquisition code can be exercised through the NeuroVerse hardware layer.",
            "Calibration and shadow inference can run without physical hardware.",
        ],
        what_it_does_not_prove=[
            "Real OpenBCI physical validation.",
            "Clinical or unrestricted mental-state inference.",
        ],
        limitations=[
            "BrainFlow SyntheticBoard is not real OpenBCI physical validation.",
            "Synthetic signals are not real EEG.",
        ],
    ),
    DataSourceDefinition(
        source_id="openbci_cyton",
        title="OpenBCI Cyton",
        mode="physical_openbci",
        description="Prepared record-only physical OpenBCI Cyton path via BrainFlow.",
        recommended_protocol_id="physical_openbci_trial_protocol",
        required_inputs=["PORT", "PROFILE_ID"],
        commands=[
            "make discover-brainflow-devices",
            "make validate-openbci-cyton PORT=/dev/ttyUSB0",
            "make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0",
        ],
        what_it_proves=[
            "Only a real passing report can prove stream quality and software integration.",
        ],
        what_it_does_not_prove=[
            "Clinical validity.",
            "Unrestricted mental-state inference.",
            "Closed-loop adaptation from real EEG.",
        ],
        limitations=[
            "OpenBCI/Galea physical validation remains unperformed unless a real "
            "device report exists.",
            "Hardware validation confirms stream quality and software integration; "
            "it does not validate clinical or unrestricted mental-state inference.",
            "Closed-loop from real EEG is disabled by default.",
        ],
    ),
    DataSourceDefinition(
        source_id="openbci_ganglion",
        title="OpenBCI Ganglion",
        mode="physical_openbci",
        description="Prepared record-only physical OpenBCI Ganglion path via BrainFlow.",
        recommended_protocol_id="physical_openbci_trial_protocol",
        required_inputs=["PORT", "PROFILE_ID"],
        commands=[
            "make discover-brainflow-devices",
            "make validate-openbci-ganglion PORT=/dev/ttyUSB0",
            "make physical-eeg-trial-openbci-ganglion PORT=/dev/ttyUSB0",
        ],
        what_it_proves=[
            "Only a real passing report can prove stream quality and software integration.",
        ],
        what_it_does_not_prove=[
            "Clinical validity.",
            "Unrestricted mental-state inference.",
            "Closed-loop adaptation from real EEG.",
        ],
        limitations=[
            "OpenBCI/Galea physical validation remains unperformed unless a real "
            "device report exists.",
            "Hardware validation confirms stream quality and software integration; "
            "it does not validate clinical or unrestricted mental-state inference.",
            "Closed-loop from real EEG is disabled by default.",
        ],
    ),
]


def list_data_source_definitions() -> list[DataSourceDefinition]:
    return DATA_SOURCE_DEFINITIONS


def get_data_source_definition(source_id: str) -> DataSourceDefinition | None:
    return next(
        (source for source in DATA_SOURCE_DEFINITIONS if source.source_id == source_id),
        None,
    )
