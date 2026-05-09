from __future__ import annotations

import time


class SessionClock:
    """Monotonic clock relative to session start, supporting replay override."""

    def __init__(self) -> None:
        self._start: float = 0.0
        self._override: float | None = None

    def reset(self) -> None:
        self._start = time.monotonic()
        self._override = None

    def elapsed(self) -> float:
        if self._override is not None:
            return self._override
        return time.monotonic() - self._start

    def set_override(self, t: float) -> None:
        self._override = t

    def clear_override(self) -> None:
        self._override = None
