from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.deps import get_engine
from app.core.runtime_status import runtime_status
from app.inference.model_loader import (
    ModelActivationError,
    activate_model,
    deactivate_model,
    get_active_model_status,
)
from app.ml.registry import get_model_metadata, list_models

router = APIRouter(prefix="/api")


@router.get("/v1/models")
@router.get("/models")
async def api_list_models() -> dict:
    return {"active": get_active_model_status(), "models": list_models()}


@router.get("/v1/models/active")
@router.get("/models/active")
async def api_get_active_model() -> dict:
    return get_active_model_status()


@router.post("/v1/models/deactivate")
@router.post("/models/deactivate")
async def api_deactivate_model() -> dict:
    if get_engine().is_running:
        raise HTTPException(
            status_code=409,
            detail="Cannot change estimator while a session is running",
        )
    status = deactivate_model()
    runtime_status.set_active_model("heuristic", None, None)
    return status


@router.get("/v1/models/{model_id}")
@router.get("/models/{model_id}")
async def api_get_model(model_id: str) -> dict:
    try:
        return get_model_metadata(model_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found")


@router.post("/v1/models/{model_id}/activate")
@router.post("/models/{model_id}/activate")
async def api_activate_model(model_id: str) -> dict:
    if get_engine().is_running:
        raise HTTPException(
            status_code=409,
            detail="Cannot activate model while a session is running",
        )
    try:
        status = activate_model(model_id)
        runtime_status.set_active_model(
            "learned",
            status.get("model_id"),
            status.get("prediction_semantics"),
        )
        return status
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found")
    except ModelActivationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
