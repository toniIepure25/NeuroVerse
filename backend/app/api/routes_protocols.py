"""Protocol engine API routes for NeuroVerse."""

from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.runtime_status import runtime_status
from app.protocols.models import (
    ORCH_CANCELLED,
    ORCH_COMPLETED,
    ORCH_RUNNING,
    ORCH_STOPPED_BLOCKED,
    ORCH_STOPPED_FAILED,
    ORCH_STOPPED_MANUAL,
    PreflightResult,
    ProtocolDefinition,
    ProtocolMode,
    ProtocolRun,
    ProtocolStepResult,
    ProtocolStepStatus,
)
from app.protocols.registry import get_protocol, list_protocols
from app.protocols.runner import execute_step_async
from app.protocols.storage import (
    find_latest_auto_run,
    generate_completion_report,
    list_runs,
    load_run,
    save_run,
    update_latest_auto_run_evidence,
)
from app.safety.closed_loop_governance import evaluate_closed_loop_governance
from app.safety.report_status import get_cached_report_evidence
from app.safety.state_machine import safety_state_machine

router = APIRouter(prefix="/api/v1", tags=["protocols"])

# In-memory stores (persisted to disk on each update)
_ACTIVE_RUNS: dict[str, ProtocolRun] = {}
_RUNNING_TASKS: dict[str, asyncio.Task] = {}
_STOP_EVENTS: dict[str, asyncio.Event] = {}


class CreateRunRequest(BaseModel):
    inputs: dict[str, str] = {}


class PreflightRequest(BaseModel):
    inputs: dict[str, str] = {}


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def _safety_summary() -> dict[str, Any]:
    rs = runtime_status.snapshot()
    ev, cache_meta = get_cached_report_evidence()
    gov = evaluate_closed_loop_governance(
        environment_flag=bool(rs.get("hardware_closed_loop_enabled")),
        hardware_validated=ev.physical_hardware_validated,
        signal_quality_ok=ev.signal_quality_ok,
        timing_validated=ev.timing_ok,
        calibration_complete=ev.calibration_complete,
        shadow_inference_passed=ev.shadow_inference_passed,
        emergency_stop_active=bool(rs.get("emergency_stop_active")),
        adaptation_frozen=bool(rs.get("adaptation_frozen")),
        mode="simulated",
    )
    state = safety_state_machine.get_current_state()
    return {
        "state_id": state.get("state_id"),
        "severity": state.get("severity"),
        "governance": gov.to_dict(),
        "evidence_cache": cache_meta,
    }


def _get_active_run(run_id: str) -> ProtocolRun:
    if run_id in _ACTIVE_RUNS:
        return _ACTIVE_RUNS[run_id]
    run = load_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Protocol run '{run_id}' not found")
    _ACTIVE_RUNS[run_id] = run
    return run


def _is_step_running(run_id: str) -> bool:
    """Return True if a background step or orchestration task is active for this run."""
    task = _RUNNING_TASKS.get(run_id)
    return task is not None and not task.done()


