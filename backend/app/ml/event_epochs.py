from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy.signal import butter, filtfilt, iirnotch, sosfiltfilt, welch

from app.acquisition.eeg_fixture import create_eeg_fixture_raw, load_mne_raw
from app.ml.event_label_mapping import normalize_event_label

BANDS = {
    "delta": (1.0, 4.0),
    "theta": (4.0, 8.0),
    "alpha": (8.0, 13.0),
    "beta": (13.0, 30.0),
    "gamma": (30.0, 45.0),
}

REPO_ROOT = Path(__file__).resolve().parents[3]


def load_raw_source(
    *,
    input_file: str | None = None,
    fixture_mode: bool = False,
    duration_seconds: float = 30.0,
    seed: int = 42,
) -> Any:
    if fixture_mode:
        return create_eeg_fixture_raw(duration_seconds, seed)
    if not input_file:
        raise ValueError("--input-file is required unless fixture mode is enabled")
    return load_mne_raw(input_file)


def inspect_raw_source(
    *,
    input_file: str | None = None,
    fixture_mode: bool = False,
    duration_seconds: float = 30.0,
    seed: int = 42,
) -> dict[str, Any]:
    raw = load_raw_source(
        input_file=input_file,
        fixture_mode=fixture_mode,
        duration_seconds=duration_seconds,
        seed=seed,
    )
    sfreq = float(raw.info["sfreq"])
    duration = float(raw.n_times / sfreq)
    labels = [str(label) for label in raw.annotations.description]
    return {
        "source": "fixture" if fixture_mode else str(input_file),
        "format": "mne_rawarray_fixture" if fixture_mode else Path(str(input_file)).suffix.lower(),
        "channel_count": len(raw.ch_names),
        "channel_names": list(raw.ch_names),
        "sampling_rate_hz": sfreq,
        "duration_seconds": round(duration, 4),
        "annotation_count": len(labels),
        "annotation_labels": sorted(set(labels)),
        "annotation_distribution": dict(sorted(Counter(labels).items())),
        "bad_channels": list(raw.info.get("bads", [])),
        "estimated_memory_mb": round(raw.n_times * len(raw.ch_names) * 8 / 1_000_000, 4),
        "suggested_profile": (
            "eeg_lsl_10_20_fixture" if fixture_mode else "create a local hardware profile"
        ),
        "warnings": _inspection_warnings(raw, labels, fixture_mode),
        "scientific_note": (
            "EEG inspection reports file metadata and annotations; it is not clinical review."
        ),
    }


