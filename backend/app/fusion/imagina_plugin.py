"""IMAGINA plugin foundation.

The v1 plugin computes conservative imagery proxy scores from optional EEG
features, self-report vividness, task metadata, and baseline hints. It never
returns decoded imagery content.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any

from app.core.numeric import clamp
from app.fusion.models import IMAGINA_LIMITATION, ImaginaPluginOutput, ModalityFeaturePacket


def _f(data: Mapping[str, Any], key: str, default: float = 0.5) -> float:
    try:
        return clamp(float(data.get(key, default)), 0.0, 1.0)
    except (TypeError, ValueError):
        return default


class BaseImaginaPlugin(ABC):
    plugin_id = "base_imagina_plugin"
    version = "0.0"

    @abstractmethod
    def evaluate(
        self,
        *,
        eeg_packet: ModalityFeaturePacket | None = None,
        self_report_packet: ModalityFeaturePacket | None = None,
        task_metadata: dict[str, Any] | None = None,
        calibration_baseline: dict[str, Any] | None = None,
    ) -> ImaginaPluginOutput:
        """Return experimental imagery-quality proxies."""


class ImaginaProxyPluginV1(BaseImaginaPlugin):
    plugin_id = "imagina_proxy_v1"
    version = "1.0"

    def evaluate(
        self,
        *,
        eeg_packet: ModalityFeaturePacket | None = None,
        self_report_packet: ModalityFeaturePacket | None = None,
        task_metadata: dict[str, Any] | None = None,
        calibration_baseline: dict[str, Any] | None = None,
    ) -> ImaginaPluginOutput:
        task_metadata = task_metadata or {}
        calibration_baseline = calibration_baseline or {}
        imagery_task_active = bool(
            task_metadata.get("imagery_task_active")
            or task_metadata.get("imagery_task_label")
            or task_metadata.get("task") == "imagery"
        )

        # Attempt to run external Imagina integration packet first
        try:
            from app.integrations.imagina import external_imagina_to_fusion_packet  # noqa: PLC0415
            ext_packet = external_imagina_to_fusion_packet()
            if not ext_packet.missing and "imagery_quality_proxy" in ext_packet.features:
                features = ext_packet.features
                return ImaginaPluginOutput(
                    imagery_quality_proxy=features.get("imagery_quality_proxy"),
                    imagery_stability_proxy=features.get("imagery_stability_proxy"),
                    imagery_engagement_proxy=features.get("imagery_engagement_proxy"),
                    confidence=ext_packet.confidence or 0.70,
                    limitations=ext_packet.limitations,
                    source="external_imagina",
                    provenance=ext_packet.provenance,
                )
        except Exception:
            pass

        # Attempt to run trained baseline model if available (internal fallback)
        try:
            import numpy as np  # noqa: PLC0415

            from app.imagina.registry import (  # noqa: PLC0415
                get_latest_imagina_model,
                load_imagina_model,
            )
            latest = get_latest_imagina_model()
            if latest and eeg_packet and not eeg_packet.missing and eeg_packet.features:
                model = load_imagina_model(latest["model_id"])

                # Check compatibility
                feat_dict = eeg_packet.features
                if all(name in feat_dict for name in model.feature_names):
                    row = [float(feat_dict[name]) for name in model.feature_names]
                    pred = model.predict(np.array([row]))[0]

                    if model.target_type == "classification":
                        score = 0.75 if int(pred) == 1 else 0.35
                    else:
                        score = float(pred)

                    prob = model.predict_proba(np.array([row]))
                    confidence = float(prob[0][int(pred)]) if prob is not None else 0.65

                    return ImaginaPluginOutput(
                        imagery_quality_proxy=score,
                        imagery_stability_proxy=score * 0.90,
                        imagery_engagement_proxy=score * 0.95,
                        confidence=confidence,
                        limitations=[
                            "IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.",
                            IMAGINA_LIMITATION,
                        ],
                        source="internal_fixture_fallback",
                        provenance={
                            "plugin_id": self.plugin_id,
                            "version": self.version,
                            "model_id": latest["model_id"],
                        },
                    )
        except Exception:
            pass

        limitations = [IMAGINA_LIMITATION]
        if not imagery_task_active:
            limitations.append("No active imagery task metadata was supplied.")
            return ImaginaPluginOutput(
                imagery_quality_proxy=0.2,
                imagery_stability_proxy=0.2,
                imagery_engagement_proxy=0.2,
                confidence=0.15,
                limitations=limitations,
                source="missing_imagery_task",
                provenance={"plugin_id": self.plugin_id, "version": self.version},
            )

        eeg_features = eeg_packet.features if eeg_packet and not eeg_packet.missing else {}
        report = (
            self_report_packet.features
            if self_report_packet and not self_report_packet.missing
            else {}
        )

        eeg_quality = (
            eeg_packet.quality_score if eeg_packet and eeg_packet.quality_score is not None else 0.5
        )
        eeg_conf = (
            eeg_packet.confidence if eeg_packet and eeg_packet.confidence is not None else 0.5
        )
        vividness = _f(report, "imagery_vividness", _f(report, "vividness", 0.5))
        controllability = _f(report, "imagery_controllability", _f(report, "controllability", 0.5))
        spectral = _f(eeg_features, "spectral_entropy_proxy", 0.5)
        p300 = _f(eeg_features, "p300_proxy", 0.5)
        alpha = _f(eeg_features, "alpha_power", 0.5)
        baseline = _f(calibration_baseline, "imagery_baseline", 0.5)

        eeg_proxy = clamp(0.35 * spectral + 0.30 * p300 + 0.20 * alpha + 0.15 * baseline, 0.0, 1.0)
        self_report_proxy = clamp(0.55 * vividness + 0.45 * controllability, 0.0, 1.0)

        if eeg_features and report:
            source = "eeg_self_report_proxy"
            quality = clamp(0.55 * eeg_quality + 0.45 * eeg_conf, 0.0, 1.0)
            confidence = clamp(
                0.45 * quality + 0.35 * self_report_proxy + 0.20 * eeg_proxy, 0.0, 0.72
            )
            imagery_quality = clamp(0.52 * self_report_proxy + 0.48 * eeg_proxy, 0.0, 1.0)
        elif report:
            source = "self_report_proxy"
            confidence = clamp(0.35 + 0.25 * self_report_proxy, 0.0, 0.55)
            imagery_quality = self_report_proxy
            limitations.append("Only self-report imagery evidence was available.")
        elif eeg_features:
            source = "eeg_proxy"
            confidence = clamp(0.25 + 0.45 * min(eeg_quality, eeg_conf), 0.0, 0.55)
            imagery_quality = eeg_proxy
            limitations.append("Only EEG proxy features were available.")
        else:
            source = "missing_imagery_features"
            confidence = 0.1
            imagery_quality = 0.2
            limitations.append("No imagery-specific EEG or self-report features were available.")

        if eeg_packet and eeg_quality < 0.4:
            confidence *= 0.65
            limitations.append("Low EEG feature quality reduced IMAGINA confidence.")

        stability = clamp(
            0.45 * controllability + 0.35 * eeg_quality + 0.20 * (1.0 - abs(vividness - alpha)),
            0.0,
            1.0,
        )
        engagement = clamp(
            0.50 * imagery_quality
            + 0.30 * _f(eeg_features, "engagement_index", 0.5)
            + 0.20 * vividness,
            0.0,
            1.0,
        )

        return ImaginaPluginOutput(
            imagery_quality_proxy=imagery_quality,
            imagery_stability_proxy=stability,
            imagery_engagement_proxy=engagement,
            confidence=clamp(confidence, 0.0, 0.72),
            limitations=limitations,
            source=source,
            provenance={"plugin_id": self.plugin_id, "version": self.version},
        )
