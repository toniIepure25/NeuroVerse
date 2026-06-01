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


@router.get("/api/v1/system/overview")
async def system_overview() -> dict[str, Any]:
    import json
    from datetime import datetime, timezone

    from app.api.routes_protocols import find_latest_auto_run
    from app.api.routes_safety import _build_governance, _evidence_summary
    from app.core.runtime_status import runtime_status
    from app.datasources.readiness import list_data_sources
    from app.integrations.imagina.external_client import detect_external_imagina_project
    from app.safety.report_status import get_cached_report_evidence
    from app.safety.state_machine import safety_state_machine

    # 1. Safety & Governance
    state = safety_state_machine.get_current_state()
    rs = runtime_status.snapshot()
    ev, cache_meta = get_cached_report_evidence()
    governance = _build_governance(rs, ev)

    # 2. Data Sources
    try:
        data_sources = list_data_sources().model_dump()
    except Exception:
        data_sources = {"sources": [], "generated_at": datetime.now(timezone.utc).isoformat()}

    # 3. Protocol
    try:
        latest_run = find_latest_auto_run()
    except Exception:
        latest_run = None

    # 4. Imagina
    try:
        ext_status = detect_external_imagina_project()
        imagina_status = ext_status.model_dump()
    except Exception:
        imagina_status = {"exists": False}

    # 5. Latest success import
    latest_import = None
    latest_import_path = Path("reports/external_imagina_imports/latest_import_summary.json")
    if latest_import_path.exists():
        try:
            latest_import = json.loads(latest_import_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # 6. Latest Fusion Validation
    fusion_validation = None
    try:
        from app.api.routes_fusion import _LATEST_VALIDATION
        fusion_validation = _LATEST_VALIDATION
    except Exception:
        pass

    if fusion_validation is None:
        validation_dir = Path("reports/fusion_validation")
        if validation_dir.exists():
            try:
                subdirs = sorted(
                    validation_dir.glob("*/fusion_validation_summary.json"),
                    key=lambda p: p.stat().st_mtime,
                    reverse=True
                )
                if subdirs:
                    fusion_validation = json.loads(subdirs[0].read_text(encoding="utf-8"))
            except Exception:
                pass

    # 7. Aggregate
    warnings = list(ev.evidence_warnings)
    if not imagina_status.get("exists"):
        warnings.append(
            "External IMAGINA project directory not detected. "
            "Falling back to internal smoke-test fixtures."
        )

    limitations = [
        "Closed-loop from real EEG is disabled by default.",
        (
            "The corridor is not a decoded mental image. "
            "It is an adaptive scaffold driven by experimental proxy metrics."
        ),
        "IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams.",
        "Static evidence is a baked snapshot, not live runtime evidence.",
        "Physical OpenBCI/Galea validation remains unperformed unless a real device report exists."
    ]

    return {
        "source": "live_backend",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "warnings": warnings,
        "limitations": limitations,
        "closed_loop_allowed": False,
        "safety": {
            "current_state": state.get("state_id"),
            "severity": state.get("severity"),
            "closed_loop_allowed": False,
            "lock_reasons": governance.lock_reasons,
            "lock_reason_codes": governance.lock_reason_codes,
            "emergency_stop_active": bool(rs.get("emergency_stop_active")),
            "adaptation_frozen": bool(rs.get("adaptation_frozen")),
            "evidence_summary": _evidence_summary(ev, cache_meta),
            "safety_audit_report_path": ev.safety_audit_report_path
        },
        "data_sources": data_sources,
        "protocol": {
            "latest_run": latest_run,
        },
        "imagina": {
            "external_detected": imagina_status.get("exists", False),
            "external_status": imagina_status,
            "latest_import": latest_import
        },
        "fusion": {
            "latest_validation": fusion_validation,
            "imagina_proxy_status": "proxy_estimates_only",
            "disclaimer": (
                "IMAGINA exports are experimental imagery proxy artifacts, "
                "not decoded thoughts or dreams."
            )
        },
        "evidence_health": {
            "artifact_count": len(ev.evidence_sources),
            "evidence_sources": ev.evidence_sources,
            "cache_meta": cache_meta
        }
    }