def prepare_event_feature_dataset(
    *,
    input_file: str | None = None,
    dataset_config: str | Path | None = None,
    fixture_mode: bool = False,
    output_path: str | Path,
    tmin: float = 0.0,
    tmax: float = 1.5,
    event_labels: list[str] | None = None,
    seed: int = 42,
    source_id: str | None = None,
    pick_eeg_only: bool = True,
    max_channels: int | None = None,
    pick_channels: list[str] | None = None,
    bandpass_low: float | None = None,
    bandpass_high: float | None = None,
    notch_freq: float | None = None,
    baseline_correction: bool = False,
    reject_amplitude_uv: float | None = None,
    feature_set: str = "combined",
) -> dict[str, Any]:
    if dataset_config:
        rows, summary_meta = _rows_from_dataset_config(
            dataset_config,
            tmin=tmin,
            tmax=tmax,
            event_labels=event_labels,
            pick_eeg_only=pick_eeg_only,
            max_channels=max_channels,
            pick_channels=pick_channels,
            bandpass_low=bandpass_low,
            bandpass_high=bandpass_high,
            notch_freq=notch_freq,
            baseline_correction=baseline_correction,
            reject_amplitude_uv=reject_amplitude_uv,
            feature_set=feature_set,
        )
    else:
        raw = load_raw_source(
            input_file=input_file,
            fixture_mode=fixture_mode,
            duration_seconds=30.0,
            seed=seed,
        )
        if pick_eeg_only:
            raw.pick_types(eeg=True, exclude=[])
        if pick_channels:
            available = [name for name in pick_channels if name in raw.ch_names]
            if available:
                raw.pick(available)
        if max_channels:
            raw.pick(raw.ch_names[:max_channels])
        raw.load_data()
        source = source_id or ("fixture" if fixture_mode else str(input_file))
        rows = event_feature_rows(
            raw,
            tmin=tmin,
            tmax=tmax,
            event_labels=event_labels,
            source_id=source,
            subject_id="fixture" if fixture_mode else None,
            run_id=None,
            file_id=Path(source).stem,
            bandpass_low=bandpass_low,
            bandpass_high=bandpass_high,
            notch_freq=notch_freq,
            baseline_correction=baseline_correction,
            reject_amplitude_uv=reject_amplitude_uv,
            feature_set=feature_set,
        )
        summary_meta = {
            "channel_names": list(raw.ch_names),
            "sampling_rate_hz": float(raw.info["sfreq"]),
            "source": "fixture" if fixture_mode else str(input_file),
            "subjects": ["fixture"] if fixture_mode else [],
            "runs": [],
        }
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No event-locked rows generated from EEG source.")
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "output": str(out),
        "row_count": len(rows),
        "event_labels": sorted({row["event_label"] for row in rows}),
        "label_distribution": dict(Counter(row["event_label"] for row in rows)),
        "feature_count": len([key for key in rows[0] if key.startswith("eeg_")]),
        "epoch_window": {"tmin": tmin, "tmax": tmax},
        "preprocessing": {
            "bandpass_low": bandpass_low,
            "bandpass_high": bandpass_high,
            "notch_freq": notch_freq,
            "baseline_correction": baseline_correction,
            "reject_amplitude_uv": reject_amplitude_uv,
            "pick_channels": pick_channels or [],
            "max_channels": max_channels,
        },
        "feature_set": feature_set,
        "quality": {
            "failed_epoch_count": sum(
                1 for row in rows if str(row.get("epoch_quality_pass", "true")).lower() == "false"
            ),
            "failed_epoch_fraction": round(
                sum(
                    1
                    for row in rows
                    if str(row.get("epoch_quality_pass", "true")).lower() == "false"
                )
                / max(len(rows), 1),
                4,
            ),
        },
        "subject_distribution": dict(Counter(str(row.get("subject_id", "")) for row in rows)),
        "run_distribution": dict(Counter(str(row.get("run_id", "")) for row in rows)),
        "warnings": _feature_warnings(rows),
        **summary_meta,
    }
    Path(f"{out}.summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def event_feature_rows(
    raw: Any,
    *,
    tmin: float,
    tmax: float,
    event_labels: list[str] | None = None,
    source_id: str,
    subject_id: str | None = None,
    run_id: int | str | None = None,
    file_id: str | None = None,
    custom_mapping: dict[str, str] | None = None,
    bandpass_low: float | None = None,
    bandpass_high: float | None = None,
    notch_freq: float | None = None,
    baseline_correction: bool = False,
    reject_amplitude_uv: float | None = None,
    feature_set: str = "combined",
) -> list[dict[str, Any]]:
    sfreq = float(raw.info["sfreq"])
    labels_filter = set(event_labels or [])
    rows = []
    for idx, (onset, label) in enumerate(
        zip(raw.annotations.onset, raw.annotations.description, strict=False)
    ):
        original_label = str(label)
        mapped = normalize_event_label(
            original_label,
            run_id=run_id,
            custom_mapping=custom_mapping,
        )
        normalized_label = mapped["event_label"]
        if (
            labels_filter
            and original_label not in labels_filter
            and normalized_label not in labels_filter
        ):
            continue
        start = int(round((float(onset) + tmin) * sfreq))
        end = int(round((float(onset) + tmax) * sfreq))
        if start < 0 or end <= start or end > raw.n_times:
            continue
        data = raw.get_data(start=start, stop=end) * 1_000_000.0
        data = preprocess_epoch(
            data,
            sfreq,
            bandpass_low=bandpass_low,
            bandpass_high=bandpass_high,
            notch_freq=notch_freq,
            baseline_correction=baseline_correction,
        )
        peak_abs = float(np.nanmax(np.abs(data))) if data.size else 0.0
        quality_pass = reject_amplitude_uv is None or peak_abs <= reject_amplitude_uv
        sid = subject_id or Path(source_id).stem or "unknown"
        rid = str(run_id or "")
        row = {
            "sample_id": f"{Path(source_id).stem}_{idx}",
            "source_id": source_id,
            "file_id": file_id or Path(source_id).name,
            "subject_id": sid,
            "run_id": rid,
            "group_subject": sid,
            "group_run": f"{sid}_run_{rid}" if rid else Path(source_id).stem,
            "original_label": original_label,
            "event_label": normalized_label,
            "task_context": mapped["task_context"],
            "event_onset_seconds": round(float(onset), 4),
            "epoch_start_seconds": round(float(onset) + tmin, 4),
            "epoch_end_seconds": round(float(onset) + tmax, 4),
            "sampling_rate_hz": sfreq,
            "group": f"{sid}_run_{rid}" if rid else Path(source_id).stem or "fixture",
            "epoch_quality_pass": quality_pass,
            "epoch_peak_abs_uv": round(peak_abs, 6),
            "epoch_quality_flags": (
                ""
                if quality_pass
                else f"amplitude_gt_{reject_amplitude_uv}_uv"
            ),
        }
        row.update(extract_epoch_features(data, sfreq, list(raw.ch_names), feature_set=feature_set))
        rows.append(row)
    return rows


