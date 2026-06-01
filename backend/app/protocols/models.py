"""Pydantic models for NeuroVerse protocol engine."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ProtocolMode(str, Enum):
    SIMULATED = "simulated"
    REPLAY = "replay"
    BRAINFLOW_SYNTHETIC = "brainflow_synthetic"
    PHYSICAL_HARDWARE = "physical_hardware"


class ProtocolStepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    MANUAL_COMMAND_REQUIRED = "manual_command_required"


# Orchestration status values (string literals, not Enum, for simpler serialisation)
ORCH_IDLE = "idle"
ORCH_RUNNING = "running"
ORCH_STOPPED_MANUAL = "stopped_manual_required"
ORCH_STOPPED_BLOCKED = "stopped_blocked"
ORCH_STOPPED_FAILED = "stopped_failed"
ORCH_COMPLETED = "completed"
ORCH_CANCELLED = "cancelled"


class ProtocolStepDefinition(BaseModel):
    """Immutable definition of a single step within a protocol."""

    step_id: str
    title: str
    description: str
    action: str  # internal_function | subprocess_script | manual_command_required
    command: str | None = None
    required_inputs: list[str] = Field(default_factory=list)
    optional: bool = False
    produces_artifact: str | None = None
    notes: str | None = None


class ProtocolDefinition(BaseModel):
    """Immutable definition of a protocol."""

    protocol_id: str
    title: str
    description: str
    mode: ProtocolMode
    steps: list[ProtocolStepDefinition]
    required_inputs: list[str] = Field(default_factory=list)
    generated_artifacts: list[str] = Field(default_factory=list)
    safety_requirements: list[str] = Field(default_factory=list)
    closed_loop_allowed_default: bool = False
    scientific_limitations: str = ""
    estimated_duration_seconds: int = 60
    tags: list[str] = Field(default_factory=list)
    # Auto-run metadata
    supports_auto_run: bool = False
    # full | until_manual_step | disabled
    auto_run_policy: str = "disabled"
    reviewer_demo_recommended: bool = False


class PreflightResult(BaseModel):
    """Result of a protocol preflight check."""

    protocol_id: str
    can_start: bool
    can_auto_run: bool
    blocking_issues: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    manual_steps: list[str] = Field(default_factory=list)
    executable_steps: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    closed_loop_allowed: bool = False
    safety_summary: dict[str, Any] | None = None
    # Convenience labels for frontend
    auto_run_label: str = ""
    auto_run_policy: str = "disabled"
    reviewer_demo_recommended: bool = False


class ProtocolStepResult(BaseModel):
    """Mutable result of executing a single step."""

    step_id: str
    title: str
    status: ProtocolStepStatus = ProtocolStepStatus.PENDING
    started_at: str | None = None
    completed_at: str | None = None
    last_updated_at: str | None = None
    artifact_paths: list[str] = Field(default_factory=list)
    safety_state_snapshot: dict[str, Any] | None = None
    stdout: str | None = None
    stderr: str | None = None
    error_message: str | None = None
    notes: str | None = None
    manual_command: str | None = None
    block_reason: str | None = None
    progress_percent: int | None = None
    log_lines: list[str] = Field(default_factory=list)
    duration_seconds: float | None = None
    # background_task | manual_command_required | internal_function | subprocess_script
    execution_mode: str | None = None
    exit_code: int | None = None
    log_file_path: str | None = None

    def start(self, *, execution_mode: str | None = None) -> None:
        self.status = ProtocolStepStatus.RUNNING
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.last_updated_at = self.started_at
        self.execution_mode = execution_mode or "background_task"

    def touch(self, message: str | None = None) -> None:
        self.last_updated_at = datetime.now(timezone.utc).isoformat()
        if message:
            self.log_lines.append(f"[{self.last_updated_at}] {message}")

    def complete(
        self,
        *,
        passed: bool,
        artifact_paths: list[str] | None = None,
        notes: str | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
        error_message: str | None = None,
        safety_state_snapshot: dict[str, Any] | None = None,
        exit_code: int | None = None,
    ) -> None:
        self.status = ProtocolStepStatus.PASSED if passed else ProtocolStepStatus.FAILED
        self.completed_at = datetime.now(timezone.utc).isoformat()
        self.last_updated_at = self.completed_at
        self.progress_percent = 100 if passed else None
        if artifact_paths:
            self.artifact_paths = artifact_paths
        if notes:
            self.notes = notes
        if stdout:
            self.stdout = stdout
        if stderr:
            self.stderr = stderr
        if error_message:
            self.error_message = error_message
        if safety_state_snapshot:
            self.safety_state_snapshot = safety_state_snapshot
        if exit_code is not None:
            self.exit_code = exit_code
        if self.started_at:
            try:
                from datetime import datetime as _dt  # noqa: PLC0415

                started = _dt.fromisoformat(self.started_at)
                completed = _dt.fromisoformat(self.completed_at)
                self.duration_seconds = round((completed - started).total_seconds(), 2)
            except Exception:
                pass

    def block(self, reason: str, manual_command: str | None = None) -> None:
        self.status = ProtocolStepStatus.BLOCKED
        self.block_reason = reason
        if manual_command:
            self.manual_command = manual_command
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def mark_manual(self, manual_command: str, notes: str | None = None) -> None:
        self.status = ProtocolStepStatus.MANUAL_COMMAND_REQUIRED
        self.manual_command = manual_command
        if notes:
            self.notes = notes
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def skip(self, reason: str | None = None) -> None:
        self.status = ProtocolStepStatus.SKIPPED
        if reason:
            self.notes = reason
        self.completed_at = datetime.now(timezone.utc).isoformat()


class ProtocolRun(BaseModel):
    """A single execution run of a protocol."""

    run_id: str
    protocol_id: str
    protocol_title: str
    mode: ProtocolMode
    status: ProtocolStepStatus = ProtocolStepStatus.PENDING
    current_step_id: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None
    steps: list[ProtocolStepResult] = Field(default_factory=list)
    inputs: dict[str, str] = Field(default_factory=dict)
    safety_summary: dict[str, Any] | None = None
    evidence_summary: dict[str, Any] | None = None
    final_report_path: str | None = None
    closed_loop_allowed: bool = False
    scientific_disclaimer: str = (
        "Closed-loop from real EEG is disabled by default. "
        "Hardware validation confirms stream quality and software integration; "
        "it does not validate clinical or unrestricted mental-state inference. "
        "The corridor is not a decoded mental image. "
        "It is an adaptive scaffold driven by experimental proxy metrics."
    )
    # Orchestration state
    auto_advance: bool = False
    orchestration_status: str = ORCH_IDLE
    orchestration_started_at: str | None = None
    orchestration_completed_at: str | None = None
    orchestration_stop_reason: str | None = None
    preflight_result: dict[str, Any] | None = None
    # Auto-completion fields
    auto_completed: bool = False
    auto_completed_at: str | None = None
    protocol_completion_report_path: str | None = None
    final_report_generated: bool = False
    final_report_generation_reason: str | None = None

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def overall_status(self) -> ProtocolStepStatus:
        statuses = {s.status for s in self.steps}
        if ProtocolStepStatus.FAILED in statuses:
            return ProtocolStepStatus.FAILED
        if ProtocolStepStatus.RUNNING in statuses:
            return ProtocolStepStatus.RUNNING
        if all(
            s.status in {ProtocolStepStatus.PASSED, ProtocolStepStatus.SKIPPED}
            for s in self.steps
        ):
            return ProtocolStepStatus.PASSED
        if all(
            s.status
            in {
                ProtocolStepStatus.PASSED,
                ProtocolStepStatus.SKIPPED,
                ProtocolStepStatus.MANUAL_COMMAND_REQUIRED,
                ProtocolStepStatus.BLOCKED,
            }
            for s in self.steps
        ):
            return ProtocolStepStatus.MANUAL_COMMAND_REQUIRED
        return ProtocolStepStatus.PENDING
