from __future__ import annotations

from statistics import mean
from typing import Any


def estimate_effective_sampling_rate(timestamps: list[float]) -> float | None:
    if len(timestamps) < 2:
        return None
    duration = timestamps[-1] - timestamps[0]
    if duration <= 0:
        return None
    return round((len(timestamps) - 1) / duration, 4)


def compute_jitter(timestamps: list[float], expected_rate_hz: float) -> dict[str, float | None]:
    if len(timestamps) < 2 or expected_rate_hz <= 0:
        return {
            "jitter_ms_mean": None,
            "jitter_ms_p50": None,
            "jitter_ms_p95": None,
            "jitter_ms_p99": None,
            "jitter_ms_max": None,
        }
    expected_dt = 1.0 / expected_rate_hz
    deltas = [b - a for a, b in zip(timestamps, timestamps[1:], strict=False)]
    jitter_ms = [abs(delta - expected_dt) * 1000.0 for delta in deltas]
    return {
        "jitter_ms_mean": round(mean(jitter_ms), 4),
        "jitter_ms_p50": _percentile(jitter_ms, 0.50),
        "jitter_ms_p95": _percentile(jitter_ms, 0.95),
        "jitter_ms_p99": _percentile(jitter_ms, 0.99),
        "jitter_ms_max": round(max(jitter_ms), 4),
    }


def detect_time_gaps(timestamps: list[float], max_gap_ms: float) -> list[dict[str, float]]:
    gaps = []
    for idx, (a, b) in enumerate(zip(timestamps, timestamps[1:], strict=False)):
        gap_ms = (b - a) * 1000.0
        if gap_ms > max_gap_ms:
            gaps.append({"index": idx, "gap_ms": round(gap_ms, 4)})
    return gaps


def detect_duplicate_timestamps(timestamps: list[float]) -> int:
    return len(timestamps) - len(set(timestamps))


def monotonic_timestamp_pass(timestamps: list[float]) -> bool:
    return all(b > a for a, b in zip(timestamps, timestamps[1:], strict=False))


def validate_sampling_rate(
    expected_rate_hz: float,
    observed_rate_hz: float | None,
    tolerance_percent: float = 5.0,
) -> dict[str, Any]:
    if observed_rate_hz is None or expected_rate_hz <= 0:
        return {
            "pass": False,
            "drift_percent": None,
            "warning": "Insufficient timestamps for sampling-rate validation.",
        }
    drift = ((observed_rate_hz - expected_rate_hz) / expected_rate_hz) * 100.0
    passed = abs(drift) <= tolerance_percent
    return {
        "pass": passed,
        "drift_percent": round(drift, 4),
        "warning": None if passed else "Observed sampling rate drift exceeds tolerance.",
    }


def summarize_window_timing(
    timestamps: list[float],
    expected_rate_hz: float,
    max_gap_ms: float | None = None,
    tolerance_percent: float = 5.0,
    clock_offsets: list[float] | None = None,
) -> dict[str, Any]:
    max_gap_ms = max_gap_ms or (1000.0 / expected_rate_hz) * 3.0
    observed = estimate_effective_sampling_rate(timestamps)
    rate = validate_sampling_rate(expected_rate_hz, observed, tolerance_percent)
    jitter = compute_jitter(timestamps, expected_rate_hz)
    gaps = detect_time_gaps(timestamps, max_gap_ms)
    duplicate_count = detect_duplicate_timestamps(timestamps)
    monotonic = monotonic_timestamp_pass(timestamps)
    clock = _clock_offset_summary(clock_offsets or [])
    warnings = []
    if rate["warning"]:
        warnings.append(rate["warning"])
    if gaps:
        warnings.append(f"Detected {len(gaps)} timestamp gap(s).")
    if duplicate_count:
        warnings.append(f"Detected {duplicate_count} duplicate timestamp(s).")
    if not monotonic:
        warnings.append("Timestamps are not strictly monotonic.")
    if clock["clock_offset_estimate"] is None:
        warnings.append("Clock offset estimate unavailable.")
    passed = bool(rate["pass"]) and not gaps and duplicate_count == 0 and monotonic
    quality = classify_timing_quality(
        passed=passed,
        drift_percent=rate["drift_percent"],
        jitter_ms_p95=jitter["jitter_ms_p95"],
        gap_count=len(gaps),
        duplicate_count=duplicate_count,
        monotonic=monotonic,
    )
    return {
        "pass": passed,
        "quality": quality,
        "expected_rate_hz": expected_rate_hz,
        "observed_rate_hz": observed,
        "drift_percent": rate["drift_percent"],
        **jitter,
        "gap_count": len(gaps),
        "gaps": gaps[:20],
        "duplicate_count": duplicate_count,
        "monotonic_timestamp_pass": monotonic,
        **clock,
        "warnings": warnings,
    }


def classify_timing_quality(
    *,
    passed: bool,
    drift_percent: float | None,
    jitter_ms_p95: float | None,
    gap_count: int,
    duplicate_count: int,
    monotonic: bool,
) -> str:
    """Classify engineering timing quality for validation reports."""
    if not passed or not monotonic or duplicate_count > 0:
        return "failed"
    drift = abs(drift_percent or 0.0)
    jitter = jitter_ms_p95 if jitter_ms_p95 is not None else float("inf")
    if gap_count > 0:
        return "warning"
    if drift <= 1.0 and jitter <= 2.0:
        return "excellent"
    if drift <= 5.0 and jitter <= 10.0:
        return "acceptable"
    return "warning"


def _clock_offset_summary(offsets: list[float]) -> dict[str, float | None]:
    if not offsets:
        return {"clock_offset_estimate": None, "clock_offset_jitter": None}
    return {
        "clock_offset_estimate": round(mean(offsets), 6),
        "clock_offset_jitter": round(max(offsets) - min(offsets), 6),
    }


def _percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    idx = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * q)))
    return round(ordered[idx], 4)
