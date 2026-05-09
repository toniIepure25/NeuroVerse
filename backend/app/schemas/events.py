from __future__ import annotations

import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field

EventType = Literal[
    "neuroverse.signal.raw_window",
    "neuroverse.signal.window_processed",
    "neuroverse.features.extracted",
    "neuroverse.state.predicted",
    "neuroverse.safety.decision",
    "neuroverse.adaptation.action",
    "neuroverse.session.started",
    "neuroverse.session.stopped",
    "neuroverse.replay.started",
    "neuroverse.replay.completed",
    "neuroverse.runtime.emergency_stop",
    "neuroverse.runtime.freeze",
    "neuroverse.runtime.unfreeze",
    "neuroverse.error",
]


def new_event_id() -> str:
    return str(uuid.uuid4())


class BaseEvent(BaseModel):
    """Universal event envelope for all NeuroVerse events."""

    event_id: str = Field(default_factory=new_event_id)
    session_id: str
    event_type: EventType
    timestamp: float
    source: str
    correlation_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] | None = None
