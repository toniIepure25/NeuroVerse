from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.acquisition.brainflow_adapter import (
    BRAINFLOW_INSTALL_HINT,
    BrainFlowAcquisition,
    detect_serial_ports,
    discover_brainflow_devices,
)
from app.acquisition.channel_mapping import get_profile, list_profiles, validate_profile
from app.acquisition.diagnostics import acquisition_status, select_adapter, test_adapter
from app.acquisition.lsl_adapter import LSLAcquisition
from app.acquisition.lsl_discovery import PYLSL_INSTALL_HINT, inspect_stream, pylsl_available
from app.acquisition.validation import (
    get_validation_report,
    list_validation_reports,
    run_hardware_validation,
    validation_status,
)

router = APIRouter(prefix="/api/v1/acquisition", tags=["acquisition"])
_ACTIVE_BRAINFLOW: BrainFlowAcquisition | None = None


class AcquisitionSelectRequest(BaseModel):
    adapter: str = Field(..., description="simulator, brainflow, lsl, csv_replay, or xdf_replay")
    config: dict[str, Any] = Field(default_factory=dict)


class ValidationStartRequest(BaseModel):
    adapter: str = "simulator"
    adapter_type: str | None = None
    stream_name: str | None = None
    stream_type: str | None = None
    source_id: str | None = None
    marker_stream_name: str | None = None
    marker_stream_type: str | None = "Markers"
    board_id: int | str | None = None
    serial_port: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)
    profile_id: str | None = None
    duration_seconds: float = Field(default=2.0, ge=0.1, le=30.0)
    record_windows: bool = True
    run_sqi: bool = True
    run_shadow_inference: bool = False


class LslSelectRequest(BaseModel):
    stream_name: str | None = None
    stream_type: str | None = "EEG"
    source_id: str | None = None
    profile_id: str | None = None
    timeout_seconds: float = Field(default=1.0, ge=0.0, le=10.0)


class BrainFlowRequest(BaseModel):
    profile_id: str | None = "brainflow_synthetic_eeg"
    board_id: int | str | None = None
    serial_port: str | None = None
    ip_address: str | None = None
    mac_address: str | None = None
    timeout: int | None = None
    start_stream: bool = False


@router.get("/status")
async def api_acquisition_status() -> dict[str, Any]:
    return acquisition_status()


@router.post("/test")
async def api_acquisition_test(request: AcquisitionSelectRequest | None = None) -> dict[str, Any]:
    if request is None:
        return await test_adapter()
    return await test_adapter(request.adapter, request.config)


@router.post("/select")
async def api_acquisition_select(request: AcquisitionSelectRequest) -> dict[str, Any]:
    try:
        return select_adapter(request.adapter, request.config)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/lsl/status")
async def api_lsl_status() -> dict[str, Any]:
    adapter = LSLAcquisition()
    return {
        "pylsl_available": pylsl_available(),
        "install_hint": None if pylsl_available() else PYLSL_INSTALL_HINT,
        "selected_stream": adapter.status().get("selected_stream"),
        "active_stream_status": adapter.status(),
        "last_error": adapter.status().get("last_error"),
    }


@router.get("/lsl/streams")
async def api_lsl_streams(
    stream_name: str | None = None,
    stream_type: str | None = None,
    source_id: str | None = None,
    timeout_seconds: float = 1.0,
) -> dict[str, Any]:
    if not pylsl_available():
        return {"available": False, "install_hint": PYLSL_INSTALL_HINT, "streams": []}
    try:
        return {
            "available": True,
            "streams": LSLAcquisition.discover_streams(
                name=stream_name,
                stream_type=stream_type,
                source_id=source_id,
                timeout=timeout_seconds,
            ),
        }
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/lsl/streams/{stream_id}/metadata")
async def api_lsl_stream_metadata(stream_id: str, timeout_seconds: float = 1.0) -> dict[str, Any]:
    if not pylsl_available():
        raise HTTPException(status_code=409, detail=PYLSL_INSTALL_HINT)
    try:
        return inspect_stream(stream_id=stream_id, timeout=timeout_seconds)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/brainflow/status")
async def api_brainflow_status() -> dict[str, Any]:
    adapter = _ACTIVE_BRAINFLOW or BrainFlowAcquisition()
    return {
        "brainflow_available": BrainFlowAcquisition.is_available(),
        "install_hint": None if BrainFlowAcquisition.is_available() else BRAINFLOW_INSTALL_HINT,
        "active_board": adapter.status(),
        "serial_ports": detect_serial_ports(),
        "last_error": adapter.status().get("last_error"),
    }


@router.get("/brainflow/profiles")
async def api_brainflow_profiles() -> list[dict[str, Any]]:
    return [
        profile
        for profile in list_profiles()
        if profile.get("adapter_type") == "brainflow"
    ]


@router.get("/brainflow/devices")
async def api_brainflow_devices() -> dict[str, Any]:
    return discover_brainflow_devices()


