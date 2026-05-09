from __future__ import annotations

import hashlib
import importlib
import importlib.util
from typing import Any

PYLSL_INSTALL_HINT = (
    'pylsl is not installed. Install with: cd backend && pip install -e ".[hardware]"'
)


def pylsl_available() -> bool:
    return importlib.util.find_spec("pylsl") is not None


def load_pylsl() -> Any:
    if not pylsl_available():
        raise RuntimeError(PYLSL_INSTALL_HINT)
    return importlib.import_module("pylsl")


def discover_streams(
    name: str | None = None,
    stream_type: str | None = None,
    source_id: str | None = None,
    timeout: float = 1.0,
) -> list[dict[str, Any]]:
    pylsl = load_pylsl()
    streams = pylsl.resolve_streams(wait_time=timeout)
    normalized = [stream_info_to_dict(info) for info in streams]
    return [
        stream
        for stream in normalized
        if _matches(stream, name=name, stream_type=stream_type, source_id=source_id)
    ]


def discover_marker_streams(timeout: float = 0.25) -> list[dict[str, Any]]:
    return discover_streams(stream_type="Markers", timeout=timeout) + discover_streams(
        stream_type="Marker",
        timeout=timeout,
    )


def inspect_stream(
    stream_id: str | None = None,
    name: str | None = None,
    stream_type: str | None = None,
    source_id: str | None = None,
    timeout: float = 1.0,
) -> dict[str, Any]:
    streams = discover_streams(
        name=name,
        stream_type=stream_type,
        source_id=source_id,
        timeout=timeout,
    )
    if stream_id:
        streams = [stream for stream in streams if stream["stream_id"] == stream_id]
    if not streams:
        raise FileNotFoundError(
            "No LSL stream detected. Start make lsl-stream-demo in another terminal."
        )
    return streams[0]


def make_stream_id(info: dict[str, Any]) -> str:
    raw = "|".join(
        str(info.get(key, ""))
        for key in ("name", "type", "source_id", "uid", "hostname")
    )
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def stream_info_to_dict(info: Any) -> dict[str, Any]:
    data = {
        "name": _safe_call(info, "name"),
        "type": _safe_call(info, "type"),
        "source_id": _safe_call(info, "source_id"),
        "uid": _safe_call(info, "uid"),
        "hostname": _safe_call(info, "hostname"),
        "channel_count": _safe_call(info, "channel_count"),
        "nominal_srate": _safe_call(info, "nominal_srate"),
        "channel_format": _safe_call(info, "channel_format"),
        "created_at": _safe_call(info, "created_at"),
        "metadata_summary": _metadata_summary(info),
        "channel_names": _channel_names(info),
    }
    data["stream_id"] = make_stream_id(data)
    return data


def _matches(
    stream: dict[str, Any],
    name: str | None,
    stream_type: str | None,
    source_id: str | None,
) -> bool:
    if name and stream.get("name") != name:
        return False
    if stream_type and stream.get("type") != stream_type:
        return False
    if source_id and stream.get("source_id") != source_id:
        return False
    return True


def _safe_call(info: Any, method: str) -> Any:
    try:
        return getattr(info, method)()
    except Exception:
        return None


def _metadata_summary(info: Any) -> dict[str, Any]:
    try:
        desc = info.desc()
        return {
            "has_desc": not desc.empty(),
            "xml_preview": info.as_xml()[:1000],
        }
    except Exception:
        return {"has_desc": False, "xml_preview": ""}


def _channel_names(info: Any) -> list[str]:
    try:
        channels = info.desc().child("channels").child("channel")
        names: list[str] = []
        while not channels.empty():
            label = channels.child_value("label")
            names.append(label or f"ch{len(names) + 1}")
            channels = channels.next_sibling()
        return names
    except Exception:
        count = _safe_call(info, "channel_count") or 0
        return [f"ch{i + 1}" for i in range(int(count))]
