from __future__ import annotations

import math

import numpy as np

from app.core.numeric import clamp

_EPS = 1e-9


def _sigmoid_01(x: float, scale: float = 1.0) -> float:
    return clamp(1.0 / (1.0 + math.exp(-x / scale)), 0.0, 1.0)


def _band_power(sig: np.ndarray, sr: float, f_lo: float, f_hi: float) -> float:
    sig = np.asarray(sig, dtype=float)
    n = sig.size
    if n < 8 or sr <= 0:
        return 0.0
    x = sig - np.nanmean(sig)
    if not np.any(np.isfinite(x)):
        return 0.0
    psd = np.abs(np.fft.rfft(x)) ** 2
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    mask = (freqs >= f_lo) & (freqs < f_hi)
    return float(np.sum(psd[mask]))


def _norm_band_power(p: float) -> float:
    """Map band power to ~0..1 via log-scaled sigmoid."""
    return _sigmoid_01(math.log1p(max(p, 0.0)), scale=2.0)


def extract_eeg_features(
    data: list[list[float]],
    channel_names: list[str],
    sampling_rate: float,
) -> dict[str, float]:
    """Extract EEG band proxies and composite indices; outputs in ~0..1."""
    if not data or sampling_rate <= 0:
        return {
            "alpha_power": 0.0,
            "beta_power": 0.0,
            "theta_power": 0.0,
            "delta_power": 0.0,
            "gamma_power": 0.0,
            "engagement_index": 0.0,
            "relaxation_index": 0.0,
            "fatigue_index": 0.0,
            "spectral_entropy_proxy": 0.0,
            "p300_proxy": 0.0,
        }

    chans = [np.asarray(row, dtype=float) for row in data if len(row) > 0]
    if not chans:
        return extract_eeg_features([], channel_names, sampling_rate)

    n = min(c.size for c in chans)
    if n < 8:
        return extract_eeg_features([], channel_names, sampling_rate)

    deltas, thetas, alphas, betas, gammas = [], [], [], [], []
    p300_vals: list[float] = []

    lo = int(0.40 * n)
    hi = min(n, int(0.70 * n))
    if hi <= lo + 1:
        lo, hi = max(0, n // 3), max(n // 3 + 1, (2 * n) // 3)

    for c in chans:
        seg = c[:n]
        deltas.append(_band_power(seg, sampling_rate, 0.5, 4.0))
        thetas.append(_band_power(seg, sampling_rate, 4.0, 8.0))
        alphas.append(_band_power(seg, sampling_rate, 8.0, 13.0))
        betas.append(_band_power(seg, sampling_rate, 13.0, 30.0))
        gammas.append(_band_power(seg, sampling_rate, 30.0, 45.0))
        w = seg[lo:hi]
        if w.size:
            p300_vals.append(float(np.max(np.abs(w))))

    def _mean(xs: list[float]) -> float:
        return float(np.mean(xs)) if xs else 0.0

    d_raw, th_raw, a_raw, b_raw, g_raw = map(
        _mean, [deltas, thetas, alphas, betas, gammas]
    )

    delta_power = _norm_band_power(d_raw)
    theta_power = _norm_band_power(th_raw)
    alpha_power = _norm_band_power(a_raw)
    beta_power = _norm_band_power(b_raw)
    gamma_power = _norm_band_power(g_raw)

    eng_r = b_raw / (a_raw + th_raw + _EPS)
    relax_r = a_raw / (b_raw + th_raw + _EPS)
    fat_r = th_raw / (a_raw + b_raw + _EPS)
    engagement_index = _sigmoid_01(math.log1p(eng_r), scale=0.35)
    relaxation_index = _sigmoid_01(math.log1p(relax_r), scale=0.35)
    fatigue_index = _sigmoid_01(math.log1p(fat_r), scale=0.35)

    p_vec = np.array([d_raw, th_raw, a_raw, b_raw, g_raw], dtype=float)
    s = float(np.sum(p_vec)) + _EPS
    p_norm = p_vec / s
    ent = float(-np.sum(p_norm * np.log(p_norm + _EPS)))
    spectral_entropy_proxy = clamp(ent / math.log(5.0), 0.0, 1.0)

    if p300_vals:
        p300_amp = float(np.mean(p300_vals))
        p300_proxy = _sigmoid_01(math.log1p(p300_amp), scale=1.0)
    else:
        p300_proxy = 0.0

    _ = channel_names  # reserved for future channel-specific logic

    return {
        "alpha_power": alpha_power,
        "beta_power": beta_power,
        "theta_power": theta_power,
        "delta_power": delta_power,
        "gamma_power": gamma_power,
        "engagement_index": engagement_index,
        "relaxation_index": relaxation_index,
        "fatigue_index": fatigue_index,
        "spectral_entropy_proxy": spectral_entropy_proxy,
        "p300_proxy": p300_proxy,
    }
