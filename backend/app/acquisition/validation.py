from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

from app.acquisition.artifacts import merge_artifact_summaries, summarize_eeg_artifacts
from app.acquisition.brainflow_adapter import BrainFlowAcquisition
from app.acquisition.channel_mapping import (
    get_profile,
    validate_profile,
    validate_profile_against_stream,
)
from app.acquisition.diagnostics import optional_dependency_status
from app.acquisition.lsl_adapter import LSLAcquisition
from app.acquisition.marker_collector import BackgroundMarkerCollector
from app.acquisition.markers import (
    MarkerEvent,
    empty_marker_report,
    marker_report,
)
from app.acquisition.pipeline import extract_features_and_sqi
from app.acquisition.simulator import BiosignalSimulator
from app.acquisition.timing import summarize_window_timing
from app.core.config import settings
from app.core.runtime_status import runtime_status

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATION_REPORT_DIR = REPO_ROOT / "reports" / "hardware_validation"
VALIDATION_REPORT_DIR.mkdir(parents=True, exist_ok=True)
_VALIDATION_STATUS: dict[str, Any] = {
    "state": "UNKNOWN",
    "active_report_id": None,
    "last_report_id": None,
    "closed_loop_allowed": False,
    "reason": "No hardware validation has run.",
}


def validation_status() -> dict[str, Any]:
    return dict(_VALIDATION_STATUS)


def list_validation_reports() -> list[dict[str, Any]]:
    reports = []
    for path in sorted(VALIDATION_REPORT_DIR.glob("*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            reports.append({
                "report_id": path.stem,
                "path": str(path),
                "adapter": data.get("adapter"),
                "passed": data.get("passed"),
                "closed_loop_allowed": data.get("closed_loop_allowed"),
                "created_at": data.get("created_at"),
                "warnings": data.get("warnings", []),
            })
        except json.JSONDecodeError:
            continue
    return reports


def get_validation_report(report_id: str) -> dict[str, Any]:
    path = VALIDATION_REPORT_DIR / f"{report_id}.json"
    if not path.exists():
        raise FileNotFoundError(report_id)
    return json.loads(path.read_text(encoding="utf-8"))


