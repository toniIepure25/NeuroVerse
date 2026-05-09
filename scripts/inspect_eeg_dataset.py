"""Inspect a local EEG dataset config without moving data into Git."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.event_epochs import inspect_eeg_dataset_config  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect an EEG dataset config")
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument(
        "--output",
        default="reports/public_eeg_inspection/physionet_eegbci_inspection.json",
    )
    args = parser.parse_args()
    report = inspect_eeg_dataset_config(_resolve(args.dataset_config))
    output = _resolve(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md = output.with_suffix(".md")
    md.write_text(_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Dataset inspection written to {output}")


def _markdown(report: dict[str, object]) -> str:
    return "\n".join([
        f"# EEG Dataset Inspection: {report.get('dataset_id')}",
        "",
        f"- files configured: `{report.get('file_count')}`",
        f"- files inspected: `{report.get('inspected_file_count')}`",
        f"- subjects: `{', '.join(report.get('subjects') or [])}`",
        f"- runs: `{', '.join(report.get('runs') or [])}`",
        f"- annotation labels: `{report.get('annotation_label_distribution')}`",
        f"- warnings: `{len(report.get('warnings') or [])}`",
        "",
        "Dataset inspection reports file metadata and annotations; it is not clinical review.",
    ])


def _resolve(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
