"""Self-report adapter for Fusion v1.

Accepts structured self-report data or generates demo self-report packets
for testing and validation purposes.
"""

from __future__ import annotations

import random
from typing import Any

from app.fusion.adapters.base import FusionSensorAdapter
from app.fusion.models import ModalityFeaturePacket


class SelfReportAdapter(FusionSensorAdapter):
    """Self-report adapter.

    Accepts user-provided self-report values or generates simulated demo
    self-report packets. Source is 'user_input' when real data is provided,
    'simulated' for demo packets.
    """

    adapter_id = "self_report_v1"
    modality_id = "self_report"  # type: ignore[assignment]
    source_type = "user_input"  # type: ignore[assignment]
    version = "1.0"

    def __init__(
        self,
        *,
        demo_mode: bool = False,
        seed: int | None = None,
    ) -> None:
        self._demo_mode = demo_mode
        self._rng = random.Random(seed)
        self._pending: dict[str, float] | None = None

    def is_available(self) -> bool:
        return True

    def get_status(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "modality_id": self.modality_id,
            "source_type": "simulated_demo" if self._demo_mode else "user_input",
            "available": True,
            "demo_mode": self._demo_mode,
            "has_pending": self._pending is not None,
            "limitations": self.limitations,
        }

    def submit_report(self, report: dict[str, float]) -> None:
        """Accept a structured self-report from a user."""
        self._pending = report

    def read_packet(self) -> ModalityFeaturePacket:
        if self._pending is not None:
            features = dict(self._pending)
            self._pending = None
            return ModalityFeaturePacket(
                modality_id="self_report",
                source="user_input",
                quality_score=0.65,
                confidence=0.58,
                features=features,
                limitations=[
                    "Self-report is subjective user input and is treated as proxy evidence.",
                    "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
                ],
                provenance={"adapter_id": self.adapter_id, "source": "user_input"},
            )

        # Demo/simulated mode
        return ModalityFeaturePacket(
            modality_id="self_report",
            source="simulated",
            quality_score=0.64,
            confidence=0.56,
            features={
                "vividness": max(0.0, min(1.0, self._rng.gauss(0.65, 0.1))),
                "effort": max(0.0, min(1.0, self._rng.gauss(0.55, 0.1))),
                "perceived_focus": max(0.0, min(1.0, self._rng.gauss(0.60, 0.1))),
                "perceived_relaxation": max(0.0, min(1.0, self._rng.gauss(0.50, 0.1))),
                "imagery_task_active": 1.0,
                "focus": max(0.0, min(1.0, self._rng.gauss(0.62, 0.08))),
                "relaxation": max(0.0, min(1.0, self._rng.gauss(0.52, 0.08))),
                "workload": max(0.0, min(1.0, self._rng.gauss(0.42, 0.08))),
                "stress": max(0.0, min(1.0, self._rng.gauss(0.35, 0.08))),
                "fatigue": max(0.0, min(1.0, self._rng.gauss(0.30, 0.08))),
                "imagery_vividness": max(0.0, min(1.0, self._rng.gauss(0.68, 0.1))),
                "imagery_controllability": max(0.0, min(1.0, self._rng.gauss(0.58, 0.1))),
            },
            limitations=[
                "Simulated self-report for demo/validation purposes.",
                "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
            ],
            provenance={
                "adapter_id": self.adapter_id,
                "source": "simulated_demo",
            },
        )

    @property
    def limitations(self) -> list[str]:
        return [
            "Self-report is subjective user input and is treated as proxy evidence.",
            "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
        ]
