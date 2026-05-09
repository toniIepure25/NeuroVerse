from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

SafetyDecision = Literal["ALLOWED", "BLOCKED", "WAIT", "ASK"]
SafetyLevel = Literal["normal", "caution", "freeze"]


class SafetyDecisionPayload(BaseModel):
    """Safety gate output controlling whether adaptation proceeds."""

    decision: SafetyDecision
    reason: str
    sqi_scores: dict[str, float] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)
    blocked_actions: list[str] = Field(default_factory=list)
    safety_level: SafetyLevel = "normal"