def preprocess_epoch(
    data: np.ndarray,
    sfreq: float,
    *,
    bandpass_low: float | None = None,
    bandpass_high: float | None = None,
    notch_freq: float | None = None,
    baseline_correction: bool = False,
) -> np.ndarray:
    arr = np.asarray(data, dtype=float)
    if baseline_correction:
        arr = arr - np.nanmean(arr, axis=1, keepdims=True)
    nyquist = sfreq / 2.0
    if bandpass_low is not None or bandpass_high is not None:
        low = max(float(bandpass_low or 0.1), 0.001)
        high = min(float(bandpass_high or (nyquist - 1.0)), nyquist - 0.001)
        if low < high:
            sos = butter(4, [low, high], btype="bandpass", fs=sfreq, output="sos")
            arr = sosfiltfilt(sos, arr, axis=1)
    if notch_freq is not None and 0.0 < float(notch_freq) < nyquist:
        b, a = iirnotch(float(notch_freq), Q=30.0, fs=sfreq)
        arr = filtfilt(b, a, arr, axis=1)
    return arr


def extract_epoch_features(
    data: np.ndarray,
    sfreq: float,
    channel_names: list[str],
    feature_set: str = "combined",
) -> dict[str, float]:
    features: dict[str, float] = {}
    arr = np.asarray(data, dtype=float)
    requested = _feature_set(feature_set)
    for idx, channel in enumerate(channel_names):
        values = arr[idx]
        finite = values[np.isfinite(values)]
        if finite.size == 0:
            finite = np.asarray([0.0])
        if "statistical" in requested:
            features[f"eeg_{channel}_mean_uv"] = float(np.mean(finite))
            features[f"eeg_{channel}_std_uv"] = float(np.std(finite))
        if "logvar" in requested:
            features[f"eeg_{channel}_logvar"] = float(np.log(np.var(finite) + 1e-9))
        freqs, power = welch(finite, fs=sfreq, nperseg=min(len(finite), int(sfreq)))
        total = float(np.trapezoid(power, freqs) + 1e-12)
        if "bandpower" in requested:
            for band, (low, high) in BANDS.items():
                mask = (freqs >= low) & (freqs < high)
                value = (
                    float(np.trapezoid(power[mask], freqs[mask]) / total)
                    if np.any(mask)
                    else 0.0
                )
                features[f"eeg_{channel}_{band}_relpower"] = value
    if "bandpower" in requested:
        for band in BANDS:
            keys = [key for key in features if key.endswith(f"_{band}_relpower")]
            features[f"eeg_global_{band}_relpower"] = float(
                np.mean([features[key] for key in keys])
            )
    if "lateralized" in requested:
        features.update(_lateralized_features(features, channel_names))
    return features


def _feature_set(value: str) -> set[str]:
    raw = {item.strip().lower() for item in value.split(",") if item.strip()}
    if not raw or "combined" in raw:
        return {"statistical", "bandpower", "logvar", "lateralized"}
    return raw


