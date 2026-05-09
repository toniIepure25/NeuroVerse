from __future__ import annotations

import threading
import time
from typing import Any

from app.acquisition.markers import MarkerEvent, MarkerStreamReader


class BackgroundMarkerCollector:
    def __init__(
        self,
        stream_name: str | None = None,
        stream_type: str = "Markers",
        timeout: float = 0.5,
        poll_interval: float = 0.025,
    ) -> None:
        self.reader = MarkerStreamReader(stream_name, stream_type, timeout)
        self.poll_interval = poll_interval
        self.error: str | None = None
        self._events: list[MarkerEvent] = []
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def stream_metadata(self) -> dict[str, Any] | None:
        return self.reader.stream_metadata

    def start(self) -> None:
        try:
            self.reader.start()
        except Exception as exc:
            self.error = str(exc)
            return
        if self.reader.stream_metadata is None:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def snapshot(self) -> list[MarkerEvent]:
        with self._lock:
            return list(self._events)

    def stop(self) -> list[MarkerEvent]:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)
        self._collect_once()
        self.reader.stop()
        return self.snapshot()

    def _run(self) -> None:
        while not self._stop.is_set():
            self._collect_once()
            time.sleep(self.poll_interval)

    def _collect_once(self) -> None:
        try:
            events = self.reader.pull_available()
        except Exception as exc:
            self.error = str(exc)
            return
        if not events:
            return
        with self._lock:
            seen = {(event.label, round(event.timestamp, 6)) for event in self._events}
            for event in events:
                key = (event.label, round(event.timestamp, 6))
                if key not in seen:
                    self._events.append(event)
                    seen.add(key)
