from __future__ import annotations

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/api")


@router.get("/config")
async def get_config() -> dict:
    return {
        "tick_interval_ms": settings.tick_interval_ms,
        "session_duration_s": settings.session_duration_s,
        "safety": {
            "eeg_sqi_block": settings.eeg_sqi_block,
            "multimodal_sqi_wait": settings.multimodal_sqi_wait,
            "confidence_wait": settings.confidence_wait,
            "confidence_block": settings.confidence_block,
            "stress_limit_threshold": settings.stress_limit_threshold,
        },
        "smoothing": {
            "max_intensity_delta": settings.max_intensity_delta,
            "action_cooldown_ms": settings.action_cooldown_ms,
            "smoothing_window": settings.smoothing_window,
        },
    }
