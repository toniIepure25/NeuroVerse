"""Run live LSL raw-epoch BCI shadow inference with safe fallback."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))
os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-neuroverse")
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/numba-neuroverse")

from app.ml.event_epochs import preprocess_epoch  # noqa: E402
from app.ml.event_label_mapping import normalize_event_label  # noqa: E402
from app.ml.metrics import evaluate_classification  # noqa: E402

INSTALL_HINT = 'pylsl/mne unavailable. Install with: cd backend && pip install -e ".[hardware]"'
TARGET_LABELS = {"LEFT_HAND_IMAGERY", "RIGHT_HAND_IMAGERY"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run live/fallback raw BCI shadow inference")
    parser.add_argument("--best-model", required=True)
    parser.add_argument("--epochs", required=True, help="Raw epoch NPZ used for metadata/fallback.")
    parser.add_argument("--input-file", default=None, help="Representative EDF. Defaults to first metadata source_path.")
    parser.add_argument("--output-dir", default="reports/raw_bci_shadow")
    parser.add_argument("--mode", choices=["auto", "live_lsl", "fallback_offline"], default="auto")
    parser.add_argument("--stream-name", default="NeuroVerseRawShadowEEG")
    parser.add_argument("--marker-stream-name", default="NeuroVerseRawShadowMarkers")
    parser.add_argument("--duration", type=float, default=45.0)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--startup-timeout", type=float, default=8.0)
    parser.add_argument("--epoch-timeout", type=float, default=4.0)
    args = parser.parse_args()
    result = run_shadow_suite(
        best_model=_resolve(args.best_model),
        epochs=_resolve(args.epochs),
        input_file=_resolve(args.input_file) if args.input_file else None,
        output_dir=_resolve(args.output_dir),
        mode=args.mode,
        stream_name=args.stream_name,
        marker_stream_name=args.marker_stream_name,
        duration=args.duration,
        speed=args.speed,
        limit=args.limit,
        startup_timeout=args.startup_timeout,
        epoch_timeout=args.epoch_timeout,
    )
    print(json.dumps(result, indent=2, default=str))


def run_shadow_suite(
    *,
    best_model: Path,
    epochs: Path,
    input_file: Path | None,
    output_dir: Path,
    mode: str,
    stream_name: str,
    marker_stream_name: str,
    duration: float,
    speed: float,
    limit: int,
    startup_timeout: float,
    epoch_timeout: float,
) -> dict[str, object]:
    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_raw_bci_shadow"
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    if mode in {"auto", "live_lsl"}:
        try:
            report = _run_live_lsl_shadow(
                run_id=run_id,
                run_dir=run_dir,
                best_model=best_model,
                epochs=epochs,
                input_file=input_file,
                stream_name=stream_name,
                marker_stream_name=marker_stream_name,
                duration=duration,
                speed=speed,
                limit=limit,
                startup_timeout=startup_timeout,
                epoch_timeout=epoch_timeout,
            )
            _write_report_files(run_dir, report)
            return report
        except Exception as exc:
            if mode == "live_lsl":
                failure = {
                    "run_id": run_id,
                    "mode": "live_lsl",
                    "status": "failed",
                    "error": str(exc),
                    "closed_loop_allowed": False,
                    "real_adaptation_actions_emitted": 0,
                }
                _write_report_files(run_dir, failure)
                return failure
            fallback_reason = f"Live LSL raw shadow failed; fallback used. Reason: {exc}"
    else:
        fallback_reason = "Fallback mode requested explicitly."

    report = _run_fallback_shadow(
        run_id=run_id,
        run_dir=run_dir,
        best_model=best_model,
        epochs=epochs,
        limit=limit,
        fallback_reason=fallback_reason,
    )
    _write_report_files(run_dir, report)
    return report


def _run_live_lsl_shadow(
    *,
    run_id: str,
    run_dir: Path,
    best_model: Path,
    epochs: Path,
    input_file: Path | None,
    stream_name: str,
    marker_stream_name: str,
    duration: float,
    speed: float,
    limit: int,
    startup_timeout: float,
    epoch_timeout: float,
) -> dict[str, object]:
    try:
        from pylsl import StreamInlet, resolve_byprop
    except Exception as exc:
        raise RuntimeError(INSTALL_HINT) from exc

    source_file = input_file or _first_source_path(epochs)
    if source_file is None or not source_file.exists():
        raise FileNotFoundError("No representative EDF file found for live LSL shadow.")

    best = json.loads(best_model.read_text(encoding="utf-8"))
    model = _load_model(best)
    epoch_cfg = _epoch_config(epochs)
    run_id_from_file = _run_id_from_file(source_file)

    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "eeg_lsl_replay_streamer.py"),
        "--input-file",
        str(source_file),
        "--stream-name",
        stream_name,
        "--marker-stream-name",
        marker_stream_name,
        "--duration",
        str(duration),
        "--speed",
        str(speed),
        "--markers",
    ]
    env = os.environ.copy()
    env.setdefault("NUMBA_DISABLE_JIT", "1")
    env.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-neuroverse")
    env.setdefault("NUMBA_CACHE_DIR", "/tmp/numba-neuroverse")
    process = subprocess.Popen(
        cmd,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        eeg_info = _resolve_stream(resolve_byprop, "name", stream_name, startup_timeout)
        marker_info = _resolve_stream(resolve_byprop, "name", marker_stream_name, startup_timeout)
        eeg_inlet = StreamInlet(eeg_info, max_buflen=max(60, int(duration + 10)))
        marker_inlet = StreamInlet(marker_info, max_buflen=max(60, int(duration + 10)))
        sampling_rate = float(eeg_info.nominal_srate() or epoch_cfg["sampling_rate"])
        expected_samples = int(round((epoch_cfg["tmax"] - epoch_cfg["tmin"]) * epoch_cfg["sampling_rate"]))
        expected_channels = int(epoch_cfg["channel_count"])

        samples: list[list[float]] = []
        timestamps: list[float] = []
        pending: list[dict[str, Any]] = []
        predictions: list[dict[str, Any]] = []
        missed: list[dict[str, Any]] = []
        markers_seen: list[dict[str, Any]] = []
        start = time.monotonic()
        last_sample_timestamp: float | None = None

        while time.monotonic() - start < duration + epoch_cfg["tmax"] + epoch_timeout:
            chunk, ts = eeg_inlet.pull_chunk(timeout=0.02, max_samples=128)
            if chunk and ts:
                samples.extend([[float(value) for value in row] for row in chunk])
                timestamps.extend(float(item) for item in ts)
                last_sample_timestamp = float(ts[-1])
                cutoff = last_sample_timestamp - max(duration + 5.0, 30.0)
                while timestamps and timestamps[0] < cutoff:
                    timestamps.pop(0)
                    samples.pop(0)

            marker_chunk, marker_ts = marker_inlet.pull_chunk(timeout=0.01, max_samples=64)
            for marker_sample, marker_time in zip(marker_chunk or [], marker_ts or [], strict=False):
                original = str(marker_sample[0] if isinstance(marker_sample, list) else marker_sample)
                mapped = normalize_event_label(original, run_id=run_id_from_file)
                normalized = str(mapped["event_label"])
                event = {
                    "original_label": original,
                    "marker_label": normalized,
                    "timestamp": float(marker_time),
                    "task_context": mapped["task_context"],
                }
                markers_seen.append(event)
                if normalized in TARGET_LABELS and len(predictions) < limit:
                    pending.append(event)

            still_pending: list[dict[str, Any]] = []
            for event in pending:
                ready_time = event["timestamp"] + epoch_cfg["tmax"]
                if last_sample_timestamp is None or last_sample_timestamp < ready_time:
                    if time.monotonic() - start > duration + epoch_timeout:
                        missed.append({**event, "reason": "insufficient_post_marker_samples"})
                    else:
                        still_pending.append(event)
                    continue
                epoch, reason = epoch_from_buffer(
                    samples,
                    timestamps,
                    marker_timestamp=float(event["timestamp"]),
                    tmin=float(epoch_cfg["tmin"]),
                    tmax=float(epoch_cfg["tmax"]),
                    expected_samples=expected_samples,
                    expected_channels=expected_channels,
                )
                if epoch is None:
                    missed.append({**event, "reason": reason})
                    continue
                epoch = preprocess_epoch(
                    epoch,
                    float(epoch_cfg["sampling_rate"]),
                    bandpass_low=epoch_cfg["bandpass_low"],
                    bandpass_high=epoch_cfg["bandpass_high"],
                    notch_freq=epoch_cfg["notch_freq"],
                    baseline_correction=bool(epoch_cfg["baseline_correction"]),
                )
                pred = model.predict(epoch[np.newaxis, :, :])[0]
                proba = model.predict_proba(epoch[np.newaxis, :, :]) if hasattr(model, "predict_proba") else None
                confidence = float(np.max(proba)) if proba is not None else None
                predictions.append({
                    "index": len(predictions),
                    "marker_label": event["marker_label"],
                    "original_label": event["original_label"],
                    "predicted_label": str(pred),
                    "confidence": confidence,
                    "marker_timestamp": event["timestamp"],
                    "epoch_start": event["timestamp"] + epoch_cfg["tmin"],
                    "epoch_end": event["timestamp"] + epoch_cfg["tmax"],
                })
                if len(predictions) >= limit:
                    still_pending = []
                    break
            pending = still_pending
            if len(predictions) >= limit:
                break
            if process.poll() is not None and not pending:
                break

        for event in pending:
            missed.append({**event, "reason": "stream_ended_before_epoch_complete"})

        y_true = [row["marker_label"] for row in predictions]
        y_pred = [row["predicted_label"] for row in predictions]
        labels = sorted(set(y_true) | set(y_pred))
        metrics = evaluate_classification(y_true, y_pred, None, labels) if predictions else {}
        timing = _timing_summary(timestamps, sampling_rate)
        report = {
            "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "mode": "live_lsl",
            "status": "completed",
            "live_lsl_stream_used": True,
            "model_id": best.get("model_id"),
            "model": best.get("model"),
            "model_type": best.get("model"),
            "n_components": best.get("n_components"),
            "source_edf": str(source_file),
            "stream_name": stream_name,
            "marker_stream_name": marker_stream_name,
            "markers_seen": len(markers_seen),
            "target_markers_seen": len([item for item in markers_seen if item["marker_label"] in TARGET_LABELS]),
            "epochs_built": len(predictions),
            "prediction_count": len(predictions),
            "predictions": predictions,
            "missed_epochs": len(missed),
            "missed_epoch_reasons": _reason_counts(missed),
            "missed_epoch_examples": missed[:20],
            "metrics": metrics,
            "timing_summary": timing,
            "real_adaptation_actions_emitted": 0,
            "closed_loop_allowed": False,
            "scientific_note": (
                "Live raw BCI shadow predicts controlled event labels from replayed public EEG "
                "markers. It emits no Dream Corridor adaptation actions."
            ),
        }
        _write_predictions(run_dir / "predictions.csv", predictions)
        (run_dir / "marker_alignment.json").write_text(
            json.dumps({
                "mode": "live_lsl",
                "markers_seen": len(markers_seen),
                "target_markers_seen": report["target_markers_seen"],
                "epochs_built": len(predictions),
                "missed_epochs": len(missed),
                "missed_epoch_reasons": report["missed_epoch_reasons"],
                "markers": markers_seen[:100],
            }, indent=2),
            encoding="utf-8",
        )
        (run_dir / "timing_summary.json").write_text(json.dumps(timing, indent=2), encoding="utf-8")
        return report
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()


def epoch_from_buffer(
    samples: list[list[float]] | np.ndarray,
    timestamps: list[float] | np.ndarray,
    *,
    marker_timestamp: float,
    tmin: float,
    tmax: float,
    expected_samples: int,
    expected_channels: int,
) -> tuple[np.ndarray | None, str | None]:
    ts = np.asarray(timestamps, dtype=float)
    x = np.asarray(samples, dtype=float)
    if ts.size == 0 or x.size == 0:
        return None, "empty_buffer"
    if x.ndim != 2:
        return None, "invalid_sample_shape"
    if x.shape[1] != expected_channels:
        return None, f"channel_count_mismatch:{x.shape[1]}!={expected_channels}"
    start = marker_timestamp + tmin
    end = marker_timestamp + tmax
    mask = (ts >= start) & (ts <= end)
    if int(mask.sum()) < max(4, expected_samples // 4):
        return None, "insufficient_samples_in_epoch_window"
    selected_ts = ts[mask]
    selected = x[mask].T
    if selected.shape[1] == expected_samples:
        return selected, None
    grid = np.linspace(start, end, expected_samples, endpoint=False)
    interpolated = np.vstack([
        np.interp(grid, selected_ts, selected[channel])
        for channel in range(selected.shape[0])
    ])
    return interpolated.astype(np.float32), None


def _run_fallback_shadow(
    *,
    run_id: str,
    run_dir: Path,
    best_model: Path,
    epochs: Path,
    limit: int,
    fallback_reason: str,
) -> dict[str, object]:
    report_path = run_dir / "live_shadow_summary.json"
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "run_best_raw_bci_shadow.py"),
        "--best-model",
        str(best_model),
        "--epochs",
        str(epochs),
        "--output",
        str(report_path),
        "--limit",
        str(limit),
    ]
    completed = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        return {
            "run_id": run_id,
            "mode": "fallback_offline",
            "status": "failed",
            "error": completed.stderr or completed.stdout,
            "closed_loop_allowed": False,
            "real_adaptation_actions_emitted": 0,
        }
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report.update({
        "run_id": run_id,
        "mode": "fallback_offline",
        "live_lsl_stream_used": False,
        "fallback_reason": fallback_reason,
        "closed_loop_allowed": False,
        "real_adaptation_actions_emitted": 0,
        "markers_seen": report.get("prediction_count", 0),
        "epochs_built": report.get("prediction_count", 0),
        "missed_epochs": 0,
        "missed_epoch_reasons": {},
    })
    _write_predictions(run_dir / "predictions.csv", report.get("predictions") or [])
    (run_dir / "marker_alignment.json").write_text(
        json.dumps({
            "mode": "fallback_offline",
            "marker_source": "saved_epoch_labels",
            "prediction_count": report.get("prediction_count"),
        }, indent=2),
        encoding="utf-8",
    )
    (run_dir / "timing_summary.json").write_text(
        json.dumps({
            "mode": "fallback_offline",
            "live_lsl_stream_used": False,
            "note": "No LSL timing measured in fallback mode.",
        }, indent=2),
        encoding="utf-8",
    )
    return report


def _write_report_files(run_dir: Path, report: dict[str, object]) -> None:
    (run_dir / "live_shadow_summary.json").write_text(
        json.dumps(report, indent=2, default=str),
        encoding="utf-8",
    )
    (run_dir / "live_shadow_summary.md").write_text(_markdown(report), encoding="utf-8")


def _write_predictions(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames = [
        "index",
        "marker_label",
        "original_label",
        "predicted_label",
        "confidence",
        "marker_timestamp",
        "epoch_start",
        "epoch_end",
        "subject_id",
        "run_id",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _markdown(report: dict[str, object]) -> str:
    metrics = report.get("metrics") or {}
    return "\n".join([
        "# Live Raw BCI Shadow Report",
        "",
        f"- Mode: {report.get('mode')}",
        f"- Status: {report.get('status', 'completed')}",
        f"- Model: {report.get('model_id')}",
        f"- Source EDF: {report.get('source_edf', '—')}",
        f"- Markers seen: {report.get('markers_seen')}",
        f"- Epochs built: {report.get('epochs_built')}",
        f"- Predictions: {report.get('prediction_count')}",
        f"- Missed epochs: {report.get('missed_epochs')}",
        f"- Balanced accuracy against markers: {metrics.get('balanced_accuracy')}",
        f"- Macro F1 against markers: {metrics.get('macro_f1')}",
        f"- Live LSL stream used: {report.get('live_lsl_stream_used')}",
        f"- Real adaptation actions emitted: {report.get('real_adaptation_actions_emitted')}",
        f"- Closed-loop allowed: {report.get('closed_loop_allowed')}",
        "",
        str(report.get("fallback_reason", "")),
        "",
        "Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models.",
    ])


def _resolve_stream(resolve_byprop: Any, prop: str, value: str, timeout: float) -> Any:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        streams = resolve_byprop(prop, value, timeout=0.5)
        if streams:
            return streams[0]
    raise TimeoutError(f"Timed out waiting for LSL stream {prop}={value!r}.")


def _load_model(best: dict[str, Any]) -> Any:
    model_dir = Path(str(best.get("model_dir", "")))
    if not model_dir.is_absolute():
        model_dir = ROOT / model_dir
    return joblib.load(model_dir / "model.joblib")


def _first_source_path(epochs: Path) -> Path | None:
    metadata_path = epochs.with_name(f"{epochs.stem}_metadata.json")
    if not metadata_path.exists():
        return None
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for row in metadata.get("rows", []):
        source = row.get("source_path")
        if source:
            return Path(str(source))
    return None


def _epoch_config(epochs: Path) -> dict[str, Any]:
    with np.load(epochs, allow_pickle=True) as npz:
        sampling_rate = float(npz["sampling_rate"])
        tmin = float(npz["tmin"])
        tmax = float(npz["tmax"])
        channel_count = int(len(npz["channel_names"]))
    cfg = {
        "sampling_rate": sampling_rate,
        "tmin": tmin,
        "tmax": tmax,
        "channel_count": channel_count,
        "bandpass_low": 7.0,
        "bandpass_high": 35.0,
        "notch_freq": None,
        "baseline_correction": False,
    }
    metadata_path = epochs.with_name(f"{epochs.stem}_metadata.json")
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        preprocessing = metadata.get("preprocessing") or {}
        cfg.update({
            "bandpass_low": preprocessing.get("bandpass_low"),
            "bandpass_high": preprocessing.get("bandpass_high"),
            "notch_freq": preprocessing.get("notch_freq"),
            "baseline_correction": preprocessing.get("baseline_correction", False),
        })
    return cfg


def _run_id_from_file(path: Path) -> str | None:
    match = re.search(r"R(\d{2})", path.name)
    return str(int(match.group(1))) if match else None


def _timing_summary(timestamps: list[float], nominal_rate: float) -> dict[str, object]:
    if len(timestamps) < 2:
        return {"sample_count": len(timestamps), "observed_srate": None, "nominal_srate": nominal_rate}
    ts = np.asarray(timestamps, dtype=float)
    duration = float(ts[-1] - ts[0])
    observed = float((len(ts) - 1) / duration) if duration > 0 else None
    return {
        "sample_count": len(timestamps),
        "first_timestamp": float(ts[0]),
        "last_timestamp": float(ts[-1]),
        "duration_seconds": duration,
        "nominal_srate": nominal_rate,
        "observed_srate": observed,
    }


def _reason_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        reason = str(row.get("reason") or "unknown")
        counts[reason] = counts.get(reason, 0) + 1
    return dict(sorted(counts.items()))


def _resolve(path: str) -> Path:
    item = Path(path)
    return item if item.is_absolute() else ROOT / item


if __name__ == "__main__":
    main()
