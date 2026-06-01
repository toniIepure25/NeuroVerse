"""Base sensor adapter interface for Fusion v1.

All adapters must declare their source_type honestly. No simulated adapter
may claim to be real hardware.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Literal

from app.fusion.models import ModalityFeaturePacket, ModalityId, ModalitySource

AdapterSourceType = Literal["simulated", "replay", "live_optional", "user_input"]


class FusionSensorAdapter(ABC):
    """Common interface for all fusion sensor adapters."""

    adapter_id: str = "base_adapter"
    modality_id: ModalityId = "eeg"
    source_type: AdapterSourceType = "simulated"
    version: str = "0.1"

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if the adapter can produce packets right now."""

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Return adapter status including availability, source type, limitations."""

    @abstractmethod
    def read_packet(self) -> ModalityFeaturePacket:
        """Read a single feature packet from the adapter."""

    def read_window(self, n: int = 5) -> list[ModalityFeaturePacket]:
        """Read a window of n packets. Default implementation calls read_packet n times."""
        return [self.read_packet() for _ in range(n)]

    def validate_packet(self, packet: ModalityFeaturePacket) -> dict[str, Any]:
        """Validate that a packet is well-formed for this modality."""
        issues: list[str] = []
        if packet.modality_id != self.modality_id:
            issues.append(
                f"Modality mismatch: expected {self.modality_id}, got {packet.modality_id}"
            )
        if packet.quality_score is not None and not (0 <= packet.quality_score <= 1):
            issues.append(f"Quality score out of range: {packet.quality_score}")
        if packet.confidence is not None and not (0 <= packet.confidence <= 1):
            issues.append(f"Confidence out of range: {packet.confidence}")
        return {"valid": len(issues) == 0, "issues": issues}

    @property
    def limitations(self) -> list[str]:
        """Return scientific limitations for this adapter."""
        return [
            f"Adapter '{self.adapter_id}' source_type={self.source_type}.",
            "Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
        ]

    def _make_source(self) -> ModalitySource:
        """Map adapter source_type to ModalitySource."""
        mapping: dict[str, ModalitySource] = {
            "simulated": "simulated",
            "replay": "replay",
            "live_optional": "real",
            "user_input": "user_input",
        }
        return mapping.get(self.source_type, "simulated")
