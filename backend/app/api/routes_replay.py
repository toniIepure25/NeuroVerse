from __future__ import annotations

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from app.core.exceptions import SessionNotFoundError
from app.sessions.replay import SessionReplayer

router = APIRouter()


@router.post("/api/v1/replay/{session_id}")
@router.post("/api/replay/{session_id}")
async def start_replay(session_id: str, speed: float = 1.0) -> dict:
    try:
        replayer = SessionReplayer(session_id, speed=speed)
        events = replayer.load_events()
        return {
            "status": "ready",
            "session_id": session_id,
            "event_count": len(events),
            "speed": speed,
        }
    except SessionNotFoundError:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/api/v1/replay/{session_id}/pause")
async def pause_replay(session_id: str) -> dict:
    return {
        "status": "not_running",
        "session_id": session_id,
        "note": "Replay WebSocket streaming is stateless in this prototype.",
    }


@router.post("/api/v1/replay/{session_id}/resume")
async def resume_replay(session_id: str) -> dict:
    return {
        "status": "not_running",
        "session_id": session_id,
        "note": "Replay WebSocket streaming is stateless in this prototype.",
    }


@router.post("/api/v1/replay/{session_id}/restart")
async def restart_replay(session_id: str, speed: float = 1.0) -> dict:
    return await start_replay(session_id, speed=speed)


@router.websocket("/ws/replay/{session_id}")
async def replay_stream(ws: WebSocket, session_id: str, speed: float = 1.0) -> None:
    await ws.accept()
    try:
        replayer = SessionReplayer(session_id, speed=speed)
        async for event in replayer.stream():
            await ws.send_json(event.model_dump())
        await ws.send_json({"event_type": "neuroverse.replay.completed", "session_id": session_id})
    except SessionNotFoundError:
        await ws.send_json({"error": "Session not found"})
    except WebSocketDisconnect:
        pass
    finally:
        try:
            await ws.close()
        except Exception:
            pass