def _compute_preflight(
    protocol: ProtocolDefinition,
    inputs: dict[str, str],
    safety: dict[str, Any],
) -> PreflightResult:
    """Evaluate protocol readiness given the provided inputs and current safety state."""
    blocking_issues: list[str] = []
    warnings: list[str] = []
    manual_steps: list[str] = []
    executable_steps: list[str] = []

    # Required inputs at the protocol level
    for inp in protocol.required_inputs:
        if not inputs.get(inp):
            blocking_issues.append(f"Required input missing: {inp}")

    # Physical hardware without PORT
    if protocol.mode == ProtocolMode.PHYSICAL_HARDWARE and not inputs.get("PORT"):
        if not any("PORT" in b for b in blocking_issues):
            blocking_issues.append(
                "Physical hardware protocol requires PORT input (e.g. /dev/ttyUSB0)."
            )

    # Categorise each step
    for step in protocol.steps:
        if step.action == "manual_command_required":
            manual_steps.append(step.step_id)
        elif step.required_inputs and any(not inputs.get(i) for i in step.required_inputs):
            # Step-level missing inputs → blocked (effectively manual from auto-run perspective)
            manual_steps.append(step.step_id)
            warnings.append(
                f"Step '{step.step_id}' requires inputs: {', '.join(step.required_inputs)}"
            )
        else:
            executable_steps.append(step.step_id)

    # Hardware dependency hints (informational only)
    try:
        import brainflow as _bf  # noqa: F401
    except ImportError:
        if "brainflow" in protocol.tags or "brainflow_installed" in protocol.safety_requirements:
            warnings.append("BrainFlow not installed — run: pip install brainflow")

    try:
        import pylsl as _lsl  # noqa: F401
    except ImportError:
        if "lsl" in protocol.tags or "pylsl_installed" in protocol.safety_requirements:
            warnings.append("pylsl not installed — run: pip install pylsl")

    # Governance check
    gov = safety.get("governance", {})
    if gov.get("closed_loop_allowed", False):
        warnings.append(
            "closed_loop_allowed is True in current safety state — contact safety team."
        )

    if manual_steps:
        warnings.append(
            f"{len(manual_steps)} step(s) require manual action: "
            + ", ".join(manual_steps)
        )

    # can_start: no protocol-level blocking issues
    can_start = len(blocking_issues) == 0

    # can_auto_run: protocol supports it + there are executable steps + can start
    policy = protocol.auto_run_policy
    can_auto_run = (
        can_start
        and protocol.supports_auto_run
        and policy != "disabled"
        and len(executable_steps) > 0
    )

    # Auto-run label for the frontend
    if not can_auto_run:
        auto_run_label = "Auto-run not supported"
    elif manual_steps and policy == "until_manual_step":
        auto_run_label = f"Run all (stops before {len(manual_steps)} manual step(s))"
    elif manual_steps:
        auto_run_label = "Run all (will stop at first manual step)"
    else:
        auto_run_label = "Run all steps (fully automated)"

    return PreflightResult(
        protocol_id=protocol.protocol_id,
        can_start=can_start,
        can_auto_run=can_auto_run,
        blocking_issues=blocking_issues,
        warnings=warnings,
        manual_steps=manual_steps,
        executable_steps=executable_steps,
        required_inputs=protocol.required_inputs,
        closed_loop_allowed=False,
        safety_summary=safety,
        auto_run_label=auto_run_label,
        auto_run_policy=policy,
        reviewer_demo_recommended=protocol.reviewer_demo_recommended,
    )


# ---------------------------------------------------------------------------
#  Background orchestration
# ---------------------------------------------------------------------------


async def _background_run_step(
    run: ProtocolRun,
    step_def: Any,
    step_result: ProtocolStepResult,
) -> None:
    """Single-step background wrapper (used by individual step endpoint)."""
    try:
        await execute_step_async(run, step_def, step_result, pre_started=True)
    except asyncio.CancelledError:
        if step_result.status == ProtocolStepStatus.RUNNING:
            step_result.complete(passed=False, error_message="Step cancelled by request")
    except Exception as exc:  # noqa: BLE001
        if step_result.status == ProtocolStepStatus.RUNNING:
            step_result.complete(passed=False, error_message=f"Background error: {exc!s}")
    finally:
        try:
            ev, _ = get_cached_report_evidence(force_refresh=True)
            run.evidence_summary = ev.to_dict()
            run.safety_summary = _safety_summary()
        except Exception:  # noqa: BLE001
            pass
        run.current_step_id = None
        run.touch()
        _RUNNING_TASKS.pop(run.run_id, None)
        save_run(run)


