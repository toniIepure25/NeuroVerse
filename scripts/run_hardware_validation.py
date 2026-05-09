"""Run NeuroVerse hardware validation in safe record-only simulator mode."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.acquisition.validation import run_hardware_validation


async def _main() -> None:
    parser = argparse.ArgumentParser(description="Run a NeuroVerse acquisition validation report")
    parser.add_argument("--adapter", default="simulator")
    parser.add_argument("--profile-id", default="synthetic_multimodal")
    parser.add_argument("--duration-seconds", type=float, default=2.0)
    parser.add_argument("--board-id", default=None)
    parser.add_argument("--serial-port", default=None)
    args = parser.parse_args()
    config = {}
    if args.board_id is not None:
        config["board_id"] = int(args.board_id) if str(args.board_id).lstrip("-").isdigit() else args.board_id
    if args.serial_port:
        config["serial_port"] = args.serial_port
    config["adapter_type"] = args.adapter
    report = await run_hardware_validation(
        adapter=args.adapter,
        config=config,
        profile_id=args.profile_id,
        duration_seconds=args.duration_seconds,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    asyncio.run(_main())
