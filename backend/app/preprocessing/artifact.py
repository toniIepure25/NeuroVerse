from __future__ import annotations

import numpy as np


def reject_amplitude(data: np.ndarray | list[float], threshold: float) -> bool:
    """Return True if any sample magnitude exceeds ``threshold`` (bad window)."""
    x = np.asarray(data, dtype=np.float64)
    if x.size == 0:
        return False
    return bool(np.any(np.abs(x) > threshold))


def check_variance(
    data: np.ndarray | list[float],
    min_var: float,
    max_var: float,
) -> bool:
    """Return True if sample variance is outside ``[min_var, max_var]`` (bad window)."""
    x = np.asarray(data, dtype=np.float64)
    if x.size < 2:
        return True
    v = float(np.var(x, ddof=1))
    return bool(v < min_var or v > max_var)
