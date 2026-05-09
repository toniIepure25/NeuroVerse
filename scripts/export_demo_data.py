"""Export recorded session events to a summary CSV for analysis."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))


def export_session(session_id: str, output: str) -> None:
    from app.core.config import settings

    path = settings.sessions_dir / f"{session_id}.jsonl"
    if not path.exists():
        print(f"Session {session_id} not found at {path}")
        return

    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            if event.get("event_type") == "neuroverse.state.predicted":
                p = event["payload"]
                rows.append({
                    "timestamp": event["timestamp"],
                    "focus": p.get("focus"),
                    "relaxation": p.get("relaxation"),
                    "workload": p.get("workload"),
                    "stress": p.get("stress"),
                    "fatigue": p.get("fatigue"),
                    "imagery_engagement": p.get("imagery_engagement"),
                    "confidence": p.get("confidence"),
                })

    if rows:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"Exported {len(rows)} state predictions to {out}")
    else:
        print("No state predictions found in session")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export NeuroVerse session data to CSV")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--output", default="data/export.csv")
    args = parser.parse_args()
    export_session(args.session_id, args.output)


if __name__ == "__main__":
    main()
