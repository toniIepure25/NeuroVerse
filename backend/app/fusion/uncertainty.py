"""Uncertainty helpers for Fusion v1."""

from __future__ import annotations

from app.core.numeric import clamp
from app.fusion.models import ModalityFeaturePacket, ModalityId


def packet_quality(packet: ModalityFeaturePacket) -> float:
    if packet.missing:
        return 0.0
    quality = packet.quality_score if packet.quality_score is not None else 0.55
    confidence = packet.confidence if packet.confidence is not None else quality
    return clamp(0.6 * float(quality) + 0.4 * float(confidence), 0.0, 1.0)


def estimate_uncertainty(
    packets: list[ModalityFeaturePacket],
    expected_modalities: list[ModalityId],
) -> tuple[float, list[ModalityId]]:
    present = {p.modality_id for p in packets if not p.missing}
    missing = [m for m in expected_modalities if m not in present]
    qualities = [packet_quality(p) for p in packets if not p.missing]
    mean_quality = sum(qualities) / len(qualities) if qualities else 0.0
    missing_penalty = min(0.45, 0.08 * len(missing))
    low_quality_penalty = clamp(0.55 - mean_quality, 0.0, 0.55)
    uncertainty = clamp(0.20 + missing_penalty + low_quality_penalty, 0.05, 0.95)
    return uncertainty, missing
