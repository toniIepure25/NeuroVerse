"""Adapter registry for Fusion v1.

Maintains a registry of available sensor adapters and provides
convenience functions for instantiation and status queries.
"""

from __future__ import annotations

from typing import Any

from app.fusion.adapters.base import FusionSensorAdapter
from app.fusion.adapters.csv_replay import CSVReplayAdapter
from app.fusion.adapters.self_report import SelfReportAdapter
from app.fusion.adapters.simulated import (
    SimulatedGazeAdapter,
    SimulatedPhysiologyAdapter,
)


def _create_default_adapters() -> dict[str, FusionSensorAdapter]:
    """Create the default set of adapters."""
    return {
        "simulated_gaze_v1": SimulatedGazeAdapter(seed=42),
        "simulated_physiology_v1": SimulatedPhysiologyAdapter(seed=42),
        "self_report_v1": SelfReportAdapter(demo_mode=True, seed=42),
        "csv_replay_v1": CSVReplayAdapter(),
    }


_ADAPTER_REGISTRY: dict[str, FusionSensorAdapter] = _create_default_adapters()


def get_adapter(adapter_id: str) -> FusionSensorAdapter | None:
    """Get an adapter by ID."""
    return _ADAPTER_REGISTRY.get(adapter_id)


def list_adapters() -> list[dict[str, Any]]:
    """List all registered adapters with their status."""
    return [adapter.get_status() for adapter in _ADAPTER_REGISTRY.values()]


def get_adapter_statuses() -> dict[str, dict[str, Any]]:
    """Get a map of adapter_id -> status for all registered adapters."""
    return {
        adapter_id: adapter.get_status()
        for adapter_id, adapter in _ADAPTER_REGISTRY.items()
    }


def register_adapter(adapter: FusionSensorAdapter) -> None:
    """Register a new adapter. Overwrites existing adapter with same ID."""
    _ADAPTER_REGISTRY[adapter.adapter_id] = adapter


def reset_adapters() -> None:
    """Reset to default adapters. Useful for testing."""
    global _ADAPTER_REGISTRY  # noqa: PLW0603
    _ADAPTER_REGISTRY = _create_default_adapters()