async def _orchestrate_run(
    run: ProtocolRun,
    protocol: ProtocolDefinition,
    stop_event: asyncio.Event,
) -> None:
    """Run all executable protocol steps in sequence.

    Stops cleanly at manual steps, blocked steps, failures, or a stop request.
    Never enables closed-loop; never runs physical hardware without PORT.
    """
    run.orchestration_status = ORCH_RUNNING
    run.orchestration_started_at = datetime.now(timezone.utc).isoformat()
    run.auto_advance = True
    run.touch()
    save_run(run)

    try:
        for step_def in protocol.steps:
            # Honour stop request between steps
            if stop_event.is_set():
                run.orchestration_status = ORCH_CANCELLED
                run.orchestration_stop_reason = "Stopped by user request"
                break

            # Locate or create step result
            step_result = next(
                (s for s in run.steps if s.step_id == step_def.step_id), None
            )
            if step_result is None:
                step_result = ProtocolStepResult(
                    step_id=step_def.step_id, title=step_def.title
                )
                run.steps.append(step_result)

            # Skip already-passed steps
            if step_result.status == ProtocolStepStatus.PASSED:
                continue

            # Manual steps — mark and stop orchestration
            if step_def.action == "manual_command_required":
                run.orchestration_status = ORCH_STOPPED_MANUAL
                run.orchestration_stop_reason = (
                    f"Manual step required: {step_def.title}. "
                    "Complete it manually, then run individual steps or restart run-all."
                )
                await execute_step_async(run, step_def, step_result, pre_started=False)
                run.touch()
                save_run(run)
                break

            # Missing required inputs → blocked
            missing = [i for i in step_def.required_inputs if not run.inputs.get(i)]
            if missing:
                run.orchestration_status = ORCH_STOPPED_BLOCKED
                run.orchestration_stop_reason = (
                    f"Missing required inputs for step '{step_def.step_id}': "
                    + ", ".join(missing)
                )
                step_result.block(reason=f"Missing required inputs: {', '.join(missing)}")
                run.touch()
                save_run(run)
                break

            # Pre-mark running and persist before awaiting
            step_result.start(execution_mode="background_task")
            run.current_step_id = step_def.step_id
            run.touch()
            save_run(run)

            # Yield once so SSE picks up the "running" state
            await asyncio.sleep(0)

            await execute_step_async(run, step_def, step_result, pre_started=True)

            run.touch()
            save_run(run)

            if step_result.status == ProtocolStepStatus.FAILED:
                run.orchestration_status = ORCH_STOPPED_FAILED
                run.orchestration_stop_reason = (
                    f"Step failed: {step_def.title} — "
                    + (step_result.error_message or "unknown error")
                )
                break

            if step_result.status == ProtocolStepStatus.BLOCKED:
                run.orchestration_status = ORCH_STOPPED_BLOCKED
                run.orchestration_stop_reason = (
                    f"Step blocked: {step_def.title} — "
                    + (step_result.block_reason or "unknown reason")
                )
                break

        else:
            # for-loop completed without break
            run.orchestration_status = ORCH_COMPLETED
            run.orchestration_stop_reason = "All steps completed successfully"

    except asyncio.CancelledError:
        run.orchestration_status = ORCH_CANCELLED
        run.orchestration_stop_reason = "Task cancelled"
        # Mark any still-running step as cancelled
        for step in run.steps:
            if step.status == ProtocolStepStatus.RUNNING:
                step.complete(passed=False, error_message="Cancelled by orchestration stop")
    except Exception as exc:  # noqa: BLE001
        run.orchestration_status = ORCH_STOPPED_FAILED
        run.orchestration_stop_reason = f"Orchestration error: {exc!s}"
    finally:
        try:
            ev, _ = get_cached_report_evidence(force_refresh=True)
            run.evidence_summary = ev.to_dict()
            run.safety_summary = _safety_summary()
        except Exception:  # noqa: BLE001
            pass

        run.orchestration_completed_at = datetime.now(timezone.utc).isoformat()
        run.current_step_id = None
        run.touch()

        # Auto-complete when all steps succeeded
        if run.orchestration_status == ORCH_COMPLETED:
            _auto_complete_run(run, protocol)

        _RUNNING_TASKS.pop(run.run_id, None)
        _STOP_EVENTS.pop(run.run_id, None)
        save_run(run)


def _auto_complete_run(run: ProtocolRun, protocol: Any) -> None:
    """Mark run as auto-completed and generate completion report v2."""
    run.auto_completed = True
    run.auto_completed_at = datetime.now(timezone.utc).isoformat()
    run.completed_at = run.auto_completed_at
    run.status = run.overall_status()
    run.final_report_generated = True
    run.final_report_generation_reason = (
        "Auto-completed after successful run-all orchestration"
    )
    try:
        run_dir = generate_completion_report(run, protocol)
        run.protocol_completion_report_path = str(
            run_dir / "protocol_completion_report.json"
        )
        run.final_report_path = str(run_dir / "protocol_run.json")
    except Exception:  # noqa: BLE001
        pass
    try:
        update_latest_auto_run_evidence(run)
    except Exception:  # noqa: BLE001
        pass


