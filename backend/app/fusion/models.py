"""Pydantic models for Multimodal Fusion v1.

These models intentionally use proxy language. NeuroVerse does not claim
clinical inference, dream decoding, thought decoding, or real EEG closed-loop
control from these outputs.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

ModalityId = Literal["eeg", "gaze", "physiology", "behavior", "self_report", "imagina"]
ModalitySource = Literal["real", "replay", "simulated", "user_input", "derived"]
SafetyRecommendation = Literal["allow_shadow", "wait", "block"]

PROXY_LIMITATION = (
    "Multimodal fusion outputs are experimental proxy estimates, not clinical "
    "or unrestricted mental-state measurements."
)
CORRIDOR_LIMITATION = (
    "The corridor is not a decoded mental image. It is an adaptive scaffold "
    "driven by experimental proxy metrics."
)
CLOSED_LOOP_LIMITATION = "Closed-loop from real EEG is disabled by default."
IMAGINA_LIMITATION = (
    "IMAGINA plugin outputs are experimental imagery-quality proxies, not decoded "
    "thoughts or dreams."
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ModalityFeaturePacket(BaseModel):
    modality_id: ModalityId
    timestamp: datetime = Field(default_factory=utc_now)
    source: ModalitySource
    features: dict[str, Any] = Field(default_factory=dict)
    quality_score: float | None = Field(default=None, ge=0, le=1)
    confidence: float | None = Field(default=None, ge=0, le=1)
    missing: bool = False
    limitations: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)


class FusionInput(BaseModel):
    session_id: str | None = None
    packets: list[ModalityFeaturePacket] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)


class ImaginaPluginOutput(BaseModel):
    imagery_quality_proxy: float = Field(ge=0, le=1)
    imagery_stability_proxy: float = Field(ge=0, le=1)
    imagery_engagement_proxy: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    limitations: list[str] = Field(default_factory=list)
    not_decoded_content: bool = True
    source: str = "imagina_proxy_v1"
    provenance: dict[str, Any] = Field(default_factory=dict)


class FusionOutput(BaseModel):
    focus_proxy: float = Field(ge=0, le=1)
    relaxation_proxy: float = Field(ge=0, le=1)
    workload_proxy: float = Field(ge=0, le=1)
    stress_arousal_proxy: float = Field(ge=0, le=1)
    fatigue_proxy: float = Field(ge=0, le=1)
    imagery_engagement_proxy: float = Field(ge=0, le=1)
    imagery_quality_proxy: float | None = Field(default=None, ge=0, le=1)
    overall_confidence: float = Field(ge=0, le=1)
    uncertainty: float = Field(ge=0, le=1)
    missing_modalities: list[ModalityId] = Field(default_factory=list)
    modality_weights: dict[str, float] = Field(default_factory=dict)
    safety_recommendation: SafetyRecommendation
    safety_reason_codes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=utc_now)
    proxy_estimates_only: bool = True
    closed_loop_allowed: bool = False
    proposed_visual_mapping: dict[str, Any] = Field(default_factory=dict)
    imagina_plugin: ImaginaPluginOutput | None = None


class FusionStatusResponse(BaseModel):
    available_modalities: list[ModalityId]
    plugin_status: dict[str, Any]
    proxy_estimates_only: bool = True
    closed_loop_allowed: bool = False
    limitations: list[str]
    provenance: dict[str, Any] = Field(default_factory=dict)
