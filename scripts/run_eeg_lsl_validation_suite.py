"""Run EEG replay-over-LSL validation with event markers."""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import HTTPException

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.acquisition.lsl_discovery import PYLSL_INSTALL_HINT, discover_streams, pylsl_available  # noqa: E402
from app.acquisition.validation import run_hardware_validation  # noqa: E402
from app.api.routes_calibration import CalibrationStartRequest, start_calibration  # noqa: E402
from app.api.routes_shadow import ShadowStartRequest, start_shadow_mode  # noqa: E402

MNE_HINT = 'mne is not installed. Install with: cd backend && pip install -e ".[hardware]"'


def main() -> None:
    parser = argparse.ArgumentParser(description="Run EEG replay LSL validation suite")
    parser.add_argument("--input-file", default=None)
    parser.add_argument("--fixture-mode", action="store_true", default=True)
    parser.add_argument("--stream-name", default="NeuroVerseReplayEEG")
    parser.add_argument("--marker-stream-name", default="NeuroVerseReplayMarkers")
    parser.add_argument("--profile-id", default="eeg_lsl_10_20_fixture")
    parser.add_argument("--duration-validation", type=float, default=6.0)
    parser.add_argument("--duration-calibration", type=float, default=6.0)
    parser.add_argument("--duration-shadow", type=float, default=6.0)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--with-markers", action="store_true", default=True)
    parser.add_argument("--output-dir", default="reports/eeg_lsl_validation")
    parser.add_argument("--skip-evidence-pack", action="store_true")
    args = parser.parse_args()
    if args.input_file:
        args.fixture_mode = False

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_eeg_lsl")
    output_dir = _output_dir(args.output_dir) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stream_name": args.stream_name,
        "marker_stream_name": args.marker_stream_name,
        "profile_id": args.profile_id,
        "fixture_mode": args.fixture_mode,
        "pylsl_available": pylsl_available(),
        "mne_available": _mne_available(),
        "closed_loop_allowed": False,
        "scientific_note": (
            "This validates EEG replay over LSL with event markers. It is not "
            "clinical validation or a thought decoder."
        ),
        "failures": [],
        "artifacts": {},
    }
    if not pylsl_available():
        return _fail(output_dir, summary, PYLSL_INSTALL_HINT)
    if not _mne_available():
        return _fail(output_dir, summary, MNE_HINT)

    streamer = _start_streamer(args, output_dir)
    try:
        discovery = {
            "eeg": _wait_for_stream(args.stream_name, "EEG"),
            "markers": _wait_for_stream(args.marker_stream_name, "Markers"),
        }
        _write_json(output_dir / "discovery.json", discovery)
        summary["discovery"] = discovery
        results = asyncio.run(_run_suite(args))
        summary.update(results)
        _copy_artifacts(output_dir, results)
        if not args.skip_evidence_pack:
            subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "generate_evidence_pack.py")],
                cwd=ROOT,
                check=True,
            )
            summary["artifacts"]["evidence_pack_path"] = str(ROOT / "evidence_pack")
            (output_dir / "evidence_pack_path.txt").write_text(
                str(ROOT / "evidence_pack"),
                encoding="utf-8",
            )
        summary["completed_at"] = datetime.now(timezone.utc).isoformat()
        _write_summary(output_dir, summary)
        print(json.dumps(summary, indent=2))
    except Exception as exc:
        _fail(output_dir, summary, str(exc), code=1)
    finally:
        _stop_streamer(streamer)


async def _run_suite(args: argparse.Namespace) -> dict[str, Any]:
    config = {
        "adapter_type": "lsl",
        "stream_name": args.stream_name,
        "stream_type": "EEG",
        "marker_stream_name": args.marker_stream_name,
        "marker_stream_type": "Markers",
        "source_type": "eeg_lsl_replay",
        "timeout_seconds": 2.0,
    }
    validation = await run_hardware_validation(
        adapter="lsl",
        config=config,
        profile_id=args.profile_id,
        duration_seconds=args.duration_validation,
    )
    calibration = await _calibration(args)
    shadow = await _shadow(args, calibration.get("calibration_id"))
    return {
        "validation_report": validation,
        "calibration_report": calibration,
        "shadow_report": shadow,
        "closed_loop_allowed": bool(validation.get("closed_loop_allowed")),
    }


