from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from app.api.websocket_manager import manager
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "service": "neuroverse-backend", "version": "0.1.0"}


@router.get("/api/v1/health")
async def api_v1_health() -> dict:
    return await health()


@router.get("/ready")
async def ready() -> dict:
    checks = _deep_checks()
    ready_state = all(item["ok"] for item in checks.values() if item["required"])
    return {
        "status": "ready" if ready_state else "not_ready",
        "ready": ready_state,
        "checks": checks,
    }


@router.get("/api/v1/health/deep")
async def deep_health() -> dict:
    checks = _deep_checks()
    ok = all(item["ok"] for item in checks.values() if item["required"])
    return {
        "status": "ok" if ok else "degraded",
        "service": "neuroverse-backend",
        "version": "0.1.0",
        "environment_mode": settings.environment_mode,
        "performance_mode": settings.performance_mode,
        "checks": checks,
        "websocket": manager.status(),
    }


def _deep_checks() -> dict[str, dict[str, Any]]:
    return {
        "config_loaded": {"ok": settings.tick_interval_ms > 0, "required": True},
        "session_storage_writable": {
            "ok": _is_writable(settings.sessions_dir),
            "required": True,
            "path": str(settings.sessions_dir),
        },
        "model_registry_readable": {
            "ok": settings.models_dir.exists(),
            "required": False,
            "path": str(settings.models_dir),
        },
        "report_directory_writable": {
            "ok": _is_writable(settings.reports_dir),
            "required": True,
            "path": str(settings.reports_dir),
        },
        "optional_hardware_brainflow": {
            "ok": importlib.util.find_spec("brainflow") is not None,
            "required": False,
        },
        "optional_hardware_lsl": {
            "ok": importlib.util.find_spec("pylsl") is not None,
            "required": False,
        },
        "optional_xdf": {
            "ok": importlib.util.find_spec("pyxdf") is not None,
            "required": False,
        },
        "websocket_manager": {
            "ok": True,
            "required": True,
            **manager.status(),
        },
    }


def _is_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".neuroverse_write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return True
    except OSError:
        return False
