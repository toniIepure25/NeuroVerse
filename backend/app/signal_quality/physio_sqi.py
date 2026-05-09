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


def compute_physio_sqi(data: list[list[float]], channel_names: list[str]) -> float:
    """Physiological signal quality score in [0, 1]."""
    cmap = _upper_map(channel_names)
    hr = _series(data, cmap, "HR")
    hrv = _series(data, cmap, "HRV_RMSSD")
    eda_t = _series(data, cmap, "EDA_TONIC")
    eda_p = _series(data, cmap, "EDA_PHASIC")

    parts: list[float] = []

    if hr.size and np.any(np.isfinite(hr)):
        h = hr[np.isfinite(hr)]
        valid_hr_range = float(np.mean((h >= 40.0) & (h <= 200.0)))
    else:
        valid_hr_range = 0.5
    parts.append(valid_hr_range)

    if hrv.size and np.any(np.isfinite(hrv)):
        v = hrv[np.isfinite(hrv)]
        pos = float(np.mean(v > 0.0))
        stab = 1.0 - float(np.std(v) / (abs(float(np.mean(v))) + 1e-9)) if v.size > 1 else 1.0
        hrv_consistency = clamp(0.6 * pos + 0.4 * stab, 0.0, 1.0)
    else:
        hrv_consistency = 0.5
    parts.append(hrv_consistency)

    eda_all = []
    for arr in (eda_t, eda_p):
        if arr.size:
            eda_all.append(arr)
    if eda_all:
        ea = np.concatenate(eda_all)
        ea = ea[np.isfinite(ea)]
        if ea.size:
            q1, q99 = np.percentile(ea, [1, 99])
            span = q99 - q1
            # Loose microsiemens-style bounds for simulated EDA.
            in_range = float(np.mean((ea >= -50.0) & (ea <= 200.0)))
            spread_ok = clamp(1.0 - abs(span - 20.0) / 40.0, 0.0, 1.0)
            eda_range_score = clamp(0.7 * in_range + 0.3 * spread_ok, 0.0, 1.0)
        else:
            eda_range_score = 0.5
    else:
        eda_range_score = 0.5
    parts.append(eda_range_score)

    dropouts = []
    for arr in (hr, hrv, eda_t, eda_p):
        if arr.size == 0:
            continue
        bad = float(np.mean(~np.isfinite(arr) | (arr == 0.0)))
        dropouts.append(bad)
    if dropouts:
        worst = float(max(dropouts))
        dropout_score = clamp(1.0 - worst / 0.15, 0.0, 1.0)
    else:
        dropout_score = 0.5
    parts.append(dropout_score)

    w = (0.30, 0.25, 0.25, 0.20)
    return clamp(float(np.dot(w, parts)), 0.0, 1.0)
