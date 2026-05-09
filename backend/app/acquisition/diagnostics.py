from __future__ import annotations

import importlib.util
from copy import deepcopy
from typing import Any

from app.acquisition.brainflow_adapter import BrainFlowAcquisition
from app.acquisition.lsl_adapter import LSLAcquisition
from app.acquisition.simulator import BiosignalSimulator
from app.acquisition.xdf_replay_adapter import XDFReplayAcquisition

_ACTIVE_ADAPTER: dict[str, Any] = {
    "adapter": "simulator",
    "config": {},
    "last_error": None,
}


def optional_dependency_status() -> dict[str, bool]:
    return {
        "brainflow": importlib.util.find_spec("brainflow") is not None,
        "pylsl": importlib.util.find_spec("pylsl") is not None,
        "pyxdf": importlib.util.find_spec("pyxdf") is not None,
        "mne": importlib.util.find_spec("mne") is not None,
    }


def acquisition_status() -> dict[str, Any]:
    active_adapter = _ACTIVE_ADAPTER["adapter"]
    return {
        "active_adapter": active_adapter,
        "active_config": deepcopy(_ACTIVE_ADAPTER["config"]),
        "last_error": _ACTIVE_ADAPTER["last_error"],
        "optional_dependencies": optional_dependency_status(),
        "available_adapters": {
            "simulator": _adapter_summary(BiosignalSimulator()),
            "brainflow": _adapter_summary(BrainFlowAcquisition()),
            "lsl": _adapter_summary(LSLAcquisition()),
            "xdf_replay": _adapter_summary(XDFReplayAcquisition("data/external/example.xdf")),
        },
    }


def select_adapter(adapter: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    config = config or {}
    adapter = adapter.lower()
    if adapter not in {"simulator", "brainflow", "lsl", "csv_replay", "xdf_replay"}:
        raise ValueError(f"Unsupported acquisition adapter: {adapter}")
    if adapter == "brainflow" and not BrainFlowAcquisition.is_available():
        raise RuntimeError("Cannot select BrainFlow: optional dependency 'brainflow' is missing.")
    if adapter == "lsl" and not LSLAcquisition.is_available():
        raise RuntimeError("Cannot select LSL: optional dependency 'pylsl' is missing.")
    if adapter == "xdf_replay" and not XDFReplayAcquisition.is_available():
        raise RuntimeError("Cannot select XDF replay: optional dependency 'pyxdf' is missing.")

    _ACTIVE_ADAPTER.update({"adapter": adapter, "config": config, "last_error": None})
    return acquisition_status()


async def test_adapter(
    adapter: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    adapter = (adapter or _ACTIVE_ADAPTER["adapter"]).lower()
    config = config or deepcopy(_ACTIVE_ADAPTER["config"])
    try:
        acquisition = _build_adapter(adapter, config)
        return {
            "adapter": adapter,
            "ok": True,
            "status": acquisition.status(),
            "capabilities": acquisition.capabilities(),
            "note": (
                "Diagnostics only; hardware streams are not opened unless explicitly configured."
            ),
        }
    except Exception as exc:
        return {
            "adapter": adapter,
            "ok": False,
            "error": str(exc),
            "recoverable": True,
        }


def _build_adapter(adapter: str, config: dict[str, Any]) -> Any:
    if adapter == "simulator":
        return BiosignalSimulator()
    if adapter == "brainflow":
        return BrainFlowAcquisition(config)
    if adapter == "lsl":
        return LSLAcquisition(config)
    if adapter == "xdf_replay":
        return XDFReplayAcquisition(config.get("path", "data/external/example.xdf"))
    if adapter == "csv_replay":
        from app.acquisition.csv_replay_adapter import CSVReplayAcquisition

        return CSVReplayAcquisition(config.get("path", "data/external/example.csv"))
    raise ValueError(f"Unsupported acquisition adapter: {adapter}")


def _adapter_summary(adapter: Any) -> dict[str, Any]:
    return {
        "status": adapter.status(),
        "capabilities": adapter.capabilities(),
    }