def _clean_channel_name(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def _lateralized_features(features: dict[str, float], channel_names: list[str]) -> dict[str, float]:
    result: dict[str, float] = {}
    cleaned = {_clean_channel_name(name): name for name in channel_names}
    pairs = [("c3", "c4"), ("fc3", "fc4"), ("cp3", "cp4")]
    for left_clean, right_clean in pairs:
        left = cleaned.get(left_clean)
        right = cleaned.get(right_clean)
        if not left or not right:
            continue
        for band in BANDS:
            left_key = f"eeg_{left}_{band}_relpower"
            right_key = f"eeg_{right}_{band}_relpower"
            if left_key in features and right_key in features:
                result[f"eeg_lateral_{left_clean}_{right_clean}_{band}_relpower_diff"] = float(
                    features[left_key] - features[right_key]
                )
    return result


def read_feature_csv(
    path: str | Path,
) -> tuple[np.ndarray, np.ndarray, list[str], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(dict(row))
    if not rows:
        raise ValueError(f"No rows in feature CSV: {path}")
    feature_names = [key for key in rows[0] if key.startswith("eeg_")]
    x = np.asarray([[float(row[name]) for name in feature_names] for row in rows], dtype=float)
    y = np.asarray([row["event_label"] for row in rows])
    return x, y, feature_names, rows


def inspect_eeg_dataset_config(config_path: str | Path) -> dict[str, Any]:
    cfg = _load_dataset_config(config_path)
    file_items = _file_items(cfg, Path(config_path).parent)
    reports = []
    warnings = []
    for item in file_items:
        path = Path(item["path"])
        if not path.exists():
            warnings.append(f"Missing EEG file: {path}")
            continue
        try:
            raw = load_mne_raw(str(path))
            labels = [str(label) for label in raw.annotations.description]
            reports.append({
                "path": str(path),
                "subject_id": str(item.get("subject_id", "")),
                "run_id": str(item.get("run_id", "")),
                "channel_count": len(raw.ch_names),
                "channel_names": list(raw.ch_names),
                "sampling_rate_hz": float(raw.info["sfreq"]),
                "duration_seconds": float(raw.n_times / float(raw.info["sfreq"])),
                "annotation_count": len(labels),
                "annotation_distribution": dict(Counter(labels)),
                "event_mapping": [
                    normalize_event_label(label, run_id=item.get("run_id"))
                    for label in sorted(set(labels))
                ],
            })
        except Exception as exc:
            warnings.append(f"Could not inspect {path}: {exc}")
    return {
        "dataset_id": cfg.get("dataset_id"),
        "dataset_name": cfg.get("dataset_name"),
        "source": cfg.get("source"),
        "file_count": len(file_items),
        "inspected_file_count": len(reports),
        "subjects": sorted({str(item.get("subject_id", "")) for item in file_items}),
        "runs": sorted({str(item.get("run_id", "")) for item in file_items}),
        "channel_count_distribution": dict(Counter(str(r["channel_count"]) for r in reports)),
        "sampling_rate_distribution": dict(Counter(str(r["sampling_rate_hz"]) for r in reports)),
        "annotation_label_distribution": dict(
            sum((Counter(r["annotation_distribution"]) for r in reports), Counter())
        ),
        "files": reports,
        "warnings": warnings + _dataset_split_warnings(file_items),
        "recommended_splits": ["group_run", "within_subject", "group_subject"],
        "scientific_note": (
            "Dataset inspection summarizes metadata and annotations; it is not clinical review."
        ),
    }


def _inspection_warnings(raw: Any, labels: list[str], fixture_mode: bool) -> list[str]:
    warnings = []
    if fixture_mode:
        warnings.append("Fixture mode is deterministic EEG-like data, not external public EEG.")
    if not labels:
        warnings.append(
            "No annotations found; event-locked classifier training may be unavailable."
        )
    if len(set(labels)) < 2:
        warnings.append("Fewer than two event labels found.")
    if raw.info.get("bads"):
        warnings.append("File metadata contains bad channel labels.")
    return warnings


def _rows_from_dataset_config(
    config_path: str | Path,
    *,
    tmin: float,
    tmax: float,
    event_labels: list[str] | None,
    pick_eeg_only: bool,
    max_channels: int | None,
    pick_channels: list[str] | None,
    bandpass_low: float | None,
    bandpass_high: float | None,
    notch_freq: float | None,
    baseline_correction: bool,
    reject_amplitude_uv: float | None,
    feature_set: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = _load_dataset_config(config_path)
    rows: list[dict[str, Any]] = []
    channel_names: list[str] = []
    sampling_rates: list[float] = []
    warnings: list[str] = []
    custom_mapping = (
        cfg.get("event_mapping") if isinstance(cfg.get("event_mapping"), dict) else None
    )
    file_items = _file_items(cfg, Path(config_path).parent)
    for item in file_items:
        path = Path(item["path"])
        if not path.exists():
            warnings.append(f"Missing EEG file: {path}")
            continue
        raw = load_mne_raw(str(path))
        if pick_eeg_only:
            raw.pick_types(eeg=True, exclude=[])
        if pick_channels:
            available = [name for name in pick_channels if name in raw.ch_names]
            if available:
                raw.pick(available)
        if max_channels:
            raw.pick(raw.ch_names[:max_channels])
        raw.load_data()
        channel_names = channel_names or list(raw.ch_names)
        sampling_rates.append(float(raw.info["sfreq"]))
        rows.extend(
            event_feature_rows(
                raw,
                tmin=tmin,
                tmax=tmax,
                event_labels=event_labels,
                source_id=str(path),
                subject_id=str(item.get("subject_id", "")),
                run_id=item.get("run_id"),
                file_id=str(item.get("file_id") or path.name),
                custom_mapping=custom_mapping,
                bandpass_low=bandpass_low,
                bandpass_high=bandpass_high,
                notch_freq=notch_freq,
                baseline_correction=baseline_correction,
                reject_amplitude_uv=reject_amplitude_uv,
                feature_set=feature_set,
            )
        )
    return rows, {
        "dataset_id": cfg.get("dataset_id"),
        "dataset_name": cfg.get("dataset_name"),
        "source": cfg.get("source", "dataset_config"),
        "subjects": sorted({str(item.get("subject_id", "")) for item in file_items}),
        "runs": sorted({str(item.get("run_id", "")) for item in file_items}),
        "channel_names": channel_names,
        "sampling_rate_hz": float(np.median(sampling_rates)) if sampling_rates else None,
        "warnings": warnings,
    }


def _load_dataset_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)
    with open(path, encoding="utf-8") as f:
        if path.suffix.lower() in {".yaml", ".yml"}:
            data = yaml.safe_load(f) or {}
        else:
            data = json.load(f)
    data["_config_path"] = str(path)
    return data


def _file_items(cfg: dict[str, Any], config_dir: Path) -> list[dict[str, Any]]:
    items = []
    for idx, item in enumerate(cfg.get("files") or []):
        path = Path(str(item.get("path", "")))
        if not path.is_absolute():
            root = Path(str(cfg.get("local_root", "")))
            if root and not root.is_absolute():
                root = (REPO_ROOT / root).resolve()
            path = root / path if root else (config_dir / path).resolve()
        enriched = dict(item)
        enriched["path"] = str(path)
        enriched["file_id"] = enriched.get("file_id") or f"file_{idx:03d}"
        items.append(enriched)
    return items


def _feature_warnings(rows: list[dict[str, Any]]) -> list[str]:
    warnings = []
    labels = Counter(row["event_label"] for row in rows)
    if len(labels) < 2:
        warnings.append("Fewer than two normalized event labels were generated.")
    if labels and min(labels.values()) < 2:
        warnings.append(
            "At least one event class has fewer than two epochs; split metrics may be unstable."
        )
    subjects = {str(row.get("subject_id", "")) for row in rows}
    if len(subjects) < 2:
        warnings.append(
            "Only one subject is present; subject-level generalization cannot be estimated."
        )
    return warnings


def _dataset_split_warnings(file_items: list[dict[str, Any]]) -> list[str]:
    warnings = []
    if len({str(item.get("subject_id", "")) for item in file_items}) < 2:
        warnings.append("Only one subject found; leave-one-subject-out is unavailable.")
    if len({str(item.get("run_id", "")) for item in file_items}) < 2:
        warnings.append("Only one run found; cross-run validation is unavailable.")
    return warnings
