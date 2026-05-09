from __future__ import annotations

from collections.abc import Iterator, Sequence

import numpy as np
from numpy.typing import DTypeLike


class SlidingWindowBuffer:
    """Collects samples and exposes fixed-length windows with a configured overlap."""

    def __init__(
        self,
        window_size: int,
        overlap: int,
        dtype: DTypeLike | None = None,
    ) -> None:
        if window_size < 1:
            raise ValueError("window_size must be at least 1")
        if overlap < 0 or overlap >= window_size:
            raise ValueError("overlap must satisfy 0 <= overlap < window_size")

        self._window_size = window_size
        self._overlap = overlap
        self._step = window_size - overlap
        self._dtype = np.dtype(dtype) if dtype is not None else np.dtype(np.float64)
        self._buf: list[float] = []

    @property
    def window_size(self) -> int:
        """Number of samples per emitted window."""

        return self._window_size

    @property
    def overlap(self) -> int:
        """Samples shared between consecutive windows."""

        return self._overlap

    def clear(self) -> None:
        """Drop all buffered samples."""

        self._buf.clear()

    def push(
        self,
        samples: float | np.floating | np.ndarray | Sequence[float],
    ) -> None:
        """Append one sample or a sequence of samples to the internal buffer."""

        if isinstance(samples, (int, float, np.floating)):
            self._buf.append(float(samples))
            return

        arr = np.asarray(samples, dtype=self._dtype)
        if arr.ndim == 0:
            self._buf.append(float(arr))
            return
        if arr.ndim != 1:
            raise ValueError("samples must be a scalar or a 1-D sequence")
        self._buf.extend(float(x) for x in arr.flat)

    def drain_windows(self) -> Iterator[np.ndarray]:
        """Yield every complete window currently available, consuming ``step`` samples each time."""

        while len(self._buf) >= self._window_size:
            window = np.asarray(self._buf[: self._window_size], dtype=self._dtype)
            del self._buf[: self._step]
            yield window
