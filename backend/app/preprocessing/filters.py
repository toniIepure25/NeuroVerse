from __future__ import annotations

import numpy as np

ArrayLike = np.ndarray


def bandpass_filter(
    data: ArrayLike,
    low: float,
    high: float,
    fs: float,
) -> np.ndarray:
    """Apply a lightweight band-limited smoothing suitable for simulated pipelines.

    For real data, replace with a proper Butterworth or SOS bandpass implementation.

    Args:
        data: One-dimensional samples.
        low: Low cutoff frequency in Hz.
        high: High cutoff frequency in Hz.
        fs: Sampling rate in Hz.

    Returns:
        Smoothed array with the same shape as ``data``.
    """
    x = np.asarray(data, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("data must be one-dimensional")
    if fs <= 0:
        raise ValueError("fs must be positive")
    if low <= 0 or high <= low:
        raise ValueError("require 0 < low < high")

    mid = max(1.0, float(np.sqrt(low * high)))
    win = max(
        3,
        min(int(round(fs / mid)) | 1, max(3, x.size // 2 * 2 + 1)),
    )
    if win > x.size:
        win = max(3, x.size // 2 * 2 + 1) if x.size >= 3 else x.size
    k = np.hanning(win)
    k /= k.sum() + 1e-12
    smooth = np.convolve(x, k, mode="same")
    mix = float(np.clip((high - low) / (0.5 * fs), 0.06, 0.28))
    return (1.0 - mix) * x + mix * smooth


def notch_filter(data: ArrayLike, freq: float, fs: float) -> np.ndarray:
    """Attenuate a narrow band near ``freq`` using a simple IIR-style proxy.

    Args:
        data: One-dimensional samples.
        freq: Line frequency to suppress (e.g. 50 or 60 Hz).
        fs: Sampling rate in Hz.

    Returns:
        Filtered array with the same shape as ``data``.
    """
    x = np.asarray(data, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("data must be one-dimensional")
    if fs <= 0:
        raise ValueError("fs must be positive")
    if freq <= 0 or freq >= fs / 2:
        raise ValueError("freq must be in (0, Nyquist)")

    n = x.size
    if n < 4:
        return x.copy()

    t = np.arange(n, dtype=np.float64) / fs
    phase = 2.0 * np.pi * freq * t
    c = np.cos(phase)
    s = np.sin(phase)
    a_c = 2.0 * np.dot(x, c) / (np.dot(c, c) + 1e-12)
    a_s = 2.0 * np.dot(x, s) / (np.dot(s, s) + 1e-12)
    narrow = a_c * c + a_s * s
    return x - 0.85 * narrow
