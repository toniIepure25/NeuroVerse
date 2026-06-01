"""Tests for the safety state machine and closed-loop governance layer."""

from __future__ import annotations

from app.safety.closed_loop_governance import evaluate_closed_loop_governance
from app.safety.reason_codes import SafetyReasonCode, SafetySeverity
from app.safety.state_machine import SAFETY_STATES, SafetyStateMachine

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def fresh_machine(initial: str = "NO_DATA") -> SafetyStateMachine:
    """Return a fresh state machine for each test."""
    return SafetyStateMachine(initial_state=initial)


# ---------------------------------------------------------------------------
#  State initialization
# ---------------------------------------------------------------------------


class TestSafetyStateInitialization:
    def test_default_initial_state_is_no_data(self):
        sm = fresh_machine()
        assert sm.current_state_id == "NO_DATA"

    def test_initial_state_can_be_closed_loop_locked(self):
        sm = fresh_machine("CLOSED_LOOP_LOCKED")
        assert sm.current_state_id == "CLOSED_LOOP_LOCKED"

    def test_unknown_initial_state_falls_back_to_no_data(self):
        sm = fresh_machine("NONEXISTENT_STATE")
        assert sm.current_state_id == "NO_DATA"

    def test_get_current_state_returns_dict(self):
        sm = fresh_machine()
        state = sm.get_current_state()
        assert isinstance(state, dict)
        assert state["state_id"] == "NO_DATA"
        assert "severity" in state
        assert "allowed_actions" in state
        assert "blocked_actions" in state

    def test_initial_timeline_has_one_entry(self):
        sm = fresh_machine()
        assert len(sm.get_timeline()) == 1
        assert sm.get_timeline()[0]["from_state"] == "INIT"


# ---------------------------------------------------------------------------
#  State definitions
# ---------------------------------------------------------------------------


class TestSafetyStateDefinitions:
    def test_all_required_states_exist(self):
        required = {
            "NO_DATA",
            "SIMULATED_ONLY",
            "DATA_REPLAY",
            "RECORD_ONLY",
            "VALIDATION_RUNNING",
            "VALIDATION_PASSED",
            "VALIDATION_FAILED",
            "CALIBRATION_REQUIRED",
            "CALIBRATION_RUNNING",
            "CALIBRATED",
            "SHADOW_READY",
            "SHADOW_RUNNING",
            "CLOSED_LOOP_LOCKED",
            "HARDWARE_UNVALIDATED",
            "SIGNAL_UNSAFE",
            "SENSOR_DROPOUT",
            "HIGH_UNCERTAINTY",
            "ADAPTATION_FROZEN",
            "EMERGENCY_STOP",
        }
        assert required.issubset(SAFETY_STATES.keys())

    def test_emergency_stop_severity_is_emergency(self):
        state = SAFETY_STATES["EMERGENCY_STOP"]
        assert state.severity == SafetySeverity.EMERGENCY

    def test_closed_loop_locked_severity_is_blocked(self):
        state = SAFETY_STATES["CLOSED_LOOP_LOCKED"]
        assert state.severity == SafetySeverity.BLOCKED

    def test_no_data_allows_start_simulator(self):
        state = SAFETY_STATES["NO_DATA"]
        assert "start_simulator" in state.allowed_actions

    def test_shadow_running_blocks_real_eeg_adaptation(self):
        state = SAFETY_STATES["SHADOW_RUNNING"]
        assert "real_eeg_adaptation" in state.blocked_actions

    def test_emergency_stop_blocks_all_main_actions(self):
        state = SAFETY_STATES["EMERGENCY_STOP"]
        for action in ("adapt", "calibrate", "shadow_inference", "unfreeze"):
            assert action in state.blocked_actions


# ---------------------------------------------------------------------------
#  Transitions
# ---------------------------------------------------------------------------


