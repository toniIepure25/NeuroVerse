from __future__ import annotations

import math
from statistics import mean
from typing import Any

import numpy as np


def summarize_eeg_artifacts(
    data: list[list[float]],
    channel_names: list[str],
    amplitude_limit_uv: float = 200.0,
) -> dict[str, Any]:
    if not data:
        return {
            "channel_count": 0,
            "nan_inf_count": 0,
            "bad_channel_candidates": [],
            "per_channel": [],
            "warnings": ["No EEG samples available for artifact summary."],
        }

    per_channel = []
    bad: list[str] = []
    nan_inf_total = 0
    for idx, row in enumerate(data):
        name = channel_names[idx] if idx < len(channel_names) else f"ch{idx + 1}"
        arr = np.asarray(row, dtype=float)
        finite = np.isfinite(arr)
        nan_inf = int(arr.size - int(np.sum(finite)))
        nan_inf_total += nan_inf
        finite_values = arr[finite]
        if finite_values.size == 0:
            summary = {
                "channel": name,
                "min": None,
                "max": None,
                "peak_to_peak": None,
                "variance": None,
                "flatline": True,
                "extreme_amplitude": True,
                "nan_inf_count": nan_inf,
            }
            bad.append(name)
            per_channel.append(summary)
            continue
        min_v = float(np.min(finite_values))
        max_v = float(np.max(finite_values))
        ptp = max_v - min_v
        variance = float(np.var(finite_values))
        flatline = ptp < 1e-6 or variance < 1e-10
        extreme = max(abs(min_v), abs(max_v)) > amplitude_limit_uv
        if flatline or extreme or nan_inf:
            bad.append(name)
        per_channel.append({
            "channel": name,
            "min": round(min_v, 4),
            "max": round(max_v, 4),
            "peak_to_peak": round(ptp, 4),
            "variance": round(variance, 4),
            "flatline": flatline,
            "extreme_amplitude": extreme,
            "nan_inf_count": nan_inf,
        })

    peak_to_peak = [
        float(item["peak_to_peak"])
        for item in per_channel
        if isinstance(item.get("peak_to_peak"), int | float) and math.isfinite(item["peak_to_peak"])
    ]
    return {
        "channel_count": len(data),
        "nan_inf_count": nan_inf_total,
        "bad_channel_candidates": sorted(set(bad)),
        "mean_peak_to_peak": round(mean(peak_to_peak), 4) if peak_to_peak else None,
        "per_channel": per_channel,
        "warnings": (
            ["SQI is a software diagnostic proxy, not a clinical quality assessment."]
            + ([f"Bad channel candidates: {', '.join(sorted(set(bad)))}."] if bad else [])
        ),
    }


def merge_artifact_summaries(summaries: list[dict[str, Any]]) -> dict[str, Any]:
    if not summaries:
        return summarize_eeg_artifacts([], [])
    bad = sorted({
        channel
        for summary in summaries
        for channel in summary.get("bad_channel_candidates", [])
    })
    nan_inf = sum(int(summary.get("nan_inf_count") or 0) for summary in summaries)
    ptp_values = [
        float(summary["mean_peak_to_peak"])
        for summary in summaries
        if isinstance(summary.get("mean_peak_to_peak"), int | float)
    ]
    return {
        "window_count": len(summaries),
        "nan_inf_count": nan_inf,
        "bad_channel_candidates": bad,
        "mean_peak_to_peak": round(mean(ptp_values), 4) if ptp_values else None,
        "warnings": (
            ["SQI is a software diagnostic proxy, not a clinical quality assessment."]
            + ([f"Bad channel candidates: {', '.join(bad)}."] if bad else [])
        ),
    }
