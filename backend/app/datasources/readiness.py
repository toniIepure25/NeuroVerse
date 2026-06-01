"""Data-source readiness checks for setup assistant UI."""

from __future__ import annotations

import importlib.util
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.acquisition.brainflow_adapter import (
    BRAINFLOW_INSTALL_HINT,
    BrainFlowAcquisition,
    discover_brainflow_devices,
)
from app.acquisition.lsl_discovery import PYLSL_INSTALL_HINT, discover_streams, pylsl_available
from app.datasources.models import (
    DataSourceDefinition,
    DataSourceListResponse,
    DataSourcePreflightSummary,
    DataSourceStatus,
)
from app.datasources.registry import get_data_source_definition, list_data_source_definitions
from app.protocols.registry import get_protocol
from app.safety.closed_loop_governance import evaluate_closed_loop_governance
from app.safety.report_status import get_cached_report_evidence

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def list_data_sources(*, force_refresh: bool = False) -> DataSourceListResponse:
    evidence, cache_meta = get_cached_report_evidence(force_refresh=force_refresh)
    evidence_dict = evidence.to_dict()
    sources = [
        _build_status(definition, evidence_dict=evidence_dict, cache_meta=cache_meta)
        for definition in list_data_source_definitions()
    ]
    return DataSourceListResponse(
        generated_at=datetime.now(timezone.utc).isoformat(),
        sources=sources,
    )


def get_data_source(source_id: str, *, force_refresh: bool = False) -> DataSourceStatus | None:
    definition = get_data_source_definition(source_id)
    if definition is None:
        return None
    evidence, cache_meta = get_cached_report_evidence(force_refresh=force_refresh)
    return _build_status(definition, evidence_dict=evidence.to_dict(), cache_meta=cache_meta)


def preflight_data_source(
    source_id: str,
    inputs: dict[str, str] | None = None,
    *,
    force_refresh: bool = False,
) -> DataSourceStatus | None:
    status = get_data_source(source_id, force_refresh=force_refresh)
    if status is None:
        return None
    status.protocol_preflight = _protocol_preflight(
        status.recommended_protocol_id,
        inputs or {},
        status.missing_requirements,
    )
    return status


