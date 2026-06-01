"""Protocol run persistence — stores ProtocolRun to disk as JSON and Markdown."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.protocols.models import ProtocolRun, ProtocolStepStatus

_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # repo root
PROTOCOL_RUNS_DIR = _ROOT / "reports" / "protocol_runs"
PROTOCOL_RUNS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
#  Persistence
# ---------------------------------------------------------------------------


def save_run(run: ProtocolRun) -> Path:
    """Write run to disk. Creates run directory if needed."""
    run_dir = PROTOCOL_RUNS_DIR / run.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Primary JSON
    (run_dir / "protocol_run.json").write_text(run.model_dump_json(indent=2), encoding="utf-8")

    # Step results JSON
    (run_dir / "step_results.json").write_text(
        json.dumps([s.model_dump() for s in run.steps], indent=2), encoding="utf-8"
    )

    # Artifacts manifest
    artifacts: dict[str, list[str]] = {}
    for step in run.steps:
        if step.artifact_paths:
            artifacts[step.step_id] = step.artifact_paths
    (run_dir / "artifacts_manifest.json").write_text(
        json.dumps(artifacts, indent=2), encoding="utf-8"
    )

    # Markdown summary
    (run_dir / "protocol_run.md").write_text(_build_markdown(run), encoding="utf-8")

    return run_dir


def load_run(run_id: str) -> ProtocolRun | None:
    run_file = PROTOCOL_RUNS_DIR / run_id / "protocol_run.json"
    if not run_file.exists():
        return None
    try:
        return ProtocolRun.model_validate_json(run_file.read_text())
    except Exception:
        return None


def list_runs() -> list[dict[str, Any]]:
    result = []
    for d in sorted(PROTOCOL_RUNS_DIR.iterdir(), reverse=True):
        if not d.is_dir():
            continue
        run_file = d / "protocol_run.json"
        if not run_file.exists():
            continue
        try:
            data = json.loads(run_file.read_text())
            result.append(
                {
                    "run_id": data.get("run_id"),
                    "protocol_id": data.get("protocol_id"),
                    "protocol_title": data.get("protocol_title"),
                    "mode": data.get("mode"),
                    "status": data.get("status"),
                    "created_at": data.get("created_at"),
                    "completed_at": data.get("completed_at"),
                }
            )
        except Exception:
            continue
    return result


# ---------------------------------------------------------------------------
#  Markdown report builder
# ---------------------------------------------------------------------------


def _status_emoji(status: str) -> str:
    return {
        ProtocolStepStatus.PASSED: "✓",
        ProtocolStepStatus.FAILED: "✗",
        ProtocolStepStatus.SKIPPED: "—",
        ProtocolStepStatus.BLOCKED: "⊘",
        ProtocolStepStatus.MANUAL_COMMAND_REQUIRED: "⚙",
        ProtocolStepStatus.RUNNING: "▷",
        ProtocolStepStatus.PENDING: "○",
    }.get(status, "?")


def _build_markdown(run: ProtocolRun) -> str:
    lines: list[str] = [
        f"# NeuroVerse Protocol Run: {run.protocol_title}",
        f"\n**Run ID:** `{run.run_id}`  ",
        f"**Protocol:** `{run.protocol_id}`  ",
        f"**Mode:** `{run.mode}`  ",
        f"**Created:** {run.created_at}  ",
        f"**Status:** `{run.overall_status()}`",
        "",
        f"> {run.scientific_disclaimer}",
        "",
        "---",
        "",
        "## Steps",
        "",
        "| # | Step | Status | Notes |",
        "| --- | --- | --- | --- |",
    ]

    for i, step in enumerate(run.steps, 1):
        icon = _status_emoji(step.status)
        notes = step.notes or step.error_message or step.block_reason or ""
        notes = notes[:80].replace("|", "\\|")
        lines.append(f"| {i} | {step.title} | {icon} `{step.status}` | {notes} |")

    lines += ["", "---", "", "## Artifacts", ""]
    has_artifacts = False
    for step in run.steps:
        for p in step.artifact_paths:
            lines.append(f"- `{p}`")
            has_artifacts = True
    if not has_artifacts:
        lines.append("No artifacts generated yet.")

    lines += ["", "---", "", "## Safety Summary", ""]
    if run.safety_summary:
        gov = run.safety_summary.get("governance", {})
        lines.append(f"- **Closed-loop allowed:** `{gov.get('closed_loop_allowed', False)}`")
        lock_reasons = gov.get("lock_reasons", [])
        if lock_reasons:
            lines.append("\n**Lock reasons:**")
            for r in lock_reasons:
                lines.append(f"  - {r}")
    else:
        lines.append("Safety summary not yet generated.")

    # Manual commands
    manual_steps = [s for s in run.steps if s.manual_command]
    if manual_steps:
        lines += ["", "---", "", "## Manual Commands Required", ""]
        for step in manual_steps:
            lines.append(f"**{step.title}:**")
            lines.append(f"```bash\n{step.manual_command}\n```")
            lines.append("")

    lines += [
        "---",
        "",
        "## Scientific Limitations",
        "",
        run.scientific_disclaimer,
        "",
        "---",
        "*Generated by NeuroVerse Protocol Engine v1*",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
#  Completion report v2
# ---------------------------------------------------------------------------

_PROVES_BY_MODE: dict[str, list[str]] = {
    "simulated": [
        "Full pipeline validated end-to-end with built-in biosignal simulator.",
        "Safety gate confirmed: real EEG closed-loop adaptation blocked by default.",
        "Protocol orchestration, background task execution, and evidence aggregation "
        "all function correctly.",
        "No hardware required — fully reproducible in any environment.",
    ],
    "brainflow_synthetic": [
        "BrainFlow SyntheticBoard integration through the acquisition layer.",
        "Hardware ingestion pipeline validated end-to-end with synthetic EEG.",
        "Safety gate confirmed: no closed-loop adaptation emitted.",
        "Calibration and shadow inference run correctly on synthetic board data.",
    ],
    "replay": [
        "LSL replay stream ingested and validated (timing, jitter, markers).",
        "Shadow inference runs over replayed EEG without emitting adaptation actions.",
        "Safety gate confirmed throughout replay session.",
    ],
    "physical_hardware": [
        "Physical OpenBCI hardware pipeline exercised in record-only shadow mode.",
        "Safety gate confirmed: no real closed-loop adaptation emitted.",
    ],
}

_NOT_PROVES_COMMON = [
    "Clinical performance or mental-state inference accuracy.",
    "Closed-loop adaptation (explicitly locked by safety gate at all times).",
    "Thought reading or dream decoding of any kind.",
]

_NOT_PROVES_BY_MODE: dict[str, list[str]] = {
    "simulated": [
        "Real EEG neural dynamics — signals are fully synthesized.",
        "Physical device integration or real hardware performance.",
    ] + _NOT_PROVES_COMMON,
    "brainflow_synthetic": [
        "Real OpenBCI/Galea hardware performance (BrainFlow SyntheticBoard only).",
        "Real EEG signals (synthetic data generator).",
    ] + _NOT_PROVES_COMMON,
    "replay": [
        "Real-time unseen EEG performance — data is pre-recorded PhysioNet.",
        "Generalization to new subjects (controlled dataset labels only).",
    ] + _NOT_PROVES_COMMON,
    "physical_hardware": [
        "Clinical performance — physical trial is a sanity check only.",
        "Generalization to other devices or subjects.",
    ] + _NOT_PROVES_COMMON,
}


def generate_completion_report(run: ProtocolRun, protocol: Any = None) -> Path:
    """Write completion report v2 (JSON + Markdown) to the run directory.

    Returns the run directory path.
    """
    run_dir = PROTOCOL_RUNS_DIR / run.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    mode_key = str(run.mode).split(".")[-1].lower()
    proves = _PROVES_BY_MODE.get(mode_key, ["Protocol steps executed and evidence collected."])
    not_proves = _NOT_PROVES_BY_MODE.get(mode_key, _NOT_PROVES_COMMON)

    # Build step timeline
    step_timeline = []
    all_artifacts: list[str] = []
    for step in run.steps:
        step_timeline.append(
            {
                "step_id": step.step_id,
                "title": step.title,
                "status": step.status,
                "started_at": step.started_at,
                "completed_at": step.completed_at,
                "duration_seconds": step.duration_seconds,
                "execution_mode": step.execution_mode,
                "artifact_paths": step.artifact_paths,
                "log_file_path": step.log_file_path,
                "error_message": step.error_message,
                "block_reason": step.block_reason,
                "manual_command": step.manual_command,
            }
        )
        all_artifacts.extend(step.artifact_paths)

    report_data: dict[str, Any] = {
        "run_id": run.run_id,
        "protocol_id": run.protocol_id,
        "protocol_title": run.protocol_title,
        "mode": mode_key,
        "status": run.overall_status().value,  # always a plain string e.g. "passed"
        "auto_completed": run.auto_completed,
        "auto_completed_at": run.auto_completed_at,
        "orchestration_status": run.orchestration_status,
        "orchestration_stop_reason": run.orchestration_stop_reason,
        "closed_loop_allowed": False,
        "created_at": run.created_at,
        "completed_at": run.completed_at,
        "step_timeline": step_timeline,
        "all_artifacts": all_artifacts,
        "artifact_count": len(all_artifacts),
        "safety_summary": run.safety_summary,
        "evidence_summary": run.evidence_summary,
        "what_this_proves": proves,
        "what_this_does_not_prove": not_proves,
        "scientific_disclaimer": run.scientific_disclaimer,
        "scientific_limitations": (
            protocol.scientific_limitations if protocol else ""
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "report_version": "2",
    }

    json_path = run_dir / "protocol_completion_report.json"
    json_path.write_text(
        json.dumps(report_data, indent=2, default=str), encoding="utf-8"
    )

    md_path = run_dir / "protocol_completion_report.md"
    md_path.write_text(
        _build_completion_report_md(report_data, run), encoding="utf-8"
    )

    return run_dir


def _build_completion_report_md(data: dict[str, Any], run: ProtocolRun) -> str:
    overall = data["status"]
    auto_tag = "✓ Auto-completed" if data["auto_completed"] else "— Not auto-completed"
    lines = [
        "# NeuroVerse Protocol Completion Report v2",
        "",
        f"**Protocol:** {data['protocol_title']}  ",
        f"**Run ID:** `{data['run_id']}`  ",
        f"**Mode:** `{data['mode']}`  ",
        f"**Status:** `{overall}` {'✓' if overall == 'passed' else '✗'}  ",
        f"**Auto-Completed:** {auto_tag}  ",
        "**Closed-Loop Allowed:** `false` 🔒  ",
        f"**Generated:** {data['generated_at']}  ",
        "",
        f"> {run.scientific_disclaimer}",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
        f"Protocol **{data['protocol_title']}** ran in **{data['mode']}** mode.",
        f"Overall status: **{overall}**.",
        f"Orchestration: **{data['orchestration_status']}**.",
    ]
    if data.get("orchestration_stop_reason"):
        lines.append(f"Stop reason: {data['orchestration_stop_reason']}")
    lines += [
        "",
        "---",
        "",
        "## 2. Step Timeline",
        "",
        "| # | Step | Status | Duration | Mode |",
        "| --- | --- | --- | --- | --- |",
    ]
    for i, step in enumerate(data["step_timeline"], 1):
        status = step["status"]
        icon = {"passed": "✓", "failed": "✗", "blocked": "⊘",
                "manual_command_required": "⚙", "skipped": "—"}.get(status, "○")
        dur = (
            f"{step['duration_seconds']:.1f}s"
            if step.get("duration_seconds") is not None
            else "—"
        )
        mode = step.get("execution_mode") or "—"
        lines.append(
            f"| {i} | {step['title']} | {icon} `{status}` | {dur} | {mode} |"
        )

    lines += ["", "---", "", "## 3. Generated Artifacts", ""]
    if data["all_artifacts"]:
        for p in data["all_artifacts"]:
            lines.append(f"- `{p}`")
    else:
        lines.append("No artifacts generated.")

    lines += ["", "---", "", "## 4. Safety Summary", ""]
    gov = (data.get("safety_summary") or {}).get("governance", {})
    lines += [
        f"- **Closed-loop allowed:** `{gov.get('closed_loop_allowed', False)}`",
        f"- **Safety state:** `{(data.get('safety_summary') or {}).get('state_id', 'UNKNOWN')}`",
    ]
    lock_reasons = gov.get("lock_reasons", [])
    if lock_reasons:
        lines.append("- **Lock reasons:**")
        for r in lock_reasons:
            lines.append(f"  - {r}")

    lines += ["", "---", "", "## 5. What This Run Proves", ""]
    for item in data["what_this_proves"]:
        lines.append(f"- ✓ {item}")

    lines += ["", "---", "", "## 6. What This Run Does Not Prove", ""]
    for item in data["what_this_does_not_prove"]:
        lines.append(f"- ✗ {item}")

    lines += [
        "",
        "---",
        "",
        "## 7. Scientific Limitations",
        "",
        data.get("scientific_limitations") or run.scientific_disclaimer,
        "",
        "---",
        "",
        "*Generated by NeuroVerse Protocol Engine v2*",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
#  Latest auto-run evidence (written to evidence_pack/)
# ---------------------------------------------------------------------------

_EVIDENCE_PACK_DIR = _ROOT / "evidence_pack"


def update_latest_auto_run_evidence(run: ProtocolRun) -> None:
    """Write latest auto-run summary to evidence_pack/ for Evidence Center consumption."""
    _EVIDENCE_PACK_DIR.mkdir(parents=True, exist_ok=True)

    step_summary = {
        "total": len(run.steps),
        "passed": sum(1 for s in run.steps if s.status == ProtocolStepStatus.PASSED),
        "failed": sum(1 for s in run.steps if s.status == ProtocolStepStatus.FAILED),
        "blocked": sum(1 for s in run.steps if s.status == ProtocolStepStatus.BLOCKED),
        "manual": sum(
            1
            for s in run.steps
            if s.status == ProtocolStepStatus.MANUAL_COMMAND_REQUIRED
        ),
        "skipped": sum(1 for s in run.steps if s.status == ProtocolStepStatus.SKIPPED),
    }
    all_artifacts = [p for s in run.steps for p in s.artifact_paths]
    mode_key = str(run.mode).split(".")[-1].lower()

    evidence: dict[str, Any] = {
        "run_id": run.run_id,
        "protocol_id": run.protocol_id,
        "protocol_title": run.protocol_title,
        "mode": mode_key,
        "status": run.overall_status().value,  # always a plain string e.g. "passed"
        "auto_completed": run.auto_completed,
        "auto_completed_at": run.auto_completed_at,
        "final_report_generated": run.final_report_generated,
        "final_report_path": run.final_report_path,
        "protocol_completion_report_path": run.protocol_completion_report_path,
        "orchestration_status": run.orchestration_status,
        "closed_loop_allowed": False,
        "created_at": run.created_at,
        "completed_at": run.completed_at,
        "step_summary": step_summary,
        "artifact_paths": all_artifacts,
        "artifact_count": len(all_artifacts),
        "what_this_proves": _PROVES_BY_MODE.get(
            mode_key, ["Protocol steps executed successfully."]
        ),
        "what_this_does_not_prove": _NOT_PROVES_BY_MODE.get(mode_key, _NOT_PROVES_COMMON),
        "scientific_disclaimer": run.scientific_disclaimer,
        "safety_summary": run.safety_summary,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    (_EVIDENCE_PACK_DIR / "latest_auto_run_protocol.json").write_text(
        json.dumps(evidence, indent=2, default=str), encoding="utf-8"
    )
    (_EVIDENCE_PACK_DIR / "latest_auto_run_protocol.md").write_text(
        _build_latest_auto_run_md(evidence), encoding="utf-8"
    )


def _build_latest_auto_run_md(ev: dict[str, Any]) -> str:
    lines = [
        "# NeuroVerse Latest Auto-Run Protocol Evidence",
        "",
        f"**Protocol:** {ev['protocol_title']}  ",
        f"**Run ID:** `{ev['run_id']}`  ",
        f"**Mode:** `{ev['mode']}`  ",
        f"**Status:** `{ev['status']}`  ",
        f"**Auto-Completed:** `{ev['auto_completed']}`  ",
        "**Closed-Loop Allowed:** `false` 🔒  ",
        f"**Generated:** {ev['generated_at']}  ",
        "",
        f"> {ev['scientific_disclaimer']}",
        "",
        "---",
        "",
        "## Step Summary",
        "",
        f"- Total: {ev['step_summary']['total']}",
        f"- Passed: {ev['step_summary']['passed']}",
        f"- Failed: {ev['step_summary']['failed']}",
        f"- Blocked: {ev['step_summary']['blocked']}",
        f"- Manual: {ev['step_summary']['manual']}",
        "",
        "---",
        "",
        "## What This Run Proves",
        "",
    ]
    for item in ev.get("what_this_proves", []):
        lines.append(f"- ✓ {item}")
    lines += ["", "---", "", "## What This Run Does Not Prove", ""]
    for item in ev.get("what_this_does_not_prove", []):
        lines.append(f"- ✗ {item}")
    lines += [
        "",
        "---",
        "",
        "## Artifacts",
        "",
    ]
    for p in ev.get("artifact_paths", []):
        lines.append(f"- `{p}`")
    if not ev.get("artifact_paths"):
        lines.append("No artifacts.")
    lines += [
        "",
        "---",
        "",
        "*Generated by NeuroVerse Evidence Engine*",
    ]
    return "\n".join(lines)


def find_latest_auto_run() -> dict[str, Any] | None:
    """Return the latest auto-completed protocol run data dict, or None."""
    if not PROTOCOL_RUNS_DIR.exists():
        return None
    for d in sorted(PROTOCOL_RUNS_DIR.iterdir(), reverse=True):
        run_file = d / "protocol_run.json"
        if not run_file.exists():
            continue
        try:
            data = json.loads(run_file.read_text())
            if data.get("auto_completed") is True:
                completion_path = d / "protocol_completion_report.json"
                data["_completion_report_path"] = (
                    str(completion_path) if completion_path.exists() else None
                )
                return data
        except Exception:
            continue
    return None
