from __future__ import annotations

from pydantic import BaseModel, Field


class StatePredictionPayload(BaseModel):
    """Estimated cognitive / affective state from multimodal features."""

    focus: float = Field(ge=0, le=1)
    relaxation: float = Field(ge=0, le=1)
    workload: float = Field(ge=0, le=1)
    stress: float = Field(ge=0, le=1)
    fatigue: float = Field(ge=0, le=1)
    imagery_engagement: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    model_version: str = "heuristic-v1"
    feature_window_ms: int = 500
