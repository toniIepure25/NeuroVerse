"""Export event-locked raw EEG epochs for CSP-style BCI benchmarks."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.acquisition.eeg_fixture import load_mne_raw  # noqa: E402
from app.ml.event_epochs import _file_items, _load_dataset_config, preprocess_epoch  # noqa: E402
from app.ml.event_label_mapping import normalize_event_label  # noqa: E402

DEFAULT_LABELS = ["LEFT_HAND_IMAGERY", "RIGHT_HAND_IMAGERY"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare raw epoch EEG tensor dataset")
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument("--subjects", nargs="*", default=None)
    parser.add_argument("--runs", nargs="*", default=None)
    parser.add_argument("--labels", nargs="*", default=DEFAULT_LABELS)
    parser.add_argument("--exclude-rest", action="store_true", default=False)
    parser.add_argument("--tmin", type=float, default=0.5)
    parser.add_argument("--tmax", type=float, default=2.5)
    parser.add_argument("--bandpass-low", type=float, default=7.0)
    parser.add_argument("--bandpass-high", type=float, default=35.0)
    parser.add_argument("--notch-freq", type=float, default=None)
    parser.add_argument("--baseline-correction", action="store_true", default=False)
    parser.add_argument("--reject-amplitude-uv", type=float, default=None)
    parser.add_argument("--pick-eeg-only", action="store_true", default=True)
    parser.add_argument("--max-channels", type=int, default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    summary = prepare_raw_epoch_dataset(
        dataset_config=_resolve(args.dataset_config),
        output_path=_resolve(args.output),
        subjects=args.subjects,
        runs=args.runs,
        labels=args.labels,
        exclude_rest=args.exclude_rest,
        tmin=args.tmin,
        tmax=args.tmax,
        bandpass_low=args.bandpass_low,
        bandpass_high=args.bandpass_high,
        notch_freq=args.notch_freq,
        baseline_correction=args.baseline_correction,
        reject_amplitude_uv=args.reject_amplitude_uv,
        pick_eeg_only=args.pick_eeg_only,
        max_channels=args.max_channels,
    )
    print(json.dumps(summary, indent=2, default=str))


def prepare_raw_epoch_dataset(
    *,
    dataset_config: Path,
    output_path: Path,
    subjects: list[str] | None = None,
    runs: list[str] | None = None,
    labels: list[str] | None = None,
    exclude_rest: bool = False,
    tmin: float = 0.5,
    tmax: float = 2.5,
    bandpass_low: float | None = 7.0,
    bandpass_high: float | None = 35.0,
    notch_freq: float | None = None,
    baseline_correction: bool = False,
    reject_amplitude_uv: float | None = None,
    pick_eeg_only: bool = True,
    max_channels: int | None = None,
) -> dict[str, Any]:
    cfg = _load_dataset_config(dataset_config)
    wanted_subjects = {_subject_key(value) for value in subjects or []}
    wanted_runs = {str(value) for value in runs or []}
    wanted_labels = set(labels or [])
    if exclude_rest:
        wanted_labels.discard("REST")
    file_items = _file_items(cfg, dataset_config.parent)
    epochs: list[np.ndarray] = []
    y: list[str] = []
    rows: list[dict[str, Any]] = []
    channel_names: list[str] = []
    sampling_rates: list[float] = []
    warnings: list[str] = []
    dropped = 0

    for item in file_items:
        subject_id = str(item.get("subject_id", ""))
        run_id = str(item.get("run_id", ""))
        if wanted_subjects and _subject_key(subject_id) not in wanted_subjects:
            continue
        if wanted_runs and run_id not in wanted_runs:
            continue
        path = Path(str(item["path"]))
        if not path.exists():
            warnings.append(f"Missing EEG file: {path}")
            continue
        raw = load_mne_raw(path)
        if pick_eeg_only:
            raw.pick_types(eeg=True, exclude=[])
        if max_channels:
            raw.pick(raw.ch_names[:max_channels])
        raw.load_data()
        sfreq = float(raw.info["sfreq"])
        local_channels = list(raw.ch_names)
        if channel_names and local_channels != channel_names:
            warnings.append(f"Channel names differ in {path.name}; skipped for tensor consistency.")
            continue
        channel_names = channel_names or local_channels
        sampling_rates.append(sfreq)
        for idx, (onset, label) in enumerate(
            zip(raw.annotations.onset, raw.annotations.description, strict=False)
        ):
            mapped = normalize_event_label(str(label), run_id=run_id)
            event_label = str(mapped["event_label"])
            if wanted_labels and event_label not in wanted_labels:
                continue
            if exclude_rest and event_label == "REST":
                continue
            start = int(round((float(onset) + tmin) * sfreq))
            end = int(round((float(onset) + tmax) * sfreq))
            if start < 0 or end <= start or end > raw.n_times:
                dropped += 1
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
            if reject_amplitude_uv is not None and peak_abs > reject_amplitude_uv:
                dropped += 1
                continue
            epochs.append(data.astype(np.float32))
            y.append(event_label)
            rows.append({
                "sample_id": f"{path.stem}_{idx}",
                "subject_id": subject_id,
                "run_id": run_id,
                "file_id": str(item.get("file_id") or path.name),
                "source_path": str(path),
                "original_label": str(label),
                "event_label": event_label,
                "task_context": mapped["task_context"],
                "event_onset_seconds": float(onset),
                "epoch_start_seconds": float(onset) + tmin,
                "epoch_end_seconds": float(onset) + tmax,
                "peak_abs_uv": peak_abs,
            })

    if not epochs:
        raise ValueError("No raw epochs generated from dataset config.")
    x = np.stack(epochs, axis=0)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path = output_path.with_name(f"{output_path.stem}_metadata.json")
    summary_path = output_path.with_name(f"{output_path.stem}_summary.md")
    np.savez_compressed(
        output_path,
        X=x,
        y=np.asarray(y),
        y_labels=np.asarray(sorted(set(y))),
        subject_ids=np.asarray([row["subject_id"] for row in rows]),
        run_ids=np.asarray([row["run_id"] for row in rows]),
        file_ids=np.asarray([row["file_id"] for row in rows]),
        original_labels=np.asarray([row["original_label"] for row in rows]),
        channel_names=np.asarray(channel_names),
        sampling_rate=np.asarray(float(np.median(sampling_rates))),
        tmin=np.asarray(tmin),
        tmax=np.asarray(tmax),
    )
    summary = {
        "output": str(output_path),
        "metadata": str(metadata_path),
        "epoch_count": int(x.shape[0]),
        "shape": list(x.shape),
        "labels": sorted(set(y)),
        "class_distribution": dict(Counter(y)),
        "subjects": sorted(set(row["subject_id"] for row in rows)),
        "runs": sorted(set(row["run_id"] for row in rows)),
        "channel_count": int(x.shape[1]),
        "channel_names": channel_names,
        "time_samples": int(x.shape[2]),
        "sampling_rate_hz": float(np.median(sampling_rates)),
        "epoch_window": {"tmin": tmin, "tmax": tmax},
        "preprocessing": {
            "bandpass_low": bandpass_low,
            "bandpass_high": bandpass_high,
            "notch_freq": notch_freq,
            "baseline_correction": baseline_correction,
            "reject_amplitude_uv": reject_amplitude_uv,
            "pick_eeg_only": pick_eeg_only,
            "max_channels": max_channels,
        },
        "dropped_epoch_count": dropped,
        "warnings": warnings + _warnings(y, rows),
        "closed_loop_allowed": False,
        "scientific_note": (
            "Raw epochs are for controlled task-label BCI benchmarking, not thought decoding."
        ),
    }
    metadata = {**summary, "rows": rows, "dataset_config": str(dataset_config)}
    metadata_path.write_text(json.dumps(metadata, indent=2, default=str), encoding="utf-8")
    summary_path.write_text(_markdown(summary), encoding="utf-8")
    return summary


def _warnings(y: list[str], rows: list[dict[str, Any]]) -> list[str]:
    warnings = []
    if len(set(y)) < 2:
        warnings.append("Fewer than two labels are present.")
    if len(set(row["subject_id"] for row in rows)) < 2:
        warnings.append("Fewer than two subjects; LOSO is unavailable.")
    if "REST" not in set(y):
        warnings.append("REST excluded; this is a binary motor imagery benchmark dataset.")
    return warnings


def _markdown(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Raw Epoch Dataset Summary",
        "",
        f"- Epochs: {summary['epoch_count']}",
        f"- Shape: {summary['shape']}",
        f"- Labels: {summary['class_distribution']}",
        f"- Subjects: {', '.join(summary['subjects'])}",
        f"- Runs: {', '.join(summary['runs'])}",
        f"- Channels: {summary['channel_count']}",
        f"- Window: {summary['epoch_window']['tmin']} to {summary['epoch_window']['tmax']} s",
        f"- Preprocessing: `{json.dumps(summary['preprocessing'])}`",
        f"- Dropped epochs: {summary['dropped_epoch_count']}",
        "",
        "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
        "Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.",
    ])


def _subject_key(value: str) -> str:
    value = str(value)
    return value if value.startswith("S") else f"S{int(value):03d}" if value.isdigit() else value


def _resolve(path: str) -> Path:
    item = Path(path)
    return item if item.is_absolute() else ROOT / item


if __name__ == "__main__":
    main()
