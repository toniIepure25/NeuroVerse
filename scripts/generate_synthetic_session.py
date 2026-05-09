"""Generate a synthetic biosignal session CSV for testing and demos."""
from __future__ import annotations

import argparse
import asyncio
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

import numpy as np

from app.acquisition.simulator import BiosignalSimulator


async def generate(duration_s: int, output: str) -> None:
    sim = BiosignalSimulator(
        duration_s=duration_s,
        tick_interval_ms=500,
        rng=np.random.default_rng(42),
    )
    await sim.start()

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    tick = 0
    while True:
        try:
            window = await sim.get_window()
        except RuntimeError:
            break
        t = tick * 0.5
        if t >= duration_s:
            break
        n_samples = len(window.data[0]) if window.data else 0
        for s in range(n_samples):
            row = {"time_s": round(t + s / window.sampling_rate, 4)}
            for ch_idx, ch_name in enumerate(window.channel_names):
                row[ch_name] = round(window.data[ch_idx][s], 6)
            row["sqi_hint"] = window.signal_quality_hint
            rows.append(row)
        tick += 1

    await sim.stop()

    if rows:
        fieldnames = list(rows[0].keys())
        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {len(rows)} samples to {out_path}")
    else:
        print("No data generated")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic NeuroVerse session")
    parser.add_argument("--duration", type=int, default=180, help="Session duration in seconds")
    parser.add_argument("--output", type=str, default="data/simulated/sample_session.csv")
    args = parser.parse_args()
    asyncio.run(generate(args.duration, args.output))


if __name__ == "__main__":
    main()
