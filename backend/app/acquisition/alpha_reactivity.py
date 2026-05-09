from __future__ import annotations

import math
from statistics import mean
from typing import Any

import numpy as np

from app.acquisition.artifacts import summarize_eeg_artifacts

POSTERIOR_CHANNELS = {"o1", "o2", "oz", "p3", "p4", "pz", "po7", "po8"}


def analyze_alpha_reactivity(
    phases: dict[str, dict[str, Any]],
    *,
    sampling_rate: float,
    channel_names: list[str],
    min_seconds: float = 2.0,
) -> dict[str, Any]:
    """Compare eyes-closed vs eyes-open alpha power as an EEG sanity check."""
    warnings: list[str] = [
        (
            "Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal "
            "behavior, not a medical test."
        )
    ]
    if "eyes_open" not in phases or "eyes_closed" not in phases:
        return {
            "status": "insufficient_data",
            "alpha_band_hz": [8.0, 12.0],
            "warnings": warnings + ["Both eyes_open and eyes_closed phases are required."],
            "closed_loop_allowed": False,
        }
    if sampling_rate <= 0:
        return {
            "status": "insufficient_data",
            "alpha_band_hz": [8.0, 12.0],
            "warnings": warnings + ["Sampling rate is missing or invalid."],
            "closed_loop_allowed": False,
        }

    open_data = _phase_array(phases["eyes_open"])
    closed_data = _phase_array(phases["eyes_closed"])
    if open_data.size == 0 or closed_data.size == 0:
        return {
            "status": "insufficient_data",
            "alpha_band_hz": [8.0, 12.0],
            "warnings": warnings + ["One or more phases contain no EEG samples."],
            "closed_loop_allowed": False,
        }

    min_samples = int(round(min_seconds * sampling_rate))
    if open_data.shape[1] < min_samples or closed_data.shape[1] < min_samples:
        warnings.append(
            f"Short phase data: alpha estimates are less stable below {min_seconds:g} seconds."
        )

    open_power = _bandpower_per_channel(open_data, sampling_rate, 8.0, 12.0)
    closed_power = _bandpower_per_channel(closed_data, sampling_rate, 8.0, 12.0)
    ratios = _safe_ratio(closed_power, open_power)
    posterior_indices = [
        idx
        for idx, name in enumerate(channel_names)
        if _normalize_channel_name(name) in POSTERIOR_CHANNELS and idx < len(ratios)
    ]
    aggregate_ratio = _finite_mean(ratios)
    posterior_ratio = _finite_mean([ratios[idx] for idx in posterior_indices])
    artifact_open = summarize_eeg_artifacts(open_data.tolist(), channel_names)
    artifact_closed = summarize_eeg_artifacts(closed_data.tolist(), channel_names)
    bad = sorted(
        set(artifact_open.get("bad_channel_candidates", []))
        | set(artifact_closed.get("bad_channel_candidates", []))
    )
    if bad:
        warnings.append("Noisy or extreme-amplitude channel candidates may affect alpha estimates.")
    if not posterior_indices:
        warnings.append(
            "No named posterior channels found; aggregate alpha ratio uses all channels."
        )

    status = _classify_alpha_status(
        aggregate_ratio=aggregate_ratio,
        posterior_ratio=posterior_ratio,
        bad_count=len(bad),
        channel_count=len(channel_names) or int(open_data.shape[0]),
    )
    per_channel = []
    for idx, ratio in enumerate(ratios):
        name = channel_names[idx] if idx < len(channel_names) else f"ch{idx + 1}"
        per_channel.append({
            "channel": name,
            "eyes_open_alpha_power": _round_float(open_power[idx]),
            "eyes_closed_alpha_power": _round_float(closed_power[idx]),
            "eyes_closed_over_open_ratio": _round_float(ratio),
            "posterior_channel": idx in posterior_indices,
        })

    return {
        "status": status,
        "quality_flag": status,
        "alpha_band_hz": [8.0, 12.0],
        "eyes_open_alpha_mean": _round_float(_finite_mean(open_power)),
        "eyes_closed_alpha_mean": _round_float(_finite_mean(closed_power)),
        "aggregate_alpha_ratio": _round_float(aggregate_ratio),
        "posterior_alpha_ratio": _round_float(posterior_ratio),
        "posterior_channels": [channel_names[idx] for idx in posterior_indices],
        "per_channel": per_channel,
        "artifact_summary": {
            "eyes_open": artifact_open,
            "eyes_closed": artifact_closed,
            "bad_channel_candidates": bad,
        },
        "warnings": warnings,
        "closed_loop_allowed": False,
        "scientific_note": (
            "Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal behavior, "
            "not a medical test."
        ),
    }


