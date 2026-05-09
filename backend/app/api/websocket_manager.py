from __future__ import annotations

from typing import Any

from fastapi import WebSocket

from app.core.logging import logger
from app.core.telemetry import telemetry


class ConnectionManager:
    """Manages WebSocket connections and broadcasts events to all clients."""

    def __init__(self) -> None:
        self._connections: list[WebSocket] = []
        self._dropped_events = 0

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._connections.append(ws)
        logger.info("WebSocket client connected (%d total)", len(self._connections))

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self._connections:
            self._connections.remove(ws)
        logger.info("WebSocket client disconnected (%d remaining)", len(self._connections))

    async def broadcast(self, data: dict[str, Any]) -> None:
        stale: list[WebSocket] = []
        for ws in self._connections:
            try:
                await ws.send_json(data)
            except Exception:
                stale.append(ws)
                self._dropped_events += 1
                telemetry.add_dropped_events()
        for ws in stale:
            self.disconnect(ws)

    @property
    def client_count(self) -> int:
        return len(self._connections)

    @property
    def dropped_events(self) -> int:
        return self._dropped_events

    def status(self) -> dict[str, int]:
        return {
            "connected_clients": self.client_count,
            "dropped_events": self._dropped_events,
        }


manager = ConnectionManager()
