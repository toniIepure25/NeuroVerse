from __future__ import annotations

import numpy as np

from app.core.numeric import clamp

# Assumed sampling rate for 50/60 Hz band localization when `data` has no timing metadata.
_DEFAULT_FS_HZ = 250.0
_AMPLITUDE_LIMIT = 200.0


def _channel_scores(matrix: np.ndarray) -> tuple[float, float, float, float, float]:
    """Per-channel aggregates max abs, variance, kurtosis excess, dropout frac, line noise ratio."""
    x = np.asarray(matrix, dtype=float).ravel()
    if x.size == 0:
        return 0.0, 0.0, 0.0, 1.0, 0.0

    max_abs = float(np.nanmax(np.abs(x)))
    finite = np.isfinite(x)
    dropout = float(np.mean(~finite | (x == 0.0)))

    xv = x[finite]
    if xv.size < 4:
        return max_abs, 0.0, 0.0, dropout, 0.0

    xv = xv - float(np.mean(xv))
    var = float(np.var(xv))
    std = float(np.std(xv))
    if std < 1e-12:
        kur = 0.0
    else:
        kur = float(np.mean((xv / std) ** 4.0) - 3.0)

    n = xv.size
    psd = np.abs(np.fft.rfft(xv)) ** 2
    freqs = np.fft.rfftfreq(n, 1.0 / _DEFAULT_FS_HZ)
    line_mask = (freqs >= 49.0) & (freqs <= 61.0)
    total = float(np.sum(psd) + 1e-12)
    line_ratio = float(np.sum(psd[line_mask]) / total)

    return max_abs, var, abs(kur), dropout, line_ratio


def compute_eeg_sqi(data: list[list[float]], channel_names: list[str]) -> float:
    """Return aggregate EEG signal quality in [0, 1]."""
    _ = channel_names
    if not data:
        return 0.0

    max_abs_vals: list[float] = []
    var_vals: list[float] = []
    kur_vals: list[float] = []
    drop_vals: list[float] = []
    line_vals: list[float] = []

    for row in data:
        m = np.asarray(row, dtype=float)
        if m.size == 0:
            continue
        ma, va, ku, dr, ln = _channel_scores(m)
        max_abs_vals.append(ma)
        var_vals.append(va)
        kur_vals.append(ku)
        drop_vals.append(dr)
        line_vals.append(min(ln, 1.0))

    if not max_abs_vals:
        return 0.0

    amp = float(np.max(max_abs_vals))
    over = max(0.0, amp - _AMPLITUDE_LIMIT) / _AMPLITUDE_LIMIT
    amplitude_range_score = clamp(1.0 - over, 0.0, 1.0)

    var_med = float(np.median(var_vals)) if var_vals else 0.0
    if var_med < 1e-8:
        variance_score = 0.2
    elif var_med > 1e6:
        variance_score = 0.3
    else:
        variance_score = 1.0

    kur_med = float(np.median(kur_vals)) if kur_vals else 0.0
    kurtosis_proxy_score = clamp(1.0 - kur_med / 10.0, 0.0, 1.0)

    drop_med = float(np.median(drop_vals)) if drop_vals else 1.0
    if drop_med <= 0.10:
        dropout_score = 1.0
    else:
        dropout_score = clamp(1.0 - (drop_med - 0.10) / 0.40, 0.0, 1.0)

    line_med = float(np.median(line_vals)) if line_vals else 0.0
    line_noise_proxy = clamp(1.0 - line_med * 8.0, 0.0, 1.0)

    weights = (0.25, 0.20, 0.15, 0.25, 0.15)
    parts = (
        amplitude_range_score,
        variance_score,
        kurtosis_proxy_score,
        dropout_score,
        line_noise_proxy,
    )
    return clamp(float(np.dot(weights, parts)), 0.0, 1.0)
