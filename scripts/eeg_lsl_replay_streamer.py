"""Replay MNE-compatible EEG data over LSL with event markers."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.acquisition.eeg_fixture import FIXTURE_MARKERS, create_eeg_fixture_raw, load_mne_raw  # noqa: E402

INSTALL_HINT = 'pylsl/mne unavailable. Install with: cd backend && pip install -e ".[hardware]"'


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay EEG over LSL for NeuroVerse validation")
    parser.add_argument("--input-file", default=None)
    parser.add_argument("--fixture-mode", action="store_true", default=False)
    parser.add_argument("--stream-name", default="NeuroVerseReplayEEG")
    parser.add_argument("--stream-type", default="EEG")
    parser.add_argument("--marker-stream-name", default="NeuroVerseReplayMarkers")
    parser.add_argument("--marker-stream-type", default="Markers")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--start-offset", type=float, default=0.0)
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--pick-eeg-only", action="store_true", default=True)
    parser.add_argument("--max-channels", type=int, default=None)
    parser.add_argument("--resample", type=float, default=None)
    parser.add_argument("--event-map-json", default=None)
    parser.add_argument("--markers", action="store_true", default=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    try:
        import numpy as np
        from pylsl import StreamInfo, StreamOutlet, local_clock
    except Exception:
        print(INSTALL_HINT, file=sys.stderr)
        raise SystemExit(2)

    try:
        raw = create_eeg_fixture_raw(args.duration + args.start_offset, args.seed) if args.fixture_mode else load_mne_raw(args.input_file)
    except Exception as exc:
        print(f"{INSTALL_HINT}\nEEG file load failed: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    if args.pick_eeg_only:
        raw.pick_types(eeg=True, exclude=[])
    if args.max_channels:
        raw.pick(raw.ch_names[: args.max_channels])
    if args.resample:
        raw.load_data()
        raw.resample(args.resample, verbose=False)
    raw.load_data()
    sfreq = float(raw.info["sfreq"])
    start_sample = int(max(args.start_offset, 0.0) * sfreq)
    end_sample = min(raw.n_times, start_sample + int(round(args.duration * sfreq)))
    data = raw.get_data(start=start_sample, stop=end_sample) * 1_000_000.0
    channel_names = list(raw.ch_names)
    event_map = _load_event_map(args.event_map_json)
    annotations = _annotation_events(raw, args.start_offset, args.duration, event_map)

    info = StreamInfo(
        args.stream_name,
        args.stream_type,
        len(channel_names),
        sfreq,
        "float32",
        f"neuroverse-replay-{args.stream_name}",
    )
    channels = info.desc().append_child("channels")
    for name in channel_names:
        ch = channels.append_child("channel")
        ch.append_child_value("label", name)
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")
    outlet = StreamOutlet(info)

    marker_outlet = None
    if args.markers:
        marker_info = StreamInfo(
            args.marker_stream_name,
            args.marker_stream_type,
            1,
            0,
            "string",
            f"neuroverse-replay-{args.marker_stream_name}",
        )
        marker_outlet = StreamOutlet(marker_info)

    print(
        "\n".join([
            "Starting NeuroVerse EEG replay LSL stream",
            f"- source: {'fixture' if args.fixture_mode else args.input_file}",
            f"- stream: {args.stream_name}",
            f"- marker_stream: {args.marker_stream_name if marker_outlet else 'disabled'}",
            f"- channels: {len(channel_names)}",
            f"- sampling_rate_hz: {sfreq}",
            f"- duration_seconds: {args.duration}",
            f"- start_offset_seconds: {args.start_offset}",
            f"- marker_count: {len(annotations)}",
            "- scientific_note: EEG replay validation, not clinical interpretation",
        ]),
        flush=True,
    )

    sample_idx = 0
    marker_idx = 0
    max_samples = min(data.shape[1], int(round(args.duration * sfreq)))
    start = local_clock()
    try:
        while sample_idx < max_samples or args.loop:
            elapsed = (local_clock() - start) * max(args.speed, 1e-6)
            target_idx = min(max_samples, int(elapsed * sfreq))
            while sample_idx < target_idx:
                outlet.push_sample(data[:, sample_idx].astype(float).tolist())
                sample_idx += 1
            while marker_outlet and marker_idx < len(annotations) and elapsed >= annotations[marker_idx][1]:
                marker_outlet.push_sample([annotations[marker_idx][0]])
                marker_idx += 1
            if sample_idx >= max_samples and args.loop:
                sample_idx = 0
                marker_idx = 0
                start = local_clock()
            if sample_idx >= max_samples:
                break
            time.sleep(0.002)
    except KeyboardInterrupt:
        print("EEG replay stream interrupted; shutting down cleanly.", flush=True)
    finally:
        if marker_outlet:
            marker_outlet.push_sample(["END"])
        print("EEG replay LSL stream complete", flush=True)


def _annotation_events(
    raw: object,
    start_offset: float,
    duration: float,
    event_map: dict[str, str],
) -> list[tuple[str, float]]:
    events = [
        (event_map.get(str(desc), str(desc)), float(onset) - start_offset)
        for onset, desc in zip(raw.annotations.onset, raw.annotations.description, strict=False)
        if start_offset <= float(onset) <= start_offset + duration
    ]
    if not events:
        return [item for item in FIXTURE_MARKERS if item[1] <= duration]
    if events[-1][0] != "END":
        events.append(("END", min(duration, max(duration - 0.1, 0.0))))
    return events


def _load_event_map(path: str | None) -> dict[str, str]:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {str(key): str(value) for key, value in data.items()}


if __name__ == "__main__":
    main()
