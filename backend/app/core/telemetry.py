from __future__ import annotations

import time
from collections import deque
from statistics import mean
from typing import Any


def _percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * q)))
    return round(ordered[idx], 4)


class TelemetryStore:
    """Small in-memory telemetry store for local/demo runtime observability."""

    def __init__(self, max_samples: int = 500) -> None:
        self.started_at = time.time()
        self._max_samples = max_samples
        self._latencies_ms: dict[str, deque[float]] = {}
        self._confidence: deque[float] = deque(maxlen=max_samples)
        self._multimodal_sqi: deque[float] = deque(maxlen=max_samples)
        self._counters: dict[str, int] = {
            "ticks_processed": 0,
            "events_emitted": 0,
            "safety_blocks": 0,
            "freeze_events": 0,
            "dropped_events": 0,
        }

    @property
    def uptime_seconds(self) -> float:
        return round(time.time() - self.started_at, 3)

    def record_latency(self, stage: str, latency_ms: float) -> None:
        samples = self._latencies_ms.setdefault(stage, deque(maxlen=self._max_samples))
        samples.append(round(float(latency_ms), 4))

    def record_tick(self, stage_latencies_ms: dict[str, float]) -> None:
        self._counters["ticks_processed"] += 1
        total = sum(stage_latencies_ms.values())
        self.record_latency("total_tick", total)
        for stage, latency_ms in stage_latencies_ms.items():
            self.record_latency(stage, latency_ms)

    def record_event(self, event_type: str, payload: dict[str, Any]) -> None:
        self._counters["events_emitted"] += 1
        if event_type == "neuroverse.state.predicted":
            confidence = payload.get("confidence")
            if isinstance(confidence, int | float):
                self._confidence.append(float(confidence))
        elif event_type == "neuroverse.safety.decision":
            decision = str(payload.get("decision", "")).lower()
            if decision in {"block", "blocked"}:
                self._counters["safety_blocks"] += 1
        elif event_type == "neuroverse.adaptation.action":
            action_type = str(payload.get("action_type") or payload.get("action") or "").lower()
            if "freeze" in action_type:
                self._counters["freeze_events"] += 1

    def record_sqi(self, sqi_scores: dict[str, float]) -> None:
        value = sqi_scores.get("multimodal")
        if isinstance(value, int | float):
            self._multimodal_sqi.append(float(value))

    def add_dropped_events(self, count: int = 1) -> None:
        self._counters["dropped_events"] += count

    def latency_summary(self) -> dict[str, Any]:
        return {
            stage: self._summarize_samples(list(samples))
            for stage, samples in sorted(self._latencies_ms.items())
        }

    def metrics(
        self,
        connected_clients: int = 0,
        tick_rate_hz: float | None = None,
    ) -> dict[str, Any]:
        ticks = self._counters["ticks_processed"]
        total_events = self._counters["events_emitted"]
        safety_blocks = self._counters["safety_blocks"]
        total_tick = self._summarize_samples(list(self._latencies_ms.get("total_tick", [])))
        return {
            **self._counters,
            "connected_clients": connected_clients,
            "safety_block_rate": round(safety_blocks / max(ticks, 1), 4),
            "average_confidence": self._average(self._confidence),
            "average_multimodal_sqi": self._average(self._multimodal_sqi),
            "current_tick_rate_hz": tick_rate_hz,
            "average_end_to_end_latency_ms": total_tick.get("mean"),
            "events_per_tick": round(total_events / max(ticks, 1), 4),
            "uptime_seconds": self.uptime_seconds,
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "uptime_seconds": self.uptime_seconds,
            "latency": self.latency_summary(),
            "metrics": self.metrics(),
        }

    @staticmethod
    def _average(values: deque[float]) -> float | None:
        if not values:
            return None
        return round(mean(values), 4)

    @staticmethod
    def _summarize_samples(values: list[float]) -> dict[str, Any]:
        if not values:
            return {
                "count": 0,
                "mean": None,
                "p50": None,
                "p95": None,
                "p99": None,
                "max": None,
                "last_samples": [],
            }
        return {
            "count": len(values),
            "mean": round(mean(values), 4),
            "p50": _percentile(values, 0.50),
            "p95": _percentile(values, 0.95),
            "p99": _percentile(values, 0.99),
            "max": round(max(values), 4),
            "last_samples": values[-25:],
        }


telemetry = TelemetryStore()
