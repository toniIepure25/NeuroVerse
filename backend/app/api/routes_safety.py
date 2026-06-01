"""Safety governance API routes.

Exposes the safety state machine, closed-loop governance, timeline, and
blocked-action log. Operator controls (freeze, unfreeze, emergency-stop)
are wired through the existing engine so all state is consistent.

Read-only endpoints use cached evidence (30s TTL) to avoid re-scanning
disk on every polling request.  Operator state-change endpoints
force-refresh the cache, invalidate it, and broadcast a governance update
event to all connected WebSocket clients.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import get_engine
from app.api.websocket_manager import manager
from app.core.runtime_status import runtime_status
from app.safety.closed_loop_governance import evaluate_closed_loop_governance
from app.safety.reason_codes import SafetyReasonCode
from app.safety.report_status import (
    ReportEvidenceSummary,
    get_cached_report_evidence,
    invalidate_report_evidence_cache,
)
from app.safety.state_machine import safety_state_machine

router = APIRouter(prefix="/api/v1/safety", tags=["safety"])


class SafetyControlRequest(BaseModel):
    reason: str = Field(default="operator request")


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def _build_governance(rs: dict, ev: ReportEvidenceSummary):
    """Combine runtime snapshot and aggregated evidence into a governance result."""
    return evaluate_closed_loop_governance(
        environment_flag=bool(rs.get("hardware_closed_loop_enabled")),
        hardware_validated=ev.physical_hardware_validated,
        signal_quality_ok=ev.signal_quality_ok,
        timing_validated=ev.timing_ok,
        calibration_complete=ev.calibration_complete,
        shadow_inference_passed=ev.shadow_inference_passed,
        emergency_stop_active=bool(rs.get("emergency_stop_active")),
        adaptation_frozen=bool(rs.get("adaptation_frozen")),
        mode="simulated",
        model_compatible=True,
    )


def _evidence_summary(ev: ReportEvidenceSummary, cache_meta: dict | None = None) -> dict:
    """Return a full evidence summary dict for API responses."""
    summary: dict = {
        # Quality booleans
        "signal_quality_ok": ev.signal_quality_ok,
        "signal_quality_source": ev.signal_quality_source,
        "signal_quality_note": ev.signal_quality_note,
        "timing_ok": ev.timing_ok,
        "calibration_complete": ev.calibration_complete,
        "shadow_inference_passed": ev.shadow_inference_passed,
        # Validation flags
        "validation_report_present": ev.validation_report_present,
        "validation_passed": ev.validation_passed,
        "brainflow_synthetic_validated": ev.brainflow_synthetic_validated,
        "lsl_synthetic_validated": ev.lsl_synthetic_validated,
        "lsl_replay_validated": ev.lsl_replay_validated,
        "physical_hardware_validated": ev.physical_hardware_validated,
        "lsl_live_validation_passed": ev.lsl_live_validation_passed,
        # SQI
        "latest_sqi_mean": ev.latest_sqi_mean,
        "latest_sqi_min": ev.latest_sqi_min,
        "best_sqi_mean": ev.best_sqi_mean,
        "best_sqi_min": ev.best_sqi_min,
        # Timing
        "latest_jitter_p95_ms": ev.latest_jitter_p95_ms,
        "latest_drift_percent": ev.latest_drift_percent,
        "best_jitter_p95_ms": ev.best_jitter_p95_ms,
        # Report paths — latest
        "latest_validation_report_path": ev.latest_validation_report_path,
        "latest_calibration_report_path": ev.latest_calibration_report_path,
        "latest_shadow_report_path": ev.latest_shadow_report_path,
        "latest_physical_trial_report_path": ev.latest_physical_trial_report_path,
        # Report paths — valid vs failed
        "latest_valid_validation_report_path": ev.latest_valid_validation_report_path,
        "latest_failed_validation_report_path": ev.latest_failed_validation_report_path,
        # Safety audit
        "safety_audit_report_path": ev.safety_audit_report_path,
        # Adapter
        "adapter": ev.adapter,
        # Provenance
        "evidence_sources": ev.evidence_sources,
        "evidence_warnings": ev.evidence_warnings,
        "note": (
            "Physical hardware validation requires a real device report with "
            "physical_device_detected=True. BrainFlow SyntheticBoard and LSL "
            "synthetic streams do not count as physical hardware."
        ),
    }
    if cache_meta is not None:
        summary["evidence_cache"] = cache_meta
    return summary


async def _broadcast_governance_update(rs: dict, ev: ReportEvidenceSummary) -> None:
    """Broadcast a governance update event to all WebSocket clients."""
    if manager.client_count == 0:
        return
    try:
        governance = _build_governance(rs, ev)
        state = safety_state_machine.get_current_state()
        payload = {
            "event_type": "neuroverse.safety.governance_update",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "current_state": state.get("state_id"),
                "severity": state.get("severity"),
                "closed_loop_allowed": governance.closed_loop_allowed,
                "lock_reasons": governance.lock_reasons,
                "lock_reason_codes": governance.lock_reason_codes,
                "emergency_stop_active": bool(rs.get("emergency_stop_active")),
                "adaptation_frozen": bool(rs.get("adaptation_frozen")),
                "evidence_summary": _evidence_summary(ev),
            },
        }
        await manager.broadcast(payload)
    except Exception:
        pass  # Broadcast failure must never break the control endpoint


# ---------------------------------------------------------------------------
#  Read-only endpoints  (use cached evidence)
# ---------------------------------------------------------------------------


@router.get("/state")
async def api_safety_state() -> dict:
    """Return the current safety state with governance context and evidence summary."""
    state = safety_state_machine.get_current_state()
    rs = runtime_status.snapshot()
    ev, cache_meta = get_cached_report_evidence()
    governance = _build_governance(rs, ev)
    state["governance"] = governance.to_dict()
    state["evidence_summary"] = _evidence_summary(ev, cache_meta)
    state["emergency_stop_active"] = bool(rs.get("emergency_stop_active"))
    state["adaptation_frozen"] = bool(rs.get("adaptation_frozen"))
    return state


@router.get("/timeline")
async def api_safety_timeline(limit: int = 50) -> dict:
    """Return the recent safety state transition timeline."""
    return {
        "timeline": safety_state_machine.get_timeline(limit=limit),
        "total_transitions": len(safety_state_machine._timeline),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/blocked-actions")
async def api_blocked_actions(limit: int = 50) -> dict:
    """Return the recent blocked-action log."""
    return {
        "blocked_actions": safety_state_machine.get_blocked_actions(limit=limit),
        "total_blocked": len(safety_state_machine._blocked_actions),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/closed-loop")
async def api_closed_loop_status() -> dict:
    """Return the closed-loop governance decision with full evidence provenance."""
    rs = runtime_status.snapshot()
    ev, cache_meta = get_cached_report_evidence()
    governance = _build_governance(rs, ev)
    result = governance.to_dict()
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["evidence_summary"] = _evidence_summary(ev, cache_meta)
    result["note"] = (
        "Closed-loop from real EEG is disabled by default. "
        "Hardware validation confirms stream quality and software integration; "
        "it does not validate clinical or unrestricted mental-state inference."
    )
    return result


@router.get("/report/latest")
async def api_safety_report_latest() -> dict:
    """Return a serialized safety audit snapshot with full evidence provenance."""
    rs = runtime_status.snapshot()
    ev, cache_meta = get_cached_report_evidence()
    governance = _build_governance(rs, ev)
    serialized = safety_state_machine.serialize()
    serialized["governance"] = governance.to_dict()
    serialized["evidence_summary"] = _evidence_summary(ev, cache_meta)
    serialized["runtime_snapshot"] = {
        "emergency_stop_active": rs.get("emergency_stop_active"),
        "adaptation_frozen": rs.get("adaptation_frozen"),
        "hardware_validation_state": rs.get("hardware_validation_state"),
        "current_data_source": rs.get("current_data_source"),
    }
    serialized["generated_at"] = datetime.now(timezone.utc).isoformat()
    serialized["scientific_disclaimer"] = (
        "Closed-loop from real EEG is disabled by default. "
        "The corridor is not a decoded mental image. "
        "It is an adaptive scaffold driven by experimental proxy metrics."
    )
    return serialized


# ---------------------------------------------------------------------------
#  Evidence cache management
# ---------------------------------------------------------------------------


@router.post("/evidence/refresh")
async def api_evidence_refresh() -> dict:
    """Force-refresh the report evidence cache and return updated summary.

    Does not change safety state or unlock closed-loop.
    Used to pick up newly generated report files without waiting for TTL expiry.
    """
    ev, cache_meta = get_cached_report_evidence(force_refresh=True)
    rs = runtime_status.snapshot()
    governance = _build_governance(rs, ev)
    return {
        "status": "refreshed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evidence_summary": _evidence_summary(ev, cache_meta),
        "closed_loop_allowed": governance.closed_loop_allowed,
        "note": "Cache force-refreshed. closed_loop_allowed remains false by default.",
    }


# ---------------------------------------------------------------------------
#  Operator control endpoints  (force-refresh evidence, broadcast)
# ---------------------------------------------------------------------------


@router.post("/reset")
async def api_safety_reset(payload: SafetyControlRequest | None = None) -> dict:
    """Reset the safety state machine to NO_DATA."""
    reason = payload.reason if payload else "operator reset"
    result = safety_state_machine.reset(reason=reason)
    invalidate_report_evidence_cache(f"safety_reset:{reason}")
    ev, cache_meta = get_cached_report_evidence(force_refresh=True)
    rs = runtime_status.snapshot()
    await _broadcast_governance_update(rs, ev)
    return {"status": "reset", "transition": result, "evidence_cache": cache_meta}


@router.post("/freeze")
async def api_safety_freeze(payload: SafetyControlRequest | None = None) -> dict:
    """Freeze adaptation via safety governance."""
    reason = payload.reason if payload else "operator freeze"
    engine = get_engine()
    engine_result = await engine.freeze_adaptation(reason)
    invalidate_report_evidence_cache(f"freeze:{reason}")
    ev, cache_meta = get_cached_report_evidence(force_refresh=True)
    rs = runtime_status.snapshot()
    await _broadcast_governance_update(rs, ev)
    return {
        "status": "frozen",
        "reason": reason,
        "engine": engine_result,
        "safety_state": safety_state_machine.get_current_state(),
        "evidence_cache": cache_meta,
    }


@router.post("/unfreeze")
async def api_safety_unfreeze() -> dict:
    """Unfreeze adaptation."""
    engine = get_engine()
    result = await engine.unfreeze_adaptation()
    if result["status"] == "blocked":
        raise HTTPException(status_code=409, detail=result["reason"])
    invalidate_report_evidence_cache("unfreeze")
    ev, cache_meta = get_cached_report_evidence(force_refresh=True)
    rs = runtime_status.snapshot()
    await _broadcast_governance_update(rs, ev)
    return {
        "status": "unfrozen",
        "engine": result,
        "safety_state": safety_state_machine.get_current_state(),
        "evidence_cache": cache_meta,
    }


@router.post("/emergency-stop")
async def api_safety_emergency_stop(payload: SafetyControlRequest | None = None) -> dict:
    """Trigger emergency stop."""
    reason = payload.reason if payload else "operator emergency stop"
    engine = get_engine()
    engine_result = await engine.emergency_stop(reason)
    safety_state_machine.record_blocked_action(
        "all_adaptation",
        reason_code=SafetyReasonCode.EMERGENCY_STOP_ACTIVE.value,
        reason=reason,
        source="operator",
    )
    invalidate_report_evidence_cache(f"emergency_stop:{reason}")
    ev, cache_meta = get_cached_report_evidence(force_refresh=True)
    rs = runtime_status.snapshot()
    await _broadcast_governance_update(rs, ev)
    return {
        "status": "emergency_stopped",
        "reason": reason,
        "engine": engine_result,
        "safety_state": safety_state_machine.get_current_state(),
        "evidence_cache": cache_meta,
    }


@router.post("/clear-emergency")
async def api_safety_clear_emergency() -> dict:
    """Clear emergency stop (only allowed when no session is running)."""
    rs = runtime_status.snapshot()
    if rs.get("current_session_id"):
        raise HTTPException(
            status_code=409,
            detail="Cannot clear emergency stop while a session is active. Stop the session first.",
        )
    transition = safety_state_machine.transition_to(
        "CLOSED_LOOP_LOCKED",
        reason_code=SafetyReasonCode.USER_MANUAL_OVERRIDE.value,
        reason="Emergency stop cleared by operator. System returned to CLOSED_LOOP_LOCKED.",
        source="operator",
        automatic_or_manual="manual",
        operator_action="clear_emergency",
    )
    runtime_status._status["emergency_stop_active"] = False
    runtime_status._status["adaptation_frozen"] = False
    runtime_status._status["freeze_reason"] = None
    invalidate_report_evidence_cache("clear_emergency")
    ev, cache_meta = get_cached_report_evidence(force_refresh=True)
    rs = runtime_status.snapshot()
    await _broadcast_governance_update(rs, ev)
    return {
        "status": "emergency_cleared",
        "safety_state": safety_state_machine.get_current_state(),
        "transition": transition,
        "evidence_cache": cache_meta,
    }