# ---------------------------------------------------------------------------
#  Protocol registry endpoints
# ---------------------------------------------------------------------------


@router.get("/protocols")
async def api_list_protocols() -> list[dict]:
    protocols = list_protocols()
    safety = _safety_summary()
    return [
        {
            **p.model_dump(),
            "current_safety_state": safety.get("state_id"),
            "closed_loop_allowed": False,
        }
        for p in protocols
    ]


@router.get("/protocols/{protocol_id}")
async def api_get_protocol(protocol_id: str) -> dict:
    protocol = get_protocol(protocol_id)
    if protocol is None:
        raise HTTPException(status_code=404, detail=f"Protocol '{protocol_id}' not found")
    safety = _safety_summary()
    return {
        **protocol.model_dump(),
        "current_safety_state": safety.get("state_id"),
        "closed_loop_allowed": False,
        "safety_summary": safety,
    }


@router.get("/protocols/{protocol_id}/preflight")
async def api_get_preflight(protocol_id: str) -> dict:
    """Run preflight checks with empty inputs (GET convenience endpoint)."""
    protocol = get_protocol(protocol_id)
    if protocol is None:
        raise HTTPException(status_code=404, detail=f"Protocol '{protocol_id}' not found")
    safety = _safety_summary()
    result = _compute_preflight(protocol, {}, safety)
    return result.model_dump()


@router.post("/protocols/{protocol_id}/preflight")
async def api_post_preflight(protocol_id: str, body: PreflightRequest) -> dict:
    """Run preflight checks with supplied inputs."""
    protocol = get_protocol(protocol_id)
    if protocol is None:
        raise HTTPException(status_code=404, detail=f"Protocol '{protocol_id}' not found")
    safety = _safety_summary()
    result = _compute_preflight(protocol, body.inputs, safety)
    return result.model_dump()


# ---------------------------------------------------------------------------
#  Protocol run endpoints
# ---------------------------------------------------------------------------


@router.post("/protocols/{protocol_id}/runs")
async def api_create_run(protocol_id: str, body: CreateRunRequest) -> dict:
    """Create a new protocol run. Returns run metadata with step list and preflight."""
    protocol = get_protocol(protocol_id)
    if protocol is None:
        raise HTTPException(status_code=404, detail=f"Protocol '{protocol_id}' not found")

    if protocol.mode == ProtocolMode.PHYSICAL_HARDWARE:
        if not body.inputs.get("PORT"):
            raise HTTPException(
                status_code=422,
                detail=(
                    "Physical hardware protocol requires 'PORT' input "
                    "(e.g. /dev/ttyUSB0). Provide it in the 'inputs' field. "
                    "Closed-loop adaptation remains disabled."
                ),
            )

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + str(uuid.uuid4())[:8]
    steps = [ProtocolStepResult(step_id=s.step_id, title=s.title) for s in protocol.steps]
    safety = _safety_summary()
    preflight = _compute_preflight(protocol, body.inputs, safety)
    run = ProtocolRun(
        run_id=run_id,
        protocol_id=protocol_id,
        protocol_title=protocol.title,
        mode=protocol.mode,
        steps=steps,
        inputs=body.inputs,
        safety_summary=safety,
        closed_loop_allowed=False,
        preflight_result=preflight.model_dump(),
    )
    _ACTIVE_RUNS[run_id] = run
    save_run(run)

    return {
        "run_id": run_id,
        "protocol_id": protocol_id,
        "protocol_title": protocol.title,
        "mode": protocol.mode,
        "status": run.overall_status(),
        "steps": [s.model_dump() for s in run.steps],
        "safety_summary": safety,
        "closed_loop_allowed": False,
        "preflight": preflight.model_dump(),
        "note": "Closed-loop from real EEG is disabled by default.",
    }


@router.get("/protocol-runs")
async def api_list_runs() -> list[dict]:
    return list_runs()


# NOTE: These literal routes must be defined BEFORE /protocol-runs/{run_id}
# so FastAPI does not match "latest-auto-run" as a run_id.


