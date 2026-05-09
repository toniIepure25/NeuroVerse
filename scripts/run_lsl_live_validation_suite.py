"""Run the full local synthetic LSL validation workflow."""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import HTTPException

ROOT = Path(__file__).resolve().parent.parent
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.acquisition.lsl_discovery import (  # noqa: E402
    PYLSL_INSTALL_HINT,
    discover_streams,
    pylsl_available,
)
from app.acquisition.validation import run_hardware_validation  # noqa: E402
from app.api.routes_calibration import (  # noqa: E402
    CalibrationStartRequest,
    start_calibration,
)
from app.api.routes_shadow import ShadowStartRequest, start_shadow_mode  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run NeuroVerse live LSL validation suite")
    parser.add_argument("--stream-name", default="NeuroVerseSyntheticEEG")
    parser.add_argument("--stream-type", default="EEG")
    parser.add_argument("--duration-validation", type=float, default=5.0)
    parser.add_argument("--duration-calibration", type=float, default=5.0)
    parser.add_argument("--duration-shadow", type=float, default=5.0)
    parser.add_argument("--profile-id", default="lsl_synthetic_eeg")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--with-markers", action="store_true", default=True)
    parser.add_argument("--output-dir", default="reports/lsl_live_validation")
    parser.add_argument("--backend-url", default="http://localhost:8000")
    parser.add_argument("--use-api", action="store_true")
    parser.add_argument("--skip-evidence-pack", action="store_true")
    args = parser.parse_args()

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_lsl_live")
    output_dir = _resolve_output_dir(args.output_dir) / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {
        "run_id": run_id,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "stream_name": args.stream_name,
        "stream_type": args.stream_type,
        "profile_id": args.profile_id,
        "mode": "api" if args.use_api else "direct",
        "pylsl_available": pylsl_available(),
        "closed_loop_allowed": False,
        "scientific_note": (
            "This validates real-time LSL streaming infrastructure using a simulated "
            "local LSL biosignal stream. It is not clinical EEG validation."
        ),
        "artifacts": {},
        "warnings": [],
        "failures": [],
    }

    if not pylsl_available():
        summary["failures"].append(PYLSL_INSTALL_HINT)
        _write_summary(output_dir, summary)
        print(PYLSL_INSTALL_HINT, file=sys.stderr)
        raise SystemExit(2)

    streamer = _start_streamer(args, output_dir)
    try:
        discovery = _wait_for_stream(args.stream_name, args.stream_type, timeout_seconds=15.0)
        summary["discovery"] = discovery
        _write_json(output_dir / "discovery.json", discovery)

        if args.use_api:
            results = _run_api_suite(args)
        else:
            results = asyncio.run(_run_direct_suite(args))
        summary.update(results)
        _copy_artifacts(output_dir, results)

        if not args.skip_evidence_pack:
            evidence = _generate_evidence_pack()
            summary["artifacts"]["evidence_pack_path"] = str(evidence)
            (output_dir / "evidence_pack_path.txt").write_text(str(evidence), encoding="utf-8")

        summary["completed_at"] = datetime.now(timezone.utc).isoformat()
        _write_summary(output_dir, summary)
        print(json.dumps(summary, indent=2))
    except Exception as exc:
        summary["failures"].append(str(exc))
        summary["completed_at"] = datetime.now(timezone.utc).isoformat()
        _write_summary(output_dir, summary)
        print(f"LSL live validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    finally:
        _stop_streamer(streamer)


def _resolve_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    return path if path.is_absolute() else ROOT / path


def _start_streamer(args: argparse.Namespace, output_dir: Path) -> subprocess.Popen[str]:
    duration = max(
        args.duration_validation + args.duration_calibration + args.duration_shadow + 20.0,
        30.0,
    )
    command = [
        sys.executable,
        str(ROOT / "scripts" / "lsl_synthetic_streamer.py"),
        "--stream-name",
        args.stream_name,
        "--stream-type",
        args.stream_type,
        "--duration",
        str(duration),
        "--seed",
        str(args.seed),
    ]
    if args.with_markers:
        command.append("--phase-markers")
    log_path = output_dir / "streamer.log"
    log_file = log_path.open("w", encoding="utf-8")
    return subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
    )


