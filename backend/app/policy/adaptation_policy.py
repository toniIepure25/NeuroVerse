from __future__ import annotations

from app.policy.behavior_tree import evaluate_behavior_tree
from app.policy.smoothing import ActionSmoother
from app.schemas.adaptation import AdaptationActionPayload
from app.schemas.safety import SafetyDecisionPayload
from app.schemas.state import StatePredictionPayload


class AdaptationPolicy:
    """Maps cognitive state + safety decisions to smoothed environment adaptation actions."""

    def __init__(
        self,
        max_delta: float = 0.25,
        cooldown_ms: int = 2000,
        smoothing_window: int = 5,
    ) -> None:
        self._smoother = ActionSmoother(
            max_delta=max_delta,
            cooldown_ms=cooldown_ms,
            window_size=smoothing_window,
        )

    def decide(
        self,
        state: StatePredictionPayload,
        safety: SafetyDecisionPayload,
    ) -> AdaptationActionPayload:
        self._smoother.add_state(state)
        raw_action = evaluate_behavior_tree(state, safety)
        smoothed = self._smoother.smooth(raw_action)
        return smoothed

    @property
    def action_history(self) -> list[str]:
        return self._smoother.action_history_list
