"""Data source readiness API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.datasources.readiness import get_data_source, list_data_sources, preflight_data_source

router = APIRouter(prefix="/api/v1/data-sources", tags=["data-sources"])


class DataSourcePreflightRequest(BaseModel):
    inputs: dict[str, str] = {}


@router.get("")
async def api_list_data_sources() -> dict:
    return list_data_sources().model_dump()


@router.get("/{source_id}")
async def api_get_data_source(source_id: str) -> dict:
    status = get_data_source(source_id)
    if status is None:
        raise HTTPException(status_code=404, detail=f"Data source '{source_id}' not found")
    return status.model_dump()


@router.post("/{source_id}/refresh")
async def api_refresh_data_source(source_id: str) -> dict:
    status = get_data_source(source_id, force_refresh=True)
    if status is None:
        raise HTTPException(status_code=404, detail=f"Data source '{source_id}' not found")
    return status.model_dump()


@router.post("/{source_id}/preflight")
async def api_preflight_data_source(source_id: str, body: DataSourcePreflightRequest) -> dict:
    status = preflight_data_source(source_id, body.inputs, force_refresh=True)
    if status is None:
        raise HTTPException(status_code=404, detail=f"Data source '{source_id}' not found")
    return status.model_dump()
