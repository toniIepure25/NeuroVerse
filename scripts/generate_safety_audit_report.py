"""Generate a safety audit report for NeuroVerse.

Uses report_status.py to extract real evidence from disk artifacts, so
the governance decisions reflect actual validation/calibration/shadow
outcomes rather than conservative defaults.

Usage:
    python3 scripts/generate_safety_audit_report.py
    python3 scripts/generate_safety_audit_report.py --output reports/safety_audit/my_run

Output files:
    safety_audit_summary.json
    safety_audit_summary.md
    runtime_evidence_summary.json
    closed_loop_lock_reasons.json
    recommendations.md
    state_transitions.csv   (if runtime available)
    blocked_actions.csv     (if runtime available)
"""

from __future__ import annotations

import csv
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
#  Backend import helpers
# ---------------------------------------------------------------------------


def _ensure_backend_on_path() -> bool:
    backend_path = str(ROOT / "backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    return True


def _read_runtime_snapshot() -> dict:
    """Try to load a runtime snapshot from the safety state machine.

    Falls back to a safe default if the backend is not running.
    """
    try:
        _ensure_backend_on_path()
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance
        from app.safety.report_status import (
            get_cached_report_evidence,
            invalidate_report_evidence_cache,
        )
        from app.safety.state_machine import safety_state_machine

        # Audit always bypasses the cache to get freshest evidence
        invalidate_report_evidence_cache("safety_audit_generation")
        ev, cache_meta = get_cached_report_evidence(ROOT, force_refresh=True)
        governance = evaluate_closed_loop_governance(
            environment_flag=False,
            hardware_validated=ev.physical_hardware_validated,
            signal_quality_ok=ev.signal_quality_ok,
            timing_validated=ev.timing_ok,
            calibration_complete=ev.calibration_complete,
            shadow_inference_passed=ev.shadow_inference_passed,
            emergency_stop_active=False,
            adaptation_frozen=False,
            mode="simulated",
        )
        state = safety_state_machine.get_current_state()
        timeline = safety_state_machine.get_timeline(limit=100)
        blocked = safety_state_machine.get_blocked_actions(limit=100)
        serialized = safety_state_machine.serialize()
        return {
            "live": True,
            "state": state,
            "governance": governance.to_dict(),
            "evidence": ev.to_dict(),
            "cache_meta": cache_meta,
            "timeline": timeline,
            "blocked_actions": blocked,
            "timeline_count": serialized["timeline_count"],
            "blocked_action_count": serialized["blocked_action_count"],
        }
    except Exception as exc:
        return {
            "live": False,
            "error": str(exc),
            "state": {
                "state_id": "CLOSED_LOOP_LOCKED",
                "label": "Closed-Loop Locked",
                "description": "Real EEG closed-loop adaptation is disabled by default.",
                "severity": "blocked",
                "allowed_actions": ["record_only", "validate", "calibrate", "shadow_inference"],
                "blocked_actions": ["real_eeg_adaptation"],
            },
            "governance": {
                "closed_loop_allowed": False,
                "lock_reasons": ["Real EEG closed-loop adaptation is disabled by default."],
                "lock_reason_codes": ["closed_loop_env_disabled"],
                "required_unlock_conditions": [
                    "Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.",
                    "Complete physical hardware validation with a real device.",
                    "Achieve sustained signal quality above safety thresholds.",
                    "Complete calibration procedure.",
                    "Complete shadow inference with acceptable results.",
                    "Complete timing validation with acceptable jitter and drift.",
                ],
            },
            "evidence": {},
            "timeline": [],
            "blocked_actions": [],
            "timeline_count": 0,
            "blocked_action_count": 0,
        }


# ---------------------------------------------------------------------------
#  Report assembly
# ---------------------------------------------------------------------------


def _build_issues(runtime: dict) -> list[str]:
    ev = runtime.get("evidence", {})
    issues: list[str] = []

    if not ev.get("validation_report_present"):
        issues.append("No hardware validation report found.")
    elif not ev.get("validation_passed"):
        issues.append("Hardware validation report found but did not pass.")

    if not ev.get("calibration_complete"):
        issues.append("No calibration report found or calibration incomplete.")

    if not ev.get("shadow_inference_passed"):
        issues.append("Shadow inference has not been completed.")

    emitted = ev.get("shadow_real_actions_emitted", 0)
    if emitted and emitted > 0:
        issues.append(
            f"WARNING: Shadow mode emitted {emitted} real adaptation actions (should be 0)."
        )

    if not ev.get("lsl_live_validation_passed"):
        issues.append("No LSL live validation report found or validation failed.")

    return issues


def _build_report(runtime: dict, run_id: str) -> dict:
    state = runtime["state"]
    governance = runtime["governance"]
    ev = runtime.get("evidence", {})
    issues = _build_issues(runtime)

    return {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "safety_state": state,
        "closed_loop_governance": governance,
        "runtime_evidence": ev,
        "evidence_cache": runtime.get("cache_meta"),
        "audit_note": "Safety audit bypasses cache (force_refresh=True) for freshest evidence.",
        "runtime_available": runtime["live"],
        "timeline_transitions_recorded": runtime["timeline_count"],
        "blocked_actions_recorded": runtime["blocked_action_count"],
        "issues": issues,
        "required_steps_for_closed_loop": governance.get("required_unlock_conditions", []),
        "scientific_disclaimer": (
            "Closed-loop from real EEG is disabled by default. "
            "Hardware validation confirms stream quality and software integration; "
            "it does not validate clinical or unrestricted mental-state inference. "
            "The corridor is not a decoded mental image. "
            "It is an adaptive scaffold driven by experimental proxy metrics."
        ),
    }


def _build_markdown(report: dict) -> str:
    state = report["safety_state"]
    gov = report["closed_loop_governance"]
    ev = report.get("runtime_evidence", {})
    ts = report["generated_at"]
    run_id = report["run_id"]

    lines: list[str] = [
        "# NeuroVerse Safety Audit Report",
        f"\n**Run ID:** `{run_id}`  \n**Generated:** {ts}",
        "\n> " + report["scientific_disclaimer"],
        "\n---",
        "\n## 1. Current Safety State",
        f"\n- **State:** `{state.get('state_id', 'UNKNOWN')}`",
        f"- **Label:** {state.get('label', '—')}",
        f"- **Severity:** `{state.get('severity', '—')}`",
        f"- **Description:** {state.get('description', '—')}",
    ]

    lines += [
        "\n---",
        "\n## 2. Closed-Loop Governance",
        f"\n**Closed-loop allowed:** `{gov.get('closed_loop_allowed', False)}`",
        "\n**Lock reasons:**",
    ]
    for r in gov.get("lock_reasons", []):
        lines.append(f"- {r}")
    lines.append("\n**Required unlock conditions:**")
    for c in gov.get("required_unlock_conditions", []):
        lines.append(f"- {c}")

    lines += [
        "\n---",
        "\n## 3. Runtime Evidence Summary",
        "\n| Field | Value |",
        "| --- | --- |",
        f"| validation_report_present | {ev.get('validation_report_present', False)} |",
        f"| validation_passed | {ev.get('validation_passed', False)} |",
        f"| adapter | {ev.get('adapter', '—')} |",
        f"| brainflow_synthetic_validated | {ev.get('brainflow_synthetic_validated', False)} |",
        f"| lsl_synthetic_validated | {ev.get('lsl_synthetic_validated', False)} |",
        f"| lsl_replay_validated | {ev.get('lsl_replay_validated', False)} |",
        f"| physical_hardware_validated | {ev.get('physical_hardware_validated', False)} |",
        f"| signal_quality_ok | {ev.get('signal_quality_ok', False)} |",
        f"| signal_quality_source | {ev.get('signal_quality_source', '—')} |",
        f"| latest_sqi_mean | {ev.get('latest_sqi_mean', '—')} |",
        f"| best_sqi_mean | {ev.get('best_sqi_mean', '—')} |",
        f"| timing_ok | {ev.get('timing_ok', False)} |",
        f"| latest_jitter_p95_ms | {ev.get('latest_jitter_p95_ms', '—')} |",
        f"| best_jitter_p95_ms | {ev.get('best_jitter_p95_ms', '—')} |",
        f"| calibration_complete | {ev.get('calibration_complete', False)} |",
        f"| shadow_inference_passed | {ev.get('shadow_inference_passed', False)} |",
        f"| shadow_real_actions_emitted | {ev.get('shadow_real_actions_emitted', 0)} |",
        f"| lsl_live_validation_passed | {ev.get('lsl_live_validation_passed', False)} |",
    ]

    # Evidence sources and warnings
    sources = ev.get("evidence_sources") or []
    if sources:
        lines.append("\n**Evidence sources:**")
        for src in sources:
            lines.append(f"- `{src}`")
    warnings = ev.get("evidence_warnings") or []
    if warnings:
        lines.append("\n**Evidence warnings:**")
        for w in warnings:
            lines.append(f"- ⚠ {w}")

    lines += ["\n**Report paths:**"]
    for field in (
        "latest_validation_report_path",
        "latest_valid_validation_report_path",
        "latest_failed_validation_report_path",
        "latest_calibration_report_path",
        "latest_shadow_report_path",
        "latest_physical_trial_report_path",
        "safety_audit_report_path",
    ):
        v = ev.get(field) or "—"
        lines.append(f"- `{field}`: `{v}`")

    lines += [
        "\n---",
        "\n## 4. Issues",
    ]
    issues = report.get("issues", [])
    if issues:
        for issue in issues:
            lines.append(f"- {issue}")
    else:
        lines.append("No critical issues detected in this audit.")

    lines += [
        "\n---",
        "\n## 5. Timeline Summary",
        f"\n- Transitions recorded: {report['timeline_transitions_recorded']}",
        f"- Blocked actions recorded: {report['blocked_actions_recorded']}",
    ]
    if not report["runtime_available"]:
        lines.append(
            "\n_Note: Runtime state machine not available (backend not running). "
            "Default CLOSED_LOOP_LOCKED state used._"
        )

    lines += [
        "\n---",
        "\n## 6. Steps Required for Any Future Closed-Loop Experiment",
    ]
    for step in report.get("required_steps_for_closed_loop", []):
        lines.append(f"1. {step}")

    return "\n".join(lines)


def _build_recommendations(report: dict) -> str:
    ev = report.get("runtime_evidence", {})
    lines = [
        "# Safety Governance Recommendations",
        "\nBased on the current runtime evidence:",
    ]
    if not ev.get("validation_report_present"):
        lines.append(
            "\n- **Run hardware validation:** `make validate-brainflow-synthetic` "
            "to generate a hardware validation report."
        )
    if not ev.get("calibration_complete"):
        lines.append(
            "\n- **Run calibration:** `make calibration-brainflow-synthetic` "
            "to generate a calibration report."
        )
    if not ev.get("shadow_inference_passed"):
        lines.append(
            "\n- **Run shadow inference:** `make shadow-brainflow-synthetic` "
            "to generate a shadow inference report."
        )
    if not ev.get("lsl_live_validation_passed"):
        lines.append(
            "\n- **Run LSL validation:** `make lsl-live-validation-suite` "
            "to validate streaming quality."
        )
    if ev.get("brainflow_synthetic_validated") and not ev.get("physical_hardware_validated"):
        lines.append(
            "\n- **Note:** BrainFlow SyntheticBoard validation is present but does NOT "
            "constitute physical hardware validation. Physical device required."
        )
    lines.append(
        "\n- **Do not enable real EEG closed-loop** without completing all validation, "
        "calibration, and shadow inference steps with a physically validated device."
    )
    lines.append(
        "\n- Physical OpenBCI/Galea hardware remains unvalidated unless a real device "
        "report exists in `reports/hardware_validation/` with physical_device_detected=True."
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
#  CSV helpers
# ---------------------------------------------------------------------------


def _write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def generate_safety_audit_report(output: str | Path | None = None, *, verbose: bool = True) -> dict:
    """Generate a safety audit report and return its key paths."""
    def emit(message: str = "") -> None:
        if verbose:
            print(message)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + str(uuid.uuid4())[:8]
    output_dir = (
        Path(output).resolve()
        if output
        else ROOT / f"reports/safety_audit/{run_id}"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    emit(f"Generating safety audit report: {output_dir}")

    runtime = _read_runtime_snapshot()
    report = _build_report(runtime, run_id)

    # Write JSON summary
    summary_path = output_dir / "safety_audit_summary.json"
    summary_path.write_text(json.dumps(report, indent=2))
    emit(f"  Written: {summary_path}")

    # Write runtime evidence summary (new)
    ev_path = output_dir / "runtime_evidence_summary.json"
    ev_path.write_text(json.dumps(runtime.get("evidence", {}), indent=2))
    emit(f"  Written: {ev_path}")

    # Write Markdown summary
    md_path = output_dir / "safety_audit_summary.md"
    md_path.write_text(_build_markdown(report))
    emit(f"  Written: {md_path}")

    # Write closed-loop lock reasons
    lock_path = output_dir / "closed_loop_lock_reasons.json"
    lock_path.write_text(json.dumps(report["closed_loop_governance"], indent=2))
    emit(f"  Written: {lock_path}")

    # Write recommendations
    rec_path = output_dir / "recommendations.md"
    rec_path.write_text(_build_recommendations(report))
    emit(f"  Written: {rec_path}")

    # Write timeline CSV (if available)
    timeline = runtime.get("timeline", [])
    if timeline:
        tl_path = output_dir / "state_transitions.csv"
        _write_csv(
            tl_path,
            timeline,
            [
                "transition_id", "timestamp", "from_state", "to_state",
                "reason_code", "reason", "source", "severity", "automatic_or_manual",
            ],
        )
        emit(f"  Written: {tl_path}")

    # Write blocked-actions CSV (if available)
    blocked = runtime.get("blocked_actions", [])
    if blocked:
        ba_path = output_dir / "blocked_actions.csv"
        _write_csv(
            ba_path,
            blocked,
            [
                "record_id", "timestamp", "action_attempted", "reason_code",
                "reason", "current_state", "severity", "source",
            ],
        )
        emit(f"  Written: {ba_path}")

    # Print summary to console
    gov = report["closed_loop_governance"]
    ev = report.get("runtime_evidence", {})
    emit(f"\nSafety state: {report['safety_state'].get('state_id', 'UNKNOWN')}")
    emit(f"Closed-loop allowed: {gov.get('closed_loop_allowed', False)}")
    emit(f"Lock reasons ({len(gov.get('lock_reasons', []))}):")
    for reason in gov.get("lock_reasons", []):
        emit(f"  - {reason}")
    emit("\nEvidence summary:")
    emit(f"  validation_passed: {ev.get('validation_passed', False)}")
    emit(f"  brainflow_synthetic: {ev.get('brainflow_synthetic_validated', False)}")
    emit(f"  physical_validated: {ev.get('physical_hardware_validated', False)}")
    emit(f"  calibration_complete: {ev.get('calibration_complete', False)}")
    emit(f"  shadow_passed: {ev.get('shadow_inference_passed', False)}")
    emit(f"  signal_quality_ok: {ev.get('signal_quality_ok', False)}")
    emit(f"  timing_ok: {ev.get('timing_ok', False)}")
    issues = report.get("issues", [])
    if issues:
        emit(f"\nIssues ({len(issues)}):")
        for issue in issues:
            emit(f"  ! {issue}")
    emit(f"\nAudit report written to: {output_dir}")
    return {
        "run_id": run_id,
        "output_dir": str(output_dir),
        "summary_path": str(summary_path),
        "runtime_evidence_path": str(ev_path),
        "markdown_path": str(md_path),
        "lock_reasons_path": str(lock_path),
        "recommendations_path": str(rec_path),
        "report": report,
    }


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate NeuroVerse safety audit report")
    parser.add_argument("--output", default=None, help="Output directory")
    args = parser.parse_args()
    generate_safety_audit_report(args.output)


if __name__ == "__main__":
    main()
