from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd

LabelStrategy = Literal["majority", "center", "nearest_previous", "interval_overlap"]


@dataclass(slots=True)
class LabelInterval:
    start: float
    end: float
    label: Any


def window_starts(
    start_time: float,
    end_time: float,
    window_size_seconds: float,
    overlap: float,
) -> list[float]:
    if window_size_seconds <= 0:
        raise ValueError("window_size_seconds must be positive")
    if not 0 <= overlap < 1:
        raise ValueError("overlap must satisfy 0 <= overlap < 1")
    step = window_size_seconds * (1.0 - overlap)
    starts: list[float] = []
    t = float(start_time)
    last_start = float(end_time) - window_size_seconds
    while t <= last_start + 1e-9:
        starts.append(round(t, 10))
        t += step
    return starts


def align_point_labels(
    timestamps: list[float] | np.ndarray,
    labels: list[Any] | np.ndarray,
    start: float,
    end: float,
    strategy: LabelStrategy = "majority",
) -> Any:
    ts = np.asarray(timestamps, dtype=float)
    label_arr = np.asarray(labels, dtype=object)
    if ts.size == 0:
        return None

    if strategy == "center":
        center = start + (end - start) / 2.0
        idx = int(np.argmin(np.abs(ts - center)))
        return label_arr[idx]

    if strategy == "nearest_previous":
        center = start + (end - start) / 2.0
        idxs = np.where(ts <= center)[0]
        if idxs.size == 0:
            return label_arr[0]
        return label_arr[int(idxs[-1])]

    mask = (ts >= start) & (ts < end)
    if not np.any(mask):
        return align_point_labels(ts, label_arr, start, end, "center")
    counts = Counter(label_arr[mask].tolist())
    return counts.most_common(1)[0][0]


def align_interval_labels(
    intervals: list[LabelInterval],
    start: float,
    end: float,
) -> Any:
    if not intervals:
        return None
    overlaps: dict[Any, float] = {}
    for item in intervals:
        overlap = max(0.0, min(end, item.end) - max(start, item.start))
        if overlap > 0:
            overlaps[item.label] = overlaps.get(item.label, 0.0) + overlap
    if not overlaps:
        center = start + (end - start) / 2.0
        nearest = min(intervals, key=lambda item: abs(((item.start + item.end) / 2.0) - center))
        return nearest.label
    return max(overlaps.items(), key=lambda kv: kv[1])[0]


def frame_windows(
    frame: pd.DataFrame,
    timestamp_col: str,
    window_size_seconds: float,
    overlap: float,
) -> list[pd.DataFrame]:
    if frame.empty:
        return []
    ordered = frame.sort_values(timestamp_col)
    t_min = float(ordered[timestamp_col].min())
    t_max = float(ordered[timestamp_col].max())
    windows: list[pd.DataFrame] = []
    for start in window_starts(t_min, t_max, window_size_seconds, overlap):
        end = start + window_size_seconds
        win = ordered[(ordered[timestamp_col] >= start) & (ordered[timestamp_col] < end)]
        if not win.empty:
            windows.append(win)
    return windows
