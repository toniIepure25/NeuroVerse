from __future__ import annotations

from pathlib import Path

from app.core.config import settings
from app.core.logging import logger
from app.schemas.events import BaseEvent


class SessionRecorder:
    """Appends BaseEvent objects as JSON lines to a session file."""

    def __init__(self, session_id: str, base_dir: Path | None = None) -> None:
        self.session_id = session_id
        self._dir = base_dir or settings.sessions_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._path = self._dir / f"{session_id}.jsonl"
        self._count = 0

    def record(self, event: BaseEvent) -> None:
        with open(self._path, "a") as f:
            f.write(event.model_dump_json() + "\n")
        self._count += 1

    @property
    def event_count(self) -> int:
        return self._count

    @property
    def file_path(self) -> Path:
        return self._path

    def close(self) -> None:
        logger.info("Session %s recorded %d events to %s", self.session_id, self._count, self._path)