@router.get("/protocol-runs/latest-auto-run")
async def api_latest_auto_run() -> dict:
    """Return the latest auto-completed run, enriched with completion report fields.

    Merges protocol_run.json data with protocol_completion_report.json so callers
    get what_this_proves, step_summary, artifact_paths, and status as a plain string.
    """
    from pathlib import Path  # noqa: PLC0415

    data = find_latest_auto_run()
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="No auto-completed protocol run found. Run: make protocol-run-demo",
        )

    # Load completion report for rich fields
    completion_data: dict[str, Any] = {}
    cp_path = data.get("_completion_report_path")
    if cp_path:
        cp_file = Path(cp_path)
        if cp_file.exists():
            try:
                completion_data = json.loads(cp_file.read_text())
            except Exception:  # noqa: BLE001
                pass

    # Build step summary from raw steps list in protocol_run.json
    steps = data.get("steps", [])
    step_summary = {
        "total": len(steps),
        "passed": sum(1 for s in steps if s.get("status") == "passed"),
        "failed": sum(1 for s in steps if s.get("status") == "failed"),
        "blocked": sum(1 for s in steps if s.get("status") == "blocked"),
        "manual": sum(
            1 for s in steps if s.get("status") == "manual_command_required"
        ),
        "skipped": sum(1 for s in steps if s.get("status") == "skipped"),
    }
    all_artifacts = [
        p for s in steps for p in (s.get("artifact_paths") or [])
    ]

    # status: prefer completion_data (guaranteed plain string), fallback to run data
    raw_status = (
        completion_data.get("status")
        or str(data.get("status", "")).split(".")[-1].lower()
        or "unknown"
    )

    return {
        "run_id": data.get("run_id"),
        "protocol_id": data.get("protocol_id"),
        "protocol_title": data.get("protocol_title"),
        "mode": str(data.get("mode", "")).split(".")[-1].lower() or data.get("mode"),
        "status": raw_status,
        "auto_completed": data.get("auto_completed", False),
        "auto_completed_at": data.get("auto_completed_at"),
        "final_report_generated": data.get("final_report_generated", False),
        "final_report_path": data.get("final_report_path"),
        "protocol_completion_report_path": data.get("protocol_completion_report_path"),
        "orchestration_status": data.get("orchestration_status"),
        "orchestration_stop_reason": data.get("orchestration_stop_reason"),
        "closed_loop_allowed": False,
        "created_at": data.get("created_at"),
        "completed_at": data.get("completed_at"),
        "step_summary": step_summary,
        "artifact_paths": all_artifacts,
        "artifact_count": len(all_artifacts),
        "what_this_proves": completion_data.get("what_this_proves", []),
        "what_this_does_not_prove": completion_data.get(
            "what_this_does_not_prove", []
        ),
        "scientific_limitations": completion_data.get("scientific_limitations", ""),
        "scientific_disclaimer": data.get("scientific_disclaimer", ""),
        "safety_summary": data.get("safety_summary"),
        "generated_at": completion_data.get("generated_at"),
        "report_version": completion_data.get("report_version", "2"),
    }


@router.get("/protocol-runs/latest-auto-run/report")
async def api_latest_auto_run_report() -> dict:
    """Return the completion report v2 of the latest auto-completed protocol run."""
    data = find_latest_auto_run()
    if data is None:
        raise HTTPException(
            status_code=404,
            detail="No auto-completed protocol run found. Run: make protocol-run-demo",
        )
    completion_path = data.get("_completion_report_path")
    if not completion_path:
        raise HTTPException(
            status_code=404,
            detail="Completion report v2 not found for this run.",
        )
    from pathlib import Path  # noqa: PLC0415

    report_file = Path(completion_path)
    if not report_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Completion report file not found: {completion_path}",
        )
    report_data = json.loads(report_file.read_text())
    return {**report_data, "closed_loop_allowed": False}


@router.get("/protocol-runs/{run_id}")
async def api_get_run(run_id: str) -> dict:
    run = _get_active_run(run_id)
    safety = _safety_summary()
    return {
        **run.model_dump(),
        "overall_status": run.overall_status(),
        "safety_summary": safety,
        "closed_loop_allowed": False,
        "is_step_running": _is_step_running(run_id),
    }