class TestSafetyTransitions:
    def test_valid_transition_changes_state(self):
        sm = fresh_machine()
        sm.transition_to("SIMULATED_ONLY", reason="test")
        assert sm.current_state_id == "SIMULATED_ONLY"

    def test_transition_to_same_state_is_noop(self):
        sm = fresh_machine()
        initial_count = len(sm._timeline)
        sm.transition_to("NO_DATA", reason="same state")
        assert len(sm._timeline) == initial_count  # no new entry

    def test_invalid_transition_returns_error(self):
        sm = fresh_machine()
        result = sm.transition_to("NONEXISTENT_STATE", reason="bad")
        assert "error" in result

    def test_transition_is_recorded_in_timeline(self):
        sm = fresh_machine()
        sm.transition_to("SIMULATED_ONLY", reason="started simulator")
        timeline = sm.get_timeline()
        assert any(t["to_state"] == "SIMULATED_ONLY" for t in timeline)

    def test_transition_includes_reason_code(self):
        sm = fresh_machine()
        sm.transition_to(
            "SIGNAL_UNSAFE",
            reason_code=SafetyReasonCode.LOW_SQI.value,
            reason="EEG SQI dropped",
        )
        timeline = sm.get_timeline()
        last = timeline[-1]
        assert last["reason_code"] == "low_sqi"
        assert last["to_state"] == "SIGNAL_UNSAFE"

    def test_transition_preserves_source(self):
        sm = fresh_machine()
        sm.transition_to("ADAPTATION_FROZEN", source="operator", reason="manual")
        last = sm.get_timeline()[-1]
        assert last["source"] == "operator"

    def test_transition_timeline_limit_enforced(self):
        sm = fresh_machine()
        sm.MAX_TIMELINE = 5
        for i in range(10):
            sm.transition_to("SIMULATED_ONLY", reason=f"cycle {i}")
            sm.transition_to("NO_DATA", reason=f"back {i}")
        assert len(sm._timeline) <= 5


# ---------------------------------------------------------------------------
#  Emergency stop
# ---------------------------------------------------------------------------


class TestEmergencyStop:
    def test_emergency_stop_transition(self):
        sm = fresh_machine("SIMULATED_ONLY")
        sm.transition_to(
            "EMERGENCY_STOP",
            reason_code=SafetyReasonCode.EMERGENCY_STOP_ACTIVE.value,
            reason="manual emergency stop",
            source="operator",
        )
        assert sm.current_state_id == "EMERGENCY_STOP"

    def test_emergency_stop_state_blocks_all_adaptation(self):
        state = SAFETY_STATES["EMERGENCY_STOP"]
        assert "adapt" in state.blocked_actions

    def test_emergency_stop_severity_is_emergency(self):
        state = SAFETY_STATES["EMERGENCY_STOP"]
        assert state.severity.value == "emergency"

    def test_emergency_stop_from_any_state(self):
        for state_id in ("SIMULATED_ONLY", "SHADOW_RUNNING", "CALIBRATED", "VALIDATION_PASSED"):
            sm = fresh_machine(state_id)
            sm.transition_to(
                "EMERGENCY_STOP",
                reason_code=SafetyReasonCode.EMERGENCY_STOP_ACTIVE.value,
                reason="test",
            )
            assert sm.current_state_id == "EMERGENCY_STOP"


# ---------------------------------------------------------------------------
#  Freeze / unfreeze
# ---------------------------------------------------------------------------


class TestFreezeUnfreeze:
    def test_freeze_transition(self):
        sm = fresh_machine("SIMULATED_ONLY")
        sm.transition_to(
            "ADAPTATION_FROZEN",
            reason_code=SafetyReasonCode.ADAPTATION_FROZEN.value,
            reason="manual freeze",
        )
        assert sm.current_state_id == "ADAPTATION_FROZEN"

    def test_frozen_state_blocks_adapt(self):
        state = SAFETY_STATES["ADAPTATION_FROZEN"]
        assert "adapt" in state.blocked_actions

    def test_frozen_state_allows_record(self):
        state = SAFETY_STATES["ADAPTATION_FROZEN"]
        assert "record" in state.allowed_actions

    def test_unfreeze_returns_to_simulated(self):
        sm = fresh_machine("ADAPTATION_FROZEN")
        sm.transition_to(
            "SIMULATED_ONLY",
            reason_code=SafetyReasonCode.USER_MANUAL_OVERRIDE.value,
            reason="unfreeze",
        )
        assert sm.current_state_id == "SIMULATED_ONLY"


# ---------------------------------------------------------------------------
#  Blocked actions
# ---------------------------------------------------------------------------


