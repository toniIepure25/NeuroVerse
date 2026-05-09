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


def compute_gaze_sqi(data: list[list[float]], channel_names: list[str]) -> float:
    """Gaze tracking quality score in [0, 1]."""
    cmap = _upper_map(channel_names)
    gx = _series(data, cmap, "GAZE_X")
    gy = _series(data, cmap, "GAZE_Y")
    blink = _series(data, cmap, "BLINK")

    parts: list[float] = []

    if gx.size and gy.size:
        n = int(min(gx.size, gy.size))
        x = gx[:n].astype(float)
        y = gy[:n].astype(float)
        mask = (
            np.isfinite(x)
            & np.isfinite(y)
            & (x >= -0.05)
            & (x <= 1.05)
            & (y >= -0.05)
            & (y <= 1.05)
        )
        alt_mask = (
            np.isfinite(x)
            & np.isfinite(y)
            & (np.abs(x) <= 1.2)
            & (np.abs(y) <= 1.2)
        )
        # Prefer standard screen-normalized bounds; fall back to symmetric if few in-range
        frac_standard = float(np.mean(mask)) if n else 0.0
        frac_alt = float(np.mean(alt_mask)) if n else 0.0
        tracking_validity = frac_standard if frac_standard >= 0.2 else frac_alt
    elif gx.size or gy.size:
        one = gx if gx.size else gy
        v = one[np.isfinite(one)]
        tracking_validity = float(np.mean((v >= -0.05) & (v <= 1.05))) if v.size else 0.5
    else:
        tracking_validity = 0.5
    parts.append(clamp(tracking_validity, 0.0, 1.0))

    if blink.size:
        b = blink[np.isfinite(blink)]
        if b.size:
            br = float(np.mean(b > 0.5))
            if br <= 0.50:
                blink_excess_score = 1.0
            else:
                blink_excess_score = clamp(1.0 - (br - 0.50) / 0.50, 0.0, 1.0)
        else:
            blink_excess_score = 0.5
    else:
        blink_excess_score = 1.0
    parts.append(blink_excess_score)

    if gx.size > 4:
        x = gx.astype(float)
        x = x[np.isfinite(x)]
        if x.size > 4:
            d2 = np.diff(x, n=2)
            d2 = d2[np.isfinite(d2)]
            if d2.size:
                jit = float(np.std(d2))
                gaze_jitter_score = clamp(1.0 - float(np.tanh(jit * 6.0)), 0.0, 1.0)
            else:
                gaze_jitter_score = 0.5
        else:
            gaze_jitter_score = 0.5
    else:
        gaze_jitter_score = 0.5
    parts.append(gaze_jitter_score)

    w = (0.45, 0.30, 0.25)
    return clamp(float(np.dot(w, parts)), 0.0, 1.0)
