from __future__ import annotations

from app.safety.rules import (
    CONFIDENCE_BLOCK,
    CONFIDENCE_WAIT,
    EEG_SQI_BLOCK,
    MULTIMODAL_SQI_WAIT,
    STRESS_LIMIT_THRESHOLD,
)
from app.schemas.safety import SafetyDecisionPayload
from app.schemas.state import StatePredictionPayload


class SafetyGate:
    """Evaluates whether adaptation actions are safe to execute."""

    def evaluate(
        self,
        prediction: StatePredictionPayload,
        sqi_scores: dict[str, float],
        action_history: list[str] | None = None,
    ) -> SafetyDecisionPayload:
        eeg_sqi = sqi_scores.get("eeg", 0.5)
        multimodal_sqi = sqi_scores.get("multimodal", 0.5)

        blocked_actions: list[str] = []

        if prediction.confidence < CONFIDENCE_BLOCK or multimodal_sqi < 0.25:
            return SafetyDecisionPayload(
                decision="BLOCKED",
                reason="Severe signal degradation or extremely low model confidence",
                sqi_scores=sqi_scores,
                confidence=prediction.confidence,
                blocked_actions=["*"],
                safety_level="freeze",
            )

        if eeg_sqi < EEG_SQI_BLOCK:
            blocked_actions.extend([
                "IncreaseSceneClarity",
                "GenerateSymbolicObject",
            ])

        if multimodal_sqi < MULTIMODAL_SQI_WAIT:
            return SafetyDecisionPayload(
                decision="WAIT",
                reason="Low multimodal SQI — waiting for stable signal",
                sqi_scores=sqi_scores,
                confidence=prediction.confidence,
                blocked_actions=blocked_actions,
                safety_level="caution",
            )

        if prediction.confidence < CONFIDENCE_WAIT:
            return SafetyDecisionPayload(
                decision="WAIT",
                reason="Low model confidence",
                sqi_scores=sqi_scores,
                confidence=prediction.confidence,
                blocked_actions=blocked_actions,
                safety_level="caution",
            )

        if prediction.stress > STRESS_LIMIT_THRESHOLD:
            blocked_actions.append("IncreaseSceneClarity")

        if _has_contradictory_actions(action_history or []):
            return SafetyDecisionPayload(
                decision="WAIT",
                reason="Contradictory state transitions detected — stabilizing",
                sqi_scores=sqi_scores,
                confidence=prediction.confidence,
                blocked_actions=blocked_actions,
                safety_level="caution",
            )

        if blocked_actions:
            return SafetyDecisionPayload(
                decision="ALLOWED",
                reason="Partial restrictions due to low EEG SQI",
                sqi_scores=sqi_scores,
                confidence=prediction.confidence,
                blocked_actions=blocked_actions,
                safety_level="caution",
            )

        return SafetyDecisionPayload(
            decision="ALLOWED",
            reason="No safety issue",
            sqi_scores=sqi_scores,
            confidence=prediction.confidence,
            blocked_actions=[],
            safety_level="normal",
        )


_OPPOSING_PAIRS = {
    "IncreaseSceneClarity": "SimplifyEnvironment",
    "SimplifyEnvironment": "IncreaseSceneClarity",
    "SmoothEnvironmentMotion": "StabilizeVisualField",
    "StabilizeVisualField": "SmoothEnvironmentMotion",
}


def _has_contradictory_actions(history: list[str], window: int = 4) -> bool:
    recent = history[-window:] if len(history) >= window else history
    if len(recent) < 2:
        return False
    for i in range(len(recent) - 1):
        if recent[i] in _OPPOSING_PAIRS and _OPPOSING_PAIRS[recent[i]] in recent[i + 1 :]:
            return True
    return False