def _stop_streamer(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _wait_for_stream(name: str, stream_type: str, timeout_seconds: float) -> dict[str, Any]:
    deadline = time.time() + timeout_seconds
    last_error = "No stream discovered yet."
    while time.time() < deadline:
        try:
            streams = discover_streams(name=name, stream_type=stream_type, timeout=0.5)
            if streams:
                return {"available": True, "streams": streams}
        except Exception as exc:
            last_error = str(exc)
        time.sleep(0.5)
    raise TimeoutError(
        f"No LSL stream detected for {name}/{stream_type}. "
        f"Start make lsl-stream-demo in another terminal. Last error: {last_error}"
    )


async def _run_direct_suite(args: argparse.Namespace) -> dict[str, Any]:
    validation = await run_hardware_validation(
        adapter="lsl",
        config={
            "adapter_type": "lsl",
            "stream_name": args.stream_name,
            "stream_type": args.stream_type,
            "timeout_seconds": 2.0,
        },
        profile_id=args.profile_id,
        duration_seconds=args.duration_validation,
        record_windows=True,
        run_sqi=True,
        run_shadow_inference=False,
    )
    calibration = await _direct_calibration(args)
    shadow = await _direct_shadow(args, calibration.get("calibration_id"))
    return {
        "validation_report": validation,
        "calibration_report": calibration,
        "shadow_report": shadow,
        "closed_loop_allowed": bool(validation.get("closed_loop_allowed")),
    }


async def _direct_calibration(args: argparse.Namespace) -> dict[str, Any]:
    try:
        return await start_calibration(
            CalibrationStartRequest(
                source="lsl",
                stream_name=args.stream_name,
                stream_type=args.stream_type,
                profile_id=args.profile_id,
                duration_seconds=args.duration_calibration,
            )
        )
    except HTTPException as exc:
        raise RuntimeError(str(exc.detail)) from exc


async def _direct_shadow(args: argparse.Namespace, calibration_id: str | None) -> dict[str, Any]:
    try:
        return await start_shadow_mode(
            ShadowStartRequest(
                source="lsl",
                stream_name=args.stream_name,
                stream_type=args.stream_type,
                profile_id=args.profile_id,
                duration_seconds=args.duration_shadow,
                calibration_id=calibration_id,
            )
        )
    except HTTPException as exc:
        raise RuntimeError(str(exc.detail)) from exc


def _run_api_suite(args: argparse.Namespace) -> dict[str, Any]:
    validation = _api_post(
        args.backend_url,
        "/api/v1/acquisition/validation/start",
        {
            "adapter": "lsl",
            "adapter_type": "lsl",
            "stream_name": args.stream_name,
            "stream_type": args.stream_type,
            "profile_id": args.profile_id,
            "duration_seconds": args.duration_validation,
            "record_windows": True,
            "run_sqi": True,
            "run_shadow_inference": False,
        },
    )
    calibration = _api_post(
        args.backend_url,
        "/api/v1/calibration/start",
        {
            "source": "lsl",
            "stream_name": args.stream_name,
            "stream_type": args.stream_type,
            "profile_id": args.profile_id,
            "duration_seconds": args.duration_calibration,
        },
    )
    shadow = _api_post(
        args.backend_url,
        "/api/v1/acquisition/shadow/start",
        {
            "source": "lsl",
            "stream_name": args.stream_name,
            "stream_type": args.stream_type,
            "profile_id": args.profile_id,
            "duration_seconds": args.duration_shadow,
            "calibration_id": calibration.get("calibration_id"),
        },
    )
    return {
        "validation_report": validation,
        "calibration_report": calibration,
        "shadow_report": shadow,
        "closed_loop_allowed": bool(validation.get("closed_loop_allowed")),
    }


def _api_post(base_url: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        base_url.rstrip("/") + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(exc.read().decode("utf-8")) from exc


def _copy_artifacts(output_dir: Path, results: dict[str, Any]) -> None:
    artifact_map = {
        "validation_report": "validation_report.json",
        "calibration_report": "calibration_report.json",
        "shadow_report": "shadow_report.json",
    }
    for key, filename in artifact_map.items():
        report = results.get(key)
        if report:
            _write_json(output_dir / filename, report)


def _generate_evidence_pack() -> Path:
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "generate_evidence_pack.py")],
        cwd=ROOT,
        check=True,
    )
    return ROOT / "evidence_pack"


def _write_summary(output_dir: Path, summary: dict[str, Any]) -> None:
    _write_json(output_dir / "live_validation_summary.json", summary)
    (output_dir / "live_validation_summary.md").write_text(
        _markdown_summary(summary),
        encoding="utf-8",
    )


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _markdown_summary(summary: dict[str, Any]) -> str:
    validation = summary.get("validation_report") or {}
    timing = validation.get("timing") or {}
    artifacts = summary.get("artifacts") or {}
    lines = [
        f"# LSL Live Validation Suite: {summary['run_id']}",
        "",
        f"- pylsl available: `{summary.get('pylsl_available')}`",
        f"- stream: `{summary.get('stream_name')}` / `{summary.get('stream_type')}`",
        f"- profile: `{summary.get('profile_id')}`",
        f"- validation passed: `{validation.get('passed')}`",
        f"- closed-loop allowed: `{summary.get('closed_loop_allowed')}`",
        f"- timing quality: `{timing.get('quality')}`",
        f"- observed rate: `{timing.get('observed_rate_hz')}` Hz",
        f"- jitter p95: `{timing.get('jitter_ms_p95')}` ms",
        f"- evidence pack: `{artifacts.get('evidence_pack_path')}`",
        "",
        (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
        "",
    ]
    if summary.get("failures"):
        lines.extend(["## Failures", "", *[f"- {item}" for item in summary["failures"]], ""])
    return "\n".join(lines)


if __name__ == "__main__":
    main()
