"""Simulated gaze and physiology adapters for Fusion v1.

These adapters emit clearly simulated feature packets for demo, testing,
and validation purposes. They do NOT claim to be real hardware sensors.
"""

from __future__ import annotations

import random
from typing import Any

from app.fusion.adapters.base import FusionSensorAdapter
from app.fusion.models import ModalityFeaturePacket


class SimulatedGazeAdapter(FusionSensorAdapter):
    """Simulated gaze sensor adapter.

    Emits gaze stability, blink proxy, fixation proxy, and pupil proxy
    features from a random generator. Source is always 'simulated'.
    """

    adapter_id = "simulated_gaze_v1"
    modality_id = "gaze"  # type: ignore[assignment]
    source_type = "simulated"  # type: ignore[assignment]
    version = "1.0"

    def __init__(self, *, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def is_available(self) -> bool:
        return True

    def get_status(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "modality_id": self.modality_id,
            "source_type": self.source_type,
            "available": True,
            "hardware_connected": False,
            "limitations": self.limitations,
        }

    def read_packet(self) -> ModalityFeaturePacket:
        fixation = self._rng.gauss(0.68, 0.08)
        dispersion = self._rng.gauss(0.30, 0.06)
        blink_rate = self._rng.gauss(0.25, 0.05)
        blink_duration = self._rng.gauss(0.28, 0.04)
        pupil = self._rng.gauss(0.45, 0.07)

        return ModalityFeaturePacket(
            modality_id="gaze",
            source="simulated",
            quality_score=max(0.0, min(1.0, self._rng.gauss(0.72, 0.06))),
            confidence=max(0.0, min(1.0, self._rng.gauss(0.65, 0.06))),
            features={
                "fixation_stability": max(0.0, min(1.0, fixation)),
                "gaze_dispersion": max(0.0, min(1.0, dispersion)),
                "blink_rate": max(0.0, min(1.0, blink_rate)),
                "blink_duration_proxy": max(0.0, min(1.0, blink_duration)),
                "pupil_diameter_proxy": max(0.0, min(1.0, pupil)),
            },
            limitations=[
                "Simulated gaze features — not from a real eye tracker.",
                "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
            ],
            provenance={"adapter_id": self.adapter_id, "source": "simulated"},
        )

    @property
    def limitations(self) -> list[str]:
        return [
            "SimulatedGazeAdapter emits synthetic gaze features, not real eye-tracking data.",
            "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
        ]


class SimulatedPhysiologyAdapter(FusionSensorAdapter):
    """Simulated physiology sensor adapter.

    Emits HR/HRV/EDA proxy features from a random generator.
    Source is always 'simulated'.
    """

    adapter_id = "simulated_physiology_v1"
    modality_id = "physiology"  # type: ignore[assignment]
    source_type = "simulated"  # type: ignore[assignment]
    version = "1.0"

    def __init__(self, *, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def is_available(self) -> bool:
        return True

    def get_status(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "modality_id": self.modality_id,
            "source_type": self.source_type,
            "available": True,
            "hardware_connected": False,
            "limitations": self.limitations,
        }

    def read_packet(self) -> ModalityFeaturePacket:
        rmssd = self._rng.gauss(0.55, 0.08)
        eda = self._rng.gauss(0.35, 0.07)
        stress = self._rng.gauss(0.38, 0.06)
        hr = self._rng.gauss(0.45, 0.06)

        return ModalityFeaturePacket(
            modality_id="physiology",
            source="simulated",
            quality_score=max(0.0, min(1.0, self._rng.gauss(0.70, 0.06))),
            confidence=max(0.0, min(1.0, self._rng.gauss(0.62, 0.06))),
            features={
                "rmssd_proxy": max(0.0, min(1.0, rmssd)),
                "eda_phasic": max(0.0, min(1.0, eda)),
                "stress_index": max(0.0, min(1.0, stress)),
                "heart_rate": max(0.0, min(1.0, hr)),
            },
            limitations=[
                "Simulated physiology features — not from a real PPG/EDA sensor.",
                "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
            ],
            provenance={"adapter_id": self.adapter_id, "source": "simulated"},
        )

    @property
    def limitations(self) -> list[str]:
        return [
            "SimulatedPhysiologyAdapter emits synthetic HR/HRV/EDA proxies, not real sensor data.",
            "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
        ]