def _build_status(
    definition: DataSourceDefinition,
    *,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    if definition.source_id == "simulator":
        return _simulator_status(definition, evidence_dict, cache_meta)
    if definition.source_id == "physionet_eegbci_replay":
        return _physionet_status(definition, evidence_dict, cache_meta)
    if definition.source_id == "lsl_stream":
        return _lsl_status(definition, evidence_dict, cache_meta)
    if definition.source_id == "brainflow_synthetic":
        return _brainflow_synthetic_status(definition, evidence_dict, cache_meta)
    if definition.mode == "physical_openbci":
        return _openbci_status(definition, evidence_dict, cache_meta)
    return _base_status(definition, evidence_dict, cache_meta)


def _base_status(
    definition: DataSourceDefinition,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    return DataSourceStatus(
        **definition.model_dump(),
        availability="unknown",
        latest_evidence_paths=_latest_evidence_paths(evidence_dict),
        safety_status=_safety_status(definition.mode, evidence_dict, cache_meta),
        closed_loop_allowed=False,
        physical_hardware_validated=bool(evidence_dict.get("physical_hardware_validated", False)),
        protocol_preflight=_protocol_preflight(definition.recommended_protocol_id, {}, []),
    )


def _simulator_status(
    definition: DataSourceDefinition,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    status = _base_status(definition, evidence_dict, cache_meta)
    status.availability = "available"
    status.can_run_now = True
    status.can_validate_now = True
    status.can_auto_run_protocol = True
    status.installed_dependencies = {"python": True}
    status.detected_resources = {"source": "built_in_simulator"}
    status.next_actions = [
        "Run the synthetic demo protocol.",
        "Bake static evidence for portfolio review.",
    ]
    status.protocol_preflight = _protocol_preflight(definition.recommended_protocol_id, {}, [])
    return status


def _physionet_status(
    definition: DataSourceDefinition,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    status = _base_status(definition, evidence_dict, cache_meta)
    info = _physionet_dataset_info()
    config_exists = bool(info["config_exists"])
    expected = int(info["expected_file_count"])
    found = int(info["existing_file_count"])
    status.installed_dependencies = {"dataset_config": config_exists}
    status.detected_resources = info
    if config_exists and expected > 0 and found == expected:
        status.availability = "available"
        status.can_validate_now = True
        status.can_run_now = False
        status.missing_requirements = ["Start LSL replay stream before protocol execution."]
        status.next_actions = [
            "Run make eeg-lsl-replay-demo in another terminal.",
            "Run preflight for the replay protocol.",
        ]
    elif config_exists and found > 0:
        status.availability = "partially_available"
        status.missing_requirements = [
            f"Only {found}/{expected or '?'} configured EDF files were found.",
            "Run make physionet-eegbci-download to complete the local dataset.",
        ]
        status.next_actions = [
            "Complete dataset download/configuration.",
            "Regenerate evidence pack.",
        ]
    else:
        status.availability = "unavailable"
        status.missing_requirements = [
            "PhysioNet EEGBCI local EDF files not found.",
            "Run make physionet-eegbci-download.",
        ]
        status.next_actions = ["Download/configure PhysioNet EEGBCI files."]
    status.can_auto_run_protocol = False
    status.protocol_preflight = _protocol_preflight(
        definition.recommended_protocol_id, {}, status.missing_requirements
    )
    return status


def _lsl_status(
    definition: DataSourceDefinition,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    status = _base_status(definition, evidence_dict, cache_meta)
    installed = pylsl_available()
    streams: list[dict[str, Any]] = []
    warnings: list[str] = []
    if installed:
        try:
            streams = discover_streams(stream_type="EEG", timeout=0.25)
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"LSL discovery failed or timed out: {exc}")
    status.installed_dependencies = {"pylsl": installed}
    status.detected_resources = {
        "streams": streams[:5],
        "stream_count": len(streams),
        "warnings": warnings,
    }
    if not installed:
        status.availability = "unavailable"
        status.missing_requirements = [PYLSL_INSTALL_HINT]
        status.next_actions = [
            'Install hardware extras: cd backend && pip install -e ".[hardware]"'
        ]
    elif streams:
        status.availability = "available"
        status.can_validate_now = True
        status.can_run_now = True
        status.next_actions = ["Run LSL validation or replay shadow protocol preflight."]
    else:
        status.availability = "partially_available"
        status.can_validate_now = False
        status.missing_requirements = ["No EEG LSL stream detected."]
        status.next_actions = [
            "Start make eeg-lsl-replay-demo in another terminal.",
            "Refresh data sources.",
        ]
    status.can_auto_run_protocol = False
    status.protocol_preflight = _protocol_preflight(
        definition.recommended_protocol_id, {}, status.missing_requirements
    )
    return status


def _brainflow_synthetic_status(
    definition: DataSourceDefinition,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    status = _base_status(definition, evidence_dict, cache_meta)
    installed = BrainFlowAcquisition.is_available()
    status.installed_dependencies = {"brainflow": installed}
    status.detected_resources = {
        "board_id": -1,
        "board_name": "BrainFlow SyntheticBoard",
        "physical_or_synthetic": "synthetic",
    }
    if installed:
        status.availability = "available"
        status.can_run_now = True
        status.can_validate_now = True
        status.can_auto_run_protocol = True
        status.next_actions = [
            "Run BrainFlow SyntheticBoard protocol preflight.",
            "Run protocol from Protocol Center.",
        ]
    else:
        status.availability = "unavailable"
        status.missing_requirements = [BRAINFLOW_INSTALL_HINT]
        status.next_actions = [
            'Install hardware extras: cd backend && pip install -e ".[hardware]"'
        ]
    status.protocol_preflight = _protocol_preflight(
        definition.recommended_protocol_id, {}, status.missing_requirements
    )
    return status


def _openbci_status(
    definition: DataSourceDefinition,
    evidence_dict: dict[str, Any],
    cache_meta: dict[str, Any],
) -> DataSourceStatus:
    status = _base_status(definition, evidence_dict, cache_meta)
    brainflow_installed = BrainFlowAcquisition.is_available()
    pyserial_installed = importlib.util.find_spec("serial") is not None
    discovery = discover_brainflow_devices()
    devices = discovery.get("devices", []) if isinstance(discovery, dict) else []
    physical_validated = bool(evidence_dict.get("physical_hardware_validated", False))
    status.installed_dependencies = {
        "brainflow": brainflow_installed,
        "pyserial": pyserial_installed,
    }
    status.detected_resources = {
        "serial_devices": devices,
        "serial_device_count": len(devices),
        "warnings": discovery.get("warnings", []) if isinstance(discovery, dict) else [],
        "physical_hardware_validated": physical_validated,
    }
    status.physical_hardware_validated = physical_validated
    status.can_auto_run_protocol = False
    status.can_run_now = False
    status.can_validate_now = brainflow_installed and bool(devices)
    status.missing_requirements = []
    if not brainflow_installed:
        status.missing_requirements.append(BRAINFLOW_INSTALL_HINT)
    if not devices:
        status.missing_requirements.append("No serial OpenBCI device detected.")
    status.missing_requirements.extend(
        ["Explicit PORT input required.", "Operator confirmation required."]
    )
    if brainflow_installed and devices:
        status.availability = "partially_available"
        port = str(devices[0].get("device") or "/dev/ttyUSB0")
        status.next_actions = [
            f"Run record-only validation with PORT={port}.",
            "Review generated physical hardware report before making any claims.",
        ]
    else:
        status.availability = "unavailable"
        status.next_actions = [
            "Connect/pair the OpenBCI board.",
            "Run make discover-brainflow-devices.",
            "Run record-only validation with an explicit PORT.",
        ]
    status.closed_loop_allowed = False
    status.protocol_preflight = _protocol_preflight(
        definition.recommended_protocol_id,
        {},
        status.missing_requirements,
    )
    return status


def _protocol_preflight(
    protocol_id: str,
    inputs: dict[str, str],
    source_missing_requirements: list[str],
) -> DataSourcePreflightSummary | None:
    protocol = get_protocol(protocol_id)
    if protocol is None:
        return None
    missing_inputs = [name for name in protocol.required_inputs if not inputs.get(name)]
    warnings = list(source_missing_requirements)
    can_start = not missing_inputs and not any("not found" in item.lower() for item in warnings)
    can_auto_run = (
        can_start and protocol.supports_auto_run and protocol.auto_run_policy != "disabled"
    )
    if protocol.mode.value == "physical_hardware":
        can_auto_run = False
        if "Explicit PORT input required." not in warnings and not inputs.get("PORT"):
            warnings.append("Explicit PORT input required.")
    return DataSourcePreflightSummary(
        protocol_id=protocol.protocol_id,
        protocol_title=protocol.title,
        can_start=can_start,
        can_auto_run=can_auto_run,
        missing_inputs=missing_inputs,
        warnings=warnings,
        auto_run_policy=protocol.auto_run_policy,
    )


def _latest_evidence_paths(evidence: dict[str, Any]) -> dict[str, str | None]:
    return {
        "validation": evidence.get("latest_valid_validation_report_path")
        or evidence.get("latest_validation_report_path"),
        "calibration": evidence.get("latest_calibration_report_path"),
        "shadow": evidence.get("latest_shadow_report_path"),
        "physical_trial": evidence.get("latest_physical_trial_report_path"),
        "safety_audit": evidence.get("safety_audit_report_path"),
    }


def _safety_status(
    mode: str,
    evidence: dict[str, Any],
    cache_meta: dict[str, Any],
) -> dict[str, Any]:
    governance_mode = "physical_hardware" if mode == "physical_openbci" else mode
    gov = evaluate_closed_loop_governance(
        environment_flag=False,
        hardware_validated=bool(evidence.get("physical_hardware_validated", False)),
        signal_quality_ok=bool(evidence.get("signal_quality_ok", False)),
        timing_validated=bool(evidence.get("timing_ok", False)),
        calibration_complete=bool(evidence.get("calibration_complete", False)),
        shadow_inference_passed=bool(evidence.get("shadow_inference_passed", False)),
        mode=governance_mode,
    )
    return {
        "closed_loop_allowed": False,
        "governance": gov.to_dict(),
        "evidence_cache": cache_meta,
        "physical_hardware_validated": bool(evidence.get("physical_hardware_validated", False)),
    }


def _physionet_dataset_info() -> dict[str, Any]:
    config_path = ROOT / "configs" / "datasets" / "physionet_eegbci_local.yaml"
    result: dict[str, Any] = {
        "config_path": str(config_path.relative_to(ROOT)),
        "config_exists": config_path.exists(),
        "local_root": None,
        "expected_file_count": 0,
        "existing_file_count": 0,
        "sample_missing_files": [],
    }
    if not config_path.exists():
        return result
    text = config_path.read_text(encoding="utf-8")
    local_root_match = re.search(r"^local_root:\s*(.+)$", text, flags=re.MULTILINE)
    local_root = local_root_match.group(1).strip() if local_root_match else "data/external/eegbci"
    result["local_root"] = local_root
    file_paths = re.findall(r"^\s*path:\s*(.+\.edf)\s*$", text, flags=re.MULTILINE)
    result["expected_file_count"] = len(file_paths)
    existing = 0
    missing: list[str] = []
    for rel in file_paths:
        candidate = ROOT / local_root / rel.strip()
        if candidate.exists():
            existing += 1
        elif len(missing) < 5:
            missing.append(str(candidate.relative_to(ROOT)))
    result["existing_file_count"] = existing
    result["sample_missing_files"] = missing
    return result
