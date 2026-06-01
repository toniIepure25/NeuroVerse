"""Conservative late-fusion baseline for Multimodal Fusion v1."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.core.numeric import clamp
from app.fusion.imagina_plugin import ImaginaProxyPluginV1
from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    CORRIDOR_LIMITATION,
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    FusionInput,
    FusionOutput,
    ModalityFeaturePacket,
    ModalityId,
)
from app.fusion.uncertainty import estimate_uncertainty, packet_quality

EXPECTED_MODALITIES: list[ModalityId] = [
    "eeg",
    "gaze",
    "physiology",
    "behavior",
    "self_report",
    "imagina",
]


def _f(features: Mapping[str, Any], key: str, default: float = 0.5) -> float:
    try:
        return clamp(float(features.get(key, default)), 0.0, 1.0)
    except (TypeError, ValueError):
        return default


def _packet_by_modality(fusion_input: FusionInput) -> dict[str, ModalityFeaturePacket]:
    return {packet.modality_id: packet for packet in fusion_input.packets if not packet.missing}


class LateFusionV1:
    """Heuristic late fusion over available modality packets.

    This is deliberately conservative. It is an engineering baseline for
    combining proxy features and estimating uncertainty; it is not validated
    cognitive decoding.
    """

    version = "late_fusion_v1"

    def __init__(self, imagina_plugin: ImaginaProxyPluginV1 | None = None) -> None:
        self.imagina_plugin = imagina_plugin or ImaginaProxyPluginV1()

    def evaluate(self, fusion_input: FusionInput) -> FusionOutput:
        packets = _packet_by_modality(fusion_input)
        context = fusion_input.context or {}
        uncertainty, missing = estimate_uncertainty(fusion_input.packets, EXPECTED_MODALITIES)
        scores_by_modality = {
            modality_id: self._modality_scores(packet) for modality_id, packet in packets.items()
        }
        weights = self._weights(packets)

        imagina = self.imagina_plugin.evaluate(
            eeg_packet=packets.get("eeg"),
            self_report_packet=packets.get("self_report"),
            task_metadata=context,
            calibration_baseline=context.get("calibration_baseline") or {},
        )
        if "imagina" not in scores_by_modality and imagina.confidence > 0.05:
            scores_by_modality["imagina"] = {
                "imagery_quality": imagina.imagery_quality_proxy,
                "imagery_engagement": imagina.imagery_engagement_proxy,
                "focus": 0.5,
                "relaxation": 0.5,
                "workload": 0.5,
                "stress": 0.5,
                "fatigue": 0.5,
            }
            weights["imagina"] = min(weights.get("imagina", 0.15), imagina.confidence)

        normalized_weights = self._normalize_weights(weights)
        focus = self._combine(scores_by_modality, normalized_weights, "focus")
        relaxation = self._combine(scores_by_modality, normalized_weights, "relaxation")
        workload = self._combine(scores_by_modality, normalized_weights, "workload")
        stress = self._combine(scores_by_modality, normalized_weights, "stress")
        fatigue = self._combine(scores_by_modality, normalized_weights, "fatigue")
        imagery_engagement = self._combine(
            scores_by_modality, normalized_weights, "imagery_engagement"
        )
        imagery_quality = self._combine(scores_by_modality, normalized_weights, "imagery_quality")

        overall_confidence = clamp(1.0 - uncertainty, 0.05, 0.78)
        if imagina.confidence < 0.25 and context.get("imagery_task_active"):
            overall_confidence = min(overall_confidence, 0.55)

        recommendation, reason_codes = self._safety_recommendation(
            fusion_input=fusion_input,
            uncertainty=uncertainty,
            missing=missing,
            packets=packets,
            imagina_confidence=imagina.confidence,
        )
        limitations = sorted(
            {
                PROXY_LIMITATION,
                CORRIDOR_LIMITATION,
                CLOSED_LOOP_LIMITATION,
                IMAGINA_LIMITATION,
                "Fusion v1 is a heuristic late-fusion baseline and is not clinically validated.",
                *[lim for p in fusion_input.packets for lim in p.limitations],
                *imagina.limitations,
            }
        )

        return FusionOutput(
            focus_proxy=focus,
            relaxation_proxy=relaxation,
            workload_proxy=workload,
            stress_arousal_proxy=stress,
            fatigue_proxy=fatigue,
            imagery_engagement_proxy=imagery_engagement,
            imagery_quality_proxy=imagery_quality,
            overall_confidence=overall_confidence,
            uncertainty=uncertainty,
            missing_modalities=missing,
            modality_weights=normalized_weights,
            safety_recommendation=recommendation,
            safety_reason_codes=reason_codes,
            limitations=limitations,
            provenance={
                "fusion_model": self.version,
                "session_id": fusion_input.session_id,
                "context": context,
                "packet_sources": {p.modality_id: p.source for p in fusion_input.packets},
                "proxy_estimates_only": True,
            },
            closed_loop_allowed=False,
            proposed_visual_mapping=build_visual_mapping(
                focus=focus,
                relaxation=relaxation,
                stress=stress,
                fatigue=fatigue,
                imagery_quality=imagery_quality,
                uncertainty=uncertainty,
                mode=str(context.get("mode", "simulated")),
            ),
            imagina_plugin=imagina,
        )

    def _modality_scores(self, packet: ModalityFeaturePacket) -> dict[str, float]:
        f = packet.features
        if packet.modality_id == "eeg":
            return {
                "focus": 0.55 * _f(f, "engagement_index")
                + 0.25 * _f(f, "beta_power")
                + 0.20 * (1 - _f(f, "fatigue_index")),
                "relaxation": 0.50 * _f(f, "relaxation_index")
                + 0.30 * _f(f, "alpha_power")
                + 0.20 * (1 - _f(f, "beta_power")),
                "workload": 0.45 * _f(f, "theta_power")
                + 0.35 * _f(f, "beta_power")
                + 0.20 * _f(f, "engagement_index"),
                "stress": 0.40 * _f(f, "beta_power")
                + 0.35 * (1 - _f(f, "relaxation_index"))
                + 0.25 * _f(f, "theta_power"),
                "fatigue": 0.60 * _f(f, "fatigue_index")
                + 0.25 * _f(f, "theta_power")
                + 0.15 * _f(f, "delta_power"),
                "imagery_engagement": 0.45 * _f(f, "spectral_entropy_proxy")
                + 0.35 * _f(f, "p300_proxy")
                + 0.20 * _f(f, "alpha_power"),
                "imagery_quality": 0.5,
            }
        if packet.modality_id == "gaze":
            fixation = _f(f, "fixation_stability")
            blink = _f(f, "blink_rate")
            return {
                "focus": 0.70 * fixation + 0.30 * (1 - blink),
                "relaxation": 0.45 * fixation + 0.55 * (1 - _f(f, "gaze_dispersion")),
                "workload": 0.65 * _f(f, "pupil_diameter_proxy") + 0.35 * (1 - fixation),
                "stress": 0.50 * _f(f, "gaze_dispersion") + 0.50 * _f(f, "pupil_diameter_proxy"),
                "fatigue": 0.55 * blink + 0.45 * _f(f, "blink_duration_proxy"),
                "imagery_engagement": 0.65 * fixation + 0.35 * (1 - _f(f, "gaze_dispersion")),
                "imagery_quality": 0.5,
            }
        if packet.modality_id == "physiology":
            stress = _f(f, "stress_index", _f(f, "eda_phasic"))
            return {
                "focus": 0.55 * (1 - stress) + 0.45 * _f(f, "rmssd_proxy"),
                "relaxation": 0.45 * _f(f, "rmssd_proxy")
                + 0.35 * (1 - _f(f, "eda_phasic"))
                + 0.20 * (1 - stress),
                "workload": 0.50 * stress + 0.30 * _f(f, "heart_rate") + 0.20 * _f(f, "eda_phasic"),
                "stress": stress,
                "fatigue": 0.45 * _f(f, "heart_rate")
                + 0.35 * (1 - _f(f, "rmssd_proxy"))
                + 0.20 * stress,
                "imagery_engagement": 0.5,
                "imagery_quality": 0.5,
            }
        if packet.modality_id == "behavior":
            performance = _f(f, "task_performance", 0.5)
            errors = _f(f, "error_rate", 0.3)
            return {
                "focus": 0.70 * performance + 0.30 * (1 - errors),
                "relaxation": 0.5,
                "workload": _f(f, "task_difficulty", 0.5),
                "stress": 0.50 * errors + 0.50 * _f(f, "response_variability", 0.4),
                "fatigue": _f(f, "reaction_time_slowdown", 0.4),
                "imagery_engagement": _f(f, "imagery_task_adherence", 0.5),
                "imagery_quality": 0.5,
            }
        if packet.modality_id == "self_report":
            return {
                "focus": _f(f, "focus", 0.5),
                "relaxation": _f(f, "relaxation", 0.5),
                "workload": _f(f, "workload", 0.5),
                "stress": _f(f, "stress", 0.5),
                "fatigue": _f(f, "fatigue", 0.5),
                "imagery_engagement": _f(f, "imagery_engagement", _f(f, "imagery_vividness", 0.5)),
                "imagery_quality": _f(f, "imagery_quality", _f(f, "imagery_vividness", 0.5)),
            }
        return {
            "focus": 0.5,
            "relaxation": 0.5,
            "workload": 0.5,
            "stress": 0.5,
            "fatigue": 0.5,
            "imagery_engagement": _f(f, "imagery_engagement_proxy", 0.5),
            "imagery_quality": _f(f, "imagery_quality_proxy", 0.5),
        }

    def _weights(self, packets: dict[str, ModalityFeaturePacket]) -> dict[str, float]:
        base = {
            "eeg": 0.32,
            "gaze": 0.18,
            "physiology": 0.20,
            "behavior": 0.10,
            "self_report": 0.12,
            "imagina": 0.08,
        }
        return {
            modality_id: base.get(modality_id, 0.05) * packet_quality(packet)
            for modality_id, packet in packets.items()
        }

    def _normalize_weights(self, weights: dict[str, float]) -> dict[str, float]:
        total = sum(max(v, 0.0) for v in weights.values())
        if total <= 0:
            return {}
        return {k: round(clamp(v / total, 0.0, 1.0), 4) for k, v in weights.items() if v > 0}

    def _combine(
        self,
        scores_by_modality: dict[str, dict[str, float]],
        weights: dict[str, float],
        field: str,
    ) -> float:
        if not weights:
            return 0.5
        value = sum(
            scores_by_modality.get(modality, {}).get(field, 0.5) * weight
            for modality, weight in weights.items()
        )
        return clamp(value, 0.0, 1.0)

    def _safety_recommendation(
        self,
        *,
        fusion_input: FusionInput,
        uncertainty: float,
        missing: list[ModalityId],
        packets: dict[str, ModalityFeaturePacket],
        imagina_confidence: float,
    ) -> tuple[str, list[str]]:
        context = fusion_input.context or {}
        reason_codes = ["proxy_only_estimate"]
        if uncertainty >= 0.72:
            reason_codes.append("high_fusion_uncertainty")
        if len(missing) >= 4:
            reason_codes.append("missing_required_modality")
        if context.get("imagery_task_active") and imagina_confidence < 0.3:
            reason_codes.append("imagina_low_confidence")
        if any(packet_quality(packet) < 0.25 for packet in packets.values()):
            reason_codes.append("low_modality_quality")
        if context.get("mode") == "physical_hardware":
            if not context.get("physical_hardware_validated") or not context.get(
                "calibration_complete"
            ):
                reason_codes.append("physical_hardware_not_cleared")

        if (
            "physical_hardware_not_cleared" in reason_codes
            or "high_fusion_uncertainty" in reason_codes
        ):
            return "block", reason_codes
        if "low_modality_quality" in reason_codes or "missing_required_modality" in reason_codes:
            return "wait", reason_codes
        return "allow_shadow", reason_codes


def build_visual_mapping(
    *,
    focus: float,
    relaxation: float,
    stress: float,
    fatigue: float,
    imagery_quality: float,
    uncertainty: float,
    mode: str,
) -> dict[str, Any]:
    intensity_cap = clamp(1.0 - uncertainty, 0.05, 0.75)
    return {
        "mapping_mode": "proposed_shadow_only",
        "executed_real_action": False,
        "closed_loop_allowed": False,
        "usable_in_modes": ["simulated", "demo", "shadow"],
        "blocked_for_real_eeg_closed_loop": True,
        "mode": mode,
        "intensity_cap": intensity_cap,
        "parameters": {
            "clarity": clamp(focus * intensity_cap, 0.0, 1.0),
            "fog_reduction": clamp(focus * 0.55 * intensity_cap, 0.0, 1.0),
            "motion_smoothness": clamp(relaxation * intensity_cap, 0.0, 1.0),
            "breathing_pulse": clamp(relaxation * 0.45 * intensity_cap, 0.0, 1.0),
            "scene_simplification": clamp(max(stress, fatigue) * intensity_cap, 0.0, 1.0),
            "guidance_cue": clamp(fatigue * intensity_cap, 0.0, 1.0),
            "symbolic_object_glow": clamp(imagery_quality * intensity_cap, 0.0, 1.0),
            "freeze_adaptation": uncertainty > 0.72,
        },
        "limitations": [CORRIDOR_LIMITATION, CLOSED_LOOP_LIMITATION],
    }
