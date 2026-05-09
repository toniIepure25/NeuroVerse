"""Prepare event-locked EEG epoch features from a local file or fixture."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.event_epochs import prepare_event_feature_dataset  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare event-locked EEG features")
    parser.add_argument("--input-file", default=None)
    parser.add_argument("--dataset-config", default=None)
    parser.add_argument("--fixture-mode", action="store_true", default=False)
    parser.add_argument("--output", required=True)
    parser.add_argument("--tmin", type=float, default=0.0)
    parser.add_argument("--tmax", type=float, default=1.5)
    parser.add_argument("--event-labels", default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--pick-eeg-only", action="store_true", default=True)
    parser.add_argument("--max-channels", type=int, default=None)
    parser.add_argument("--pick-channels", default=None)
    parser.add_argument("--bandpass-low", type=float, default=None)
    parser.add_argument("--bandpass-high", type=float, default=None)
    parser.add_argument("--notch-freq", type=float, default=None)
    parser.add_argument("--baseline-correction", action="store_true", default=False)
    parser.add_argument("--reject-amplitude-uv", type=float, default=None)
    parser.add_argument("--feature-set", default="combined")
    args = parser.parse_args()
    labels = [item.strip() for item in args.event_labels.split(",")] if args.event_labels else None
    channels = [item.strip() for item in args.pick_channels.split(",")] if args.pick_channels else None
    summary = prepare_event_feature_dataset(
        input_file=args.input_file,
        dataset_config=_resolve(args.dataset_config) if args.dataset_config else None,
        fixture_mode=args.fixture_mode,
        output_path=_resolve(args.output),
        tmin=args.tmin,
        tmax=args.tmax,
        event_labels=labels,
        seed=args.seed,
        pick_eeg_only=args.pick_eeg_only,
        max_channels=args.max_channels,
        pick_channels=channels,
        bandpass_low=args.bandpass_low,
        bandpass_high=args.bandpass_high,
        notch_freq=args.notch_freq,
        baseline_correction=args.baseline_correction,
        reject_amplitude_uv=args.reject_amplitude_uv,
        feature_set=args.feature_set,
    )
    print(json.dumps(summary, indent=2))


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
