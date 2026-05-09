"""Discover local Lab Streaming Layer streams."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.acquisition.lsl_discovery import PYLSL_INSTALL_HINT, discover_streams


def main() -> None:
    parser = argparse.ArgumentParser(description="Discover local LSL streams")
    parser.add_argument("--stream-name", default=None)
    parser.add_argument("--stream-type", default=None)
    parser.add_argument("--source-id", default=None)
    parser.add_argument("--timeout", type=float, default=1.0)
    args = parser.parse_args()
    try:
        streams = discover_streams(
            name=args.stream_name,
            stream_type=args.stream_type,
            source_id=args.source_id,
            timeout=args.timeout,
        )
    except RuntimeError:
        print(PYLSL_INSTALL_HINT, file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps({"streams": streams}, indent=2))


if __name__ == "__main__":
    main()
