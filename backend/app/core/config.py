from __future__ import annotations

import json
from pathlib import Path

from pydantic_settings import BaseSettings


class NeuroVerseSettings(BaseSettings):
    """Central configuration loaded from environment / .env file."""

    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    environment_mode: str = "dev"
    performance_mode: str = "demo"
    tick_interval_ms: int = 500
    session_duration_s: int = 180
    data_dir: Path = Path("./data")
    models_dir: Path = Path("../models")
    reports_dir: Path = Path("../reports")
    hardware_mode: str = "simulator"
    hardware_closed_loop_enabled: bool = False
    model_mode: str = "heuristic"
    cors_origins: str = '["http://localhost:5173","http://localhost:3000"]'

    # Safety thresholds
    eeg_sqi_block: float = 0.35
    multimodal_sqi_wait: float = 0.45
    confidence_wait: float = 0.45
    confidence_block: float = 0.25
    stress_limit_threshold: float = 0.75

    # Smoothing
    max_intensity_delta: float = 0.25
    action_cooldown_ms: int = 2000
    smoothing_window: int = 5

    model_config = {"env_prefix": "NEUROVERSE_"}

    @property
    def cors_origin_list(self) -> list[str]:
        return json.loads(self.cors_origins)

    @property
    def sessions_dir(self) -> Path:
        p = self.data_dir / "sessions"
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def tick_interval_s(self) -> float:
        return self.tick_interval_ms / 1000.0

    @property
    def tick_rate_hz(self) -> float:
        return round(1000.0 / self.tick_interval_ms, 4)


settings = NeuroVerseSettings()
