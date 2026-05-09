from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import get_engine
from app.api.websocket_manager import manager
from app.core.config import settings
from app.core.runtime_status import runtime_status
from app.core.telemetry import telemetry
from app.inference.model_loader import get_active_model_status

router = APIRouter(prefix="/api")


class RuntimeControlRequest(BaseModel):
    reason: str = Field(default="manual operator request")


@router.get("/v1/runtime/status")
@router.get("/runtime/status")
async def api_runtime_status() -> dict:
    status = runtime_status.snapshot()
    engine = get_engine()
    active = get_active_model_status()
    ws_status = manager.status()
    status["engine_running"] = engine.is_running
    status["engine_session_id"] = engine.session_id
    status["service_status"] = "ok"
    status["backend_version"] = "0.1.0"
    status["environment_mode"] = settings.environment_mode
    status["uptime_seconds"] = telemetry.uptime_seconds
    status["event_counts"] = telemetry.metrics(
        connected_clients=ws_status["connected_clients"],
        tick_rate_hz=settings.tick_rate_hz,
    )
    status["websocket"] = ws_status
    if not engine.is_running:
        status["active_estimator"] = active.get("active_estimator", "heuristic")
        status["active_model_id"] = active.get("model_id")
        status["prediction_semantics"] = active.get("prediction_semantics")
    return status


@router.get("/v1/runtime/latency")
@router.get("/runtime/latency")
async def api_runtime_latency() -> dict:
    return {
        "uptime_seconds": telemetry.uptime_seconds,
        "latency_ms": telemetry.latency_summary(),
    }


@router.get("/v1/runtime/metrics")
@router.get("/runtime/metrics")
async def api_runtime_metrics() -> dict:
    ws_status = manager.status()
    return telemetry.metrics(
        connected_clients=ws_status["connected_clients"],
        tick_rate_hz=settings.tick_rate_hz,
    )


@router.post("/v1/runtime/emergency-stop")
async def api_emergency_stop(payload: RuntimeControlRequest | None = None) -> dict:
    reason = payload.reason if payload else "manual emergency stop"
    return await get_engine().emergency_stop(reason)


@router.post("/v1/runtime/freeze")
async def api_freeze(payload: RuntimeControlRequest | None = None) -> dict:
    reason = payload.reason if payload else "manual freeze"
    return await get_engine().freeze_adaptation(reason)


@router.post("/v1/runtime/unfreeze")
async def api_unfreeze() -> dict:
    result = await get_engine().unfreeze_adaptation()
    if result["status"] == "blocked":
        raise HTTPException(status_code=409, detail=result["reason"])
    return result
