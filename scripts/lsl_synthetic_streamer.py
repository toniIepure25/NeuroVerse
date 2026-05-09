"""Stream deterministic synthetic EEG-like samples over Lab Streaming Layer."""

from __future__ import annotations

import argparse
import math
import random
import sys
import time

INSTALL_HINT = 'pylsl is not installed. Install with: cd backend && pip install -e ".[hardware]"'
PHASES = [
    ("BASELINE", 0.00),
    ("FOCUS_RISE", 0.17),
    ("WORKLOAD", 0.34),
    ("RELAXATION", 0.50),
    ("IMAGERY", 0.67),
    ("NOISY", 0.84),
    ("RECOVERY", 0.94),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic NeuroVerse LSL EEG stream")
    parser.add_argument("--stream-name", default="NeuroVerseSyntheticEEG")
    parser.add_argument("--stream-type", default="EEG")
    parser.add_argument("--sampling-rate", type=float, default=250.0)
    parser.add_argument("--channels", type=int, default=8)
    parser.add_argument("--duration", type=float, default=180.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--phase-markers", action="store_true")
    parser.add_argument("--jitter-ms", type=float, default=0.0)
    parser.add_argument("--dropout-prob", type=float, default=0.0)
    parser.add_argument("--noise-phase", action="store_true")
    args = parser.parse_args()

    try:
        from pylsl import StreamInfo, StreamOutlet, local_clock
    except Exception:
        print(INSTALL_HINT, file=sys.stderr)
        raise SystemExit(2)

    rng = random.Random(args.seed)
    info = StreamInfo(
        args.stream_name,
        args.stream_type,
        args.channels,
        args.sampling_rate,
        "float32",
        f"neuroverse-{args.stream_name}",
    )
    channels = info.desc().append_child("channels")
    for i in range(args.channels):
        ch = channels.append_child("channel")
        ch.append_child_value("label", f"EEG{i + 1}")
        ch.append_child_value("unit", "microvolts")
        ch.append_child_value("type", "EEG")
    outlet = StreamOutlet(info)
    marker_outlet = None
    if args.phase_markers:
        marker_info = StreamInfo(
            f"{args.stream_name}Markers",
            "Markers",
            1,
            0,
            "string",
            f"neuroverse-{args.stream_name}-markers",
        )
        marker_outlet = StreamOutlet(marker_info)

    print(
        "\n".join([
            "Starting simulated NeuroVerse LSL stream",
            f"- stream: {args.stream_name}",
            f"- type: {args.stream_type}",
            f"- channels: {args.channels}",
            f"- sampling_rate_hz: {args.sampling_rate}",
            f"- duration_seconds: {args.duration}",
            f"- markers_enabled: {bool(marker_outlet)}",
            "- scientific_note: simulated LSL biosignal stream, not real EEG",
        ]),
        flush=True,
    )
    start = local_clock()
    sample_idx = 0
    next_phase = 0
    try:
        while local_clock() - start < args.duration:
            elapsed = local_clock() - start
            phase = _phase_for(elapsed / max(args.duration, 1e-6))
            if (
                marker_outlet
                and next_phase < len(PHASES)
                and elapsed / args.duration >= PHASES[next_phase][1]
            ):
                marker_outlet.push_sample([PHASES[next_phase][0]])
                next_phase += 1
            if rng.random() >= args.dropout_prob:
                outlet.push_sample(
                    _sample(
                        sample_idx,
                        args.channels,
                        args.sampling_rate,
                        phase,
                        rng,
                        args.noise_phase,
                    )
                )
            sample_idx += 1
            target_sleep = 1.0 / args.sampling_rate
            jitter = rng.uniform(-args.jitter_ms, args.jitter_ms) / 1000.0 if args.jitter_ms else 0.0
            time.sleep(max(0.0, target_sleep + jitter))
    except KeyboardInterrupt:
        print("Synthetic LSL stream interrupted; shutting down cleanly.", flush=True)
    finally:
        if marker_outlet:
            marker_outlet.push_sample(["END"])
        print("Synthetic LSL stream complete", flush=True)


def _phase_for(frac: float) -> str:
    current = PHASES[0][0]
    for label, edge in PHASES:
        if frac >= edge:
            current = label
    return current


def _sample(
    sample_idx: int,
    channels: int,
    rate: float,
    phase: str,
    rng: random.Random,
    noise_phase: bool,
) -> list[float]:
    t = sample_idx / rate
    alpha, beta, theta, noise = 9.0, 18.0, 6.0, 0.15
    if phase == "FOCUS_RISE":
        beta, alpha = 22.0, 7.0
    elif phase == "WORKLOAD":
        theta, beta, noise = 6.5, 20.0, 0.25
    elif phase == "RELAXATION":
        alpha, beta, noise = 10.5, 14.0, 0.08
    elif phase == "IMAGERY":
        alpha, beta = 8.5, 16.5
    elif phase == "NOISY" or noise_phase:
        noise = 2.5
    elif phase == "RECOVERY":
        alpha, beta = 9.5, 15.0

    values = []
    for ch in range(channels):
        phase_shift = ch * 0.13
        value = (
            12.0 * math.sin(2 * math.pi * alpha * t + phase_shift)
            + 6.0 * math.sin(2 * math.pi * beta * t)
            + 4.0 * math.sin(2 * math.pi * theta * t + phase_shift / 2)
            + rng.gauss(0.0, noise)
        )
        values.append(float(value))
    return values


if __name__ == "__main__":
    main()
