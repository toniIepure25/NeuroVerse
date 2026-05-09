from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.datasets.registry import create_dataset_adapter
from app.datasets.validation import validate_dataset_config

router = APIRouter(prefix="/api")
REPO_ROOT = Path(__file__).resolve().parents[3]
DATASET_CONFIG_DIR = REPO_ROOT / "configs" / "datasets"


@router.get("/v1/datasets")
@router.get("/datasets")
async def list_datasets() -> list[dict]:
    items = []
    for path in sorted(DATASET_CONFIG_DIR.glob("*.*")):
        if path.suffix.lower() not in {".yaml", ".yml", ".json"}:
            continue
        try:
            adapter = create_dataset_adapter(path)
            meta = adapter.load_metadata()
            items.append({"config": str(path), **meta.to_dict()})
        except Exception as exc:
            items.append({"config": str(path), "error": str(exc)})
    return items


@router.get("/v1/datasets/{dataset_id}/metadata")
@router.get("/datasets/{dataset_id}/metadata")
async def dataset_metadata(dataset_id: str) -> dict:
    for path in sorted(DATASET_CONFIG_DIR.glob("*.*")):
        try:
            adapter = create_dataset_adapter(path)
            meta = adapter.load_metadata()
            if meta.dataset_id == dataset_id:
                return meta.to_dict()
        except Exception:
            continue
    raise HTTPException(status_code=404, detail="Dataset config not found")


@router.post("/v1/datasets/validate")
@router.post("/datasets/validate")
async def validate_dataset(payload: dict) -> dict:
    try:
        config = payload.get("config_path") or payload
        write_report = bool(payload.get("write_report", False))
        target = payload.get("target")
        if write_report:
            return validate_dataset_config(config, target=target, write_report=True)
        adapter = create_dataset_adapter(config)
        return adapter.validate()
    except Exception as exc:
        return {"ok": False, "error": str(exc)}