async def run_hardware_validation(
    adapter: str = "simulator",
    config: dict[str, Any] | None = None,
    profile_id: str | None = None,
    duration_seconds: float = 2.0,
    record_windows: bool = True,
    run_sqi: bool = True,
    run_shadow_inference: bool = False,
) -> dict[str, Any]:
    config = config or {}
    adapter = adapter.lower()
    report_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{adapter}_validation"
    _set_status("RECORDING", report_id, False, "Validation running in record-only mode.")

    adapter = config.get("adapter_type", adapter)
    if adapter != "simulator":
        dependency = {
            "brainflow": "brainflow",
            "lsl": "pylsl",
            "xdf": "pyxdf",
            "xdf_replay": "pyxdf",
        }.get(adapter)
        deps = optional_dependency_status()
        if dependency and not deps.get(dependency, False):
            report = _base_report(report_id, adapter, profile_id, duration_seconds)
            report.update({
                "passed": False,
                "closed_loop_allowed": False,
                "warnings": [f"Optional dependency '{dependency}' is not installed."],
                "failure_reasons": [f"Cannot validate {adapter} without {dependency}."],
                "dependency_status": deps,
            })
            _write_report(report)
            _set_status("FAILED", report_id, False, report["failure_reasons"][0])
            return _finalize_failed_report(report, report["failure_reasons"][0])

    if adapter == "lsl":
        return await _run_lsl_validation(
            report_id=report_id,
            config=config,
            profile_id=profile_id,
            duration_seconds=duration_seconds,
            record_windows=record_windows,
            run_sqi=run_sqi,
            run_shadow_inference=run_shadow_inference,
        )
    if adapter == "brainflow":
        return await _run_brainflow_validation(
            report_id=report_id,
            config=config,
            profile_id=profile_id,
            duration_seconds=duration_seconds,
            record_windows=record_windows,
            run_sqi=run_sqi,
            run_shadow_inference=run_shadow_inference,
        )

    profile_validation = None
    profile = None
    if profile_id:
        profile = get_profile(profile_id)
        profile_validation = validate_profile(profile)

    simulator = BiosignalSimulator(
        duration_s=max(duration_seconds, 0.5),
        tick_interval_ms=float(config.get("tick_interval_ms", settings.tick_interval_ms)),
    )
    await simulator.start()
    windows = []
    timestamps: list[float] = []
    sqi_values: list[float] = []
    try:
        tick_s = simulator.capabilities()["sampling_rate"]
        expected_rate = float(tick_s)
        window_count = max(1, int(round(duration_seconds / settings.tick_interval_s)))
        sample_cursor = 0
        for _ in range(window_count):
            window = await simulator.get_window()
            sample_count = len(window.data[0]) if window.data else 0
            for i in range(sample_count):
                timestamps.append((sample_cursor + i) / window.sampling_rate)
            sample_cursor += sample_count
            if window.signal_quality_hint is not None:
                sqi_values.append(float(window.signal_quality_hint))
            if record_windows:
                windows.append({
                    "sampling_rate": window.sampling_rate,
                    "channel_names": window.channel_names,
                    "window_size_ms": window.window_size_ms,
                    "signal_quality_hint": window.signal_quality_hint,
                })
    finally:
        await simulator.stop()

    timing = summarize_window_timing(timestamps, expected_rate_hz=expected_rate)
    channel_names = windows[0]["channel_names"] if windows else []
    channel_status = {
        "observed_channel_count": len(channel_names),
        "observed_channel_names": channel_names,
        "profile_validation": profile_validation,
    }
    warnings = list(timing["warnings"])
    failure_reasons = []
    if profile_validation and not profile_validation["ok"]:
        failure_reasons.extend(profile_validation["errors"])
    if not timing["pass"]:
        failure_reasons.append("Timing validation did not pass.")
    if run_sqi and sqi_values and mean(sqi_values) < 0.45:
        failure_reasons.append("Mean SQI is below validation threshold.")

    passed = not failure_reasons
    closed_loop_allowed = bool(
        passed
        and adapter == "simulator"
        and settings.hardware_closed_loop_enabled
    )
    report = _base_report(report_id, adapter, profile_id, duration_seconds)
    report.update({
        "passed": passed,
        "closed_loop_allowed": closed_loop_allowed,
        "mode": "hardware_record_only" if adapter != "simulator" else "simulated_closed_loop",
        "run_shadow_inference": run_shadow_inference,
        "timing": timing,
        "channel_mapping": channel_status,
        "sqi_summary": {
            "count": len(sqi_values),
            "mean": round(mean(sqi_values), 4) if sqi_values else None,
            "min": round(min(sqi_values), 4) if sqi_values else None,
            "max": round(max(sqi_values), 4) if sqi_values else None,
        },
        "windows_recorded": len(windows),
        "warnings": warnings,
        "failure_reasons": failure_reasons,
        "dependency_status": optional_dependency_status(),
    })
    _write_report(report)
    _set_status(
        "PASSED" if passed else "FAILED",
        report_id,
        closed_loop_allowed,
        _status_reason(report),
    )
    return report


