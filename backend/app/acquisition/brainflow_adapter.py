from __future__ import annotations

import asyncio
import glob
import importlib.util
from typing import Any

from app.acquisition.base import BaseAcquisition
from app.schemas.signals import RawSignalPayload

BRAINFLOW_INSTALL_HINT = 'cd backend && pip install -e ".[hardware]"'


BOARD_NAME_TO_ID = {
    "synthetic": -1,
    "synthetic_board": -1,
    "brainflow_synthetic": -1,
    "openbci_cyton": 0,
    "cyton": 0,
    "openbci_ganglion": 1,
    "ganglion": 1,
}


class BrainFlowAcquisition(BaseAcquisition):
    """Safe BrainFlow adapter for record-only validation and shadow inference."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self._running = False
        self._last_error: str | None = None
        self._board: Any | None = None
        self._board_id = self._resolve_board_id(self.config)
        self._sampling_rate = float(_numeric(self.config.get("sampling_rate")) or 0.0)
        self._eeg_channels: list[int] = []
        self._timestamp_channel: int | None = None
        self._channel_names: list[str] = []

    async def get_window(self) -> RawSignalPayload:
        if not self._running or self._board is None:
            raise RuntimeError("BrainFlow streaming is not active.")
        window_seconds = float(self.config.get("window_seconds", self.config.get("window_s", 0.5)))
        sample_count = max(1, int(round(self._sampling_rate * window_seconds)))
        await asyncio.sleep(window_seconds)
        raw = self._board.get_board_data()
        if raw.size == 0:
            raise RuntimeError("BrainFlow returned no samples.")
        if raw.shape[1] > sample_count:
            raw = raw[:, -sample_count:]

        data = [raw[channel].astype(float).tolist() for channel in self._eeg_channels]
        timestamps: list[float] | None = None
        if self._timestamp_channel is not None and self._timestamp_channel < raw.shape[0]:
            timestamps = raw[self._timestamp_channel].astype(float).tolist()
        if not timestamps or len(timestamps) != len(data[0]):
            timestamps = [idx / self._sampling_rate for idx in range(len(data[0]))]

        return RawSignalPayload(
            modality="eeg",
            sampling_rate=self._sampling_rate,
            channel_names=self._channel_names,
            data=data,
            window_size_ms=max(1, int(round(window_seconds * 1000))),
            timestamps=timestamps,
            metadata={
                "adapter": "brainflow",
                "board_id": self._board_id,
                "board_name": self.board_name(),
                "profile_id": self.config.get("profile_id"),
                "physical_or_synthetic": self.physical_or_synthetic(),
                "eeg_channel_rows": self._eeg_channels,
                "timestamp_channel": self._timestamp_channel,
            },
        )

    async def start(self) -> None:
        if not self.is_available():
            self._last_error = "Optional dependency 'brainflow' is not installed."
            raise RuntimeError(
                f"BrainFlow is optional and not installed. Install with: {BRAINFLOW_INSTALL_HINT}"
            )
        try:
            board_shim, input_params, brainflow_error = self._brainflow_classes()
            self._board_id = self._resolve_board_id(self.config)
            self._configure_static_channels(board_shim)
            params = input_params()
            for attr in (
                "serial_port",
                "ip_address",
                "ip_port",
                "ip_protocol",
                "mac_address",
                "serial_number",
                "timeout",
            ):
                value = self.config.get(attr)
                if value not in {None, ""}:
                    setattr(params, attr, value)
            self._board = board_shim(self._board_id, params)
            self._board.prepare_session()
            self._board.start_stream()
            self._running = True
            self._last_error = None
        except brainflow_error as exc:  # type: ignore[misc]
            self._last_error = str(exc)
            await self.stop()
            raise RuntimeError(f"BrainFlow board start failed: {exc}") from exc
        except Exception as exc:
            self._last_error = str(exc)
            await self.stop()
            raise

    async def stop(self) -> None:
        board = self._board
        self._running = False
        self._board = None
        if board is None:
            return
        try:
            if board.is_prepared():
                try:
                    board.stop_stream()
                except Exception:
                    pass
                board.release_session()
        except Exception as exc:
            self._last_error = str(exc)

    def is_running(self) -> bool:
        return self._running

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "brainflow",
            "available": self.is_available(),
            "running": self._running,
            "board_id": self._board_id,
            "board_name": self.board_name(),
            "profile_id": self.config.get("profile_id"),
            "serial_port": _safe_port(self.config.get("serial_port")),
            "ip_address": self.config.get("ip_address"),
            "mac_address": _redact(self.config.get("mac_address")),
            "sampling_rate": self._sampling_rate or self._safe_board_value("sampling_rate"),
            "eeg_channels": self._eeg_channels or self._safe_board_value("eeg_channels"),
            "channel_names": self._channel_names or self._safe_board_value("eeg_names"),
            "physical_or_synthetic": self.physical_or_synthetic(),
            "last_error": self._last_error,
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "modalities": ["eeg"],
            "hardware_required": self._board_id != -1,
            "dependency": "brainflow",
            "available": self.is_available(),
            "supported_profiles": [
                "brainflow_synthetic_eeg",
                "openbci_cyton_8ch",
                "openbci_ganglion_4ch",
            ],
            "sampling_rate": self._safe_board_value("sampling_rate"),
            "channel_names": self._safe_board_value("eeg_names") or [],
            "eeg_channels": self._safe_board_value("eeg_channels") or [],
        }

    def diagnostics(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "capabilities": self.capabilities(),
            "serial_ports": detect_serial_ports(),
            "config_warnings": self.config_warnings(),
        }

    def config_warnings(self) -> list[str]:
        warnings: list[str] = []
        if self._board_id in {0, 1} and not self.config.get("serial_port"):
            warnings.append("Physical OpenBCI boards require an explicit serial_port.")
        if self._board_id not in {-1, 0, 1}:
            warnings.append("Board id is not one of the documented NeuroVerse defaults.")
        return warnings

    def board_name(self) -> str:
        descr = self._safe_board_descr()
        if isinstance(descr, dict) and descr.get("name"):
            return str(descr["name"])
        if self._board_id == -1:
            return "BrainFlow SyntheticBoard"
        if self._board_id == 0:
            return "OpenBCI Cyton"
        if self._board_id == 1:
            return "OpenBCI Ganglion"
        return f"BrainFlow board {self._board_id}"

    def physical_or_synthetic(self) -> str:
        return "synthetic" if self._board_id == -1 else "physical"

    def _configure_static_channels(self, board_shim: Any) -> None:
        self._sampling_rate = float(
            _numeric(self.config.get("sampling_rate"))
            or _numeric(self.config.get("expected_sampling_rate"))
            or board_shim.get_sampling_rate(self._board_id)
        )
        self._eeg_channels = list(board_shim.get_eeg_channels(self._board_id))
        self._timestamp_channel = int(board_shim.get_timestamp_channel(self._board_id))
        descr = board_shim.get_board_descr(self._board_id)
        names = _normalize_names(descr.get("eeg_names"))
        self._channel_names = names or [
            f"EEG{i + 1}" for i in range(len(self._eeg_channels))
        ]

    def _safe_board_value(self, key: str) -> Any:
        if not self.is_available():
            return None
        try:
            board_shim, _, _ = self._brainflow_classes()
            if key == "sampling_rate":
                return board_shim.get_sampling_rate(self._board_id)
            if key == "eeg_channels":
                return list(board_shim.get_eeg_channels(self._board_id))
            if key == "eeg_names":
                return _normalize_names(board_shim.get_board_descr(self._board_id).get("eeg_names"))
        except Exception:
            return None
        return None

    def _safe_board_descr(self) -> dict[str, Any] | None:
        if not self.is_available():
            return None
        try:
            board_shim, _, _ = self._brainflow_classes()
            return dict(board_shim.get_board_descr(self._board_id))
        except Exception:
            return None

    @staticmethod
    def _brainflow_classes() -> tuple[Any, Any, type[Exception]]:
        from brainflow.board_shim import BoardShim, BrainFlowInputParams
        from brainflow.exit_codes import BrainFlowError

        return BoardShim, BrainFlowInputParams, BrainFlowError

    @staticmethod
    def _resolve_board_id(config: dict[str, Any]) -> int:
        raw = config.get("board_id", config.get("board", config.get("board_name", -1)))
        if isinstance(raw, int):
            return raw
        if isinstance(raw, str):
            stripped = raw.strip()
            if stripped.lstrip("-").isdigit():
                return int(stripped)
            return BOARD_NAME_TO_ID.get(stripped.lower(), -1)
        return -1

    @staticmethod
    def is_available() -> bool:
        return importlib.util.find_spec("brainflow") is not None


def detect_serial_ports() -> list[str]:
    candidates: list[str] = []
    for pattern in ("/dev/ttyUSB*", "/dev/ttyACM*", "/dev/cu.*", "/dev/rfcomm*"):
        candidates.extend(glob.glob(pattern))
    return sorted(set(candidates))


def discover_brainflow_devices() -> dict[str, Any]:
    """Return local serial device hints without requiring pyserial."""
    pyserial_available = importlib.util.find_spec("serial") is not None
    devices: list[dict[str, Any]] = []
    if pyserial_available:
        try:
            from serial.tools import list_ports

            for port in list_ports.comports():
                devices.append({
                    "device": port.device,
                    "description": port.description,
                    "manufacturer": port.manufacturer,
                    "vid": f"{port.vid:04x}" if port.vid is not None else None,
                    "pid": f"{port.pid:04x}" if port.pid is not None else None,
                    "likely_openbci": _looks_like_openbci(
                        " ".join(
                            str(value or "")
                            for value in (
                                port.device,
                                port.description,
                                port.manufacturer,
                                port.product,
                            )
                        )
                    ),
                })
        except Exception as exc:
            return {
                "pyserial_available": True,
                "devices": [],
                "warnings": [f"Serial metadata discovery failed: {exc}"],
                "next_commands": _device_next_commands(None),
            }
    else:
        for path in detect_serial_ports():
            devices.append({
                "device": path,
                "description": None,
                "manufacturer": None,
                "vid": None,
                "pid": None,
                "likely_openbci": _looks_like_openbci(path),
            })
    first = devices[0]["device"] if devices else None
    warnings = []
    if not pyserial_available:
        warnings.append("pyserial is not installed; showing path-only serial discovery.")
    if not devices:
        warnings.append("No serial devices detected. Connect/pair the board and retry.")
    return {
        "pyserial_available": pyserial_available,
        "devices": devices,
        "warnings": warnings,
        "next_commands": _device_next_commands(first),
    }


def _looks_like_openbci(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("openbci", "cyton", "ganglion", "ftdi", "usb serial"))


def _device_next_commands(port: str | None) -> dict[str, str]:
    placeholder = port or "/dev/ttyUSB0"
    return {
        "discover": "make discover-brainflow-devices",
        "cyton_trial": f"make physical-eeg-trial-openbci-cyton PORT={placeholder}",
        "ganglion_trial": f"make physical-eeg-trial-openbci-ganglion PORT={placeholder}",
        "record_only_validation": f"make validate-openbci-cyton PORT={placeholder}",
    }


def _safe_port(value: Any) -> Any:
    if not value:
        return value
    text = str(value)
    return text if text.startswith("/dev/") else "<configured>"


def _redact(value: Any) -> Any:
    if not value:
        return value
    text = str(value)
    return f"{text[:2]}***{text[-2:]}" if len(text) > 4 else "***"


def _normalize_names(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item) for item in value]


def _numeric(value: Any) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None
