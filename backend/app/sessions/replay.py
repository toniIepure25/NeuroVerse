from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import ReplayError, SessionNotFoundError
from app.schemas.events import BaseEvent


class SessionReplayer:
    """Loads a JSONL session file and yields events at original or accelerated timing."""

    def __init__(self, session_id: str, speed: float = 1.0, base_dir: Path | None = None) -> None:
        self.session_id = session_id
        self.speed = max(0.1, speed)
        self._dir = base_dir or settings.sessions_dir
        self._path = self._dir / f"{session_id}.jsonl"
        if not self._path.exists():
            raise SessionNotFoundError(f"Session file not found: {self._path}")

    def load_events(self) -> list[BaseEvent]:
        events: list[BaseEvent] = []
        with open(self._path) as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    events.append(BaseEvent(**data))
                except Exception as e:
                    raise ReplayError(f"Parse error at line {line_num}: {e}") from e
        return events

    async def stream(self) -> AsyncIterator[BaseEvent]:
        events = self.load_events()
        if not events:
            return

        t0 = events[0].timestamp
        for event in events:
            delay = (event.timestamp - t0) / self.speed
            t0 = event.timestamp
            if delay > 0:
                await asyncio.sleep(delay)
            yield event