async def _run_brainflow_validation(
    report_id: str,
    config: dict[str, Any],
    profile_id: str | None,
    duration_seconds: float,
    record_windows: bool,
    run_sqi: bool,
    run_shadow_inference: bool,
) -> dict[str, Any]:
    profile = get_profile(profile_id) if profile_id else None
    merged_config = {**(profile or {}), **config, "profile_id": profile_id}
    adapter = BrainFlowAcquisition(merged_config)
    windows = []
    timestamps: list[float] = []
    sqi_values: list[float] = []
    artifact_summaries: list[dict[str, Any]] = []
    failure_reasons: list[str] = []
    warnings: list[str] = []
    profile_validation = validate_profile(profile) if profile else None
    status: dict[str, Any] = {}
    try:
        await adapter.start()
        end_ts = datetime.now(timezone.utc).timestamp() + duration_seconds
        while datetime.now(timezone.utc).timestamp() < end_ts:
            window = await adapter.get_window()
            status = adapter.status()
            timestamps.extend(window.timestamps or [])
            if run_sqi:
                features = extract_features_and_sqi(window)
                sqi = features.sqi_scores.get("multimodal")
                if sqi is not None:
                    sqi_values.append(float(sqi))
                artifact_summaries.append(
                    summarize_eeg_artifacts(window.data, window.channel_names)
                )
            if record_windows:
                windows.append({
                    "sampling_rate": window.sampling_rate,
                    "channel_names": window.channel_names,
                    "window_size_ms": window.window_size_ms,
                    "sample_count": len(window.timestamps or []),
                    "start_time": min(window.timestamps) if window.timestamps else None,
                    "end_time": max(window.timestamps) if window.timestamps else None,
                })
    except Exception as exc:
        failure_reasons.append(str(exc))
        status = adapter.status()
    finally:
        await adapter.stop()

    expected_rate = _safe_float(
        merged_config.get("expected_sampling_rate"),
        merged_config.get("sampling_rate"),
        status.get("sampling_rate"),
        default=1.0,
    )
    timing = summarize_window_timing(
        timestamps,
        expected_rate_hz=expected_rate,
        max_gap_ms=(1000.0 / expected_rate) * 5.0 if expected_rate > 0 else None,
    )
    warnings.extend(timing["warnings"])
    warnings.extend(adapter.config_warnings())
    brainflow_profile_check = _validate_brainflow_profile(profile, status) if profile else None
    if profile_validation and not profile_validation["ok"]:
        failure_reasons.extend(profile_validation["errors"])
    if brainflow_profile_check and not brainflow_profile_check["ok"]:
        failure_reasons.extend(brainflow_profile_check["errors"])
    if not timing["pass"]:
        failure_reasons.append("Timing validation did not pass.")
    if run_sqi and sqi_values and mean(sqi_values) < 0.45:
        failure_reasons.append("Mean SQI is below validation threshold.")

    passed = not failure_reasons
    report = _base_report(report_id, "brainflow", profile_id, duration_seconds)
    report.update({
        "passed": passed,
        "closed_loop_allowed": False,
        "mode": "hardware_record_only",
        "run_shadow_inference": run_shadow_inference,
        "board": {
            "board_name": status.get("board_name"),
            "board_id": status.get("board_id"),
            "physical_or_synthetic": status.get("physical_or_synthetic"),
            "serial_port": status.get("serial_port"),
            "eeg_channel_indices": status.get("eeg_channels"),
        },
        "stream_metadata": {
            "name": status.get("board_name"),
            "type": "EEG",
            "channel_count": len(status.get("channel_names") or []),
            "channel_names": status.get("channel_names") or [],
            "nominal_srate": status.get("sampling_rate"),
            "source": "brainflow",
        },
        "timing": timing,
        "channel_mapping": {
            "observed_channel_count": len(status.get("channel_names") or []),
            "observed_channel_names": status.get("channel_names") or [],
            "profile_validation": profile_validation,
            "board_profile_validation": brainflow_profile_check,
        },
        "sqi_summary": {
            "count": len(sqi_values),
            "mean": round(mean(sqi_values), 4) if sqi_values else None,
            "min": round(min(sqi_values), 4) if sqi_values else None,
            "max": round(max(sqi_values), 4) if sqi_values else None,
        },
        "artifact_summary": merge_artifact_summaries(artifact_summaries),
        "windows_recorded": len(windows),
        "warnings": warnings,
        "failure_reasons": failure_reasons,
        "dependency_status": optional_dependency_status(),
        "recommendations": [
            "Review timing, channel mapping, and SQI before calibration.",
            "Run hardware calibration and shadow inference before any future closed-loop review.",
            "Closed-loop from physical EEG remains disabled by default.",
        ],
    })
    _write_report(report)
    _set_status("PASSED" if passed else "FAILED", report_id, False, _status_reason(report))
    return report


def _base_report(
    report_id: str,
    adapter: str,
    profile_id: str | None,
    duration_seconds: float,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "report_id": report_id,
        "adapter": adapter,
        "profile_id": profile_id,
        "created_at": now,
        "started_at": now,
        "ended_at": now,
        "duration_seconds": duration_seconds,
        "hardware_closed_loop_enabled": settings.hardware_closed_loop_enabled,
        "scientific_note": (
            "Hardware validation assesses timestamp consistency, channel mapping, and proxy SQI. "
            "It is not clinical validation."
        ),
    }


