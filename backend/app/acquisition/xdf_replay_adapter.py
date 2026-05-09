from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from app.acquisition.base import BaseAcquisition
from app.schemas.signals import RawSignalPayload


class XDFReplayAcquisition(BaseAcquisition):
    """Optional XDF replay adapter with graceful pyxdf dependency handling."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._running = False
        self._last_error: str | None = None

    async def start(self) -> None:
        if not self.is_available():
            self._last_error = "Optional dependency 'pyxdf' is not installed."
            raise RuntimeError("XDF replay requires optional dependency pyxdf.")
        if not self.path.exists():
            self._last_error = f"XDF file not found: {self.path}"
            raise FileNotFoundError(self._last_error)
        self._last_error = (
            "pyxdf is available, but stream-to-NeuroVerse channel mapping must be "
            "configured before replaying real XDF files."
        )
        raise RuntimeError(self._last_error)

    async def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    async def get_window(self) -> RawSignalPayload:
        raise RuntimeError("XDF replay is not running")

    def status(self) -> dict[str, Any]:
        return {
            "adapter": "xdf_replay",
            "available": self.is_available(),
            "running": self._running,
            "path": str(self.path),
            "last_error": self._last_error,
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "modalities": ["eeg", "physio", "gaze"],
            "hardware_required": False,
            "dependency": "pyxdf",
            "available": self.is_available(),
            "timestamped_streams": True,
        }

    @staticmethod
    def is_available() -> bool:
        return importlib.util.find_spec("pyxdf") is not None
