from __future__ import annotations

from collections import defaultdict

import numpy as np


class BaselineCalibrator:
    """Collect baseline period features and normalize subsequent windows via z-score."""

    def __init__(self, baseline_duration_s: float = 30.0):
        self.baseline_duration_s = baseline_duration_s
        self._buffers: dict[str, list[float]] = defaultdict(list)
        self._means: dict[str, float] = {}
        self._stds: dict[str, float] = {}
        self._calibrated = False

    def add_sample(self, key: str, value: float) -> None:
        if not self._calibrated:
            self._buffers[key].append(value)

    def finalize(self) -> None:
        for key, values in self._buffers.items():
            arr = np.array(values)
            self._means[key] = float(np.mean(arr))
            self._stds[key] = float(np.std(arr)) or 1.0
        self._calibrated = True

    def normalize(self, key: str, value: float) -> float:
        if not self._calibrated or key not in self._means:
            return value
        z = (value - self._means[key]) / self._stds[key]
        return float(np.clip((z + 2) / 4, 0, 1))

    @property
    def is_calibrated(self) -> bool:
        return self._calibrated