def _validate_brainflow_profile(
    profile: dict[str, Any] | None,
    status: dict[str, Any],
) -> dict[str, Any]:
    if not profile:
        return {"ok": True, "warnings": [], "errors": []}
    warnings: list[str] = []
    errors: list[str] = []
    expected_count = profile.get("expected_channel_count") or len(profile.get("channels") or [])
    observed_names = status.get("channel_names") or []
    if expected_count and observed_names and int(expected_count) != len(observed_names):
        errors.append(f"Expected {expected_count} EEG channels, observed {len(observed_names)}.")
    expected_rate = profile.get("expected_sampling_rate") or profile.get("sampling_rate")
    observed_rate = status.get("sampling_rate")
    if isinstance(expected_rate, int | float) and isinstance(observed_rate, int | float):
        drift = abs((float(observed_rate) - float(expected_rate)) / float(expected_rate)) * 100
        if drift > 5.0:
            errors.append(f"Sampling rate drift {drift:.2f}% exceeds 5.00%.")
    expected_names = [
        str(ch.get("name")) for ch in profile.get("channels", []) if ch.get("enabled", True)
    ]
    if observed_names and expected_names:
        missing = sorted(set(expected_names) - set(str(name) for name in observed_names))
        if missing:
            warnings.append(
                "Observed BrainFlow channel labels differ from configured profile labels: "
                + ", ".join(missing)
            )
    return {
        "ok": not errors,
        "warnings": warnings,
        "errors": errors,
        "board_name": status.get("board_name"),
        "observed_sampling_rate": observed_rate,
        "observed_channel_count": len(observed_names),
    }


def _safe_float(*values: Any, default: float) -> float:
    for value in values:
        if isinstance(value, int | float):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                continue
    return default


async def _run_lsl_validation(
    report_id: str,
    config: dict[str, Any],
    profile_id: str | None,
    duration_seconds: float,
    record_windows: bool,
    run_sqi: bool,
    run_shadow_inference: bool,
) -> dict[str, Any]:
    adapter = LSLAcquisition({
        "stream_name": config.get("stream_name"),
        "stream_type": config.get("stream_type", "EEG"),
        "source_id": config.get("source_id"),
        "timeout": config.get("timeout_seconds", config.get("timeout", 1.0)),
        "window_seconds": config.get("window_seconds", settings.tick_interval_s),
    })
    windows = []
    timestamps: list[float] = []
    clock_offsets: list[float] = []
    sqi_values: list[float] = []
    failure_reasons: list[str] = []
    warnings: list[str] = []
    stream_meta: dict[str, Any] | None = None
    profile_validation = None
    marker_collector = BackgroundMarkerCollector(
        stream_name=config.get("marker_stream_name"),
        stream_type=config.get("marker_stream_type", "Markers"),
        timeout=float(config.get("marker_timeout", 0.5)),
    )
    markers: list[MarkerEvent] = []
    marker_stream_error: str | None = None
    artifact_summaries: list[dict[str, Any]] = []

    try:
        try:
            marker_collector.start()
        except Exception as exc:
            marker_stream_error = str(exc)
        await adapter.start()
        stream_meta = adapter.status().get("selected_stream")
        profile = get_profile(profile_id) if profile_id else None
        if profile and stream_meta:
            profile_validation = validate_profile_against_stream(profile, stream_meta)
        end_time = datetime.now(timezone.utc).timestamp() + duration_seconds
        while datetime.now(timezone.utc).timestamp() < end_time:
            window = await adapter.get_window()
            if window.timestamps:
                timestamps.extend(window.timestamps)
                start_time = min(window.timestamps)
                end_time = max(window.timestamps)
            else:
                start_time = None
                end_time = None
            if window.metadata and window.metadata.get("clock_offset") is not None:
                clock_offsets.append(float(window.metadata["clock_offset"]))
            if run_sqi:
                features = extract_features_and_sqi(window)
                sqi = features.sqi_scores.get("multimodal")
                if sqi is not None:
                    sqi_values.append(float(sqi))
                artifact_summaries.append(
                    summarize_eeg_artifacts(window.data, window.channel_names)
                )
            if record_windows:
                windows.append({
                    "sampling_rate": window.sampling_rate,
                    "channel_names": window.channel_names,
                    "window_size_ms": window.window_size_ms,
                    "sample_count": len(window.timestamps or []),
                    "start_time": start_time,
                    "end_time": end_time,
                })
    except Exception as exc:
        failure_reasons.append(str(exc))
    finally:
        markers = marker_collector.stop()
        await adapter.stop()

    expected_rate = float(
        (stream_meta or {}).get("nominal_srate") or config.get("expected_rate", 1.0)
    )
    timing = summarize_window_timing(
        timestamps,
        expected_rate_hz=expected_rate,
        clock_offsets=clock_offsets,
    )
    if not timing["pass"]:
        failure_reasons.append("Timing validation did not pass.")
    if profile_validation and not profile_validation["ok"]:
        failure_reasons.extend(profile_validation["errors"])
    if run_sqi and sqi_values and mean(sqi_values) < 0.45:
        failure_reasons.append("Mean SQI is below validation threshold.")

    markers_report = (
        marker_report(
            stream_metadata=marker_collector.stream_metadata,
            markers=markers,
            windows=windows,
        )
        if marker_collector.stream_metadata
        else empty_marker_report(
            marker_stream_error or marker_collector.error or "No marker stream detected."
        )
    )
    warnings.extend(timing["warnings"])
    if markers_report.get("marker_alignment_warnings"):
        warnings.extend(markers_report["marker_alignment_warnings"])

    passed = not failure_reasons
    report = _base_report(report_id, "lsl", profile_id, duration_seconds)
    report.update({
        "passed": passed,
        "closed_loop_allowed": bool(passed and settings.hardware_closed_loop_enabled),
        "mode": "hardware_record_only",
        "run_shadow_inference": run_shadow_inference,
        "stream_metadata": stream_meta,
        "timing": timing,
        "channel_mapping": {
            "observed_channel_count": (stream_meta or {}).get("channel_count"),
            "observed_channel_names": (stream_meta or {}).get("channel_names", []),
            "profile_validation": profile_validation,
        },
        "source_type": config.get("source_type", "lsl"),
        "markers": markers_report,
        "sqi_summary": {
            "count": len(sqi_values),
            "mean": round(mean(sqi_values), 4) if sqi_values else None,
            "min": round(min(sqi_values), 4) if sqi_values else None,
            "max": round(max(sqi_values), 4) if sqi_values else None,
        },
        "artifact_summary": merge_artifact_summaries(artifact_summaries),
        "windows_recorded": len(windows),
        "warnings": warnings,
        "failure_reasons": failure_reasons,
        "dependency_status": optional_dependency_status(),
    })
    _write_report(report)
    _set_status(
        "PASSED" if passed else "FAILED",
        report_id,
        bool(report["closed_loop_allowed"]),
        _status_reason(report),
    )
    return report


