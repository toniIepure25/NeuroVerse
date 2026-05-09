"""Run a record-only eyes-open/eyes-closed BrainFlow EEG trial."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.acquisition.alpha_reactivity import (
    alpha_reactivity_markdown,
    analyze_alpha_reactivity,
)
from app.acquisition.artifacts import merge_artifact_summaries, summarize_eeg_artifacts
from app.acquisition.brainflow_adapter import (
    BrainFlowAcquisition,
    discover_brainflow_devices,
)
from app.acquisition.channel_mapping import get_profile, validate_profile
from app.acquisition.pipeline import extract_features_and_sqi
from app.acquisition.timing import summarize_window_timing
from app.core.config import settings
from app.inference.heuristic_model import HeuristicStateEstimator
from app.policy.adaptation_policy import AdaptationPolicy
from app.safety.safety_gate import SafetyGate
from app.sessions.protocol import create_calibration_profile


async def _main() -> None:
    parser = argparse.ArgumentParser(description="Run a safe first physical EEG trial")
    parser.add_argument("--profile-id", default="openbci_cyton_8ch")
    parser.add_argument("--port", default=None)
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--eyes-open-seconds", type=float, default=30.0)
    parser.add_argument("--eyes-closed-seconds", type=float, default=30.0)
    parser.add_argument("--shadow-seconds", type=float, default=30.0)
    parser.add_argument("--output-dir", default="reports/hardware_trials")
    args = parser.parse_args()

    report = await run_trial(
        profile_id=args.profile_id,
        port=args.port,
        synthetic=args.synthetic,
        eyes_open_seconds=args.eyes_open_seconds,
        eyes_closed_seconds=args.eyes_closed_seconds,
        shadow_seconds=args.shadow_seconds,
        output_dir=Path(args.output_dir),
    )
    print(json.dumps(report, indent=2))
    if report.get("physical_device_detected") is False and not args.synthetic:
        raise SystemExit(2)
    if report.get("trial_status") == "failed":
        raise SystemExit(2)


async def run_trial(
    *,
    profile_id: str,
    port: str | None,
    synthetic: bool,
    eyes_open_seconds: float,
    eyes_closed_seconds: float,
    shadow_seconds: float,
    output_dir: Path,
) -> dict[str, Any]:
    trial_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_physical_eeg_trial")
    trial_dir = output_dir / trial_id
    trial_dir.mkdir(parents=True, exist_ok=True)
    profile = get_profile(profile_id)
    board_id = profile.get("board_id")
    physical = board_id != -1 and not synthetic
    if physical and not port:
        report = _no_device_report(
            trial_id=trial_id,
            profile_id=profile_id,
            reason="Physical BrainFlow/OpenBCI trials require an explicit PORT.",
        )
        _write_json(trial_dir / "physical_eeg_trial_summary.json", report)
        _write_text(trial_dir / "physical_eeg_trial_summary.md", _trial_markdown(report))
        return report

    config = {
        **profile,
        "profile_id": profile_id,
        "serial_port": port or profile.get("serial_port"),
        "window_seconds": settings.tick_interval_s,
    }
    if synthetic:
        config["board_id"] = -1
        config["serial_port"] = None

    adapter = BrainFlowAcquisition(config)
    phases: dict[str, dict[str, Any]] = {}
    validation_report: dict[str, Any] | None = None
    calibration_report: dict[str, Any] | None = None
    shadow_report: dict[str, Any] | None = None
    try:
        await adapter.start()
        eyes_open = await _collect_phase(adapter, "eyes_open", eyes_open_seconds)
        eyes_closed = await _collect_phase(adapter, "eyes_closed", eyes_closed_seconds)
        phases = {"eyes_open": eyes_open, "eyes_closed": eyes_closed}
        shadow_windows = (
            await _collect_shadow(adapter, shadow_seconds)
            if shadow_seconds > 0
            else {"report": None, "windows": []}
        )
        status = adapter.status()
        expected_rate = float(status.get("sampling_rate") or profile.get("expected_sampling_rate") or 1.0)
        all_timestamps = eyes_open["timestamps"] + eyes_closed["timestamps"]
        all_artifacts = eyes_open["artifact_summaries"] + eyes_closed["artifact_summaries"]
        validation_report = {
            "report_id": f"{trial_id}_raw_validation",
            "adapter": "brainflow",
            "profile_id": profile_id,
            "physical_or_synthetic": "synthetic" if synthetic else status.get("physical_or_synthetic"),
            "board": {
                "board_name": status.get("board_name"),
                "board_id": status.get("board_id"),
                "serial_port": status.get("serial_port"),
                "eeg_channel_indices": status.get("eeg_channels"),
            },
            "phase_windows": {
                label: phase["window_count"] for label, phase in phases.items()
            },
            "timing": summarize_window_timing(
                all_timestamps,
                expected_rate_hz=expected_rate,
                max_gap_ms=(1000.0 / expected_rate) * 5.0 if expected_rate > 0 else None,
            ),
            "channel_mapping": {
                "profile_validation": validate_profile(profile),
                "observed_channel_count": len(status.get("channel_names") or []),
                "observed_channel_names": status.get("channel_names") or [],
            },
            "sqi_summary": _sqi_summary(eyes_open["sqi_values"] + eyes_closed["sqi_values"]),
            "artifact_summary": merge_artifact_summaries(all_artifacts),
            "closed_loop_allowed": False,
            "scientific_note": (
                "Hardware validation confirms stream quality and software integration; "
                "it does not validate clinical or unrestricted mental-state inference."
            ),
        }
        alpha_report = analyze_alpha_reactivity(
            phases,
            sampling_rate=expected_rate,
            channel_names=status.get("channel_names") or phases["eyes_open"]["channel_names"],
        )
        calibration_report = _calibration_report(
            trial_id,
            profile_id,
            status,
            eyes_open["states"] + eyes_closed["states"],
            eyes_open["sqi_values"] + eyes_closed["sqi_values"],
            all_timestamps,
            expected_rate,
        )
        shadow_report = shadow_windows["report"]
        summary = {
            "trial_id": trial_id,
            "trial_status": "completed",
            "protocol": "physical_eeg_alpha_reactivity",
            "profile_id": profile_id,
            "physical_device_detected": not synthetic,
            "synthetic_mode": synthetic,
            "device_discovery": discover_brainflow_devices(),
            "board": validation_report["board"],
            "durations": {
                "eyes_open_seconds": eyes_open_seconds,
                "eyes_closed_seconds": eyes_closed_seconds,
                "shadow_seconds": shadow_seconds,
            },
            "validation": validation_report,
            "alpha_reactivity": alpha_report,
            "calibration": calibration_report,
            "shadow": shadow_report,
            "closed_loop_allowed": False,
            "real_adaptation_actions_emitted": 0,
            "required_safety_language": [
                "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
                "Hardware validation confirms stream quality and software integration; it does not validate clinical or unrestricted mental-state inference.",
                "Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal behavior, not a medical test.",
            ],
        }
    except Exception as exc:
        status = adapter.status()
        summary = {
            "trial_id": trial_id,
            "trial_status": "failed",
            "protocol": "physical_eeg_alpha_reactivity",
            "profile_id": profile_id,
            "physical_device_detected": False if physical else synthetic,
            "synthetic_mode": synthetic,
            "board": status,
            "error": str(exc),
            "closed_loop_allowed": False,
            "real_adaptation_actions_emitted": 0,
        }
    finally:
        await adapter.stop()

    _write_outputs(trial_dir, summary, validation_report, calibration_report, shadow_report)
    return summary


async def _collect_phase(
    adapter: BrainFlowAcquisition,
    label: str,
    duration_seconds: float,
) -> dict[str, Any]:
    estimator = HeuristicStateEstimator()
    end_time = datetime.now(timezone.utc).timestamp() + max(duration_seconds, 0.1)
    windows = []
    states = []
    timestamps: list[float] = []
    sqi_values: list[float] = []
    artifacts: list[dict[str, Any]] = []
    channel_names: list[str] = []
    while datetime.now(timezone.utc).timestamp() < end_time:
        window = await adapter.get_window()
        channel_names = window.channel_names
        features = extract_features_and_sqi(window)
        states.append(estimator.predict(features).model_dump())
        sqi = features.sqi_scores.get("multimodal")
        if sqi is not None:
            sqi_values.append(float(sqi))
        timestamps.extend(window.timestamps or [])
        artifacts.append(summarize_eeg_artifacts(window.data, window.channel_names))
        windows.append(window.data)
    return {
        "label": label,
        "duration_seconds": duration_seconds,
        "window_count": len(windows),
        "channel_names": channel_names,
        "data": _concat_channel_windows(windows),
        "timestamps": timestamps,
        "sqi_values": sqi_values,
        "states": states,
        "artifact_summaries": artifacts,
    }


async def _collect_shadow(adapter: BrainFlowAcquisition, duration_seconds: float) -> dict[str, Any]:
    estimator = HeuristicStateEstimator()
    safety_gate = SafetyGate()
    policy = AdaptationPolicy()
    predictions = []
    safety_decisions = []
    would_be_actions = []
    timestamps: list[float] = []
    sqi_values: list[float] = []
    end_time = datetime.now(timezone.utc).timestamp() + max(duration_seconds, 0.1)
    while datetime.now(timezone.utc).timestamp() < end_time:
        window = await adapter.get_window()
        features = extract_features_and_sqi(window)
        prediction = estimator.predict(features)
        safety = safety_gate.evaluate(prediction, features.sqi_scores, policy.action_history)
        action = policy.decide(prediction, safety)
        predictions.append(prediction.model_dump())
        safety_decisions.append(safety.model_dump())
        would_be_actions.append(action.model_dump())
        sqi = features.sqi_scores.get("multimodal")
        if sqi is not None:
            sqi_values.append(float(sqi))
        timestamps.extend(window.timestamps or [])
    status = adapter.status()
    expected_rate = float(status.get("sampling_rate") or 1.0)
    return {
        "windows": predictions,
        "report": {
            "report_id": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ_physical_eeg_shadow"),
            "source": "brainflow_physical_trial",
            "board": {
                "board_name": status.get("board_name"),
                "board_id": status.get("board_id"),
                "physical_or_synthetic": status.get("physical_or_synthetic"),
                "serial_port": status.get("serial_port"),
            },
            "predicted_states": predictions,
            "safety_decisions": safety_decisions,
            "would_be_actions": would_be_actions,
            "real_adaptation_actions_emitted": 0,
            "closed_loop_allowed": False,
            "window_count": len(predictions),
            "sqi_summary": _sqi_summary(sqi_values),
            "timing": summarize_window_timing(
                timestamps,
                expected_rate_hz=expected_rate,
                max_gap_ms=(1000.0 / expected_rate) * 5.0,
            ),
            "scientific_note": "Physical EEG trial shadow mode emits no corridor adaptation actions.",
        },
    }


def _calibration_report(
    trial_id: str,
    profile_id: str,
    board_status: dict[str, Any],
    states: list[dict[str, Any]],
    sqi_values: list[float],
    timestamps: list[float],
    expected_rate: float,
) -> dict[str, Any]:
    calibration_id = f"{trial_id}_calibration"
    profile = create_calibration_profile(
        calibration_id,
        states,
        duration_seconds=0.0,
        sqi_values=sqi_values,
    )
    return {
        **profile.model_dump(),
        "calibration_id": calibration_id,
        "source": "physical_hardware"
        if board_status.get("physical_or_synthetic") == "physical"
        else "brainflow_synthetic_trial",
        "protocol": "eyes_open_eyes_closed_alpha_reactivity",
        "profile_id": profile_id,
        "board": {
            "board_name": board_status.get("board_name"),
            "board_id": board_status.get("board_id"),
            "physical_or_synthetic": board_status.get("physical_or_synthetic"),
            "serial_port": board_status.get("serial_port"),
        },
        "baseline_state_proxy_means": {
            key: round(mean([state[key] for state in states]), 4)
            for key in states[0]
            if key not in {"model_version", "feature_window_ms"}
        }
        if states
        else {},
        "baseline_sqi": round(mean(sqi_values), 4) if sqi_values else None,
        "timestamp_quality": summarize_window_timing(
            timestamps,
            expected_rate_hz=expected_rate,
            max_gap_ms=(1000.0 / expected_rate) * 5.0 if expected_rate > 0 else None,
        ),
        "warnings": [
            "Calibration values are proxy baselines for this hardware trial, not clinical measurements."
        ],
    }


def _concat_channel_windows(windows: list[list[list[float]]]) -> list[list[float]]:
    if not windows:
        return []
    channel_count = len(windows[0])
    combined = [[] for _ in range(channel_count)]
    for window in windows:
        for idx in range(min(channel_count, len(window))):
            combined[idx].extend(float(value) for value in window[idx])
    return combined


def _sqi_summary(values: list[float]) -> dict[str, float | int | None]:
    return {
        "count": len(values),
        "mean": round(mean(values), 4) if values else None,
        "min": round(min(values), 4) if values else None,
        "max": round(max(values), 4) if values else None,
    }


def _no_device_report(*, trial_id: str, profile_id: str, reason: str) -> dict[str, Any]:
    return {
        "trial_id": trial_id,
        "trial_status": "no_device",
        "protocol": "physical_eeg_alpha_reactivity",
        "profile_id": profile_id,
        "physical_device_detected": False,
        "device_discovery": discover_brainflow_devices(),
        "reason": reason,
        "closed_loop_allowed": False,
        "real_adaptation_actions_emitted": 0,
        "next_commands": {
            "discover": "make discover-brainflow-devices",
            "cyton": "make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0",
            "ganglion": "make physical-eeg-trial-openbci-ganglion PORT=/dev/ttyUSB0",
        },
    }


def _write_outputs(
    trial_dir: Path,
    summary: dict[str, Any],
    validation_report: dict[str, Any] | None,
    calibration_report: dict[str, Any] | None,
    shadow_report: dict[str, Any] | None,
) -> None:
    _write_json(trial_dir / "physical_eeg_trial_summary.json", summary)
    _write_text(trial_dir / "physical_eeg_trial_summary.md", _trial_markdown(summary))
    if validation_report:
        _write_json(trial_dir / "raw_validation_report.json", validation_report)
    alpha = summary.get("alpha_reactivity")
    if alpha:
        _write_json(trial_dir / "alpha_reactivity_report.json", alpha)
        _write_text(trial_dir / "alpha_reactivity_report.md", alpha_reactivity_markdown(alpha))
    if calibration_report:
        _write_json(trial_dir / "calibration_report.json", calibration_report)
    if shadow_report:
        _write_json(trial_dir / "shadow_report.json", shadow_report)


def _trial_markdown(summary: dict[str, Any]) -> str:
    alpha = summary.get("alpha_reactivity") or {}
    validation = summary.get("validation") or {}
    timing = validation.get("timing") or {}
    shadow = summary.get("shadow") or {}
    return "\n".join([
        f"# Physical EEG Trial: {summary.get('trial_id')}",
        "",
        f"- Status: `{summary.get('trial_status')}`",
        f"- Profile: `{summary.get('profile_id')}`",
        f"- Synthetic mode: `{summary.get('synthetic_mode')}`",
        f"- Physical device detected: `{summary.get('physical_device_detected')}`",
        f"- Closed-loop allowed: `{summary.get('closed_loop_allowed')}`",
        f"- Observed rate: `{timing.get('observed_rate_hz')}` Hz",
        f"- Jitter p95: `{timing.get('jitter_ms_p95')}` ms",
        f"- Alpha status: `{alpha.get('status')}`",
        f"- Alpha ratio closed/open: `{alpha.get('aggregate_alpha_ratio')}`",
        f"- Shadow windows: `{shadow.get('window_count')}`",
        f"- Real adaptation actions emitted: `{summary.get('real_adaptation_actions_emitted')}`",
        "",
        "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
        "Hardware validation confirms stream quality and software integration; it does not validate clinical or unrestricted mental-state inference.",
        "Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal behavior, not a medical test.",
        "",
        *([f"Reason: {summary.get('reason')}"] if summary.get("reason") else []),
        "",
    ])


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(_main())
