"""Registry of predefined NeuroVerse experiment protocols."""

from __future__ import annotations

from app.protocols.models import (
    ProtocolDefinition,
    ProtocolMode,
    ProtocolStepDefinition,
)

# ---------------------------------------------------------------------------
#  Protocol definitions
# ---------------------------------------------------------------------------

SYNTHETIC_DEMO_PROTOCOL = ProtocolDefinition(
    protocol_id="synthetic_demo_protocol",
    title="Synthetic Demo Protocol",
    description=(
        "End-to-end demonstration using the built-in biosignal simulator. "
        "Validates the full pipeline from simulated data through safety-gated "
        "adaptation in shadow mode. No hardware required."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="validate_simulator",
            title="Validate Simulator Pipeline",
            description="Run hardware validation using the built-in simulator adapter.",
            action="internal_function",
            command="validate_brainflow_synthetic",
            produces_artifact="reports/hardware_validation/*simulator*.json",
        ),
        ProtocolStepDefinition(
            step_id="run_calibration",
            title="Run Calibration (Simulator)",
            description="Collect baseline cognitive-proxy metrics from simulated signals.",
            action="internal_function",
            command="run_calibration_simulator",
            produces_artifact="reports/calibration/*calibration*.json",
        ),
        ProtocolStepDefinition(
            step_id="run_shadow",
            title="Run Shadow Inference (Simulator)",
            description=(
                "Run model inference over simulated data in shadow-only mode (no adaptation)."
            ),
            action="internal_function",
            command="run_shadow_simulator",
            produces_artifact="reports/shadow/*shadow*.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit",
            description="Aggregate evidence and generate a structured safety audit report.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary to reports/protocol_runs/.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/hardware_validation/*simulator*.json",
        "reports/calibration/*calibration*.json",
        "reports/shadow/*shadow*.json",
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "shadow_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "Simulated biosignals do not reflect real neural dynamics. "
        "Results are valid for pipeline validation only."
    ),
    estimated_duration_seconds=30,
    tags=["simulator", "demo", "shadow", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


EEG_LSL_REPLAY_SHADOW_PROTOCOL = ProtocolDefinition(
    protocol_id="eeg_lsl_replay_shadow_protocol",
    title="EEG LSL Replay — Shadow Inference Protocol",
    description=(
        "Replay real PhysioNet EEG data as an LSL stream, validate timing/SQI, "
        "calibrate, and run shadow inference with an event-locked classifier. "
        "Requires pylsl installed and a running EEG replay streamer."
    ),
    mode=ProtocolMode.REPLAY,
    steps=[
        ProtocolStepDefinition(
            step_id="start_eeg_replay_stream",
            title="Start EEG LSL Replay Stream",
            description="Start the EEG LSL replay streamer in a separate terminal.",
            action="manual_command_required",
            command="make eeg-lsl-replay-demo",
            notes="Run this in a separate terminal before proceeding.",
        ),
        ProtocolStepDefinition(
            step_id="validate_lsl_replay",
            title="Validate EEG LSL Replay Stream",
            description="Validate LSL timing, jitter, and marker alignment.",
            action="subprocess_script",
            command="make validate-eeg-lsl-demo",
            produces_artifact="reports/hardware_validation/*lsl*.json",
        ),
        ProtocolStepDefinition(
            step_id="calibrate_from_replay",
            title="Calibrate from LSL Replay",
            description="Collect calibration baseline from the EEG replay stream.",
            action="subprocess_script",
            command="make calibration-eeg-lsl-demo",
            produces_artifact="reports/calibration/*lsl*.json",
        ),
        ProtocolStepDefinition(
            step_id="run_shadow_inference",
            title="Run Shadow Inference (LSL Replay)",
            description="Run shadow inference over the replayed EEG stream. No adaptation actions.",
            action="subprocess_script",
            command="make shadow-eeg-lsl-demo",
            produces_artifact="reports/shadow/*lsl*.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit",
            description="Aggregate evidence and generate a structured safety audit.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/hardware_validation/*lsl*.json",
        "reports/calibration/*lsl*.json",
        "reports/shadow/*lsl*.json",
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "shadow_only", "pylsl_installed"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "LSL replay uses real EEG data from PhysioNet (controlled lab recordings). "
        "Shadow mode emits no real adaptation actions. "
        "Event-locked classifiers predict controlled task labels, not general mental states."
    ),
    estimated_duration_seconds=120,
    tags=["lsl", "replay", "shadow", "eeg", "physionet"],
    supports_auto_run=True,
    auto_run_policy="until_manual_step",
    reviewer_demo_recommended=False,
)


BRAINFLOW_SYNTHETIC_SHADOW_PROTOCOL = ProtocolDefinition(
    protocol_id="brainflow_synthetic_shadow_protocol",
    title="BrainFlow Synthetic Board — Shadow Protocol",
    description=(
        "Use the BrainFlow SyntheticBoard to validate the hardware ingestion "
        "pipeline without a physical device. Runs calibration and shadow inference "
        "on synthetic EEG data. Confirms BrainFlow integration and safety gating."
    ),
    mode=ProtocolMode.BRAINFLOW_SYNTHETIC,
    steps=[
        ProtocolStepDefinition(
            step_id="validate_brainflow_synthetic",
            title="Validate BrainFlow SyntheticBoard",
            description="Run hardware validation using BrainFlow SyntheticBoard (board_id=-1).",
            action="internal_function",
            command="validate_brainflow_synthetic",
            produces_artifact="reports/hardware_validation/*brainflow*.json",
        ),
        ProtocolStepDefinition(
            step_id="run_calibration",
            title="Run Calibration (BrainFlow Synthetic)",
            description="Collect baseline metrics from BrainFlow SyntheticBoard.",
            action="internal_function",
            command="run_calibration_brainflow",
            produces_artifact="reports/calibration/*brainflow*.json",
        ),
        ProtocolStepDefinition(
            step_id="run_shadow",
            title="Run Shadow Inference (BrainFlow Synthetic)",
            description="Run shadow inference over BrainFlow SyntheticBoard data. No adaptation.",
            action="internal_function",
            command="run_shadow_brainflow",
            produces_artifact="reports/shadow/*brainflow*.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit",
            description="Aggregate evidence and generate a structured safety audit.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/hardware_validation/*brainflow*.json",
        "reports/calibration/*brainflow*.json",
        "reports/shadow/*brainflow*.json",
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "shadow_only", "brainflow_installed"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "BrainFlow SyntheticBoard generates synthetic signals — not real EEG. "
        "Validates software integration only, not clinical performance. "
        "Physical OpenBCI/Galea hardware remains unvalidated."
    ),
    estimated_duration_seconds=45,
    tags=["brainflow", "synthetic", "shadow", "no_physical_device"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


PHYSICAL_OPENBCI_TRIAL_PROTOCOL = ProtocolDefinition(
    protocol_id="physical_openbci_trial_protocol",
    title="Physical OpenBCI Trial Protocol",
    description=(
        "Full trial protocol for a physically connected OpenBCI Cyton or Ganglion board. "
        "Requires explicit serial PORT and a connected device. "
        "Runs eyes-open/eyes-closed alpha reactivity, calibration, and shadow inference. "
        "Closed-loop adaptation is NOT enabled — all inference is shadow-only."
    ),
    mode=ProtocolMode.PHYSICAL_HARDWARE,
    required_inputs=["PORT", "PROFILE_ID"],
    steps=[
        ProtocolStepDefinition(
            step_id="discover_device",
            title="Discover Serial Device",
            description="List available serial ports to identify the OpenBCI board.",
            action="subprocess_script",
            command="make discover-brainflow-devices",
        ),
        ProtocolStepDefinition(
            step_id="validate_openbci_record_only",
            title="Validate OpenBCI (Record-Only)",
            description=(
                "Run hardware validation in record-only mode. "
                "Requires PORT=/dev/ttyUSB0 or equivalent."
            ),
            action="manual_command_required",
            command="make validate-openbci-cyton PORT=<PORT>",
            required_inputs=["PORT"],
            produces_artifact="reports/hardware_validation/*brainflow*.json",
        ),
        ProtocolStepDefinition(
            step_id="alpha_reactivity_trial",
            title="Eyes-Open / Eyes-Closed Alpha Reactivity",
            description=(
                "Record eyes-open and eyes-closed conditions to measure alpha reactivity. "
                "This is a sanity check, not a medical test."
            ),
            action="manual_command_required",
            command="make physical-eeg-trial-openbci-cyton PORT=<PORT>",
            required_inputs=["PORT"],
            produces_artifact="reports/hardware_trials/*/physical_eeg_trial_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="run_calibration",
            title="Run Calibration (Physical Board)",
            description="Collect calibration baseline from the physical board.",
            action="manual_command_required",
            command="make calibration-openbci-cyton PORT=<PORT>",
            required_inputs=["PORT"],
            produces_artifact="reports/calibration/*brainflow*.json",
        ),
        ProtocolStepDefinition(
            step_id="run_shadow",
            title="Run Shadow Inference (Physical Board)",
            description=(
                "Run shadow inference over the physical board stream. "
                "Real adaptation actions are blocked — this is shadow-only."
            ),
            action="manual_command_required",
            command="make shadow-openbci-cyton PORT=<PORT>",
            required_inputs=["PORT"],
            produces_artifact="reports/shadow/*brainflow*.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit",
            description="Aggregate evidence and generate a structured safety audit.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/hardware_validation/*brainflow*.json",
        "reports/hardware_trials/*/physical_eeg_trial_summary.json",
        "reports/calibration/*brainflow*.json",
        "reports/shadow/*brainflow*.json",
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=[
        "physical_device_required",
        "closed_loop_locked",
        "shadow_only",
        "record_only_hardware_validation",
    ],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "Physical OpenBCI/Galea hardware validation confirms stream quality and software "
        "integration; it does not validate clinical or unrestricted mental-state inference. "
        "Eyes-open/eyes-closed alpha reactivity is a sanity check, not a medical test. "
        "Closed-loop adaptation from real EEG is disabled by default and requires "
        "additional safety review, calibration, shadow inference, and operator confirmation."
    ),
    estimated_duration_seconds=300,
    tags=["physical_hardware", "openbci", "alpha_reactivity", "shadow", "record_only"],
    supports_auto_run=False,
    auto_run_policy="disabled",
    reviewer_demo_recommended=False,
)


SAFETY_AUDIT_ONLY_PROTOCOL = ProtocolDefinition(
    protocol_id="safety_audit_only_protocol",
    title="Safety Audit Protocol",
    description=(
        "Aggregate evidence from existing reports and generate a comprehensive "
        "safety audit. Useful after running individual validation steps or "
        "as a standalone governance check."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="aggregate_evidence",
            title="Aggregate Report Evidence",
            description=(
                "Load and aggregate safety evidence from hardware validation, "
                "calibration, shadow, and LSL validation reports."
            ),
            action="internal_function",
            command="aggregate_evidence",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit",
            description="Generate a structured safety audit report with governance summary.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "This protocol reads existing reports — it does not generate new signal data. "
        "Evidence quality depends on previously run validation, calibration, and shadow steps."
    ),
    estimated_duration_seconds=10,
    tags=["safety", "audit", "governance", "offline", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=False,
)


MULTIMODAL_FUSION_DEMO_PROTOCOL = ProtocolDefinition(
    protocol_id="multimodal_fusion_demo_protocol",
    title="Multimodal Fusion / IMAGINA Proxy Demo",
    description=(
        "Generate a safe simulated multimodal fusion sample, including the IMAGINA "
        "proxy plugin foundation and proposed Dream Corridor shadow mapping. "
        "No physical hardware required."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="generate_demo_fusion_sample",
            title="Generate Demo Fusion Sample",
            description=(
                "Create simulated EEG, gaze, physiology, behavior, and self-report "
                "packets; evaluate late-fusion v1; and write fusion_report artifacts."
            ),
            action="internal_function",
            command="generate_demo_fusion_sample",
            produces_artifact="reports/fusion/*/fusion_report.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Run Safety Governance Check",
            description="Generate a structured safety audit with closed-loop locked.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/fusion/*/fusion_report.json",
        "reports/fusion/*/fusion_report.md",
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "shadow_only", "proxy_estimates_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "Multimodal fusion outputs are experimental proxy estimates, not clinical "
        "or unrestricted mental-state measurements. IMAGINA plugin outputs are "
        "experimental imagery-quality proxies, not decoded thoughts or dreams. "
        "Closed-loop from real EEG is disabled by default."
    ),
    estimated_duration_seconds=12,
    tags=["fusion", "imagina", "simulator", "shadow", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


FUSION_VALIDATION_PROTOCOL = ProtocolDefinition(
    protocol_id="fusion_validation_protocol",
    title="Fusion Validation Protocol",
    description=(
        "Formal behavioral validation of the multimodal fusion engine. "
        "Tests missing modality robustness, uncertainty behavior, safety "
        "recommendation correctness, and modality ablation analysis. "
        "No physical hardware required."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="generate_demo_fusion_packets",
            title="Generate Demo Fusion Packets",
            description="Create simulated multimodal fusion packets for validation.",
            action="internal_function",
            command="generate_demo_fusion_sample",
            produces_artifact="reports/fusion/*/fusion_report.json",
        ),
        ProtocolStepDefinition(
            step_id="calibrate_fusion",
            title="Calibrate Fusion",
            description="Create a fusion calibration profile from demo packets.",
            action="internal_function",
            command="calibrate_fusion",
            produces_artifact="reports/fusion_calibration/*/fusion_calibration_profile.json",
        ),
        ProtocolStepDefinition(
            step_id="run_fusion_validation",
            title="Run Fusion Validation",
            description=(
                "Execute the full fusion validation suite: missing modality tests, "
                "uncertainty checks, safety recommendation checks, ablation analysis."
            ),
            action="internal_function",
            command="run_fusion_validation",
            produces_artifact="reports/fusion_validation/*/fusion_validation_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit",
            description="Generate a structured safety audit report.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audit/*/safety_audit_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/fusion/*/fusion_report.json",
        "reports/fusion_calibration/*/fusion_calibration_profile.json",
        "reports/fusion_validation/*/fusion_validation_summary.json",
        "reports/fusion_validation/*/fusion_ablation_table.csv",
        "reports/safety_audit/*/safety_audit_summary.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "shadow_only", "proxy_estimates_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "Fusion validation is behavioral testing under simulated conditions. "
        "It does not prove accuracy against ground-truth cognitive states. "
        "Multimodal fusion outputs are experimental proxy estimates, not clinical "
        "or unrestricted mental-state measurements. "
        "Closed-loop from real EEG is disabled by default."
    ),
    estimated_duration_seconds=20,
    tags=["fusion", "validation", "ablation", "simulator", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


IMAGINA_BRIDGE_VALIDATION_PROTOCOL = ProtocolDefinition(
    protocol_id="imagina_bridge_validation_protocol",
    title="IMAGINA Dataset Bridge Validation",
    description=(
        "Validate the IMAGINA dataset bridge foundation by loading an example "
        "manifest, converting samples to fusion inputs, and running proxy "
        "evaluation. This is NOT a trained IMAGINA model. "
        "No physical hardware required."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="validate_example_imagina_manifest",
            title="Validate Example IMAGINA Manifest",
            description="Load and validate the example IMAGINA dataset manifest.",
            action="internal_function",
            command="validate_imagina_manifest",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="convert_example_sample_to_fusion_input",
            title="Convert Example Sample to Fusion Input",
            description="Convert an example IMAGINA sample to a FusionInput.",
            action="internal_function",
            command="convert_imagina_sample",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="run_imagina_proxy_evaluation",
            title="Run IMAGINA Proxy Evaluation",
            description="Evaluate the converted IMAGINA sample through the fusion engine.",
            action="internal_function",
            command="run_imagina_proxy_evaluation",
            produces_artifact="reports/fusion/*/fusion_report.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write the protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/fusion/*/fusion_report.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "proxy_estimates_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "IMAGINA plugin outputs are experimental imagery-quality proxies, not decoded "
        "thoughts or dreams. The dataset bridge is a data loading interface, not a "
        "trained model. Closed-loop from real EEG is disabled by default."
    ),
    estimated_duration_seconds=10,
    tags=["imagina", "dataset_bridge", "validation", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=False,
)


IMAGINA_V1_BASELINE_PROTOCOL = ProtocolDefinition(
    protocol_id="imagina_v1_baseline_protocol",
    title="Internal IMAGINA Fixture Baseline",
    description=(
        "Validate, prepare, train, evaluate, and integrate the IMAGINA v1 internal fixture fallback baseline model. "
        "Used only for engineering smoke tests and offline demo fallbacks. For scientific research, use the external Imagina modeling repository. "
        "Outputs are safe, proxy-only estimates. No clinical thought reading or real closed-loop EEG adaptation is claimed."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="validate_imagina_fixture_manifest",
            title="Validate Fixture Manifest",
            description="Load and validate the example IMAGINA v1 dataset manifest.",
            action="internal_function",
            command="validate_imagina_fixture_manifest",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="prepare_imagina_fixture_dataset",
            title="Prepare Fixture Dataset",
            description="Extract features, build tables, and prepare validation split indices.",
            action="internal_function",
            command="prepare_imagina_fixture_dataset",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="train_imagina_baseline",
            title="Train Baseline Model",
            description="Train a conservative classification baseline model and register the output.",
            action="internal_function",
            command="train_imagina_baseline",
            produces_artifact="models/imagina_v1_baseline_*/model_card.md",
        ),
        ProtocolStepDefinition(
            step_id="evaluate_imagina_baseline",
            title="Evaluate Model Predictions",
            description="Calculate confusion matrix, macro F1, and leakage-safe indicators.",
            action="internal_function",
            command="evaluate_imagina_baseline",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="run_imagina_proxy_prediction",
            title="Run IMAGINA Proxy Prediction",
            description="Run proxy evaluation in LateFusionV1 utilizing the newly trained baseline model.",
            action="internal_function",
            command="run_imagina_proxy_prediction",
            produces_artifact="reports/fusion/*/fusion_report.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit Report",
            description="Run safety compliance verification ensuring closed-loop EEG remains disabled.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audits/*/safety_audit.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write final protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "models/imagina_v1_baseline_*/model_card.md",
        "reports/fusion/*/fusion_report.json",
        "reports/safety_audits/*/safety_audit.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "proxy_estimates_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams. "
        "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements. "
        "Closed-loop from real EEG is disabled by default."
    ),
    estimated_duration_seconds=15,
    tags=["imagina", "baseline_model", "validation", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


EXTERNAL_IMAGINA_INTEGRATION_CHECK_PROTOCOL = ProtocolDefinition(
    protocol_id="external_imagina_integration_check_protocol",
    title="External IMAGINA Integration Check",
    description=(
        "Detect and scan the external IMAGINA project (at ../Imagina), validate "
        "the filesystem artifact contract, adapt the latest outputs to NeuroVerse fusion packets, "
        "and generate safety audit logs. Ensures proper research/runtime separation of concerns."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="detect_external_imagina_project",
            title="Detect External IMAGINA",
            description="Locate the external Imagina project path and verify signature directories.",
            action="internal_function",
            command="detect_external_imagina_project",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="scan_external_imagina_artifacts",
            title="Scan External Artifacts",
            description="Find latest metrics, model cards, predictions, and session reports recursively.",
            action="internal_function",
            command="scan_external_imagina_artifacts",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="validate_external_imagina_contract",
            title="Validate Contract Compliance",
            description="Ensure metrics or cards are compliant with external Imagina schemas.",
            action="internal_function",
            command="validate_external_imagina_contract",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="convert_latest_external_output_to_fusion_packet",
            title="Convert to Fusion Packet",
            description="Convert latest prediction/report file into a safety-gated ModalityFeaturePacket.",
            action="internal_function",
            command="convert_latest_external_output_to_fusion_packet",
            produces_artifact="reports/fusion/*/fusion_report.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit Report",
            description="Run safety compliance verification ensuring closed-loop EEG remains disabled.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audits/*/safety_audit.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write final protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/fusion/*/fusion_report.json",
        "reports/safety_audits/*/safety_audit.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "proxy_estimates_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "IMAGINA is an external research/modeling project. NeuroVerse is the safety-gated runtime and neuroadaptive interface layer. "
        "IMAGINA outputs are experimental imagery proxy estimates, not decoded thoughts or dreams. "
        "Closed-loop from real EEG is disabled by default."
    ),
    estimated_duration_seconds=5,
    tags=["imagina", "external_integration", "validation", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


EXTERNAL_IMAGINA_EXPORT_IMPORT_PROTOCOL = ProtocolDefinition(
    protocol_id="external_imagina_export_import_protocol",
    title="External IMAGINA Export-Import Protocol",
    description=(
        "Locate, validate, and import standardized Imagina v1 Export Contract packages "
        "into the NeuroVerse safety-gated runtime repository, generating summaries and "
        "converting compliant prediction metrics to late fusion modality feature packets."
    ),
    mode=ProtocolMode.SIMULATED,
    steps=[
        ProtocolStepDefinition(
            step_id="detect_external_imagina_project",
            title="Detect External IMAGINA",
            description="Locate the external Imagina project path and verify signature directories.",
            action="internal_function",
            command="detect_external_imagina_project",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="locate_neuroverse_export_manifest",
            title="Locate Export Manifest",
            description="Locate neuroverse_imagina_export.json package manifest inside Imagina workspace.",
            action="internal_function",
            command="locate_neuroverse_export_manifest",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="validate_export_contract",
            title="Validate Export Contract",
            description="Exhaustively validate manifest schema compliance and safety certifications.",
            action="internal_function",
            command="validate_export_contract",
            produces_artifact=None,
        ),
        ProtocolStepDefinition(
            step_id="import_export_summary",
            title="Import Artifact Package",
            description="Securely copy metadata/reports and reference checkpoints to generate import records.",
            action="internal_function",
            command="import_export_summary",
            produces_artifact="reports/external_imagina_imports/*/import_summary.json",
        ),
        ProtocolStepDefinition(
            step_id="convert_latest_external_output_to_fusion_packet",
            title="Convert to Fusion Packet",
            description="Convert compliant predictions from imported package into a safety-gated ModalityFeaturePacket.",
            action="internal_function",
            command="convert_latest_external_output_to_fusion_packet",
            produces_artifact="reports/fusion/*/fusion_report.json",
        ),
        ProtocolStepDefinition(
            step_id="generate_safety_audit",
            title="Generate Safety Audit Report",
            description="Run safety compliance verification ensuring closed-loop EEG remains disabled.",
            action="internal_function",
            command="generate_safety_audit",
            produces_artifact="reports/safety_audits/*/safety_audit.json",
        ),
        ProtocolStepDefinition(
            step_id="export_report",
            title="Export Protocol Report",
            description="Write final protocol run summary.",
            action="internal_function",
            command="export_protocol_report",
            produces_artifact="reports/protocol_runs/*/protocol_run.json",
        ),
    ],
    generated_artifacts=[
        "reports/external_imagina_imports/*/import_summary.json",
        "reports/fusion/*/fusion_report.json",
        "reports/safety_audits/*/safety_audit.json",
        "reports/protocol_runs/*/protocol_run.json",
    ],
    safety_requirements=["closed_loop_locked", "proxy_estimates_only"],
    closed_loop_allowed_default=False,
    scientific_limitations=(
        "IMAGINA exports are experimental imagery proxy artifacts, not decoded thoughts or dreams. "
        "NeuroVerse validates and consumes IMAGINA exports; it does not train the source-of-truth IMAGINA model. "
        "Closed-loop from real EEG is disabled by default."
    ),
    estimated_duration_seconds=10,
    tags=["imagina", "external_integration", "validation", "contract", "no_hardware"],
    supports_auto_run=True,
    auto_run_policy="full",
    reviewer_demo_recommended=True,
)


# ---------------------------------------------------------------------------
#  Registry
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, ProtocolDefinition] = {
    p.protocol_id: p
    for p in [
        SYNTHETIC_DEMO_PROTOCOL,
        EEG_LSL_REPLAY_SHADOW_PROTOCOL,
        BRAINFLOW_SYNTHETIC_SHADOW_PROTOCOL,
        PHYSICAL_OPENBCI_TRIAL_PROTOCOL,
        SAFETY_AUDIT_ONLY_PROTOCOL,
        MULTIMODAL_FUSION_DEMO_PROTOCOL,
        FUSION_VALIDATION_PROTOCOL,
        IMAGINA_BRIDGE_VALIDATION_PROTOCOL,
        IMAGINA_V1_BASELINE_PROTOCOL,
        EXTERNAL_IMAGINA_INTEGRATION_CHECK_PROTOCOL,
        EXTERNAL_IMAGINA_EXPORT_IMPORT_PROTOCOL,
    ]
}


def list_protocols() -> list[ProtocolDefinition]:
    return list(_REGISTRY.values())


def get_protocol(protocol_id: str) -> ProtocolDefinition | None:
    return _REGISTRY.get(protocol_id)
