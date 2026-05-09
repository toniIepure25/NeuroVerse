"""Replay a recorded NeuroVerse session from JSONL."""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.sessions.replay import SessionReplayer


async def replay(session_id: str, speed: float) -> None:
    replayer = SessionReplayer(session_id, speed=speed)
    count = 0
    async for event in replayer.stream():
        print(f"[{event.timestamp:8.2f}s] {event.event_type}: {event.payload}")
        count += 1
    print(f"\nReplayed {count} events from session {session_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a NeuroVerse session")
    parser.add_argument("--session-id", required=True, help="Session ID to replay")
    parser.add_argument("--speed", type=float, default=4.0, help="Replay speed multiplier")
    args = parser.parse_args()
    asyncio.run(replay(args.session_id, args.speed))


if __name__ == "__main__":
    main()
