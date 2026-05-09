from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

DEFAULT_EEG_CHANNELS = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"]
FIXTURE_MARKERS = [
    ("BASELINE", 0.5),
    ("LEFT_HAND_IMAGERY", 3.0),
    ("REST", 5.0),
    ("RIGHT_HAND_IMAGERY", 7.0),
    ("NOISY_SEGMENT", 9.0),
    ("REST", 11.0),
    ("LEFT_HAND_IMAGERY", 13.0),
    ("RIGHT_HAND_IMAGERY", 15.0),
    ("NOISY_SEGMENT", 17.0),
    ("REST", 19.0),
    ("LEFT_HAND_IMAGERY", 21.0),
    ("RIGHT_HAND_IMAGERY", 23.0),
]


def load_mne() -> Any:
    os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-neuroverse")
    import mne

    return mne


def load_numpy() -> Any:
    import numpy as np

    return np


def create_eeg_fixture_raw(duration: float = 30.0, seed: int = 42) -> Any:
    mne = load_mne()
    np = load_numpy()
    rng = np.random.default_rng(seed)
    sfreq = 250.0
    n_samples = int(max(duration, 26.0) * sfreq)
    times = np.arange(n_samples) / sfreq
    rows = []
    for idx, name in enumerate(DEFAULT_EEG_CHANNELS):
        phase = idx * 0.17
        alpha_amp = 18e-6
        beta_amp = 7e-6
        if name == "C3":
            alpha_amp = _event_modulated(times, base=alpha_amp, left=0.55, right=1.18)
            beta_amp = _event_modulated(times, base=beta_amp, left=0.7, right=1.2)
        elif name == "C4":
            alpha_amp = _event_modulated(times, base=alpha_amp, left=1.18, right=0.55)
            beta_amp = _event_modulated(times, base=beta_amp, left=1.2, right=0.7)
        elif name.startswith("O"):
            alpha_amp = _event_modulated(times, base=alpha_amp, rest=1.25)
        alpha = alpha_amp * np.sin(2 * math.pi * 10.0 * times + phase)
        beta = beta_amp * np.sin(2 * math.pi * 20.0 * times + phase / 2)
        noise = rng.normal(0.0, 1.5e-6, size=n_samples)
        row = alpha + beta + noise
        noisy = (times >= 16.0) & (times <= 18.0)
        row[noisy] += rng.normal(0.0, 35e-6, size=int(np.sum(noisy)))
        rows.append(row)
    info = mne.create_info(DEFAULT_EEG_CHANNELS, sfreq=sfreq, ch_types="eeg")
    raw = mne.io.RawArray(np.vstack(rows), info, verbose=False)
    raw.set_annotations(
        mne.Annotations(
            onset=[onset for _label, onset in FIXTURE_MARKERS if onset <= duration],
            duration=[0.25 for _label, onset in FIXTURE_MARKERS if onset <= duration],
            description=[label for label, onset in FIXTURE_MARKERS if onset <= duration],
        )
    )
    return raw


def load_mne_raw(path: str | Path) -> Any:
    mne = load_mne()
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(file_path)
    suffix = file_path.suffix.lower()
    if suffix == ".fif":
        return mne.io.read_raw_fif(file_path, preload=False, verbose=False)
    if suffix in {".edf", ".bdf"}:
        return mne.io.read_raw_edf(file_path, preload=False, verbose=False)
    if suffix == ".gdf":
        return mne.io.read_raw_gdf(file_path, preload=False, verbose=False)
    if suffix == ".set":
        return mne.io.read_raw_eeglab(file_path, preload=False, verbose=False)
    return mne.io.read_raw(file_path, preload=False, verbose=False)


def _event_modulated(
    times: Any,
    *,
    base: float,
    left: float = 1.0,
    right: float = 1.0,
    rest: float = 1.0,
) -> Any:
    np = load_numpy()
    amp = np.full_like(times, base, dtype=float)
    for label, onset in FIXTURE_MARKERS:
        mask = (times >= onset) & (times < onset + 1.5)
        if label == "LEFT_HAND_IMAGERY":
            amp[mask] = base * left
        elif label == "RIGHT_HAND_IMAGERY":
            amp[mask] = base * right
        elif label == "REST":
            amp[mask] = base * rest
    return amp
