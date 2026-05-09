from __future__ import annotations

from app.schemas.adaptation import AdaptationActionPayload
from app.schemas.safety import SafetyDecisionPayload
from app.schemas.state import StatePredictionPayload


def evaluate_behavior_tree(
    state: StatePredictionPayload,
    safety: SafetyDecisionPayload,
) -> AdaptationActionPayload:
    """Priority-ordered rule evaluation returning the highest-priority adaptation action."""

    if safety.decision == "BLOCKED":
        return AdaptationActionPayload(
            action="FreezeAdaptation",
            intensity=0.0,
            duration_ms=1000,
            source_state="safety_blocked",
            reason=safety.reason,
        )

    if safety.decision == "WAIT":
        return AdaptationActionPayload(
            action="MaintainBaseline",
            intensity=0.1,
            duration_ms=1000,
            source_state="safety_wait",
            reason=safety.reason,
        )

    if state.stress > 0.75:
        return AdaptationActionPayload(
            action="SimplifyEnvironment",
            intensity=min(1.0, state.stress * 0.9),
            duration_ms=2000,
            source_state="high_stress",
            reason=f"Stress elevated ({state.stress:.2f})",
            parameters={"reduce_particles": True, "mute_colors": True},
        )

    if state.focus > 0.75 and state.confidence > 0.70:
        if "IncreaseSceneClarity" not in safety.blocked_actions:
            return AdaptationActionPayload(
                action="IncreaseSceneClarity",
                intensity=min(1.0, state.focus * 0.85),
                duration_ms=2000,
                source_state="high_focus",
                reason=f"Focus high ({state.focus:.2f}), confidence adequate",
                parameters={"reduce_fog": True, "increase_light": True},
            )

    if state.relaxation > 0.70 and state.stress < 0.45:
        return AdaptationActionPayload(
            action="SmoothEnvironmentMotion",
            intensity=min(1.0, state.relaxation * 0.8),
            duration_ms=3000,
            source_state="relaxed",
            reason=f"Relaxation high ({state.relaxation:.2f}), stress low",
            parameters={"slow_rotation": True, "gentle_drift": True},
        )

    if state.imagery_engagement > 0.65 and state.confidence > 0.65:
        if "GenerateSymbolicObject" not in safety.blocked_actions:
            return AdaptationActionPayload(
                action="GenerateSymbolicObject",
                intensity=min(1.0, state.imagery_engagement * 0.9),
                duration_ms=4000,
                source_state="imagery",
                reason=f"Imagery engagement elevated ({state.imagery_engagement:.2f})",
                parameters={"glow": True, "symbolic": True},
            )

    if state.fatigue > 0.70:
        return AdaptationActionPayload(
            action="ReduceVisualComplexity",
            intensity=min(1.0, state.fatigue * 0.7),
            duration_ms=2500,
            source_state="fatigued",
            reason=f"Fatigue detected ({state.fatigue:.2f})",
            parameters={"fewer_particles": True, "stabilize_camera": True},
        )

    if state.workload > 0.65:
        return AdaptationActionPayload(
            action="StabilizeVisualField",
            intensity=min(1.0, state.workload * 0.6),
            duration_ms=2000,
            source_state="high_workload",
            reason=f"Workload elevated ({state.workload:.2f})",
            parameters={"lock_sway": True},
        )

    return AdaptationActionPayload(
        action="MaintainBaseline",
        intensity=0.15,
        duration_ms=1000,
        source_state="neutral",
        reason="No dominant state — maintaining baseline",
    )
