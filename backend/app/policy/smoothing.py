from __future__ import annotations

import time
from collections import deque

from app.schemas.adaptation import AdaptationActionPayload
from app.schemas.state import StatePredictionPayload


class ActionSmoother:
    """Prevents abrupt adaptation changes with clamping, cooldowns, and oscillation checks."""

    def __init__(
        self,
        max_delta: float = 0.25,
        cooldown_ms: int = 2000,
        window_size: int = 5,
    ) -> None:
        self.max_delta = max_delta
        self.cooldown_ms = cooldown_ms
        self.window_size = window_size
        self._last_intensity: float = 0.0
        self._last_action_time: float = 0.0
        self._action_history: deque[str] = deque(maxlen=window_size * 2)
        self._state_buffer: deque[StatePredictionPayload] = deque(maxlen=window_size)

    def add_state(self, state: StatePredictionPayload) -> None:
        self._state_buffer.append(state)

    def smooth(self, action: AdaptationActionPayload) -> AdaptationActionPayload:
        now = time.monotonic() * 1000
        elapsed = now - self._last_action_time

        clamped_intensity = action.intensity
        delta = abs(clamped_intensity - self._last_intensity)
        if delta > self.max_delta:
            direction = 1.0 if clamped_intensity > self._last_intensity else -1.0
            clamped_intensity = self._last_intensity + direction * self.max_delta

        clamped_intensity = max(0.0, min(1.0, clamped_intensity))

        if elapsed < self.cooldown_ms and action.action != self._last_action:
            if action.action not in ("MaintainBaseline", "FreezeAdaptation"):
                clamped_intensity *= 0.5

        self._last_intensity = clamped_intensity
        self._last_action_time = now
        self._action_history.append(action.action)

        return AdaptationActionPayload(
            action=action.action,
            intensity=round(clamped_intensity, 4),
            duration_ms=action.duration_ms,
            source_state=action.source_state,
            reason=action.reason,
            parameters=action.parameters,
        )

    @property
    def _last_action(self) -> str:
        return self._action_history[-1] if self._action_history else ""

    @property
    def action_history_list(self) -> list[str]:
        return list(self._action_history)

    def averaged_state(self) -> dict[str, float] | None:
        if not self._state_buffer:
            return None
        n = len(self._state_buffer)
        return {
            "focus": sum(s.focus for s in self._state_buffer) / n,
            "relaxation": sum(s.relaxation for s in self._state_buffer) / n,
            "workload": sum(s.workload for s in self._state_buffer) / n,
            "stress": sum(s.stress for s in self._state_buffer) / n,
            "fatigue": sum(s.fatigue for s in self._state_buffer) / n,
            "imagery_engagement": sum(s.imagery_engagement for s in self._state_buffer) / n,
        }
