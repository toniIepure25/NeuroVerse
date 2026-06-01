"""IMAGINA Integration Contract.

Establishes formal filesystem-based and prediction contracts between
NeuroVerse (safety-gated runtime) and Imagina (external research platform).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    CORRIDOR_LIMITATION,
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    ModalityFeaturePacket,
)


class ExternalImaginaStatus(BaseModel):
    project_root: str
    exists: bool
    detected_version: str | None = None
    available_artifacts: list[str] = Field(default_factory=list)
    latest_model_path: str | None = None
    latest_report_path: str | None = None
    latest_metrics_path: str | None = None
    latest_prediction_path: str | None = None
    integration_ready: bool = False
    limitations: list[str] = Field(
        default_factory=lambda: [
            "IMAGINA is an external research project.",
            IMAGINA_LIMITATION,
            CLOSED_LOOP_LIMITATION,
        ]
    )
    warnings: list[str] = Field(default_factory=list)


class ExternalImaginaModelArtifact(BaseModel):
    model_id: str
    artifact_type: str
    path: str
    created_at: str
    metrics: dict[str, Any] | None = None
    model_card: str | None = None
    target: str
    modality: str
    paradigm: str
    source_project: str = "external_imagina"


class ExternalImaginaPrediction(BaseModel):
    imagery_quality_proxy: float | None = None
    imagery_engagement_proxy: float | None = None
    imagery_stability_proxy: float | None = None
    confidence: float = 0.5
    source: str
    model_id: str | None = None
    report_path: str | None = None
    not_decoded_content: bool = True
    limitations: list[str] = Field(
        default_factory=lambda: [
            "IMAGINA outputs are experimental imagery proxy estimates.",
            IMAGINA_LIMITATION,
            PROXY_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            CORRIDOR_LIMITATION,
        ]
    )


def external_prediction_to_modality_packet(
    pred: ExternalImaginaPrediction,
) -> ModalityFeaturePacket:
    """Translate an ExternalImaginaPrediction into a standard ModalityFeaturePacket."""
    return ModalityFeaturePacket(
        modality_id="imagina",
        timestamp=datetime.now(timezone.utc),
        source="derived",
        features={
            "imagery_quality_proxy": pred.imagery_quality_proxy,
            "imagery_engagement_proxy": pred.imagery_engagement_proxy,
            "imagery_stability_proxy": pred.imagery_stability_proxy,
            "not_decoded_content": pred.not_decoded_content,
        },
        quality_score=pred.confidence,
        confidence=pred.confidence,
        missing=False,
        limitations=pred.limitations,
        provenance={
            "source": pred.source,
            "model_id": pred.model_id,
            "report_path": pred.report_path,
            "scientific_framing": (
                "IMAGINA is an external research project. "
                "NeuroVerse is the safety-gated runtime."
            ),
        },
    )
