"""Fusion API routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException

from app.fusion.adapters.registry import get_adapter_statuses, list_adapters
from app.fusion.calibration import (
    calibrate_from_packets,
    save_calibration_report,
)
from app.fusion.imagina_dataset_bridge import validate_imagina_manifest
from app.fusion.late_fusion import LateFusionV1
from app.fusion.modality_registry import MODALITIES, available_modality_ids
from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    CORRIDOR_LIMITATION,
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    FusionInput,
    FusionOutput,
    FusionStatusResponse,
    ModalityFeaturePacket,
)
from app.fusion.report import generate_fusion_report
from app.fusion.validation import run_fusion_validation

router = APIRouter(prefix="/api/v1/fusion", tags=["fusion"])
_FUSION = LateFusionV1()
_LATEST_OUTPUT: FusionOutput | None = None
_LATEST_REPORT: dict[str, Any] | None = None
_LATEST_VALIDATION: dict[str, Any] | None = None
_LATEST_CALIBRATION: dict[str, Any] | None = None


@router.get("/status", response_model=FusionStatusResponse)
async def fusion_status() -> FusionStatusResponse:
    return FusionStatusResponse(
        available_modalities=available_modality_ids(),
        plugin_status={
            "imagina_proxy_v1": {
                "available": True,
                "not_decoded_content": True,
                "limitations": [IMAGINA_LIMITATION],
            }
        },
        closed_loop_allowed=False,
        limitations=[
            PROXY_LIMITATION,
            CORRIDOR_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            IMAGINA_LIMITATION,
        ],
        provenance={
            "modalities": {key: info.__dict__ for key, info in MODALITIES.items()},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


@router.post("/evaluate", response_model=FusionOutput)
async def evaluate_fusion(payload: FusionInput) -> FusionOutput:
    global _LATEST_OUTPUT
    output = _FUSION.evaluate(payload)
    _LATEST_OUTPUT = output
    return output


@router.get("/latest")
async def latest_fusion() -> dict[str, Any]:
    if _LATEST_OUTPUT is None:
        raise HTTPException(status_code=404, detail="No fusion output has been generated yet")
    return {
        "output": _LATEST_OUTPUT,
        "report": _LATEST_REPORT,
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "limitations": [PROXY_LIMITATION, CLOSED_LOOP_LIMITATION],
    }


@router.post("/demo-sample")
async def demo_sample() -> dict[str, Any]:
    global _LATEST_OUTPUT, _LATEST_REPORT
    payload = build_demo_fusion_input()
    output = _FUSION.evaluate(payload)
    report = generate_fusion_report(payload, output)
    _LATEST_OUTPUT = output
    _LATEST_REPORT = report
    return {
        "input": payload,
        "output": output,
        "report_paths": {
            "json": report["json_path"],
            "markdown": report["markdown_path"],
        },
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "limitations": [
            PROXY_LIMITATION,
            CORRIDOR_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            IMAGINA_LIMITATION,
        ],
    }


# ---------------------------------------------------------------------------
#  New endpoints: adapters, calibration, validation, IMAGINA
# ---------------------------------------------------------------------------


@router.get("/adapters")
async def fusion_adapters() -> dict[str, Any]:
    """List all registered fusion sensor adapters and their status."""
    return {
        "adapters": list_adapters(),
        "adapter_statuses": get_adapter_statuses(),
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "limitations": [
            PROXY_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            "Simulated adapters do not represent real hardware sensors.",
        ],
    }


@router.post("/calibrate")
async def fusion_calibrate() -> dict[str, Any]:
    """Run fusion calibration from demo packets and save profile."""
    global _LATEST_CALIBRATION
    payload = build_demo_fusion_input()
    profile = calibrate_from_packets(
        payload.packets, source="api_demo_calibration"
    )
    report = save_calibration_report(profile)
    _LATEST_CALIBRATION = report
    return {
        "profile_id": profile.profile_id,
        "source": profile.source,
        "report_paths": {
            "json": report["json_path"],
            "markdown": report["markdown_path"],
        },
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "limitations": [
            PROXY_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            "Calibration profile is derived from simulated demo packets.",
        ],
        "provenance": profile.provenance,
    }


@router.post("/validate")
async def fusion_validate() -> dict[str, Any]:
    """Run the full fusion validation suite."""
    global _LATEST_VALIDATION
    result = run_fusion_validation()
    _LATEST_VALIDATION = result
    return {
        "run_id": result["run_id"],
        "all_checks_passed": result["all_checks_passed"],
        "report_dir": result["report_dir"],
        "artifact_paths": {
            "summary_json": result["summary_json"],
            "summary_md": result["summary_md"],
            "ablation_csv": result["ablation_csv"],
        },
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "limitations": [
            PROXY_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            "Fusion validation is behavioral testing, not accuracy validation.",
        ],
    }


@router.get("/validation/latest")
async def fusion_validation_latest() -> dict[str, Any]:
    """Get the latest fusion validation result."""
    if _LATEST_VALIDATION is None:
        raise HTTPException(
            status_code=404,
            detail="No fusion validation has been run yet. POST /api/v1/fusion/validate first.",
        )
    return {
        "run_id": _LATEST_VALIDATION["run_id"],
        "all_checks_passed": _LATEST_VALIDATION["all_checks_passed"],
        "report_dir": _LATEST_VALIDATION["report_dir"],
        "artifact_paths": {
            "summary_json": _LATEST_VALIDATION["summary_json"],
            "summary_md": _LATEST_VALIDATION["summary_md"],
        },
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
    }


@router.post("/imagina/manifest/validate")
async def imagina_manifest_validate(
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate an IMAGINA dataset manifest.

    Accepts a JSON body with 'manifest_path' (relative to configs/imagina/)
    or validates the example manifest by default.
    """
    manifest_path = "configs/imagina/example_imagina_manifest.json"
    if body and "manifest_path" in body:
        manifest_path = body["manifest_path"]

    result = validate_imagina_manifest(manifest_path)
    return {
        **result,
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "manifest_path": manifest_path,
    }