@router.post("/brainflow/test")
async def api_brainflow_test(request: BrainFlowRequest) -> dict[str, Any]:
    if not BrainFlowAcquisition.is_available():
        raise HTTPException(status_code=409, detail=BRAINFLOW_INSTALL_HINT)
    config = _brainflow_config(request)
    adapter = BrainFlowAcquisition(config)
    if not request.start_stream:
        return {"ok": True, "diagnostics": adapter.diagnostics(), "stream_opened": False}
    try:
        await adapter.start()
        status = adapter.status()
        await adapter.stop()
        return {"ok": True, "status": status, "stream_opened": True}
    except Exception as exc:
        await adapter.stop()
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/brainflow/select")
async def api_brainflow_select(request: BrainFlowRequest) -> dict[str, Any]:
    return select_adapter("brainflow", _brainflow_config(request))


@router.post("/brainflow/start")
async def api_brainflow_start(request: BrainFlowRequest) -> dict[str, Any]:
    global _ACTIVE_BRAINFLOW
    if not BrainFlowAcquisition.is_available():
        raise HTTPException(status_code=409, detail=BRAINFLOW_INSTALL_HINT)
    if _ACTIVE_BRAINFLOW and _ACTIVE_BRAINFLOW.is_running():
        return {"status": "already_running", "board": _ACTIVE_BRAINFLOW.status()}
    _ACTIVE_BRAINFLOW = BrainFlowAcquisition(_brainflow_config(request))
    try:
        await _ACTIVE_BRAINFLOW.start()
        return {"status": "running", "board": _ACTIVE_BRAINFLOW.status()}
    except Exception as exc:
        await _ACTIVE_BRAINFLOW.stop()
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/brainflow/stop")
async def api_brainflow_stop() -> dict[str, Any]:
    global _ACTIVE_BRAINFLOW
    if _ACTIVE_BRAINFLOW:
        await _ACTIVE_BRAINFLOW.stop()
    status = _ACTIVE_BRAINFLOW.status() if _ACTIVE_BRAINFLOW else BrainFlowAcquisition().status()
    _ACTIVE_BRAINFLOW = None
    return {"status": "stopped", "board": status}


@router.post("/lsl/select")
async def api_lsl_select(request: LslSelectRequest) -> dict[str, Any]:
    if not pylsl_available():
        raise HTTPException(status_code=409, detail=PYLSL_INSTALL_HINT)
    try:
        stream = inspect_stream(
            name=request.stream_name,
            stream_type=request.stream_type,
            source_id=request.source_id,
            timeout=request.timeout_seconds,
        )
        return select_adapter(
            "lsl",
            {
                "stream_name": stream.get("name"),
                "stream_type": stream.get("type"),
                "source_id": stream.get("source_id"),
                "profile_id": request.profile_id,
            },
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/profiles")
async def api_acquisition_profiles() -> list[dict[str, Any]]:
    return list_profiles()


@router.get("/profiles/{profile_id}")
async def api_acquisition_profile(profile_id: str) -> dict[str, Any]:
    try:
        return get_profile(profile_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Acquisition profile not found")


@router.post("/profiles/validate")
async def api_validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    return validate_profile(profile)


@router.post("/validation/start")
async def api_validation_start(request: ValidationStartRequest) -> dict[str, Any]:
    try:
        return await run_hardware_validation(
            adapter=request.adapter_type or request.adapter,
            config={
                **request.config,
                "adapter_type": request.adapter_type or request.adapter,
                "stream_name": request.stream_name,
                "stream_type": request.stream_type,
                "source_id": request.source_id,
                "marker_stream_name": request.marker_stream_name,
                "marker_stream_type": request.marker_stream_type,
                "board_id": request.board_id,
                "serial_port": request.serial_port,
            },
            profile_id=request.profile_id,
            duration_seconds=request.duration_seconds,
            record_windows=request.record_windows,
            run_sqi=request.run_sqi,
            run_shadow_inference=request.run_shadow_inference,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Profile not found: {exc}") from exc


@router.post("/validation/stop")
async def api_validation_stop() -> dict[str, Any]:
    status = validation_status()
    return {**status, "status": "stopped"}


@router.get("/validation/status")
async def api_validation_status() -> dict[str, Any]:
    return validation_status()


@router.get("/validation/reports")
async def api_validation_reports() -> list[dict[str, Any]]:
    return list_validation_reports()


@router.get("/validation/reports/{report_id}")
async def api_validation_report(report_id: str) -> dict[str, Any]:
    try:
        return get_validation_report(report_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Validation report not found")


def _brainflow_config(request: BrainFlowRequest) -> dict[str, Any]:
    profile = get_profile(request.profile_id) if request.profile_id else {}
    return {
        **profile,
        "profile_id": request.profile_id,
        "board_id": request.board_id if request.board_id is not None else profile.get("board_id"),
        "serial_port": request.serial_port or profile.get("serial_port"),
        "ip_address": request.ip_address or profile.get("ip_address"),
        "mac_address": request.mac_address or profile.get("mac_address"),
        "timeout": request.timeout or profile.get("timeout"),
    }
