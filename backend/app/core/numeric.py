"""Small numeric helpers shared by feature and signal-quality code."""

from __future__ import annotations


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return float(max(lo, min(hi, v)))
