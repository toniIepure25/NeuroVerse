"""Export a NeuroVerse session bundle."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.sessions.storage import export_session_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a NeuroVerse session bundle")
    parser.add_argument("--session-id", required=True)
    args = parser.parse_args()
    path = export_session_bundle(args.session_id)
    print(path)


if __name__ == "__main__":
    main()
