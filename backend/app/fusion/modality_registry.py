"""Static modality metadata for Fusion v1."""

from __future__ import annotations

from dataclasses import dataclass

from app.fusion.models import ModalityId


@dataclass(frozen=True)
class ModalityInfo:
    modality_id: ModalityId
    label: str
    optional: bool
    limitations: tuple[str, ...]


MODALITIES: dict[ModalityId, ModalityInfo] = {
    "eeg": ModalityInfo(
        "eeg",
        "EEG features",
        True,
        ("EEG features are task/proxy features and may be simulated or replay-derived.",),
    ),
    "gaze": ModalityInfo(
        "gaze",
        "Gaze features",
        True,
        ("Gaze is optional and may be simulated; it is not eye-tracking validation.",),
    ),
    "physiology": ModalityInfo(
        "physiology",
        "Physiology features",
        True,
        ("Physiology is optional/simulated unless a validated sensor path is present.",),
    ),
    "behavior": ModalityInfo(
        "behavior",
        "Behavioral/task features",
        True,
        ("Behavioral proxies reflect task interaction, not diagnosis.",),
    ),
    "self_report": ModalityInfo(
        "self_report",
        "Self-report",
        True,
        ("Self-report is subjective user input and is treated as proxy evidence.",),
    ),
    "imagina": ModalityInfo(
        "imagina",
        "IMAGINA proxy plugin",
        True,
        ("IMAGINA v1 outputs proxy scores only, not decoded content.",),
    ),
}


def available_modality_ids() -> list[ModalityId]:
    return list(MODALITIES.keys())
