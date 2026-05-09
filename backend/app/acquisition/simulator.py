from __future__ import annotations

import asyncio
from enum import IntEnum
from typing import Final

import numpy as np

from app.acquisition.base import BaseAcquisition
from app.schemas.signals import RawSignalPayload

_EEG_NAMES: Final[tuple[str, ...]] = (
    "Fp1",
    "Fp2",
    "F3",
    "F4",
    "C3",
    "C4",
    "P3",
    "P4",
    "O1",
    "O2",
)
_FRONT_IDX: Final[slice] = slice(0, 4)
_PARIETAL_IDX: Final[slice] = slice(6, 8)
_OCCIPITAL_IDX: Final[slice] = slice(8, 10)


class _Phase(IntEnum):
    BASELINE = 0
    INCREASING_FOCUS = 1
    HIGH_WORKLOAD = 2
    RELAXATION_RECOVERY = 3
    IMAGERY_ENGAGEMENT = 4
    NOISY_PERIOD = 5
    FATIGUE_DRIFT = 6


def _phase_edges_s(duration_s: float) -> np.ndarray:
    base = np.array([0.0, 30, 60, 90, 120, 150, 170, 180], dtype=np.float64)
    scale = duration_s / 180.0
    return base * scale


class BiosignalSimulator(BaseAcquisition):
    """Phase-driven synthetic multimodal biosignal source for testing and demos."""

    def __init__(
        self,
        duration_s: float = 180.0,
        tick_interval_ms: float = 50.0,
        sampling_rate: float = 250.0,
        rng: np.random.Generator | None = None,
    ) -> None:
        if duration_s <= 0:
            raise ValueError("duration_s must be positive")
        if tick_interval_ms <= 0:
            raise ValueError("tick_interval_ms must be positive")
        if sampling_rate <= 0:
            raise ValueError("sampling_rate must be positive")

        self._duration_s = float(duration_s)
        self._tick_s = tick_interval_ms / 1000.0
        self._fs = float(sampling_rate)
        self._rng = rng if rng is not None else np.random.default_rng()
        self._edges = _phase_edges_s(self._duration_s)
        self._tick_count = 0
        self._running = False

    def _phase_at(self, t: float) -> _Phase:
        t_wrapped = float(np.mod(t, self._duration_s))
        for i in range(len(self._edges) - 1):
            if self._edges[i] <= t_wrapped < self._edges[i + 1]:
                return _Phase(i)
        return _Phase.FATIGUE_DRIFT

    def _phase_params(self, phase: _Phase) -> dict[str, float]:
        p = {
            "delta": 1.0,
            "theta": 1.0,
            "alpha": 1.0,
            "beta": 1.0,
            "noise_eeg": 0.35,
            "front_theta": 1.0,
            "occipital_alpha": 1.0,
            "hr_base": 72.0,
            "hrv_rmssd": 45.0,
            "eda_tonic": 2.5,
            "eda_phasic_amp": 0.15,
            "eda_phasic_rate": 0.4,
            "gaze_jitter": 0.008,
            "pupil": 3.5,
            "entropy_mix": 0.0,
            "p300_gain": 0.0,
            "blink_rate": 0.12,
            "blink_width_s": 0.12,
            "sqi": 0.92,
        }
        if phase is _Phase.BASELINE:
            return p
        if phase is _Phase.INCREASING_FOCUS:
            p["beta"] = 1.65
            p["alpha"] = 0.55
            p["noise_eeg"] = 0.28
            p["gaze_jitter"] = 0.003
            p["pupil"] = 3.7
            return p
        if phase is _Phase.HIGH_WORKLOAD:
            p["theta"] = 1.5
            p["front_theta"] = 1.85
            p["beta"] = 1.25
            p["noise_eeg"] = 0.4
            p["hr_base"] = 82.0
            p["hrv_rmssd"] = 22.0
            p["eda_tonic"] = 3.2
            p["eda_phasic_amp"] = 0.55
            p["eda_phasic_rate"] = 1.8
            p["pupil"] = 4.4
            p["gaze_jitter"] = 0.006
            return p
        if phase is _Phase.RELAXATION_RECOVERY:
            p["alpha"] = 1.75
            p["beta"] = 0.65
            p["theta"] = 0.85
            p["occipital_alpha"] = 2.1
            p["hr_base"] = 62.0
            p["hrv_rmssd"] = 62.0
            p["eda_tonic"] = 1.8
            p["eda_phasic_amp"] = 0.06
            p["eda_phasic_rate"] = 0.15
            p["pupil"] = 3.2
            p["gaze_jitter"] = 0.005
            return p
        if phase is _Phase.IMAGERY_ENGAGEMENT:
            p["entropy_mix"] = 1.0
            p["noise_eeg"] = 0.42
            p["p300_gain"] = 1.0
            p["gaze_jitter"] = 0.004
            p["beta"] = 1.1
            p["alpha"] = 0.95
            return p
        if phase is _Phase.NOISY_PERIOD:
            p["noise_eeg"] = 2.8
            p["gaze_jitter"] = 0.12
            p["sqi"] = 0.18
            p["theta"] = 1.4
            p["beta"] = 1.5
            return p
        if phase is _Phase.FATIGUE_DRIFT:
            p["theta"] = 1.65
            p["delta"] = 1.35
            p["beta"] = 0.75
            p["alpha"] = 0.7
            p["front_theta"] = 1.4
            p["noise_eeg"] = 0.55
            p["blink_rate"] = 0.35
            p["blink_width_s"] = 0.28
            p["hr_base"] = 68.0
            p["hrv_rmssd"] = 38.0
            return p
        return p

    def _synth_eeg_window(
        self,
        t0: float,
        n: int,
        phase: _Phase,
        par: dict[str, float],
    ) -> np.ndarray:
        t = t0 + np.arange(n, dtype=np.float64) / self._fs
        freqs = {"delta": 2.0, "theta": 6.0, "alpha": 10.0, "beta": 21.0}
        rng = self._rng
        out = np.zeros((len(_EEG_NAMES), n), dtype=np.float64)
        regional = np.ones(len(_EEG_NAMES), dtype=np.float64)
        regional[_FRONT_IDX] *= par["front_theta"]
        regional[_OCCIPITAL_IDX] *= par["occipital_alpha"]
        row_scales = 0.35 + 0.15 * rng.random(len(_EEG_NAMES))

        for name, f0 in freqs.items():
            amp = par.get(name, 1.0)
            ph = rng.uniform(0.0, 2.0 * np.pi)
            wobble = rng.normal(0.0, 0.02, size=n)
            carrier = np.sin(2.0 * np.pi * (f0 + wobble) * t + ph)
            mix = par["entropy_mix"]
            if mix > 0:
                carrier = carrier + mix * np.sin(
                    2.0 * np.pi * (f0 * 1.37) * t + rng.uniform(0, 2 * np.pi)
                )
            out += (
                np.outer(regional, carrier)
                * amp
                * row_scales[:, np.newaxis]
            )

        out += rng.normal(0.0, par["noise_eeg"], size=out.shape)

        if par["p300_gain"] > 0 and n > 5:
            center = int(0.55 * n)
            width = max(3, n // 12)
            gp = np.exp(-0.5 * ((np.arange(n) - center) / width) ** 2)
            bump = par["p300_gain"] * 12.0 * gp
            out[_PARIETAL_IDX, :] += bump

        if phase is _Phase.NOISY_PERIOD:
            jitter = rng.normal(0.0, 3.5, size=out.shape)
            k_sp = max(1, n // 8)
            idx = rng.choice(n, size=k_sp, replace=False)
            out[:, idx] += rng.uniform(25.0, 85.0, size=(out.shape[0], k_sp))
            out += jitter
            drop_n = max(1, n // 10)
            d0 = int(rng.integers(0, max(1, n - drop_n + 1)))
            d1 = min(n, d0 + drop_n)
            out[:, d0:d1] *= 0.05

        return out

    def _blink_wave(self, t: np.ndarray, rate: float, width_s: float) -> np.ndarray:
        rng = self._rng
        blink = np.zeros_like(t)
        span = float(t[-1] - t[0]) if len(t) > 1 else self._tick_s
        n_events = max(0, int(rate * span * 3))
        widths = rng.uniform(width_s * 0.85, width_s * 1.25, size=max(1, n_events))
        for w in widths:
            c = rng.uniform(t[0], t[-1])
            blink += np.exp(-0.5 * ((t - c) / (w + 1e-6)) ** 2)
        return np.clip(blink, 0.0, 1.0)

    def _synth_scalar_series(
        self,
        t: np.ndarray,
        mean_val: float,
        noise: float,
        slow_amp: float = 0.0,
        slow_hz: float = 0.07,
    ) -> np.ndarray:
        rng = self._rng
        base = mean_val + slow_amp * np.sin(
            2.0 * np.pi * slow_hz * t + rng.uniform(0, 2 * np.pi)
        )
        return base + rng.normal(0.0, noise, size=t.shape)

    async def start(self) -> None:
        self._tick_count = 0
        self._running = True

    async def stop(self) -> None:
        self._running = False

    def is_running(self) -> bool:
        return self._running

    def status(self) -> dict[str, object]:
        return {
            "adapter": "simulator",
            "running": self._running,
            "sampling_rate": self._fs,
            "tick_seconds": self._tick_s,
            "channels": len(_EEG_NAMES) + 8,
            "last_tick": self._tick_count,
        }

    def capabilities(self) -> dict[str, object]:
        return {
            "modalities": ["eeg", "physio", "gaze"],
            "sampling_rate": self._fs,
            "channel_names": [
                *_EEG_NAMES,
                "HR",
                "HRV_RMSSD",
                "EDA_tonic",
                "EDA_phasic",
                "gaze_x",
                "gaze_y",
                "pupil_diameter",
                "blink",
            ],
            "hardware_required": False,
            "deterministic_with_seed": True,
        }

    async def get_window(self) -> RawSignalPayload:
        await asyncio.sleep(0)
        if not self._running:
            raise RuntimeError("BiosignalSimulator is not running; call start() first")

        t0 = self._tick_count * self._tick_s
        phase = self._phase_at(t0)
        par = self._phase_params(phase)
        n = max(1, int(round(self._fs * self._tick_s)))
        t = t0 + np.arange(n, dtype=np.float64) / self._fs

        eeg = self._synth_eeg_window(t0, n, phase, par)

        hr = self._synth_scalar_series(t, par["hr_base"], 1.2, 1.5, 0.05)
        hrv = self._synth_scalar_series(t, par["hrv_rmssd"], 2.5, 4.0, 0.04)
        eda_tonic = self._synth_scalar_series(t, par["eda_tonic"], 0.08, 0.25, 0.03)

        phasic_events = np.zeros(n, dtype=np.float64)
        n_candidates = max(3, int(par["eda_phasic_rate"] * 2))
        event_times = t[0] + self._rng.exponential(
            1.0 / max(0.08, par["eda_phasic_rate"]),
            size=n_candidates,
        )
        sigma_t = 0.1
        for et in event_times:
            if t[0] <= et <= t[-1]:
                phasic_events += par["eda_phasic_amp"] * np.exp(
                    -((t - et) ** 2) / (2.0 * sigma_t**2)
                )
        eda_phasic = phasic_events + self._rng.normal(0.0, 0.02, size=n)

        gx = np.cumsum(self._rng.normal(0.0, par["gaze_jitter"], size=n))
        gx -= np.linspace(gx[0], gx[-1], n)
        gy = np.cumsum(self._rng.normal(0.0, par["gaze_jitter"], size=n))
        gy -= np.linspace(gy[0], gy[-1], n)

        pupil_noise = 0.06 * (2.0 if phase is _Phase.NOISY_PERIOD else 1.0)
        pupil = self._synth_scalar_series(t, par["pupil"], pupil_noise, 0.15, 0.09)
        blink = self._blink_wave(t, par["blink_rate"], par["blink_width_s"])

        self._tick_count += 1

        rows = [
            *eeg,
            hr,
            hrv,
            eda_tonic,
            eda_phasic,
            gx,
            gy,
            pupil,
            blink,
        ]
        channel_names = [
            *_EEG_NAMES,
            "HR",
            "HRV_RMSSD",
            "EDA_tonic",
            "EDA_phasic",
            "gaze_x",
            "gaze_y",
            "pupil_diameter",
            "blink",
        ]
        data = [row.astype(np.float64, copy=False).tolist() for row in rows]

        sqi = par["sqi"]
        if phase is not _Phase.NOISY_PERIOD:
            sqi = float(np.clip(sqi + self._rng.normal(0.0, 0.02), 0.0, 1.0))

        window_ms = int(round(self._tick_s * 1000))
        return RawSignalPayload(
            modality="multimodal",
            sampling_rate=self._fs,
            channel_names=channel_names,
            data=data,
            window_size_ms=max(1, window_ms),
            signal_quality_hint=round(sqi, 4),
        )
