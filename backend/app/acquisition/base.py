from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.schemas.signals import RawSignalPayload


class BaseAcquisition(ABC):
    """Abstract base for biosignal acquisition sources."""

    @abstractmethod
    async def get_window(self) -> RawSignalPayload:
        """Return the next data window."""
        ...

    async def read_window(self) -> RawSignalPayload:
        """Alias used by hardware-ready adapters and diagnostics."""
        return await self.get_window()

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...

    @abstractmethod
    def is_running(self) -> bool:
        ...

    def status(self) -> dict[str, Any]:
        return {
            "adapter": self.__class__.__name__,
            "running": self.is_running(),
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "modalities": [],
            "sampling_rate": None,
            "channel_names": [],
            "hardware_required": False,
        }


AcquisitionAdapter = BaseAcquisition