@router.post("/protocol-runs/{run_id}/steps/{step_id}/run")
async def api_run_step(run_id: str, step_id: str) -> dict:
    """Start background execution of a single protocol step.

    Returns immediately with status='running' for executable steps.
    Manual/blocked steps complete synchronously (they're instant).
    """
    run = _get_active_run(run_id)

    if _is_step_running(run_id):
        running_step = next(
            (s for s in run.steps if s.status == ProtocolStepStatus.RUNNING), None
        )
        raise HTTPException(
            status_code=409,
            detail={
                "error": "step_already_running",
                "message": (
                    "A step is already running for this protocol run. "
                    "Wait for it to complete before starting another."
                ),
                "running_step_id": (
                    running_step.step_id if running_step else run.current_step_id
                ),
            },
        )

    protocol = get_protocol(run.protocol_id)
    if protocol is None:
        raise HTTPException(status_code=404, detail="Protocol definition not found")

    step_def = next((s for s in protocol.steps if s.step_id == step_id), None)
    if step_def is None:
        raise HTTPException(status_code=404, detail=f"Step '{step_id}' not found in protocol")

    step_result = next((s for s in run.steps if s.step_id == step_id), None)
    if step_result is None:
        step_result = ProtocolStepResult(step_id=step_id, title=step_def.title)
        run.steps.append(step_result)

    if step_result.status == ProtocolStepStatus.PASSED:
        return {
            "run_id": run_id,
            "step_id": step_id,
            "status": step_result.status,
            "message": "Step already passed.",
            "step_result": step_result.model_dump(),
            "closed_loop_allowed": False,
        }

    # Manual and blocked steps complete immediately
    is_manual = step_def.action == "manual_command_required"
    has_missing = bool(
        step_def.required_inputs
        and any(not run.inputs.get(i) for i in step_def.required_inputs)
    )
    if is_manual or has_missing:
        run.current_step_id = step_id
        run.touch()
        await execute_step_async(run, step_def, step_result, pre_started=False)
        run.current_step_id = None
        run.touch()
        save_run(run)
        safety = _safety_summary()
        return {
            "run_id": run_id,
            "step_id": step_id,
            "status": step_result.status,
            "message": f"Step completed immediately: {step_result.status}",
            "step_result": step_result.model_dump(),
            "safety_summary": safety,
            "closed_loop_allowed": False,
        }

    # Pre-mark running and persist
    step_result.start(execution_mode="background_task")
    run.current_step_id = step_id
    run.touch()
    save_run(run)

    task = asyncio.create_task(_background_run_step(run, step_def, step_result))
    _RUNNING_TASKS[run_id] = task

    safety = _safety_summary()
    return {
        "run_id": run_id,
        "step_id": step_id,
        "status": "running",
        "message": (
            "Step execution started in background. "
            "Stream /api/v1/protocol-runs/{run_id}/status/stream for live updates."
        ),
        "step_result": step_result.model_dump(),
        "safety_summary": safety,
        "closed_loop_allowed": False,
    }


@router.post("/protocol-runs/{run_id}/steps/{step_id}/cancel")
async def api_cancel_step(run_id: str, step_id: str) -> dict:
    """Request cancellation of the currently running step."""
    task = _RUNNING_TASKS.get(run_id)
    if task is None or task.done():
        raise HTTPException(status_code=404, detail="No running step for this protocol run.")
    task.cancel()
    return {
        "run_id": run_id,
        "step_id": step_id,
        "message": "Cancellation requested. Step will stop at next asyncio checkpoint.",
    }


