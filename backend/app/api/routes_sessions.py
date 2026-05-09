from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.api.deps import get_engine
from app.sessions.storage import (
    delete_session_data,
    export_session_bundle,
    get_session_events,
    get_session_metadata,
    get_session_summary,
    list_session_files,
    list_sessions,
)

router = APIRouter(prefix="/api")


@router.post("/v1/session/start")
@router.post("/session/start")
async def start_session() -> dict:
    engine = get_engine()
    if engine.is_running:
        return {"status": "already_running", "session_id": engine.session_id}
    session_id = await engine.start_session()
    return {"status": "started", "session_id": session_id}


@router.post("/v1/session/stop")
@router.post("/session/stop")
async def stop_session() -> dict:
    engine = get_engine()
    sid = engine.session_id
    if not engine.is_running:
        return {"status": "not_running"}
    await engine.stop_session()
    return {"status": "stopped", "session_id": sid}


@router.get("/v1/sessions")
@router.get("/sessions")
async def get_sessions() -> list:
    return list_sessions()


@router.get("/v1/sessions/{session_id}/files")
@router.get("/sessions/{session_id}/files")
async def get_files(session_id: str) -> dict:
    try:
        return {"session_id": session_id, "files": list_session_files(session_id)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/v1/sessions/{session_id}/export")
@router.get("/sessions/{session_id}/export")
async def export_session(session_id: str) -> FileResponse:
    try:
        path = export_session_bundle(session_id)
        return FileResponse(
            path,
            media_type="application/zip",
            filename=path.name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")


@router.delete("/v1/sessions/{session_id}/delete")
@router.delete("/sessions/{session_id}/delete")
async def delete_session(session_id: str, confirm: bool = False) -> dict:
    try:
        return delete_session_data(session_id, confirm=confirm)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/v1/sessions/{session_id}")
@router.get("/sessions/{session_id}")
async def get_session(session_id: str) -> dict:
    meta = get_session_metadata(session_id)
    if meta is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return meta


@router.get("/v1/sessions/{session_id}/summary")
@router.get("/sessions/{session_id}/summary")
async def get_summary(session_id: str) -> dict:
    summary = get_session_summary(session_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return summary


@router.get("/v1/sessions/{session_id}/events")
@router.get("/sessions/{session_id}/events")
async def get_events(session_id: str, offset: int = 0, limit: int = 100) -> list:
    return get_session_events(session_id, offset=offset, limit=limit)
