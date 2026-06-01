"""Run a NeuroVerse protocol from the command line.

Usage:
    python3 scripts/run_protocol.py <protocol_id> [--inputs KEY=VALUE ...]
    python3 scripts/run_protocol.py synthetic_demo_protocol --run-all
    python3 scripts/run_protocol.py brainflow_synthetic_shadow_protocol --run-all
    python3 scripts/run_protocol.py safety_audit_only_protocol --run-all
    python3 scripts/run_protocol.py physical_openbci_trial_protocol --preflight
    python3 scripts/run_protocol.py physical_openbci_trial_protocol \\
        --inputs PORT=/dev/ttyUSB0 --run-all
"""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

_SEP = "=" * 60


# ---------------------------------------------------------------------------
#  Preflight printer
# ---------------------------------------------------------------------------


def _print_preflight(protocol_id: str, inputs: dict[str, str]) -> None:
    from app.protocols.models import ProtocolMode  # noqa: PLC0415
    from app.protocols.registry import get_protocol  # noqa: PLC0415

    protocol = get_protocol(protocol_id)
    if protocol is None:
        print(f"ERROR: Protocol '{protocol_id}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"\n{_SEP}")
    print(f"PREFLIGHT: {protocol.title}")
    print(_SEP)
    print(f"Mode:             {protocol.mode}")
    print(f"Auto-run policy:  {protocol.auto_run_policy}")
    print(f"Demo recommended: {protocol.reviewer_demo_recommended}")

    blocking_issues: list[str] = []
    manual_steps: list[str] = []
    executable_steps: list[str] = []

    for inp in protocol.required_inputs:
        if not inputs.get(inp):
            blocking_issues.append(f"Required input missing: {inp}")

    if protocol.mode == ProtocolMode.PHYSICAL_HARDWARE and not inputs.get("PORT"):
        if not any("PORT" in b for b in blocking_issues):
            blocking_issues.append("Physical hardware protocol requires PORT input.")

    for step in protocol.steps:
        if step.action == "manual_command_required":
            manual_steps.append(step.step_id)
        elif step.required_inputs and any(not inputs.get(i) for i in step.required_inputs):
            manual_steps.append(step.step_id)
        else:
            executable_steps.append(step.step_id)

    can_start = len(blocking_issues) == 0
    can_auto_run = (
        can_start
        and protocol.supports_auto_run
        and protocol.auto_run_policy != "disabled"
        and len(executable_steps) > 0
    )

    print(f"\nCan start:    {'YES ✓' if can_start else 'NO ✗'}")
    print(f"Can auto-run: {'YES ✓' if can_auto_run else 'NO ✗'}")

    if blocking_issues:
        print("\nBLOCKING ISSUES:")
        for issue in blocking_issues:
            print(f"  ✗ {issue}")

    if executable_steps:
        print(f"\nExecutable steps ({len(executable_steps)}):")
        for s in executable_steps:
            print(f"  ✓ {s}")
    if manual_steps:
        print(f"\nManual steps ({len(manual_steps)}):")
        for s in manual_steps:
            print(f"  ⚙ {s}")

    print(f"\nclosed_loop_allowed: false (always)")
    print(_SEP)


# ---------------------------------------------------------------------------
#  Step executor (sync CLI wrapper around async runner)
# ---------------------------------------------------------------------------


def _run_steps_sequential(run, protocol, *, run_all: bool = False) -> None:
    import asyncio  # noqa: PLC0415

    from app.protocols.models import ProtocolStepResult, ProtocolStepStatus  # noqa: PLC0415
    from app.protocols.runner import execute_step_async  # noqa: PLC0415
    from app.protocols.storage import save_run  # noqa: PLC0415

    async def _run() -> None:
        for step_def in protocol.steps:
            step_result = next(
                (s for s in run.steps if s.step_id == step_def.step_id), None
            )
            if step_result is None:
                step_result = ProtocolStepResult(
                    step_id=step_def.step_id, title=step_def.title
                )
                run.steps.append(step_result)

            if step_result.status == ProtocolStepStatus.PASSED:
                print(f"  [{step_def.step_id}] SKIP (already passed)")
                continue

            print(f"  [{step_def.step_id}] {step_def.title}...", end="", flush=True)

            if run_all and step_def.action == "manual_command_required":
                await execute_step_async(run, step_def, step_result, pre_started=False)
                print(" ⚙ MANUAL")
                if step_result.manual_command:
                    print(f"    Run: {step_result.manual_command}")
                print("  Auto-run stopping at manual step.")
                save_run(run)
                return

            await execute_step_async(run, step_def, step_result, pre_started=False)

            status = step_result.status
            dur = (
                f" [{step_result.duration_seconds:.1f}s]"
                if step_result.duration_seconds
                else ""
            )
            print(f" {status}{dur}")

            if step_result.manual_command:
                print(f"    ⚙ Manual: {step_result.manual_command}")
            if step_result.error_message:
                print(f"    ✗ Error: {step_result.error_message}")
            for p in step_result.artifact_paths:
                print(f"    ✓ Artifact: {p}")

            save_run(run)

            if run_all and status == ProtocolStepStatus.FAILED:
                print("  Auto-run stopping on failure.")
                return
            if run_all and status == ProtocolStepStatus.BLOCKED:
                print("  Auto-run stopping on blocked step.")
                return

    asyncio.run(_run())


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run a NeuroVerse protocol")
    parser.add_argument("protocol_id", help="Protocol ID to run")
    parser.add_argument(
        "--inputs",
        nargs="*",
        default=[],
        help="KEY=VALUE pairs (e.g. PORT=/dev/ttyUSB0)",
    )
    parser.add_argument(
        "--run-all",
        action="store_true",
        help=(
            "Auto-advance through executable steps. "
            "Stops cleanly at manual/blocked/failed steps."
        ),
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Run preflight checks and print result without executing any steps.",
    )
    parser.add_argument("--output", default=None, help="Output directory for run report")
    args = parser.parse_args()

    inputs: dict[str, str] = {}
    for kv in args.inputs or []:
        if "=" in kv:
            k, v = kv.split("=", 1)
            inputs[k.strip()] = v.strip()

    from app.protocols.registry import get_protocol, list_protocols  # noqa: PLC0415
    from app.protocols.models import ProtocolRun, ProtocolStepResult, ProtocolMode  # noqa: PLC0415
    from app.protocols.storage import save_run  # noqa: PLC0415

    protocol = get_protocol(args.protocol_id)
    if protocol is None:
        print(f"ERROR: Protocol '{args.protocol_id}' not found.", file=sys.stderr)
        print(
            "Available: " + ", ".join(p.protocol_id for p in list_protocols()),
            file=sys.stderr,
        )
        sys.exit(1)

    # Preflight-only mode
    if args.preflight:
        _print_preflight(args.protocol_id, inputs)
        sys.exit(0)

    # Block physical hardware without PORT
    if protocol.mode == ProtocolMode.PHYSICAL_HARDWARE and not inputs.get("PORT"):
        print(
            f"ERROR: Protocol '{args.protocol_id}' requires PORT=<serial_port>.\n"
            f"Example: python3 scripts/run_protocol.py {args.protocol_id} "
            f"--inputs PORT=/dev/ttyUSB0",
            file=sys.stderr,
        )
        sys.exit(1)

    # Reject --run-all on disabled protocols
    if args.run_all and not protocol.supports_auto_run:
        print(
            f"ERROR: Protocol '{args.protocol_id}' does not support auto-run "
            f"(auto_run_policy={protocol.auto_run_policy}).\n"
            f"Remove --run-all or run steps individually.",
            file=sys.stderr,
        )
        sys.exit(1)

    run_id = (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + str(uuid.uuid4())[:8]
    )
    steps = [ProtocolStepResult(step_id=s.step_id, title=s.title) for s in protocol.steps]
    run = ProtocolRun(
        run_id=run_id,
        protocol_id=protocol.protocol_id,
        protocol_title=protocol.title,
        mode=protocol.mode,
        steps=steps,
        inputs=inputs,
        closed_loop_allowed=False,
    )

    print(f"\n{_SEP}")
    print(f"Protocol: {protocol.title}")
    print(f"Run ID:   {run_id}")
    print(f"Mode:     {protocol.mode}")
    print(f"Steps:    {len(protocol.steps)}")
    print(f"Run-all:  {args.run_all}")
    print(f"{_SEP}\n")

    _run_steps_sequential(run, protocol, run_all=args.run_all)

    # Refresh evidence
    try:
        from app.safety.report_status import (  # noqa: PLC0415
            get_cached_report_evidence,
            invalidate_report_evidence_cache,
        )

        invalidate_report_evidence_cache("protocol_run_complete")
        ev, _ = get_cached_report_evidence(force_refresh=True)
        run.evidence_summary = ev.to_dict()
    except Exception:
        pass

    run.completed_at = datetime.now(timezone.utc).isoformat()
    run.status = run.overall_status()
    run_dir = save_run(run)

    # Auto-complete and generate completion report v2 if all steps passed
    if args.run_all and run.orchestration_status in ("", "idle", None):
        from app.protocols.storage import generate_completion_report, update_latest_auto_run_evidence  # noqa: PLC0415

        if run.overall_status().value == "passed":
            run.auto_completed = True
            run.auto_completed_at = run.completed_at
            run.final_report_generated = True
            run.final_report_generation_reason = (
                "Auto-completed after successful --run-all CLI execution"
            )
            try:
                crd = generate_completion_report(run, protocol)
                run.protocol_completion_report_path = str(
                    crd / "protocol_completion_report.json"
                )
                run.final_report_path = str(crd / "protocol_run.json")
                run_dir = save_run(run)
                update_latest_auto_run_evidence(run)
            except Exception:
                pass

    print(f"\n{_SEP}")
    print(f"Overall status:      {run.overall_status()}")
    print(f"Report:              {run_dir / 'protocol_run.json'}")
    if run.protocol_completion_report_path:
        print(f"Completion report:   {run.protocol_completion_report_path}")
    if run.auto_completed:
        print(f"Auto-completed:      true")
        print(f"Evidence:            evidence_pack/latest_auto_run_protocol.json")
    print(f"closed_loop_allowed: false (always)")
    print(_SEP)


if __name__ == "__main__":
    main()
