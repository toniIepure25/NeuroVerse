from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AdaptationActionPayload(BaseModel):
    """An environment adaptation action emitted by the policy engine."""

    action: str
    intensity: float = Field(ge=0, le=1)
    duration_ms: int = Field(ge=0)
    source_state: str = ""
    reason: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)
