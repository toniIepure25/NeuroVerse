"""Inspect an MNE-compatible EEG file or NeuroVerse EEG fixture."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.event_epochs import inspect_raw_source  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect local EEG metadata before replay")
    parser.add_argument("--input-file", default=None)
    parser.add_argument("--fixture-mode", action="store_true", default=False)
    parser.add_argument("--duration-seconds", type=float, default=30.0)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    report = inspect_raw_source(
        input_file=args.input_file,
        fixture_mode=args.fixture_mode,
        duration_seconds=args.duration_seconds,
    )
    output = _output_path(args.output, report)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Inspection written to {output}")


def _output_path(path: str | None, report: dict[str, object]) -> Path:
    if path:
        candidate = Path(path)
        return candidate if candidate.is_absolute() else ROOT / candidate
    stem = "fixture" if report.get("source") == "fixture" else Path(str(report.get("source"))).stem
    return ROOT / "reports" / "eeg_file_inspection" / f"{stem}_inspection.json"


if __name__ == "__main__":
    main()