def alpha_reactivity_markdown(report: dict[str, Any]) -> str:
    return "\n".join([
        "# Alpha Reactivity Report",
        "",
        f"- Status: `{report.get('status')}`",
        f"- Aggregate eyes-closed/open alpha ratio: `{report.get('aggregate_alpha_ratio')}`",
        f"- Posterior eyes-closed/open alpha ratio: `{report.get('posterior_alpha_ratio')}`",
        f"- Posterior channels: `{', '.join(report.get('posterior_channels') or []) or 'none'}`",
        f"- Closed-loop allowed: `{report.get('closed_loop_allowed')}`",
        "",
        (
            "Eyes-open / eyes-closed alpha reactivity is a sanity check for EEG signal "
            "behavior, not a medical test."
        ),
        (
            "Hardware validation confirms stream quality and software integration; it does "
            "not validate clinical or unrestricted mental-state inference."
        ),
        "",
        "## Warnings",
        "",
        *[f"- {warning}" for warning in report.get("warnings", [])],
        "",
    ])


def _phase_array(phase: dict[str, Any]) -> np.ndarray:
    data = phase.get("data") or []
    arr = np.asarray(data, dtype=float)
    if arr.ndim != 2:
        return np.empty((0, 0), dtype=float)
    return arr


def _bandpower_per_channel(
    data: np.ndarray,
    sampling_rate: float,
    low: float,
    high: float,
) -> list[float]:
    powers = []
    for row in data:
        finite = row[np.isfinite(row)]
        if finite.size < 2:
            powers.append(float("nan"))
            continue
        finite = finite - float(np.mean(finite))
        freqs = np.fft.rfftfreq(finite.size, d=1.0 / sampling_rate)
        spectrum = np.abs(np.fft.rfft(finite)) ** 2
        mask = (freqs >= low) & (freqs <= high)
        powers.append(float(np.mean(spectrum[mask])) if np.any(mask) else float("nan"))
    return powers


def _safe_ratio(numerators: list[float], denominators: list[float]) -> list[float]:
    ratios = []
    for numerator, denominator in zip(numerators, denominators, strict=False):
        if not math.isfinite(numerator) or not math.isfinite(denominator) or denominator <= 0:
            ratios.append(float("nan"))
        else:
            ratios.append(float(numerator / denominator))
    return ratios


def _finite_mean(values: list[float]) -> float | None:
    finite = [
        float(value)
        for value in values
        if isinstance(value, int | float) and math.isfinite(value)
    ]
    return float(mean(finite)) if finite else None


def _classify_alpha_status(
    *,
    aggregate_ratio: float | None,
    posterior_ratio: float | None,
    bad_count: int,
    channel_count: int,
) -> str:
    if aggregate_ratio is None:
        return "insufficient_data"
    if channel_count and bad_count / channel_count >= 0.5:
        return "noisy_signal"
    target_ratio = posterior_ratio if posterior_ratio is not None else aggregate_ratio
    if target_ratio >= 1.2:
        return "visible_reactivity"
    if target_ratio >= 1.05:
        return "weak_reactivity"
    return "inconclusive"


def _round_float(value: float | None) -> float | None:
    if value is None or not math.isfinite(value):
        return None
    return round(float(value), 6)


def _normalize_channel_name(value: str) -> str:
    return value.strip().lower().replace(" ", "")
