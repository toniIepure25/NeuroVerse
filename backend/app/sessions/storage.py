from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.sessions.summary import summarize_session

_SAFE_SESSION_ID = re.compile(r"^[A-Za-z0-9_.-]+$")


def list_sessions(base_dir: Path | None = None) -> list[dict[str, str | int]]:
    d = base_dir or settings.sessions_dir
    sessions = []
    for p in sorted(d.glob("*.jsonl")):
        line_count = sum(1 for _ in open(p))
        sessions.append({
            "session_id": p.stem,
            "file": str(p.name),
            "event_count": line_count,
        })
    return sessions


def get_session_events(
    session_id: str,
    offset: int = 0,
    limit: int = 100,
    base_dir: Path | None = None,
) -> list[dict]:
    d = base_dir or settings.sessions_dir
    path = d / f"{session_id}.jsonl"
    if not path.exists():
        return []
    events = []
    with open(path) as f:
        for i, line in enumerate(f):
            if i < offset:
                continue
            if len(events) >= limit:
                break
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events


def get_session_metadata(session_id: str, base_dir: Path | None = None) -> dict | None:
    d = base_dir or settings.sessions_dir
    path = d / f"{session_id}.jsonl"
    if not path.exists():
        return None
    first_event = None
    last_event = None
    count = 0
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if first_event is None:
                first_event = data
            last_event = data
            count += 1
    return {
        "session_id": session_id,
        "event_count": count,
        "first_timestamp": first_event.get("timestamp") if first_event else None,
        "last_timestamp": last_event.get("timestamp") if last_event else None,
    }


def get_session_summary(session_id: str, base_dir: Path | None = None) -> dict | None:
    d = base_dir or settings.sessions_dir
    summary_path = d / f"{session_id}_summary.json"
    if summary_path.exists():
        with open(summary_path) as f:
            return json.load(f)
    try:
        return summarize_session(session_id, base_dir=d, write_report=True)
    except FileNotFoundError:
        return None


def list_session_files(session_id: str, base_dir: Path | None = None) -> list[dict[str, Any]]:
    _validate_session_id(session_id)
    d = base_dir or settings.sessions_dir
    files = []
    for path in sorted(d.glob(f"{session_id}*")):
        if path.is_file() and _is_within(path, d):
            files.append({
                "name": path.name,
                "path": str(path),
                "bytes": path.stat().st_size,
            })
    return files


def export_session_bundle(session_id: str, base_dir: Path | None = None) -> Path:
    _validate_session_id(session_id)
    d = base_dir or settings.sessions_dir
    session_path = d / f"{session_id}.jsonl"
    if not session_path.exists():
        raise FileNotFoundError(session_id)
    get_session_summary(session_id, base_dir=d)
    bundle_path = d / f"{session_id}_export.zip"
    disclaimer = (
        "NeuroVerse records local research-prototype events. Cognitive values are proxy "
        "estimates, not clinical measurements. The corridor is not a decoded mental image."
    )
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in list_session_files(session_id, base_dir=d):
            path = Path(item["path"])
            if path.name != bundle_path.name:
                zf.write(path, arcname=path.name)
        zf.writestr("DISCLAIMER.txt", disclaimer)
    return bundle_path


def delete_session_data(
    session_id: str,
    confirm: bool,
    base_dir: Path | None = None,
) -> dict[str, Any]:
    _validate_session_id(session_id)
    if not confirm:
        return {
            "deleted": False,
            "reason": "Deletion requires confirm=true",
            "deleted_files": [],
        }
    d = base_dir or settings.sessions_dir
    files = list_session_files(session_id, base_dir=d)
    if not files:
        raise FileNotFoundError(session_id)
    deleted: list[str] = []
    for item in files:
        path = Path(item["path"])
        if not _is_within(path, d):
            continue
        path.unlink(missing_ok=True)
        deleted.append(path.name)
    return {"deleted": True, "session_id": session_id, "deleted_files": deleted}


def _validate_session_id(session_id: str) -> None:
    if not _SAFE_SESSION_ID.fullmatch(session_id):
        raise ValueError("Invalid session_id")


def _is_within(path: Path, base_dir: Path) -> bool:
    try:
        path.resolve().relative_to(base_dir.resolve())
        return True
    except ValueError:
        return False
