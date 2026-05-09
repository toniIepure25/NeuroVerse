from __future__ import annotations

from app.safety.safety_gate import SafetyGate
from app.schemas.state import StatePredictionPayload


def _state(**overrides) -> StatePredictionPayload:
    defaults = dict(
        focus=0.5, relaxation=0.5, workload=0.5,
        stress=0.3, fatigue=0.3, imagery_engagement=0.3,
        confidence=0.8,
    )
    defaults.update(overrides)
    return StatePredictionPayload(**defaults)


class TestSafetyGate:
    def setup_method(self):
        self.gate = SafetyGate()

    def test_normal_signals_allowed(self):
        result = self.gate.evaluate(
            _state(),
            {"eeg": 0.9, "physio": 0.85, "gaze": 0.88, "multimodal": 0.87},
        )
        assert result.decision == "ALLOWED"
        assert result.safety_level == "normal"

    def test_low_eeg_sqi_blocks_eeg_actions(self):
        result = self.gate.evaluate(
            _state(),
            {"eeg": 0.2, "physio": 0.85, "gaze": 0.88, "multimodal": 0.6},
        )
        assert "IncreaseSceneClarity" in result.blocked_actions

    def test_low_multimodal_sqi_triggers_wait(self):
        result = self.gate.evaluate(
            _state(),
            {"eeg": 0.5, "physio": 0.3, "gaze": 0.3, "multimodal": 0.35},
        )
        assert result.decision == "WAIT"

    def test_very_low_confidence_triggers_block(self):
        result = self.gate.evaluate(
            _state(confidence=0.15),
            {"eeg": 0.5, "physio": 0.5, "gaze": 0.5, "multimodal": 0.5},
        )
        assert result.decision == "BLOCKED"
        assert result.safety_level == "freeze"

    def test_low_confidence_triggers_wait(self):
        result = self.gate.evaluate(
            _state(confidence=0.35),
            {"eeg": 0.5, "physio": 0.6, "gaze": 0.6, "multimodal": 0.55},
        )
        assert result.decision == "WAIT"

    def test_high_stress_blocks_clarity(self):
        result = self.gate.evaluate(
            _state(stress=0.85),
            {"eeg": 0.9, "physio": 0.85, "gaze": 0.88, "multimodal": 0.87},
        )
        assert "IncreaseSceneClarity" in result.blocked_actions

    def test_contradictory_actions_trigger_wait(self):
        history = [
            "IncreaseSceneClarity",
            "SimplifyEnvironment",
            "IncreaseSceneClarity",
            "SimplifyEnvironment",
        ]
        result = self.gate.evaluate(
            _state(),
            {"eeg": 0.9, "physio": 0.85, "gaze": 0.88, "multimodal": 0.87},
            action_history=history,
        )
        assert result.decision == "WAIT"
