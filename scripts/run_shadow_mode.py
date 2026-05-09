"""Run simulator shadow inference without emitting real adaptation actions."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from fastapi import HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.api.routes_shadow import ShadowStartRequest, start_shadow_mode


async def _main() -> None:
    parser = argparse.ArgumentParser(description="Run NeuroVerse shadow mode")
    parser.add_argument("--duration-seconds", type=float, default=2.0)
    parser.add_argument("--source", default="simulator")
    parser.add_argument("--stream-name", default="NeuroVerseSyntheticEEG")
    parser.add_argument("--stream-type", default="EEG")
    parser.add_argument("--marker-stream-name", default=None)
    parser.add_argument("--marker-stream-type", default="Markers")
    parser.add_argument("--profile-id", default=None)
    parser.add_argument("--calibration-id", default=None)
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--board-id", default=None)
    parser.add_argument("--serial-port", default=None)
    args = parser.parse_args()
    default_profile = (
        "eeg_lsl_10_20_fixture"
        if args.source == "eeg_lsl_replay"
        else "lsl_synthetic_eeg" if args.source == "lsl"
        else "brainflow_synthetic_eeg" if args.source == "brainflow"
        else "synthetic_multimodal"
    )
    try:
        report = await start_shadow_mode(
            ShadowStartRequest(
                duration_seconds=args.duration_seconds,
                source=args.source,
                stream_name=args.stream_name,
                stream_type=args.stream_type,
                marker_stream_name=args.marker_stream_name,
                marker_stream_type=args.marker_stream_type,
                profile_id=args.profile_id or default_profile,
                calibration_id=args.calibration_id,
                model_id=args.model_id,
                board_id=args.board_id,
                serial_port=args.serial_port,
            )
        )
    except HTTPException as exc:
        print(str(exc.detail), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(_main())