def build_demo_fusion_input() -> FusionInput:
    """Safe simulated fusion sample for UI demos and protocol execution."""
    return FusionInput(
        session_id="fusion_demo_sample",
        context={
            "protocol_id": "multimodal_fusion_demo_protocol",
            "data_source": "simulator",
            "mode": "simulated",
            "safety_state": "CLOSED_LOOP_LOCKED",
            "imagery_task_active": True,
            "imagery_task_label": "symbolic_object_imagery",
        },
        packets=[
            ModalityFeaturePacket(
                modality_id="eeg",
                source="simulated",
                quality_score=0.78,
                confidence=0.68,
                features={
                    "engagement_index": 0.66,
                    "relaxation_index": 0.48,
                    "alpha_power": 0.58,
                    "beta_power": 0.52,
                    "theta_power": 0.42,
                    "delta_power": 0.26,
                    "fatigue_index": 0.34,
                    "spectral_entropy_proxy": 0.61,
                    "p300_proxy": 0.57,
                },
                limitations=["Simulated EEG proxy features."],
                provenance={"generator": "fusion_demo_sample"},
            ),
            ModalityFeaturePacket(
                modality_id="gaze",
                source="simulated",
                quality_score=0.72,
                confidence=0.64,
                features={
                    "fixation_stability": 0.70,
                    "gaze_dispersion": 0.32,
                    "blink_rate": 0.28,
                    "blink_duration_proxy": 0.30,
                    "pupil_diameter_proxy": 0.46,
                },
                limitations=["Simulated gaze features."],
                provenance={"generator": "fusion_demo_sample"},
            ),
            ModalityFeaturePacket(
                modality_id="physiology",
                source="simulated",
                quality_score=0.70,
                confidence=0.62,
                features={
                    "rmssd_proxy": 0.57,
                    "eda_phasic": 0.34,
                    "stress_index": 0.38,
                    "heart_rate": 0.45,
                },
                limitations=["Simulated physiology features."],
                provenance={"generator": "fusion_demo_sample"},
            ),
            ModalityFeaturePacket(
                modality_id="behavior",
                source="derived",
                quality_score=0.66,
                confidence=0.58,
                features={
                    "task_performance": 0.72,
                    "error_rate": 0.18,
                    "response_variability": 0.30,
                    "task_difficulty": 0.44,
                    "imagery_task_adherence": 0.67,
                },
                limitations=["Derived task behavior proxy features."],
                provenance={"generator": "fusion_demo_sample"},
            ),
            ModalityFeaturePacket(
                modality_id="self_report",
                source="user_input",
                quality_score=0.64,
                confidence=0.56,
                features={
                    "focus": 0.64,
                    "relaxation": 0.52,
                    "workload": 0.43,
                    "stress": 0.35,
                    "fatigue": 0.30,
                    "imagery_vividness": 0.68,
                    "imagery_controllability": 0.58,
                },
                limitations=["Self-report is subjective proxy evidence."],
                provenance={"generator": "fusion_demo_sample"},
            ),
        ],
    )
