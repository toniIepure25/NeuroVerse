from __future__ import annotations

from typing import Any

from app.acquisition.base import BaseAcquisition
from app.acquisition.lsl_discovery import (
    PYLSL_INSTALL_HINT,
    discover_streams,
    inspect_stream,
    load_pylsl,
    pylsl_available,
    stream_info_to_dict,
)
from app.schemas.signals import RawSignalPayload


class LSLAcquisition(BaseAcquisition):
    """Hardware-ready adapter shell for Lab Streaming Layer streams."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self._running = False
        self._last_error: str | None = None
        self._pylsl: Any | None = None
        self._inlet: Any | None = None
        self._stream_info: dict[str, Any] | None = None
        self._last_timestamp: float | None = None
        self._last_clock_offset: float | None = None

    async def get_window(self) -> RawSignalPayload:
        if not self._running or self._inlet is None or self._stream_info is None:
            raise RuntimeError("LSL stream is not running; call start() first.")
        max_samples = int(self.config.get("max_samples", self._samples_per_window()))
        timeout = float(self.config.get("pull_timeout", 1.0))
        chunk, timestamps = self._inlet.pull_chunk(timeout=timeout, max_samples=max_samples)
        if not chunk or not timestamps:
            self._last_error = "Timed out while reading from selected LSL stream."
            raise TimeoutError(self._last_error)
        self._last_timestamp = float(timestamps[-1])
        data = _chunk_to_channel_rows(chunk)
        return RawSignalPayload(
            modality="eeg",
            sampling_rate=float(self._stream_info.get("nominal_srate") or 1.0),
            channel_names=self._channel_names(),
            data=data,
            window_size_ms=max(1, int(round((len(timestamps) / self._nominal_rate()) * 1000))),
            signal_quality_hint=None,
            timestamps=[float(ts) for ts in timestamps],
            metadata={
                "source": "lsl",
                "stream": self._stream_info,
                "clock_offset": self._last_clock_offset,
            },
        )

    async def start(self) -> None:
        if not self.is_available():
            self._last_error = "Optional dependency 'pylsl' is not installed."
            raise RuntimeError(PYLSL_INSTALL_HINT)
        self._pylsl = load_pylsl()
        self._stream_info = inspect_stream(
            name=self.config.get("stream_name"),
            stream_type=self.config.get("stream_type"),
            source_id=self.config.get("source_id"),
            timeout=float(self.config.get("timeout", 1.0)),
        )
        infos = self._pylsl.resolve_streams(wait_time=float(self.config.get("timeout", 1.0)))
        selected = None
        for info in infos:
            if stream_info_to_dict(info).get("stream_id") == self._stream_info["stream_id"]:
                selected = info
                break
        if selected is None:
            self._last_error = "Selected LSL stream disappeared before inlet creation."
            raise FileNotFoundError(self._last_error)
        self._inlet = self._pylsl.StreamInlet(selected, max_buflen=60)
        try:
            full_info = self._inlet.info(timeout=float(self.config.get("timeout", 1.0)))
            self._stream_info = stream_info_to_dict(full_info)
        except Exception:
            pass
        try:
            self._last_clock_offset = float(self._inlet.time_correction(timeout=0.5))
        except Exception:
            self._last_clock_offset = None
        self._running = True
        self._last_error = None

    async def stop(self) -> None:
        self._running = False
        self._inlet = None

    def is_running(self) -> bool:
        return self._running

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "lsl",
            "available": self.is_available(),
            "running": self._running,
            "stream_name": self.config.get("stream_name"),
            "stream_type": self.config.get("stream_type"),
            "source_id": self.config.get("source_id"),
            "selected_stream": self._stream_info,
            "last_timestamp": self._last_timestamp,
            "clock_offset": self._last_clock_offset,
            "last_error": self._last_error,
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "modalities": ["eeg", "physio", "gaze"],
            "hardware_required": False,
            "dependency": "pylsl",
            "available": self.is_available(),
            "timestamped_streams": True,
        }

    @staticmethod
    def is_available() -> bool:
        return pylsl_available()

    @staticmethod
    def discover_streams(
        name: str | None = None,
        stream_type: str | None = None,
        source_id: str | None = None,
        timeout: float = 1.0,
    ) -> list[dict[str, Any]]:
        return discover_streams(
            name=name,
            stream_type=stream_type,
            source_id=source_id,
            timeout=timeout,
        )

    def _nominal_rate(self) -> float:
        if self._stream_info is None:
            return 1.0
        return float(self._stream_info.get("nominal_srate") or 1.0)

    def _samples_per_window(self) -> int:
        window_seconds = float(self.config.get("window_seconds", 0.5))
        return max(1, int(round(self._nominal_rate() * window_seconds)))

    def _channel_names(self) -> list[str]:
        if self._stream_info is None:
            return []
        names = self._stream_info.get("channel_names") or []
        count = int(self._stream_info.get("channel_count") or len(names))
        if len(names) == count:
            return names
        return [*names, *[f"ch{i + 1}" for i in range(len(names), count)]]


def _chunk_to_channel_rows(chunk: list[list[float]]) -> list[list[float]]:
    if not chunk:
        return []
    channel_count = len(chunk[0])
    return [[float(sample[i]) for sample in chunk] for i in range(channel_count)]
