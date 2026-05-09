"""Delete a NeuroVerse session after explicit confirmation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.sessions.storage import delete_session_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete local NeuroVerse session artifacts")
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()
    result = delete_session_data(args.session_id, confirm=args.confirm)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
