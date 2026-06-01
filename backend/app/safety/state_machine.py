"""Explicit safety state machine for auditable safety governance.

The state machine is lightweight, deterministic, and testable.
Every state transition is logged to an in-memory timeline.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.safety.reason_codes import SafetyReasonCode, SafetySeverity

# ---------------------------------------------------------------------------
#  State definitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SafetyStateDefinition:
    """Immutable definition of a single safety state."""

    state_id: str
    label: str
    description: str
    severity: SafetySeverity
    allowed_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    required_conditions_to_exit: tuple[str, ...]


SAFETY_STATES: dict[str, SafetyStateDefinition] = {
    "NO_DATA": SafetyStateDefinition(
        state_id="NO_DATA",
        label="No Data",
        description="No biosignal data is available.",
        severity=SafetySeverity.INFO,
        allowed_actions=("configure", "connect_hardware", "start_simulator"),
        blocked_actions=("adapt", "calibrate", "shadow_inference"),
        required_conditions_to_exit=("Start a data source (simulator, replay, or hardware).",),
    ),
    "SIMULATED_ONLY": SafetyStateDefinition(
        state_id="SIMULATED_ONLY",
        label="Simulated Only",
        description="Running on simulated biosignals. No real EEG connected.",
        severity=SafetySeverity.INFO,
        allowed_actions=("adapt_simulated", "validate", "calibrate", "shadow_inference"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=("Connect real hardware or switch to replay.",),
    ),
    "DATA_REPLAY": SafetyStateDefinition(
        state_id="DATA_REPLAY",
        label="Data Replay",
        description="Replaying recorded or dataset EEG data.",
        severity=SafetySeverity.INFO,
        allowed_actions=("shadow_inference", "validate", "benchmark"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=("Switch to live data source.",),
    ),
    "RECORD_ONLY": SafetyStateDefinition(
        state_id="RECORD_ONLY",
        label="Record Only",
        description="Recording data without adaptation.",
        severity=SafetySeverity.INFO,
        allowed_actions=("record", "validate"),
        blocked_actions=("adapt", "shadow_inference"),
        required_conditions_to_exit=("Complete recording and proceed to validation.",),
    ),
    "VALIDATION_RUNNING": SafetyStateDefinition(
        state_id="VALIDATION_RUNNING",
        label="Validation Running",
        description="Hardware or signal validation is in progress.",
        severity=SafetySeverity.INFO,
        allowed_actions=("record",),
        blocked_actions=("adapt", "calibrate"),
        required_conditions_to_exit=("Wait for validation to complete.",),
    ),
    "VALIDATION_PASSED": SafetyStateDefinition(
        state_id="VALIDATION_PASSED",
        label="Validation Passed",
        description="Hardware or signal validation has passed.",
        severity=SafetySeverity.INFO,
        allowed_actions=("calibrate", "shadow_inference", "record"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=("Proceed to calibration or shadow inference.",),
    ),
    "VALIDATION_FAILED": SafetyStateDefinition(
        state_id="VALIDATION_FAILED",
        label="Validation Failed",
        description="Hardware or signal validation has failed.",
        severity=SafetySeverity.WARNING,
        allowed_actions=("record", "retry_validation"),
        blocked_actions=("adapt", "calibrate", "shadow_inference"),
        required_conditions_to_exit=("Fix validation issues and retry.",),
    ),
    "CALIBRATION_REQUIRED": SafetyStateDefinition(
        state_id="CALIBRATION_REQUIRED",
        label="Calibration Required",
        description="System requires calibration before shadow inference.",
        severity=SafetySeverity.WARNING,
        allowed_actions=("calibrate", "record"),
        blocked_actions=("adapt", "shadow_inference"),
        required_conditions_to_exit=("Complete calibration procedure.",),
    ),
    "CALIBRATION_RUNNING": SafetyStateDefinition(
        state_id="CALIBRATION_RUNNING",
        label="Calibration Running",
        description="Calibration procedure is in progress.",
        severity=SafetySeverity.INFO,
        allowed_actions=("record",),
        blocked_actions=("adapt",),
        required_conditions_to_exit=("Wait for calibration to complete.",),
    ),
    "CALIBRATED": SafetyStateDefinition(
        state_id="CALIBRATED",
        label="Calibrated",
        description="Calibration is complete.",
        severity=SafetySeverity.INFO,
        allowed_actions=("shadow_inference", "record"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=("Proceed to shadow inference.",),
    ),
    "SHADOW_READY": SafetyStateDefinition(
        state_id="SHADOW_READY",
        label="Shadow Ready",
        description="Ready for shadow-only inference.",
        severity=SafetySeverity.INFO,
        allowed_actions=("shadow_inference", "record"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=("Start shadow inference.",),
    ),
    "SHADOW_RUNNING": SafetyStateDefinition(
        state_id="SHADOW_RUNNING",
        label="Shadow Running",
        description="Shadow inference is running. No real adaptation actions.",
        severity=SafetySeverity.INFO,
        allowed_actions=("shadow_inference", "record", "freeze", "emergency_stop"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=("Wait for shadow inference to complete.",),
    ),
    "CLOSED_LOOP_LOCKED": SafetyStateDefinition(
        state_id="CLOSED_LOOP_LOCKED",
        label="Closed-Loop Locked",
        description="Real EEG closed-loop adaptation is disabled by default.",
        severity=SafetySeverity.BLOCKED,
        allowed_actions=("record_only", "validate", "calibrate", "shadow_inference"),
        blocked_actions=("real_eeg_adaptation",),
        required_conditions_to_exit=(
            "Validated hardware",
            "Passed signal quality",
            "Completed calibration",
            "Passed shadow inference",
            "Operator confirmation",
            "Environment flag enabled",
        ),
    ),
    "HARDWARE_UNVALIDATED": SafetyStateDefinition(
        state_id="HARDWARE_UNVALIDATED",
        label="Hardware Unvalidated",
        description="Physical hardware has not been validated.",
        severity=SafetySeverity.WARNING,
        allowed_actions=("validate", "record_only"),
        blocked_actions=("adapt", "calibrate", "shadow_inference"),
        required_conditions_to_exit=("Complete hardware validation.",),
    ),
    "SIGNAL_UNSAFE": SafetyStateDefinition(
        state_id="SIGNAL_UNSAFE",
        label="Signal Unsafe",
        description="Signal quality is below safety thresholds.",
        severity=SafetySeverity.WARNING,
        allowed_actions=("record",),
        blocked_actions=("adapt", "shadow_inference"),
        required_conditions_to_exit=("Signal quality must recover above thresholds.",),
    ),
    "SENSOR_DROPOUT": SafetyStateDefinition(
        state_id="SENSOR_DROPOUT",
        label="Sensor Dropout",
        description="One or more sensors have dropped out.",
        severity=SafetySeverity.WARNING,
        allowed_actions=("record",),
        blocked_actions=("adapt",),
        required_conditions_to_exit=("Restore sensor connections.",),
    ),
    "HIGH_UNCERTAINTY": SafetyStateDefinition(
        state_id="HIGH_UNCERTAINTY",
        label="High Uncertainty",
        description="Model prediction uncertainty is too high.",
        severity=SafetySeverity.WARNING,
        allowed_actions=("record", "shadow_inference"),
        blocked_actions=("adapt",),
        required_conditions_to_exit=("Model confidence must increase.",),
    ),
    "ADAPTATION_FROZEN": SafetyStateDefinition(
        state_id="ADAPTATION_FROZEN",
        label="Adaptation Frozen",
        description="Adaptation is frozen by operator or safety gate.",
        severity=SafetySeverity.BLOCKED,
        allowed_actions=("record", "unfreeze"),
        blocked_actions=("adapt",),
        required_conditions_to_exit=("Unfreeze adaptation.",),
    ),
    "EMERGENCY_STOP": SafetyStateDefinition(
        state_id="EMERGENCY_STOP",
        label="Emergency Stop",
        description="Emergency stop is active. All adaptation halted.",
        severity=SafetySeverity.EMERGENCY,
        allowed_actions=("record",),
        blocked_actions=("adapt", "calibrate", "shadow_inference", "unfreeze"),
        required_conditions_to_exit=("Clear emergency stop and start a new session.",),
    ),
}


# ---------------------------------------------------------------------------
#  Timeline entry
# ---------------------------------------------------------------------------


@dataclass
class SafetyTransition:
    """Record of a single state transition."""

    transition_id: str
    timestamp: str
    from_state: str
    to_state: str
    reason_code: str
    reason: str
    source: str
    session_id: str | None = None
    related_event_id: str | None = None
    related_report_path: str | None = None
    operator_action: str | None = None
    automatic_or_manual: str = "automatic"
    severity: str = "info"

    def to_dict(self) -> dict[str, Any]:
        return {
            "transition_id": self.transition_id,
            "timestamp": self.timestamp,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "reason_code": self.reason_code,
            "reason": self.reason,
            "source": self.source,
            "session_id": self.session_id,
            "related_event_id": self.related_event_id,
            "related_report_path": self.related_report_path,
            "operator_action": self.operator_action,
            "automatic_or_manual": self.automatic_or_manual,
            "severity": self.severity,
        }


# ---------------------------------------------------------------------------
#  Blocked action entry
# ---------------------------------------------------------------------------


@dataclass
class BlockedActionRecord:
    """Record of a blocked action."""

    record_id: str
    timestamp: str
    action_attempted: str
    reason_code: str
    reason: str
    current_state: str
    severity: str
    source: str
    session_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "timestamp": self.timestamp,
            "action_attempted": self.action_attempted,
            "reason_code": self.reason_code,
            "reason": self.reason,
            "current_state": self.current_state,
            "severity": self.severity,
            "source": self.source,
            "session_id": self.session_id,
        }


# ---------------------------------------------------------------------------
#  State machine
# ---------------------------------------------------------------------------


class SafetyStateMachine:
    """Explicit, auditable safety state machine.

    Manages the current safety state, records all transitions and blocked
    actions, and provides serialization for audit reports.
    """

    MAX_TIMELINE = 500
    MAX_BLOCKED = 500

    def __init__(self, initial_state: str = "NO_DATA") -> None:
        if initial_state not in SAFETY_STATES:
            initial_state = "NO_DATA"
        self._current_state_id = initial_state
        self._timeline: list[SafetyTransition] = []
        self._blocked_actions: list[BlockedActionRecord] = []
        self._session_id: str | None = None

        # Record initial transition
        self._timeline.append(
            SafetyTransition(
                transition_id=str(uuid.uuid4())[:12],
                timestamp=datetime.now(timezone.utc).isoformat(),
                from_state="INIT",
                to_state=initial_state,
                reason_code=SafetyReasonCode.NORMAL_OPERATION.value,
                reason="State machine initialized.",
                source="state_machine",
                automatic_or_manual="automatic",
                severity=SafetySeverity.INFO.value,
            )
        )

    # -- State access -------------------------------------------------------

    def get_current_state(self) -> dict[str, Any]:
        """Return the current state as a dictionary."""
        definition = SAFETY_STATES.get(self._current_state_id)
        if definition is None:
            definition = SAFETY_STATES["NO_DATA"]

        return {
            "state_id": definition.state_id,
            "label": definition.label,
            "description": definition.description,
            "severity": definition.severity.value,
            "allowed_actions": list(definition.allowed_actions),
            "blocked_actions": list(definition.blocked_actions),
            "required_conditions_to_exit": list(definition.required_conditions_to_exit),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self._session_id,
        }

    @property
    def current_state_id(self) -> str:
        return self._current_state_id

    # -- Transitions --------------------------------------------------------

    def transition_to(
        self,
        new_state: str,
        *,
        reason_code: str = "unknown",
        reason: str = "",
        source: str = "system",
        automatic_or_manual: str = "automatic",
        operator_action: str | None = None,
        related_event_id: str | None = None,
        related_report_path: str | None = None,
    ) -> dict[str, Any]:
        """Transition to a new state. Returns the transition record."""
        if new_state not in SAFETY_STATES:
            return {"error": f"Unknown state: {new_state}"}

        old_state = self._current_state_id
        if old_state == new_state:
            return {"info": f"Already in state {new_state}"}

        new_def = SAFETY_STATES[new_state]
        transition = SafetyTransition(
            transition_id=str(uuid.uuid4())[:12],
            timestamp=datetime.now(timezone.utc).isoformat(),
            from_state=old_state,
            to_state=new_state,
            reason_code=reason_code,
            reason=reason,
            source=source,
            session_id=self._session_id,
            related_event_id=related_event_id,
            related_report_path=related_report_path,
            operator_action=operator_action,
            automatic_or_manual=automatic_or_manual,
            severity=new_def.severity.value,
        )

        self._current_state_id = new_state
        self._timeline.append(transition)

        # Trim timeline
        if len(self._timeline) > self.MAX_TIMELINE:
            self._timeline = self._timeline[-self.MAX_TIMELINE :]

        return transition.to_dict()

    # -- Blocked actions ----------------------------------------------------

    def record_blocked_action(
        self,
        action_attempted: str,
        *,
        reason_code: str = "unknown",
        reason: str = "",
        source: str = "safety_gate",
    ) -> dict[str, Any]:
        """Record a blocked action."""
        definition = SAFETY_STATES.get(self._current_state_id, SAFETY_STATES["NO_DATA"])
        record = BlockedActionRecord(
            record_id=str(uuid.uuid4())[:12],
            timestamp=datetime.now(timezone.utc).isoformat(),
            action_attempted=action_attempted,
            reason_code=reason_code,
            reason=reason,
            current_state=self._current_state_id,
            severity=definition.severity.value,
            source=source,
            session_id=self._session_id,
        )
        self._blocked_actions.append(record)

        if len(self._blocked_actions) > self.MAX_BLOCKED:
            self._blocked_actions = self._blocked_actions[-self.MAX_BLOCKED :]

        return record.to_dict()

    # -- Timeline and reports -----------------------------------------------

    def get_timeline(self, limit: int = 50) -> list[dict[str, Any]]:
        """Return recent timeline entries."""
        entries = self._timeline[-limit:]
        return [t.to_dict() for t in entries]

    def get_blocked_actions(self, limit: int = 50) -> list[dict[str, Any]]:
        """Return recent blocked actions."""
        entries = self._blocked_actions[-limit:]
        return [r.to_dict() for r in entries]

    # -- Session management -------------------------------------------------

    def set_session_id(self, session_id: str | None) -> None:
        self._session_id = session_id

    # -- Reset --------------------------------------------------------------

    def reset(self, reason: str = "Manual reset") -> dict[str, Any]:
        """Reset the state machine to initial state."""
        result = self.transition_to(
            "NO_DATA",
            reason_code=SafetyReasonCode.USER_MANUAL_OVERRIDE.value,
            reason=reason,
            source="operator",
            automatic_or_manual="manual",
            operator_action="reset",
        )
        self._blocked_actions.clear()
        return result

    # -- Serialization ------------------------------------------------------

    def serialize(self) -> dict[str, Any]:
        """Full serialization for audit reports."""
        return {
            "current_state": self.get_current_state(),
            "timeline_count": len(self._timeline),
            "blocked_action_count": len(self._blocked_actions),
            "timeline": [t.to_dict() for t in self._timeline],
            "blocked_actions": [r.to_dict() for r in self._blocked_actions],
        }

    # -- Context-aware inference --------------------------------------------

    def infer_state_from_runtime_context(
        self,
        *,
        emergency_stop_active: bool = False,
        adaptation_frozen: bool = False,
        data_source: str = "idle",
        hardware_validation_state: str = "UNKNOWN",
        hardware_closed_loop_enabled: bool = False,
    ) -> str:
        """Infer the appropriate safety state from runtime context.

        This is a deterministic mapping used at startup or after context
        changes to synchronize the state machine with runtime status.
        """
        if emergency_stop_active:
            target = "EMERGENCY_STOP"
        elif adaptation_frozen:
            target = "ADAPTATION_FROZEN"
        elif data_source == "idle":
            target = "NO_DATA"
        elif data_source == "live_synthetic":
            target = "SIMULATED_ONLY"
        elif data_source in {"recorded_replay", "dataset_replay"}:
            target = "DATA_REPLAY"
        elif hardware_validation_state == "FAILED":
            target = "VALIDATION_FAILED"
        elif hardware_validation_state == "PASSED":
            if not hardware_closed_loop_enabled:
                target = "CLOSED_LOOP_LOCKED"
            else:
                target = "SHADOW_READY"
        elif hardware_validation_state == "UNKNOWN":
            target = "HARDWARE_UNVALIDATED"
        else:
            target = "CLOSED_LOOP_LOCKED"

        if target != self._current_state_id:
            self.transition_to(
                target,
                reason_code=SafetyReasonCode.NORMAL_OPERATION.value,
                reason=f"Inferred from runtime context: data_source={data_source}, "
                f"hw_validation={hardware_validation_state}",
                source="state_machine",
            )

        return target

    def infer_from_evidence(self, ev: Any, *, source: str = "startup_evidence_inference") -> str:
        """Infer the appropriate safety state from aggregated report evidence.

        Called once at startup after loading disk artifacts. Never allows real
        EEG closed-loop. Only sets informative audit state so users can see
        the system's evidence-based posture without starting a session.
        """
        from app.safety.report_status import infer_startup_safety_state  # noqa: PLC0415

        target = infer_startup_safety_state(ev)

        if target != self._current_state_id:
            warnings = getattr(ev, "evidence_warnings", [])
            sources = getattr(ev, "evidence_sources", [])
            reason = (
                f"Startup evidence inference: {target}. "
                f"Sources: {', '.join(sources[:3]) or 'none'}. "
                f"Warnings: {len(warnings)}."
            )
            self.transition_to(
                target,
                reason_code=SafetyReasonCode.NORMAL_OPERATION.value,
                reason=reason,
                source=source,
                automatic_or_manual="automatic",
            )

        return target


# ---------------------------------------------------------------------------
#  Global singleton
# ---------------------------------------------------------------------------

safety_state_machine = SafetyStateMachine()