@router.post("/protocol-runs/{run_id}/run-all")
async def api_run_all(run_id: str) -> dict:
    """Start background orchestration of all executable steps in sequence.

    Stops cleanly at manual steps, blocked steps, or failures.
    Returns immediately. Stream /status/stream for live progress.
    """
    run = _get_active_run(run_id)

    if _is_step_running(run_id):
        raise HTTPException(
            status_code=409,
            detail={
                "error": "already_running",
                "message": (
                    "A step or orchestration is already running. "
                    "Wait for completion or call /stop first."
                ),
                "orchestration_status": run.orchestration_status,
                "current_step_id": run.current_step_id,
            },
        )

    protocol = get_protocol(run.protocol_id)
    if protocol is None:
        raise HTTPException(status_code=404, detail="Protocol definition not found")

    if not protocol.supports_auto_run or protocol.auto_run_policy == "disabled":
        raise HTTPException(
            status_code=422,
            detail={
                "error": "auto_run_not_supported",
                "message": (
                    f"Protocol '{protocol.protocol_id}' does not support auto-run. "
                    "Run steps individually."
                ),
                "auto_run_policy": protocol.auto_run_policy,
            },
        )

    # Check there are actually pending executable steps to run
    done_statuses = {ProtocolStepStatus.PASSED, ProtocolStepStatus.SKIPPED}
    pending = [s for s in run.steps if s.status not in done_statuses]
    if not pending:
        return {
            "run_id": run_id,
            "orchestration_status": ORCH_COMPLETED,
            "message": "All steps already completed — nothing to run.",
            "closed_loop_allowed": False,
        }

    stop_event = asyncio.Event()
    _STOP_EVENTS[run_id] = stop_event

    task = asyncio.create_task(_orchestrate_run(run, protocol, stop_event))
    _RUNNING_TASKS[run_id] = task

    return {
        "run_id": run_id,
        "orchestration_status": ORCH_RUNNING,
        "message": (
            "Orchestration started. "
            "Stream GET /api/v1/protocol-runs/{run_id}/status/stream for live updates."
        ),
        "auto_run_policy": protocol.auto_run_policy,
        "closed_loop_allowed": False,
    }


@router.post("/protocol-runs/{run_id}/stop")
async def api_stop_orchestration(run_id: str) -> dict:
    """Request the running orchestration or step to stop after the current step."""
    stop_event = _STOP_EVENTS.get(run_id)
    if stop_event:
        stop_event.set()

    task = _RUNNING_TASKS.get(run_id)
    if task and not task.done():
        task.cancel()
        run = _ACTIVE_RUNS.get(run_id)
        if run and run.orchestration_status == ORCH_RUNNING:
            run.orchestration_status = ORCH_CANCELLED
            run.orchestration_stop_reason = "Stopped by user request"
            run.touch()
            save_run(run)
        return {
            "run_id": run_id,
            "orchestration_status": ORCH_CANCELLED,
            "message": "Stop requested. Orchestration will halt at next checkpoint.",
            "closed_loop_allowed": False,
        }

    return {
        "run_id": run_id,
        "orchestration_status": "idle",
        "message": "No active orchestration to stop.",
        "closed_loop_allowed": False,
    }


