from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

VALID_MODALITIES = {"eeg", "eog", "emg", "eda", "ppg", "gaze", "marker", "physio"}
REPO_ROOT = Path(__file__).resolve().parents[3]
PROFILE_DIR = REPO_ROOT / "configs" / "hardware"


def list_profiles(profile_dir: Path | None = None) -> list[dict[str, Any]]:
    directory = profile_dir or PROFILE_DIR
    profiles = []
    for path in sorted(directory.glob("*.yaml")):
        try:
            profile = load_profile(path)
            profiles.append(_profile_summary(profile, path))
        except Exception as exc:
            profiles.append({"profile_id": path.stem, "path": str(path), "error": str(exc)})
    return profiles


def get_profile(profile_id: str, profile_dir: Path | None = None) -> dict[str, Any]:
    directory = profile_dir or PROFILE_DIR
    for path in sorted(directory.glob("*.yaml")):
        profile = load_profile(path)
        if profile.get("profile_id") == profile_id or path.stem == profile_id:
            return profile
    raise FileNotFoundError(profile_id)


def load_profile(path: str | Path) -> dict[str, Any]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if "profile_id" not in data:
        data["profile_id"] = Path(path).stem
    return data


def validate_profile(profile: dict[str, Any]) -> dict[str, Any]:
    channels = profile.get("channels") or []
    required_modalities = set(profile.get("required_modalities") or [])
    warnings: list[str] = []
    errors: list[str] = []

    if not channels:
        errors.append("Profile does not define channels.")

    seen_indices: set[int] = set()
    present_modalities: set[str] = set()
    for channel in channels:
        index = channel.get("index")
        modality = channel.get("modality")
        enabled = bool(channel.get("enabled", True))
        if not isinstance(index, int) or index < 0:
            errors.append(f"Invalid channel index for {channel.get('name', '<unknown>')}.")
        elif index in seen_indices:
            errors.append(f"Duplicate channel index: {index}.")
        else:
            seen_indices.add(index)
        if modality not in VALID_MODALITIES:
            errors.append(f"Unknown modality '{modality}' for channel {channel.get('name')}.")
        elif enabled:
            present_modalities.add(str(modality))

    missing = sorted(required_modalities - present_modalities)
    if missing:
        errors.append(f"Missing required modality/modalities: {', '.join(missing)}.")

    optional_missing = sorted(set(profile.get("optional_modalities") or []) - present_modalities)
    if optional_missing:
        warnings.append(f"Optional modality/modalities not mapped: {', '.join(optional_missing)}.")

    return {
        "ok": not errors,
        "profile_id": profile.get("profile_id"),
        "channel_count": len(channels),
        "modalities": sorted(present_modalities),
        "warnings": warnings,
        "errors": errors,
    }


def validate_profile_against_stream(
    profile: dict[str, Any],
    stream: dict[str, Any],
    tolerance_percent: float = 5.0,
) -> dict[str, Any]:
    base = validate_profile(profile)
    warnings = list(base["warnings"])
    errors = list(base["errors"])

    expected_name = profile.get("stream_name")
    if expected_name and stream.get("name") != expected_name:
        errors.append(f"Expected stream name {expected_name}, observed {stream.get('name')}.")

    expected_type = profile.get("stream_type") or profile.get("adapter_type")
    if expected_type and expected_type != "lsl" and stream.get("type") != expected_type:
        errors.append(f"Expected stream type {expected_type}, observed {stream.get('type')}.")

    expected_count = profile.get("expected_channel_count") or len(profile.get("channels") or [])
    observed_count = stream.get("channel_count")
    if expected_count and observed_count and int(expected_count) != int(observed_count):
        errors.append(f"Expected {expected_count} channels, observed {observed_count}.")

    expected_rate = profile.get("expected_sampling_rate") or profile.get("sampling_rate")
    observed_rate = stream.get("nominal_srate")
    if isinstance(expected_rate, int | float) and isinstance(observed_rate, int | float):
        drift = abs((float(observed_rate) - float(expected_rate)) / float(expected_rate)) * 100
        if drift > tolerance_percent:
            errors.append(
                f"Sampling rate drift {drift:.2f}% exceeds tolerance {tolerance_percent:.2f}%."
            )

    expected_names = [
        ch.get("name") for ch in profile.get("channels", []) if ch.get("enabled", True)
    ]
    observed_names = stream.get("channel_names") or []
    missing_names = sorted(set(expected_names) - set(observed_names))
    if observed_names and missing_names:
        warnings.append(f"Observed stream missing configured labels: {', '.join(missing_names)}.")

    return {
        **base,
        "ok": not errors,
        "stream_name": stream.get("name"),
        "stream_type": stream.get("type"),
        "observed_channel_count": observed_count,
        "observed_sampling_rate": observed_rate,
        "warnings": warnings,
        "errors": errors,
    }


def _profile_summary(profile: dict[str, Any], path: Path) -> dict[str, Any]:
    validation = validate_profile(profile)
    return {
        "profile_id": profile.get("profile_id"),
        "adapter_type": profile.get("adapter_type") or profile.get("adapter"),
        "device_name": profile.get("device_name") or profile.get("profile"),
        "path": str(path),
        "validation": validation,
    }
