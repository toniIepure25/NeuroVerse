from __future__ import annotations

import numpy as np

from app.core.numeric import clamp


def _upper_map(names: list[str]) -> dict[str, int]:
    return {str(n).strip().upper(): i for i, n in enumerate(names)}


def _series(data: list[list[float]], cmap: dict[str, int], key: str) -> np.ndarray:
    idx = cmap.get(key.upper())
    if idx is None or idx >= len(data):
        return np.array([], dtype=float)
    return np.asarray(data[idx], dtype=float)


def extract_gaze_features(
    data: list[list[float]],
    channel_names: list[str],
) -> dict[str, float]:
    cmap = _upper_map(channel_names)
    gx = _series(data, cmap, "GAZE_X")
    gy = _series(data, cmap, "GAZE_Y")
    pupil = _series(data, cmap, "PUPIL_DIAMETER")
    blink = _series(data, cmap, "BLINK")

    n = 0
    if gx.size and gy.size:
        n = int(min(gx.size, gy.size))
    elif gx.size:
        n = int(gx.size)
    elif gy.size:
        n = int(gy.size)

    if n < 2:
        return {
            "fixation_stability": 0.5,
            "gaze_dispersion": 0.5,
            "blink_rate": 0.0,
            "blink_duration_proxy": 0.0,
            "pupil_diameter_proxy": 0.5,
            "saccade_rate_proxy": 0.0,
        }

    x = gx[:n].astype(float)
    y = gy[:n].astype(float)
    if not np.any(np.isfinite(x)) or not np.any(np.isfinite(y)):
        fixation_stability = 0.5
        gaze_dispersion = 0.5
        saccade_rate_proxy = 0.0
    else:
        xs = float(np.nanstd(x))
        ys = float(np.nanstd(y))
        pos_std = float(np.sqrt(xs * xs + ys * ys))
        fixation_stability = clamp(1.0 - float(np.tanh(pos_std * 3.0)), 0.0, 1.0)
        span_x = float(np.nanmax(x) - np.nanmin(x))
        span_y = float(np.nanmax(y) - np.nanmin(y))
        area = span_x * span_y
        gaze_dispersion = clamp(float(np.tanh(area * 2.0)), 0.0, 1.0)

        dx = np.diff(x)
        dy = np.diff(y)
        step = np.sqrt(dx * dx + dy * dy)
        step = step[np.isfinite(step)]
        if step.size:
            thresh = float(np.percentile(step, 90) + 1e-9)
            if thresh < 1e-6:
                thresh = 0.05
            saccades = int(np.sum(step > max(thresh, 0.02)))
            saccade_rate_proxy = clamp(saccades / max(5.0, float(step.size) / 8.0), 0.0, 1.0)
        else:
            saccade_rate_proxy = 0.0

    if blink.size:
        b = blink[: min(n, blink.size)].astype(float)
        valid = np.isfinite(b)
        if np.any(valid):
            blink_rate = clamp(float(np.mean((b > 0.5) & valid)), 0.0, 1.0)
        else:
            blink_rate = 0.0
        runs_mask = (b > 0.5).astype(np.int8)
        if runs_mask.size:
            padded = np.concatenate([[0], runs_mask, [0]])
            diffs = np.diff(padded)
            starts = np.where(diffs == 1)[0]
            ends = np.where(diffs == -1)[0]
            lengths = ends - starts
            if lengths.size:
                mean_len = float(np.mean(lengths))
                blink_duration_proxy = clamp(float(np.tanh(mean_len / 5.0)), 0.0, 1.0)
            else:
                blink_duration_proxy = 0.0
        else:
            blink_duration_proxy = 0.0
    else:
        blink_rate = 0.0
        blink_duration_proxy = 0.0

    if pupil.size:
        pseg = pupil[: min(n, pupil.size)].astype(float)
        if np.any(np.isfinite(pseg)):
            pm = float(np.nanmean(pseg))
            pupil_diameter_proxy = clamp(float(np.tanh(abs(pm))), 0.0, 1.0)
        else:
            pupil_diameter_proxy = 0.5
    else:
        pupil_diameter_proxy = 0.5

    return {
        "fixation_stability": clamp(fixation_stability, 0.0, 1.0),
        "gaze_dispersion": clamp(gaze_dispersion, 0.0, 1.0),
        "blink_rate": blink_rate,
        "blink_duration_proxy": blink_duration_proxy,
        "pupil_diameter_proxy": pupil_diameter_proxy,
        "saccade_rate_proxy": clamp(saccade_rate_proxy, 0.0, 1.0),
    }
