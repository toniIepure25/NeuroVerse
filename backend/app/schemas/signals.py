from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Modality = Literal["eeg", "eda", "hrv", "gaze", "multimodal"]


class RawSignalPayload(BaseModel):
    """Payload for a raw biosignal data window."""

    modality: Modality
    sampling_rate: float = Field(gt=0)
    channel_names: list[str]
    data: list[list[float]]
    window_size_ms: int = Field(gt=0)
    signal_quality_hint: float | None = Field(default=None, ge=0, le=1)
    timestamps: list[float] | None = None
    metadata: dict[str, Any] | None = None