@router.get("/protocol-runs/{run_id}/status/stream")
async def api_run_status_stream(run_id: str) -> StreamingResponse:
    """Server-Sent Events stream for live protocol run status.

    Emits a JSON event every second. Sends ``{"done": true}`` and closes
    when both orchestration and individual steps are idle (2+ consecutive idle ticks).
    Max stream duration: 5 minutes.
    """

    async def _generate():
        max_ticks = 300
        idle_ticks = 0
        for tick in range(max_ticks):
            try:
                run = _ACTIVE_RUNS.get(run_id) or load_run(run_id)
            except Exception:  # noqa: BLE001
                run = None

            if run is None:
                yield f"data: {json.dumps({'error': 'run_not_found', 'run_id': run_id})}\n\n"
                return

            is_task_running = _is_step_running(run_id)
            is_step_running_in_model = any(
                s.status == ProtocolStepStatus.RUNNING for s in run.steps
            )
            is_running = (
                is_task_running
                or is_step_running_in_model
                or run.orchestration_status == ORCH_RUNNING
            )

            step_payloads = [
                {
                    "step_id": s.step_id,
                    "title": s.title,
                    "status": s.status,
                    "progress_percent": s.progress_percent,
                    "execution_mode": s.execution_mode,
                    "duration_seconds": s.duration_seconds,
                    "log_lines": s.log_lines[-15:] if s.log_lines else [],
                    "stdout": (s.stdout or "")[-800:],
                    "stderr": (s.stderr or "")[-200:],
                    "error_message": s.error_message,
                    "artifact_paths": s.artifact_paths,
                    "log_file_path": s.log_file_path,
                }
                for s in run.steps
            ]

            try:
                safety = _safety_summary()
            except Exception:  # noqa: BLE001
                safety = {}

            payload = {
                "run_id": run_id,
                "overall_status": run.overall_status(),
                "current_step_id": run.current_step_id,
                "is_running": is_running,
                "steps": step_payloads,
                "orchestration_status": run.orchestration_status,
                "orchestration_stop_reason": run.orchestration_stop_reason,
                "auto_advance": run.auto_advance,
                "safety": {
                    "closed_loop_allowed": False,
                    "state_id": safety.get("state_id"),
                },
                "tick": tick,
                "closed_loop_allowed": False,
            }

            yield f"data: {json.dumps(payload, default=str)}\n\n"

            if not is_running:
                idle_ticks += 1
                if idle_ticks >= 2:
                    done_payload = json.dumps(
                        {"done": True, "run_id": run_id, "closed_loop_allowed": False}
                    )
                    yield f"data: {done_payload}\n\n"
                    return
            else:
                idle_ticks = 0

            await asyncio.sleep(1.0)

        yield f"data: {json.dumps({'timeout': True, 'run_id': run_id})}\n\n"

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/protocol-runs/{run_id}/complete")
async def api_complete_run(run_id: str) -> dict:
    """Mark a protocol run as complete and finalise the report.

    Rejects with 409 if a step or orchestration is currently executing.
    """
    run = _get_active_run(run_id)

    if _is_step_running(run_id):
        raise HTTPException(
            status_code=409,
            detail={
                "error": "step_running",
                "message": (
                    "Cannot complete run while a step or orchestration is executing. "
                    "Wait for it to finish or stop it first."
                ),
                "current_step_id": run.current_step_id,
                "orchestration_status": run.orchestration_status,
            },
        )

    run.completed_at = datetime.now(timezone.utc).isoformat()
    run.status = run.overall_status()
    run.safety_summary = _safety_summary()

    try:
        ev, _ = get_cached_report_evidence()
        run.evidence_summary = ev.to_dict()
    except Exception:  # noqa: BLE001
        pass

    # Generate completion report v2 on manual complete
    if not run.final_report_generated:
        try:
            protocol = get_protocol(run.protocol_id)
            run_dir = generate_completion_report(run, protocol)
            run.protocol_completion_report_path = str(
                run_dir / "protocol_completion_report.json"
            )
            run.final_report_path = str(run_dir / "protocol_run.json")
            run.final_report_generated = True
            run.final_report_generation_reason = "Generated on manual complete"
        except Exception:  # noqa: BLE001
            pass

    run.touch()
    save_run(run)

    return {
        "run_id": run_id,
        "status": run.status,
        "overall_status": run.overall_status(),
        "final_report_path": run.final_report_path,
        "protocol_completion_report_path": run.protocol_completion_report_path,
        "auto_completed": run.auto_completed,
        "final_report_generated": run.final_report_generated,
        "safety_summary": run.safety_summary,
        "orchestration_status": run.orchestration_status,
        "closed_loop_allowed": False,
        "note": (
            "Closed-loop from real EEG is disabled by default. "
            "The corridor is not a decoded mental image."
        ),
    }


@router.get("/protocol-runs/{run_id}/completion-report")
async def api_get_completion_report(run_id: str) -> dict:
    """Return the completion report v2 for a specific protocol run."""
    run = _get_active_run(run_id)
    if not run.protocol_completion_report_path:
        raise HTTPException(
            status_code=404,
            detail=(
                "Completion report v2 not yet generated for this run. "
                "Complete the run or use run-all on a supported protocol."
            ),
        )
    from pathlib import Path  # noqa: PLC0415

    report_file = Path(run.protocol_completion_report_path)
    if not report_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Completion report file missing: {run.protocol_completion_report_path}",
        )
    report_data = json.loads(report_file.read_text())
    return {**report_data, "closed_loop_allowed": False}


@router.get("/protocol-runs/{run_id}/report")
async def api_get_run_report(run_id: str) -> dict:
    """Return the full protocol run report as JSON."""
    run = _get_active_run(run_id)
    safety = _safety_summary()
    return {
        **run.model_dump(),
        "overall_status": run.overall_status(),
        "safety_summary": safety,
        "closed_loop_allowed": False,
        "scientific_disclaimer": run.scientific_disclaimer,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