def _finalize_failed_report(report: dict[str, Any], reason: str) -> dict[str, Any]:
    report.setdefault("markers", _empty_marker_summary())
    report.setdefault("timing", {})
    report.setdefault("channel_mapping", {})
    _write_report(report)
    _set_status("FAILED", report["report_id"], False, reason)
    return report


def _empty_marker_summary() -> dict[str, Any]:
    return empty_marker_report()


def _write_report(report: dict[str, Any]) -> None:
    json_path = VALIDATION_REPORT_DIR / f"{report['report_id']}.json"
    md_path = VALIDATION_REPORT_DIR / f"{report['report_id']}.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(_markdown_report(report), encoding="utf-8")


def _markdown_report(report: dict[str, Any]) -> str:
    return "\n".join([
        f"# Hardware Validation Report: {report['report_id']}",
        "",
        f"- Adapter: `{report['adapter']}`",
        f"- Profile: `{report.get('profile_id') or 'none'}`",
        f"- Passed: `{report.get('passed')}`",
        f"- Closed-loop allowed: `{report.get('closed_loop_allowed')}`",
        f"- Observed rate: `{(report.get('timing') or {}).get('observed_rate_hz')}` Hz",
        f"- Jitter p95: `{(report.get('timing') or {}).get('jitter_ms_p95')}` ms",
        f"- Gaps: `{(report.get('timing') or {}).get('gap_count')}`",
        "",
        (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
        "",
    ])


def _set_status(state: str, report_id: str | None, allowed: bool, reason: str) -> None:
    _VALIDATION_STATUS.update({
        "state": state,
        "active_report_id": report_id if state in {"RECORDING", "VALIDATING"} else None,
        "last_report_id": report_id,
        "closed_loop_allowed": allowed,
        "reason": reason,
    })
    runtime_status.set_hardware_validation_state(state, report_id)


def _status_reason(report: dict[str, Any]) -> str:
    if report.get("passed"):
        if report.get("closed_loop_allowed"):
            return "Validation passed and hardware closed-loop is explicitly enabled."
        return "Validation passed; hardware closed-loop remains disabled by default."
    return "; ".join(report.get("failure_reasons") or ["Validation failed."])
