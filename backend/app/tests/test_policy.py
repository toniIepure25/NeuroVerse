from __future__ import annotations

from app.policy.behavior_tree import evaluate_behavior_tree
from app.schemas.safety import SafetyDecisionPayload
from app.schemas.state import StatePredictionPayload


def _state(**overrides) -> StatePredictionPayload:
    defaults = dict(
        focus=0.5, relaxation=0.5, workload=0.5,
        stress=0.3, fatigue=0.3, imagery_engagement=0.3,
        confidence=0.8,
    )
    defaults.update(overrides)
    return StatePredictionPayload(**defaults)


def _safety(decision="ALLOWED", **kw) -> SafetyDecisionPayload:
    defaults = dict(
        decision=decision,
        reason="test",
        confidence=0.8,
        safety_level="normal",
    )
    defaults.update(kw)
    return SafetyDecisionPayload(**defaults)


class TestBehaviorTree:
    def test_blocked_returns_freeze(self):
        action = evaluate_behavior_tree(_state(), _safety("BLOCKED"))
        assert action.action == "FreezeAdaptation"
        assert action.intensity == 0.0

    def test_wait_returns_maintain(self):
        action = evaluate_behavior_tree(_state(), _safety("WAIT"))
        assert action.action == "MaintainBaseline"

    def test_high_stress_simplifies(self):
        action = evaluate_behavior_tree(
            _state(stress=0.85),
            _safety(),
        )
        assert action.action == "SimplifyEnvironment"
        assert action.intensity > 0

    def test_high_focus_increases_clarity(self):
        action = evaluate_behavior_tree(
            _state(focus=0.85, confidence=0.8),
            _safety(),
        )
        assert action.action == "IncreaseSceneClarity"

    def test_high_relaxation_smooths_motion(self):
        action = evaluate_behavior_tree(
            _state(relaxation=0.8, stress=0.2),
            _safety(),
        )
        assert action.action == "SmoothEnvironmentMotion"

    def test_imagery_generates_object(self):
        action = evaluate_behavior_tree(
            _state(imagery_engagement=0.8, confidence=0.75),
            _safety(),
        )
        assert action.action == "GenerateSymbolicObject"

    def test_fatigue_reduces_complexity(self):
        action = evaluate_behavior_tree(
            _state(fatigue=0.8, stress=0.3),
            _safety(),
        )
        assert action.action == "ReduceVisualComplexity"

    def test_neutral_state_maintains_baseline(self):
        action = evaluate_behavior_tree(
            _state(focus=0.5, relaxation=0.5, stress=0.3, fatigue=0.3, imagery_engagement=0.3),
            _safety(),
        )
        assert action.action == "MaintainBaseline"

    def test_stress_beats_focus(self):
        action = evaluate_behavior_tree(
            _state(stress=0.9, focus=0.9, confidence=0.9),
            _safety(),
        )
        assert action.action == "SimplifyEnvironment"

    def test_blocked_actions_respected(self):
        action = evaluate_behavior_tree(
            _state(focus=0.9, confidence=0.9),
            _safety(blocked_actions=["IncreaseSceneClarity"]),
        )
        assert action.action != "IncreaseSceneClarity"
