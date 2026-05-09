from __future__ import annotations

import numpy as np

from app.core.numeric import clamp

_HR_LO = 50.0
_HR_HI = 120.0
_RMSSD_REF = 60.0  # ms-scale proxy; larger = more relaxed


def _upper_map(names: list[str]) -> dict[str, int]:
    return {str(n).strip().upper(): i for i, n in enumerate(names)}


def _series(data: list[list[float]], cmap: dict[str, int], key: str) -> np.ndarray:
    idx = cmap.get(key.upper())
    if idx is None or idx >= len(data):
        return np.array([], dtype=float)
    return np.asarray(data[idx], dtype=float)


def _safe_cv(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    if x.size < 2:
        return 0.0
    m = float(np.mean(x))
    if abs(m) < 1e-12:
        return 0.0
    return float(np.std(x, ddof=1) / abs(m))


def _norm_minmax(x: float, lo: float, hi: float) -> float:
    if hi - lo < 1e-12:
        return 0.5
    return clamp((x - lo) / (hi - lo), 0.0, 1.0)


def _phasic_peaks_simple(x: np.ndarray) -> int:
    x = x[np.isfinite(x)]
    if x.size < 3:
        return 0
    d = np.diff(x)
    sign = np.sign(d)
    peaks = 0
    for i in range(1, sign.size):
        if sign[i - 1] > 0 and sign[i] <= 0:
            peaks += 1
    return peaks


def extract_physio_features(
    data: list[list[float]],
    channel_names: list[str],
) -> dict[str, float]:
    cmap = _upper_map(channel_names)

    hr = _series(data, cmap, "HR")
    hrv = _series(data, cmap, "HRV_RMSSD")
    eda_t = _series(data, cmap, "EDA_TONIC")
    eda_p = _series(data, cmap, "EDA_PHASIC")

    if hr.size and np.any(np.isfinite(hr)):
        hr_m = float(np.nanmean(hr))
        heart_rate = _norm_minmax(hr_m, _HR_LO, _HR_HI)
    else:
        heart_rate = 0.5

    if hrv.size and np.any(np.isfinite(hrv)):
        hm = float(np.nanmean(hrv))
        rmssd_proxy = clamp(np.tanh(hm / _RMSSD_REF), 0.0, 1.0)
        cv = _safe_cv(hrv)
        hrv_stability = clamp(1.0 - cv, 0.0, 1.0)
    else:
        rmssd_proxy = 0.5
        hrv_stability = 0.5

    def _eda_norm(x: np.ndarray) -> float:
        if x.size == 0 or not np.any(np.isfinite(x)):
            return 0.5
        v = float(np.nanmean(np.abs(x)))
        return clamp(float(np.tanh(v)), 0.0, 1.0)

    eda_tonic = _eda_norm(eda_t)
    eda_phasic = _eda_norm(eda_p)

    n = float(eda_p.size) if eda_p.size else 1.0
    peak_count = _phasic_peaks_simple(eda_p)
    eda_peak_rate = clamp(peak_count / max(8.0, n / 10.0), 0.0, 1.0)

    stress_index = clamp(
        0.45 * heart_rate + 0.30 * (1.0 - rmssd_proxy) + 0.25 * eda_phasic,
        0.0,
        1.0,
    )

    return {
        "heart_rate": clamp(heart_rate, 0.0, 1.0),
        "rmssd_proxy": clamp(rmssd_proxy, 0.0, 1.0),
        "hrv_stability": clamp(hrv_stability, 0.0, 1.0),
        "eda_tonic": clamp(eda_tonic, 0.0, 1.0),
        "eda_phasic": clamp(eda_phasic, 0.0, 1.0),
        "eda_peak_rate": clamp(eda_peak_rate, 0.0, 1.0),
        "stress_index": stress_index,
    }
