"""Fusion calibration model.

Provides baseline calibration profiles for normalizing fusion inputs,
computing baseline deviations, and conservatively improving uncertainty
estimation. Never increases confidence beyond a safe cap.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    PROXY_LIMITATION,
    FusionInput,
    ModalityFeaturePacket,
)

_ROOT = Path(__file__).resolve().parent.parent.parent.parent

CALIBRATION_LIMITATION = (
    "Calibration profiles are derived from limited samples and should not "
    "be interpreted as validated normative baselines."
)


class FusionCalibrationProfile(BaseModel):
    """Calibration profile for fusion normalization."""

    profile_id: str
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = "default"
    baseline_features: dict[str, float] = Field(default_factory=dict)
    modality_baselines: dict[str, dict[str, float]] = Field(default_factory=dict)
    self_report_baseline: dict[str, float] = Field(default_factory=dict)
    quality_thresholds: dict[str, float] = Field(default_factory=dict)
    uncertainty_thresholds: dict[str, float] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)
    proxy_estimates_only: bool = True
    closed_loop_allowed: bool = False


def create_default_calibration_profile() -> FusionCalibrationProfile:
    """Create a safe default calibration profile."""
    return FusionCalibrationProfile(
        profile_id=f"default_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
        source="default_heuristic",
        baseline_features={
            "focus": 0.50,
            "relaxation": 0.50,
            "workload": 0.50,
            "stress": 0.50,
            "fatigue": 0.50,
            "imagery_engagement": 0.50,
            "imagery_quality": 0.50,
        },
        modality_baselines={
            "eeg": {
                "engagement_index": 0.50,
                "relaxation_index": 0.50,
                "alpha_power": 0.50,
                "beta_power": 0.50,
                "theta_power": 0.40,
                "delta_power": 0.30,
                "fatigue_index": 0.35,
            },
            "gaze": {
                "fixation_stability": 0.65,
                "gaze_dispersion": 0.30,
                "blink_rate": 0.25,
                "pupil_diameter_proxy": 0.45,
            },
            "physiology": {
                "rmssd_proxy": 0.55,
                "eda_phasic": 0.35,
                "stress_index": 0.38,
                "heart_rate": 0.45,
            },
        },
        self_report_baseline={
            "vividness": 0.50,
            "effort": 0.50,
            "perceived_focus": 0.50,
            "perceived_relaxation": 0.50,
        },
        quality_thresholds={
            "minimum_quality": 0.25,
            "good_quality": 0.55,
            "high_quality": 0.75,
        },
        uncertainty_thresholds={
            "low_uncertainty": 0.30,
            "medium_uncertainty": 0.50,
            "high_uncertainty": 0.72,
        },
        limitations=[
            PROXY_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            CALIBRATION_LIMITATION,
        ],
        provenance={
            "generator": "create_default_calibration_profile",
            "proxy_estimates_only": True,
        },
    )


def calibrate_from_packets(
    packets: list[ModalityFeaturePacket],
    *,
    source: str = "packet_calibration",
) -> FusionCalibrationProfile:
    """Create a calibration profile from a list of feature packets.

    Computes mean feature values per modality as baseline references.
    """
    profile = create_default_calibration_profile()
    profile.profile_id = f"calibrated_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:6]}"
    profile.source = source

    # Group packets by modality
    by_modality: dict[str, list[ModalityFeaturePacket]] = {}
    for packet in packets:
        if not packet.missing:
            mod = packet.modality_id
            if mod not in by_modality:
                by_modality[mod] = []
            by_modality[mod].append(packet)

    # Compute per-modality baselines
    for mod_id, mod_packets in by_modality.items():
        feature_sums: dict[str, float] = {}
        feature_counts: dict[str, int] = {}
        for p in mod_packets:
            for key, value in p.features.items():
                try:
                    v = float(value)
                    feature_sums[key] = feature_sums.get(key, 0.0) + v
                    feature_counts[key] = feature_counts.get(key, 0) + 1
                except (TypeError, ValueError):
                    pass

        baseline: dict[str, float] = {}
        for key in feature_sums:
            if feature_counts[key] > 0:
                baseline[key] = round(feature_sums[key] / feature_counts[key], 4)
        profile.modality_baselines[mod_id] = baseline

        # Update self-report baseline if present
        if mod_id == "self_report":
            profile.self_report_baseline = baseline

    profile.provenance = {
        "generator": "calibrate_from_packets",
        "packet_count": len(packets),
        "modalities_calibrated": list(by_modality.keys()),
        "proxy_estimates_only": True,
    }

    return profile


def apply_calibration(
    profile: FusionCalibrationProfile,
    fusion_input: FusionInput,
) -> FusionInput:
    """Apply calibration to a fusion input by injecting baseline context.

    This does NOT modify packets in-place. It adds calibration baseline
    information to the FusionInput context for the fusion engine to use.
    """
    context = dict(fusion_input.context or {})
    context["calibration_profile_id"] = profile.profile_id
    context["calibration_source"] = profile.source
    context["calibration_baseline"] = profile.baseline_features
    context["modality_baselines"] = profile.modality_baselines
    context["self_report_baseline"] = profile.self_report_baseline
    context["quality_thresholds"] = profile.quality_thresholds

    return FusionInput(
        session_id=fusion_input.session_id,
        packets=list(fusion_input.packets),
        context=context,
    )


def serialize_profile(profile: FusionCalibrationProfile) -> str:
    """Serialize a calibration profile to JSON."""
    return profile.model_dump_json(indent=2)


def deserialize_profile(data: str) -> FusionCalibrationProfile:
    """Deserialize a calibration profile from JSON."""
    return FusionCalibrationProfile.model_validate_json(data)


def save_calibration_report(
    profile: FusionCalibrationProfile,
    *,
    run_id: str | None = None,
) -> dict[str, str]:
    """Save calibration profile and report to disk."""
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:8]
    report_dir = _ROOT / "reports" / "fusion_calibration" / run_id
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / "fusion_calibration_profile.json"
    json_path.write_text(serialize_profile(profile), encoding="utf-8")

    md_path = report_dir / "fusion_calibration_report.md"
    md_path.write_text(_calibration_markdown(profile, run_id), encoding="utf-8")

    return {
        "run_id": run_id,
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "report_dir": str(report_dir),
    }


def _calibration_markdown(profile: FusionCalibrationProfile, run_id: str) -> str:
    lines = [
        "# Fusion Calibration Report",
        "",
        f"Profile ID: `{profile.profile_id}`",
        f"Run ID: `{run_id}`",
        f"Created: `{profile.created_at}`",
        f"Source: `{profile.source}`",
        "",
        "> " + PROXY_LIMITATION,
        "> " + CALIBRATION_LIMITATION,
        "> " + CLOSED_LOOP_LIMITATION,
        "",
        "## Baseline Features",
        "",
    ]
    for key, val in sorted(profile.baseline_features.items()):
        lines.append(f"- {key}: `{val:.3f}`")
    lines += ["", "## Modality Baselines", ""]
    for mod_id, baseline in sorted(profile.modality_baselines.items()):
        lines.append(f"### {mod_id}")
        for key, val in sorted(baseline.items()):
            lines.append(f"- {key}: `{val:.4f}`")
        lines.append("")
    lines += ["## Quality Thresholds", ""]
    for key, val in sorted(profile.quality_thresholds.items()):
        lines.append(f"- {key}: `{val:.3f}`")
    lines += ["", "## Uncertainty Thresholds", ""]
    for key, val in sorted(profile.uncertainty_thresholds.items()):
        lines.append(f"- {key}: `{val:.3f}`")
    return "\n".join(lines) + "\n"