async def _calibration(args: argparse.Namespace) -> dict[str, Any]:
    try:
        return await start_calibration(
            CalibrationStartRequest(
                source="eeg_lsl_replay",
                stream_name=args.stream_name,
                stream_type="EEG",
                marker_stream_name=args.marker_stream_name,
                marker_stream_type="Markers",
                profile_id=args.profile_id,
                duration_seconds=args.duration_calibration,
            )
        )
    except HTTPException as exc:
        raise RuntimeError(str(exc.detail)) from exc


async def _shadow(args: argparse.Namespace, calibration_id: str | None) -> dict[str, Any]:
    try:
        return await start_shadow_mode(
            ShadowStartRequest(
                source="eeg_lsl_replay",
                stream_name=args.stream_name,
                stream_type="EEG",
                marker_stream_name=args.marker_stream_name,
                marker_stream_type="Markers",
                profile_id=args.profile_id,
                duration_seconds=args.duration_shadow,
                calibration_id=calibration_id,
            )
        )
    except HTTPException as exc:
        raise RuntimeError(str(exc.detail)) from exc


def _start_streamer(args: argparse.Namespace, output_dir: Path) -> subprocess.Popen[str]:
    duration = max(args.duration_validation + args.duration_calibration + args.duration_shadow + 20, 35)
    command = [
        sys.executable,
        str(ROOT / "scripts" / "eeg_lsl_replay_streamer.py"),
        "--stream-name",
        args.stream_name,
        "--marker-stream-name",
        args.marker_stream_name,
        "--duration",
        str(duration),
        "--speed",
        str(args.speed),
    ]
    if args.fixture_mode:
        command.append("--fixture-mode")
    if args.input_file:
        command.extend(["--input-file", args.input_file])
    if args.with_markers:
        command.append("--markers")
    log = (output_dir / "streamer.log").open("w", encoding="utf-8")
    return subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, text=True)


def _wait_for_stream(name: str, stream_type: str, timeout_seconds: float = 15.0) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        streams = discover_streams(name=name, stream_type=stream_type, timeout=0.5)
        if streams:
            return {"available": True, "streams": streams}
        time.sleep(0.5)
    raise TimeoutError(f"No {stream_type} LSL stream detected for {name}.")


def _stop_streamer(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _copy_artifacts(output_dir: Path, results: dict[str, Any]) -> None:
    for key, name in {
        "validation_report": "validation_report.json",
        "calibration_report": "calibration_report.json",
        "shadow_report": "shadow_report.json",
    }.items():
        _write_json(output_dir / name, results[key])


def _write_summary(output_dir: Path, summary: dict[str, Any]) -> None:
    _write_json(output_dir / "eeg_lsl_validation_summary.json", summary)
    validation = summary.get("validation_report") or {}
    calibration = summary.get("calibration_report") or {}
    shadow = summary.get("shadow_report") or {}
    timing = validation.get("timing") or {}
    markers = validation.get("markers") or {}
    calibration_markers = calibration.get("markers") or {}
    shadow_markers = shadow.get("markers") or {}
    markdown = "\n".join([
        f"# EEG LSL Validation Suite: {summary['run_id']}",
        "",
        f"- fixture mode: `{summary.get('fixture_mode')}`",
        f"- validation passed: `{validation.get('passed')}`",
        f"- closed-loop allowed: `{summary.get('closed_loop_allowed')}`",
        f"- timing quality: `{timing.get('quality')}`",
        f"- observed rate: `{timing.get('observed_rate_hz')}` Hz",
        f"- validation marker count: `{markers.get('marker_count')}`",
        f"- calibration marker count: `{calibration_markers.get('marker_count')}`",
        f"- shadow marker count: `{shadow_markers.get('marker_count')}`",
        f"- calibration marker labels: `{', '.join(calibration_markers.get('marker_labels') or [])}`",
        "",
        (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
        "",
    ])
    (output_dir / "eeg_lsl_validation_summary.md").write_text(markdown, encoding="utf-8")


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _output_dir(path: str) -> Path:
    output = Path(path)
    return output if output.is_absolute() else ROOT / output


def _mne_available() -> bool:
    try:
        import mne  # noqa: F401
    except Exception:
        return False
    return True


def _fail(output_dir: Path, summary: dict[str, Any], message: str, code: int = 2) -> None:
    summary["failures"].append(message)
    summary["completed_at"] = datetime.now(timezone.utc).isoformat()
    _write_summary(output_dir, summary)
    print(message, file=sys.stderr)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
