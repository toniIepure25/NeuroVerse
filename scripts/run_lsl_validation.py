"""Run record-only LSL validation."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.acquisition.lsl_discovery import PYLSL_INSTALL_HINT
from app.acquisition.validation import run_hardware_validation


async def _main() -> None:
    parser = argparse.ArgumentParser(description="Run NeuroVerse LSL validation")
    parser.add_argument("--stream-name", default="NeuroVerseSyntheticEEG")
    parser.add_argument("--stream-type", default="EEG")
    parser.add_argument("--marker-stream-name", default=None)
    parser.add_argument("--marker-stream-type", default="Markers")
    parser.add_argument("--profile-id", default="lsl_synthetic_eeg")
    parser.add_argument("--duration-seconds", type=float, default=5.0)
    parser.add_argument("--source-type", default="lsl")
    args = parser.parse_args()
    try:
        report = await run_hardware_validation(
            adapter="lsl",
            config={
                "adapter_type": "lsl",
                "stream_name": args.stream_name,
                "stream_type": args.stream_type,
                "marker_stream_name": args.marker_stream_name,
                "marker_stream_type": args.marker_stream_type,
                "source_type": args.source_type,
            },
            profile_id=args.profile_id,
            duration_seconds=args.duration_seconds,
        )
    except RuntimeError:
        print(PYLSL_INSTALL_HINT, file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(_main())
