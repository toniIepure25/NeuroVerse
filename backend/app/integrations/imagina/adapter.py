"""Fusion adapter for external Imagina integration.

Converts scanned model outputs or reports into NeuroVerse ModalityFeaturePackets,
ensuring strict compliance, safety-governance, and scientific limitations.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.fusion.models import IMAGINA_LIMITATION, ModalityFeaturePacket
from app.integrations.imagina.artifact_reader import get_latest_external_imagina_artifacts
from app.integrations.imagina.contract import (
    external_prediction_to_modality_packet,
)
from app.integrations.imagina.export_contract import NeuroVerseImaginaExportManifest


def external_imagina_to_fusion_packet(project_root: str | None = None) -> ModalityFeaturePacket:
    """Consume external Imagina reports or models and adapt into a ModalityFeaturePacket.

    Ensures we NEVER fabricate predictions or metrics.
    """
    arts = get_latest_external_imagina_artifacts(project_root)
    latest_pred = arts.get("latest_prediction")
    latest_model = arts.get("latest_model")
    latest_report = arts.get("latest_report")

    if latest_pred:
        # We have an actual external prediction file -> use it!
        return external_prediction_to_modality_packet(latest_pred)

        if latest_model:
            model_id = latest_model.model_id
        elif latest_report:
            model_id = latest_report.model_id
        else:
            model_id = "unknown"

        # Expose status and metadata only, NO fake live predictions!
        return ModalityFeaturePacket(
            modality_id="imagina",
            timestamp=datetime.now(timezone.utc),
            source="derived",
            features={
                "external_model_registered": True,
                "latest_model_id": model_id,
                "scientific_framing": (
                    "IMAGINA is an external research project. "
                    "NeuroVerse is the safety-gated runtime."
                ),
            },
            quality_score=0.80,
            confidence=0.80,
            missing=True,  # missing active streaming prediction
            limitations=[
                "External model is registered, but no active prediction file was found.",
                IMAGINA_LIMITATION,
            ],
            provenance={
                "source": "external_imagina_metadata",
                "model_id": model_id,
                "project": "external_imagina",
            },
        )

    # No external outputs found at all
    return ModalityFeaturePacket(
        modality_id="imagina",
        timestamp=datetime.now(timezone.utc),
        source="derived",
        features={},
        quality_score=None,
        confidence=None,
        missing=True,
        limitations=[
            "External Imagina project outputs not found at resolved path.",
            "Please configure NEUROVERSE_IMAGINA_ROOT or run evaluations in the Imagina workspace.",
            IMAGINA_LIMITATION,
        ],
        provenance={
            "source": "missing_external_imagina",
            "project": "external_imagina",
        },
    )


def imagina_export_to_fusion_packet(
    manifest: NeuroVerseImaginaExportManifest,
    manifest_path: str | Path
) -> ModalityFeaturePacket:
    """Translate a validated NeuroVerseImaginaExportManifest into a ModalityFeaturePacket.

    Uses prediction schema if active predictions file exists, otherwise returns
    a metadata-only evidence packet.
    """
    manifest_root = Path(manifest_path).parent

    # 1. Check if predictions exist and are loadable
    predictions_active = False
    pred_features: dict[str, Any] = {}
    confidence = 0.5

    if manifest.predictions and manifest.predictions.predictions_path:
        pred_file = manifest_root / manifest.predictions.predictions_path
        if pred_file.exists() and pred_file.is_file():
            try:
                # Try loading as JSON first
                pred_data = json.loads(pred_file.read_text(encoding="utf-8"))

                # Support dictionary prediction records or lists
                if isinstance(pred_data, dict):
                    # Direct dictionary matching our proxy metrics
                    pred_features = {
                        "imagery_quality_proxy": pred_data.get("imagery_quality_proxy"),
                        "imagery_engagement_proxy": pred_data.get("imagery_engagement_proxy"),
                        "imagery_stability_proxy": pred_data.get("imagery_stability_proxy"),
                        "not_decoded_content": pred_data.get("not_decoded_content", True),
                    }
                    confidence = pred_data.get("confidence", 0.75)
                    predictions_active = True
                elif isinstance(pred_data, list) and len(pred_data) > 0:
                    # List of samples, pick first or latest one
                    first_sample = pred_data[0]
                    if isinstance(first_sample, dict):
                        pred_features = {
                            "imagery_quality_proxy": first_sample.get("imagery_quality_proxy"),
                            "imagery_engagement_proxy": first_sample.get(
                                "imagery_engagement_proxy"
                            ),
                            "imagery_stability_proxy": first_sample.get("imagery_stability_proxy"),
                            "not_decoded_content": first_sample.get("not_decoded_content", True),
                        }
                        confidence = first_sample.get("confidence", 0.75)
                        predictions_active = True
            except Exception:
                # Fall back gracefully to metadata packet if reading fails
                pass

    model_id = manifest.model.model_id if manifest.model else "unknown"

    # Strict safety limitations that are always returned
    safety_limitations = [
        "IMAGINA exports are experimental imagery proxy artifacts.",
        "NeuroVerse validates and consumes IMAGINA artifacts; it does not train the model.",
        IMAGINA_LIMITATION,
    ]

    # Add custom limitations from manifest if present
    if manifest.limitations:
        safety_limitations.extend(manifest.limitations)

    if predictions_active:
        return ModalityFeaturePacket(
            modality_id="imagina",
            timestamp=datetime.now(timezone.utc),
            source="derived",
            features={
                "imagery_quality_proxy": pred_features.get("imagery_quality_proxy"),
                "imagery_engagement_proxy": pred_features.get("imagery_engagement_proxy"),
                "imagery_stability_proxy": pred_features.get("imagery_stability_proxy"),
                "not_decoded_content": True,
                "proxy_estimates_only": True,
                "external_model_registered": True,
                "latest_model_id": model_id,
            },
            quality_score=confidence,
            confidence=confidence,
            missing=False,
            limitations=safety_limitations,
            provenance={
                "source": "external_imagina_export",
                "export_id": manifest.export_id,
                "model_id": model_id,
                "project": "external_imagina",
                "scientific_framing": (
                    "IMAGINA is an external research project. "
                    "NeuroVerse is the safety-gated runtime."
                )
            }
        )

    # If no active prediction batch, return an evidence/metadata-only packet
    return ModalityFeaturePacket(
        modality_id="imagina",
        timestamp=datetime.now(timezone.utc),
        source="derived",
        features={
            "external_model_registered": True,
            "latest_model_id": model_id,
            "predictions_active": False,
            "proxy_estimates_only": True,
            "not_decoded_content": True,
            "primary_metric": (
                manifest.metrics.primary_metric if manifest.metrics else None
            ),
            "primary_metric_value": (
                manifest.metrics.primary_metric_value if manifest.metrics else None
            ),
        },
        quality_score=0.80,
        confidence=0.80,
        missing=True,  # missing active streaming prediction
        limitations=[
            "External export is registered, but active prediction file was missing.",
            *safety_limitations
        ],
        provenance={
            "source": "external_imagina_export_metadata",
            "export_id": manifest.export_id,
            "model_id": model_id,
            "project": "external_imagina",
        },
    )
