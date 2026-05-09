from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

from app.acquisition.lsl_discovery import discover_streams, load_pylsl, stream_info_to_dict


@dataclass
class MarkerEvent:
    label: str
    timestamp: float
    source_stream: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "timestamp": self.timestamp,
            "source_stream": self.source_stream,
            "metadata": self.metadata,
        }


class MarkerStreamReader:
    def __init__(
        self,
        stream_name: str | None = None,
        stream_type: str = "Markers",
        timeout: float = 0.5,
    ) -> None:
        self.stream_name = stream_name
        self.stream_type = stream_type
        self.timeout = timeout
        self.stream_metadata: dict[str, Any] | None = None
        self._pylsl: Any | None = None
        self._inlet: Any | None = None

    def start(self) -> None:
        self._pylsl = load_pylsl()
        streams = discover_streams(
            name=self.stream_name,
            stream_type=self.stream_type,
            timeout=self.timeout,
        )
        if not streams and self.stream_type == "Markers":
            streams = discover_streams(
                name=self.stream_name,
                stream_type="Marker",
                timeout=self.timeout,
            )
        if not streams:
            return
        selected_meta = streams[0]
        infos = self._pylsl.resolve_streams(wait_time=self.timeout)
        selected = None
        for info in infos:
            if stream_info_to_dict(info).get("stream_id") == selected_meta["stream_id"]:
                selected = info
                break
        if selected is None:
            return
        self._inlet = self._pylsl.StreamInlet(selected, max_buflen=60)
        try:
            self.stream_metadata = stream_info_to_dict(self._inlet.info(timeout=self.timeout))
        except Exception:
            self.stream_metadata = selected_meta

    def pull_available(self) -> list[MarkerEvent]:
        if self._inlet is None:
            return []
        samples, timestamps = self._inlet.pull_chunk(
            timeout=min(self.timeout, 0.05),
            max_samples=256,
        )
        events: list[MarkerEvent] = []
        source = (self.stream_metadata or {}).get("name") or "marker_stream"
        for sample, timestamp in zip(samples or [], timestamps or [], strict=False):
            label = str(sample[0] if isinstance(sample, list) and sample else sample)
            events.append(
                MarkerEvent(
                    label=label,
                    timestamp=float(timestamp),
                    source_stream=str(source),
                    metadata={"stream": self.stream_metadata},
                )
            )
        return events

    def stop(self) -> None:
        self._inlet = None


def align_markers_to_windows(
    markers: list[MarkerEvent],
    windows: list[dict[str, Any]],
    tolerance_seconds: float = 0.25,
) -> dict[str, Any]:
    labels = Counter(marker.label for marker in markers)
    aligned = 0
    unaligned = 0
    assignments: list[dict[str, Any]] = []
    warnings: list[str] = []

    for marker in markers:
        matched = None
        for index, window in enumerate(windows):
            start = window.get("start_time")
            end = window.get("end_time")
            if start is None or end is None:
                continue
            if float(start) <= marker.timestamp <= float(end):
                matched = index
                break
        if matched is None:
            matched = _nearest_window(marker, windows, tolerance_seconds)
        if matched is None:
            unaligned += 1
            warnings.append(f"Marker {marker.label} at {marker.timestamp:.4f} was outside windows.")
        else:
            aligned += 1
            assignments.append({"marker": marker.to_dict(), "window_index": matched})

    return {
        "marker_count": len(markers),
        "marker_labels": sorted(labels),
        "markers_per_label": dict(sorted(labels.items())),
        "first_marker_time": min((marker.timestamp for marker in markers), default=None),
        "last_marker_time": max((marker.timestamp for marker in markers), default=None),
        "aligned_window_count": aligned,
        "unaligned_marker_count": unaligned,
        "marker_alignment_pass": unaligned == 0,
        "marker_alignment_warnings": warnings[:20],
        "assignments": assignments[:50],
    }


def marker_report(
    *,
    stream_metadata: dict[str, Any] | None,
    markers: list[MarkerEvent],
    windows: list[dict[str, Any]],
) -> dict[str, Any]:
    alignment = align_markers_to_windows(markers, windows)
    return {
        "marker_stream_found": stream_metadata is not None,
        "stream_metadata": stream_metadata,
        **alignment,
    }


def empty_marker_report(warning: str | None = None) -> dict[str, Any]:
    warnings = [warning] if warning else []
    return {
        "marker_stream_found": False,
        "stream_metadata": None,
        "marker_count": 0,
        "marker_labels": [],
        "markers_per_label": {},
        "first_marker_time": None,
        "last_marker_time": None,
        "aligned_window_count": 0,
        "unaligned_marker_count": 0,
        "marker_alignment_pass": False,
        "marker_alignment_warnings": warnings,
        "assignments": [],
    }


def _nearest_window(
    marker: MarkerEvent,
    windows: list[dict[str, Any]],
    tolerance_seconds: float,
) -> int | None:
    best_index = None
    best_distance = float("inf")
    for index, window in enumerate(windows):
        start = window.get("start_time")
        end = window.get("end_time")
        if start is None or end is None:
            continue
        center = (float(start) + float(end)) / 2.0
        distance = abs(marker.timestamp - center)
        if distance < best_distance:
            best_distance = distance
            best_index = index
    if best_distance <= tolerance_seconds:
        return best_index
    return None