class TestBlockedActions:
    def test_record_blocked_action(self):
        sm = fresh_machine("CLOSED_LOOP_LOCKED")
        sm.record_blocked_action(
            "real_eeg_adaptation",
            reason_code=SafetyReasonCode.REAL_EEG_CLOSED_LOOP_DISABLED.value,
            reason="closed-loop locked",
        )
        blocked = sm.get_blocked_actions()
        assert len(blocked) == 1
        assert blocked[0]["action_attempted"] == "real_eeg_adaptation"

    def test_blocked_action_includes_current_state(self):
        sm = fresh_machine("CLOSED_LOOP_LOCKED")
        sm.record_blocked_action("adapt", reason="test")
        blocked = sm.get_blocked_actions()
        assert blocked[0]["current_state"] == "CLOSED_LOOP_LOCKED"

    def test_multiple_blocked_actions_accumulate(self):
        sm = fresh_machine()
        for i in range(5):
            sm.record_blocked_action(f"action_{i}", reason=f"reason {i}")
        assert len(sm.get_blocked_actions()) == 5

    def test_blocked_action_limit_enforced(self):
        sm = fresh_machine()
        sm.MAX_BLOCKED = 3
        for i in range(10):
            sm.record_blocked_action(f"action_{i}", reason=f"reason {i}")
        assert len(sm._blocked_actions) <= 3


# ---------------------------------------------------------------------------
#  Closed-loop locked by default
# ---------------------------------------------------------------------------


class TestClosedLoopLockedByDefault:
    def test_governance_default_is_locked(self):
        result = evaluate_closed_loop_governance()
        assert result.closed_loop_allowed is False

    def test_governance_locked_without_env_flag(self):
        result = evaluate_closed_loop_governance(environment_flag=False)
        assert result.closed_loop_allowed is False
        assert SafetyReasonCode.CLOSED_LOOP_ENV_DISABLED.value in result.lock_reason_codes

    def test_governance_locked_with_missing_calibration(self):
        result = evaluate_closed_loop_governance(
            environment_flag=True,
            hardware_validated=True,
            signal_quality_ok=True,
            timing_validated=True,
            calibration_complete=False,
            shadow_inference_passed=True,
        )
        assert result.closed_loop_allowed is False
        assert SafetyReasonCode.MISSING_CALIBRATION.value in result.lock_reason_codes

    def test_governance_locked_for_physical_hardware_unvalidated(self):
        result = evaluate_closed_loop_governance(
            environment_flag=True,
            mode="physical_hardware",
            hardware_validated=False,
        )
        assert result.closed_loop_allowed is False
        assert SafetyReasonCode.PHYSICAL_HARDWARE_UNVALIDATED.value in result.lock_reason_codes

    def test_governance_locked_for_real_eeg_mode(self):
        result = evaluate_closed_loop_governance(
            environment_flag=True,
            mode="lsl_live",
            hardware_validated=True,
            signal_quality_ok=True,
            timing_validated=True,
            calibration_complete=True,
            shadow_inference_passed=True,
        )
        assert result.closed_loop_allowed is False
        assert SafetyReasonCode.REAL_EEG_CLOSED_LOOP_DISABLED.value in result.lock_reason_codes

    def test_governance_locked_during_emergency_stop(self):
        result = evaluate_closed_loop_governance(
            environment_flag=True,
            hardware_validated=True,
            signal_quality_ok=True,
            timing_validated=True,
            calibration_complete=True,
            shadow_inference_passed=True,
            emergency_stop_active=True,
            mode="simulated",
        )
        assert result.closed_loop_allowed is False
        assert SafetyReasonCode.EMERGENCY_STOP_ACTIVE.value in result.lock_reason_codes

    def test_governance_locked_during_freeze(self):
        result = evaluate_closed_loop_governance(
            environment_flag=True,
            hardware_validated=True,
            signal_quality_ok=True,
            timing_validated=True,
            calibration_complete=True,
            shadow_inference_passed=True,
            adaptation_frozen=True,
            mode="simulated",
        )
        assert result.closed_loop_allowed is False
        assert SafetyReasonCode.ADAPTATION_FROZEN.value in result.lock_reason_codes

    def test_governance_result_has_required_unlock_conditions(self):
        result = evaluate_closed_loop_governance()
        assert len(result.required_unlock_conditions) > 0

    def test_governance_result_serializes(self):
        result = evaluate_closed_loop_governance()
        d = result.to_dict()
        assert "closed_loop_allowed" in d
        assert "lock_reasons" in d
        assert "lock_reason_codes" in d
        assert "required_unlock_conditions" in d


