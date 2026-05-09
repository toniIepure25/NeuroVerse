from __future__ import annotations

from app.api.websocket_manager import manager
from app.core.engine import NeuroVerseEngine

_engine: NeuroVerseEngine | None = None


def get_engine() -> NeuroVerseEngine:
    global _engine
    if _engine is None:
        _engine = NeuroVerseEngine(broadcast=manager.broadcast)
    return _engine
