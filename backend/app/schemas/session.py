from __future__ import annotations

from pydantic import BaseModel, Field


class FeaturePayload(BaseModel):
    """Extracted features across all modalities for one time window."""

    eeg: dict[str, float] = Field(default_factory=dict)
    physio: dict[str, float] = Field(default_factory=dict)
    gaze: dict[str, float] = Field(default_factory=dict)
    multimodal: dict[str, float] = Field(default_factory=dict)
    sqi_scores: dict[str, float] = Field(default_factory=dict)


class SessionSummaryPayload(BaseModel):
    """Summary statistics for a completed session."""

    session_id: str
    started_at: float
    ended_at: float
    total_events: int = 0
    total_adaptations: int = 0
    safety_block_rate: float = Field(default=0.0, ge=0, le=1)
    average_focus: float = Field(default=0.0, ge=0, le=1)
    average_relaxation: float = Field(default=0.0, ge=0, le=1)
    average_stress: float = Field(default=0.0, ge=0, le=1)