# ---------------------------------------------------------------------------
#  Safety timeline serialization
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_serialize_returns_full_dict(self):
        sm = fresh_machine()
        sm.transition_to("SIMULATED_ONLY", reason="started")
        sm.record_blocked_action("adapt", reason="locked")
        data = sm.serialize()
        assert "current_state" in data
        assert "timeline" in data
        assert "blocked_actions" in data
        assert data["timeline_count"] >= 1
        assert data["blocked_action_count"] == 1

    def test_timeline_entries_have_required_fields(self):
        sm = fresh_machine()
        sm.transition_to("SIMULATED_ONLY", reason="test")
        entry = sm.get_timeline()[-1]
        for field in (
            "transition_id",
            "timestamp",
            "from_state",
            "to_state",
            "reason_code",
            "source",
        ):
            assert field in entry

    def test_blocked_action_entries_have_required_fields(self):
        sm = fresh_machine()
        sm.record_blocked_action("adapt", reason="test")
        entry = sm.get_blocked_actions()[0]
        for field in ("record_id", "timestamp", "action_attempted", "reason_code", "current_state"):
            assert field in entry


# ---------------------------------------------------------------------------
#  Context inference
# ---------------------------------------------------------------------------


class TestContextInference:
    def test_infer_emergency_stop(self):
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(emergency_stop_active=True)
        assert state == "EMERGENCY_STOP"

    def test_infer_adaptation_frozen(self):
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(adaptation_frozen=True)
        assert state == "ADAPTATION_FROZEN"

    def test_infer_idle_gives_no_data(self):
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(data_source="idle")
        assert state == "NO_DATA"

    def test_infer_live_synthetic_gives_simulated(self):
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(data_source="live_synthetic")
        assert state == "SIMULATED_ONLY"

    def test_infer_replay_gives_data_replay(self):
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(data_source="dataset_replay")
        assert state == "DATA_REPLAY"

    def test_infer_hw_unknown_gives_unvalidated(self):
        # data_source must not be idle/live_synthetic/replay to reach hardware checks
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(
            data_source="live_hardware",
            hardware_validation_state="UNKNOWN",
        )
        assert state == "HARDWARE_UNVALIDATED"

    def test_infer_hw_passed_no_closed_loop_gives_locked(self):
        # data_source must not be idle/live_synthetic/replay to reach hardware checks
        sm = fresh_machine()
        state = sm.infer_state_from_runtime_context(
            data_source="live_hardware",
            hardware_validation_state="PASSED",
            hardware_closed_loop_enabled=False,
        )
        assert state == "CLOSED_LOOP_LOCKED"


# ---------------------------------------------------------------------------
#  Reset
# ---------------------------------------------------------------------------


class TestReset:
    def test_reset_returns_to_no_data(self):
        sm = fresh_machine("EMERGENCY_STOP")
        sm.reset(reason="test reset")
        assert sm.current_state_id == "NO_DATA"

    def test_reset_clears_blocked_actions(self):
        sm = fresh_machine()
        sm.record_blocked_action("adapt", reason="test")
        sm.reset(reason="test reset")
        assert len(sm.get_blocked_actions()) == 0


# ---------------------------------------------------------------------------
#  Reason codes
# ---------------------------------------------------------------------------


class TestReasonCodes:
    def test_all_required_codes_exist(self):
        codes = {rc.value for rc in SafetyReasonCode}
        required = {
            "low_sqi",
            "high_jitter",
            "missing_calibration",
            "no_validation_report",
            "validation_failed",
            "physical_hardware_unvalidated",
            "model_incompatible",
            "confidence_low",
            "high_uncertainty",
            "missing_modality",
            "sensor_dropout",
            "state_oscillation",
            "emergency_stop_active",
            "adaptation_frozen",
            "shadow_only_mode",
            "closed_loop_env_disabled",
            "real_eeg_closed_loop_disabled",
            "user_manual_override",
            "no_data",
            "unknown",
        }
        assert required.issubset(codes)

    def test_reason_code_is_string_enum(self):
        assert isinstance(SafetyReasonCode.LOW_SQI.value, str)

    def test_severity_values(self):
        from app.safety.reason_codes import SafetySeverity

        assert SafetySeverity.INFO.value == "info"
        assert SafetySeverity.WARNING.value == "warning"
        assert SafetySeverity.BLOCKED.value == "blocked"
        assert SafetySeverity.EMERGENCY.value == "emergency"
