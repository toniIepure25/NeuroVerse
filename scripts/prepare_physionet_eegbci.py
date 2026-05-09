"""Prepare a local-first PhysioNet EEGBCI config.

No dataset files are downloaded unless --download is passed explicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.event_label_mapping import PHYSIONET_EEGBCI_RUN_CONTEXTS  # noqa: E402

CITATION_NOTE = (
    "PhysioNet EEG Motor Movement/Imagery data should be cited according to "
    "PhysioNet/EEGBCI instructions. NeuroVerse stores local configs only."
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare PhysioNet EEGBCI local config")
    parser.add_argument("--info", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--local-root", default="data/external/eegbci")
    parser.add_argument("--subjects", nargs="*", type=int, default=[1])
    parser.add_argument("--runs", nargs="*", type=int, default=[4, 8, 12])
    parser.add_argument("--output-config", default="configs/datasets/physionet_eegbci_local.yaml")
    args = parser.parse_args()
    if args.info:
        print(json.dumps(_info(), indent=2))
        return
    local_root = _resolve(args.local_root)
    if args.download:
        _download(args.subjects, args.runs, local_root)
    config = _build_config(local_root, args.local_root, args.subjects, args.runs)
    output = _resolve(args.output_config)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    print(json.dumps({
        "output_config": str(output),
        "file_count": len(config["files"]),
        "missing_file_count": sum(1 for item in config["files"] if not item["exists"]),
        "citation_note": CITATION_NOTE,
    }, indent=2))


def _info() -> dict[str, object]:
    return {
        "dataset": "PhysioNet EEG Motor Movement/Imagery (EEGBCI)",
        "local_first": True,
        "download_policy": "No download occurs unless --download is explicitly supplied.",
        "typical_motor_imagery_runs": {
            "left_vs_right_imagery": [4, 8, 12],
            "hands_vs_feet_imagery": [6, 10, 14],
        },
        "run_contexts": PHYSIONET_EEGBCI_RUN_CONTEXTS,
        "citation_note": CITATION_NOTE,
    }


def _download(subjects: list[int], runs: list[int], local_root: Path) -> None:
    os.environ.setdefault("NUMBA_DISABLE_JIT", "1")
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-neuroverse")
    try:
        from mne.datasets import eegbci
    except Exception as exc:
        print(
            f"MNE EEGBCI helper unavailable ({exc}); falling back to direct PhysioNet URLs.",
            file=sys.stderr,
        )
        _direct_download(subjects, runs, local_root)
        return
    try:
        eegbci.load_data(subjects, runs, path=str(local_root), update_path=False)
    except Exception as exc:
        print(
            f"MNE EEGBCI download failed ({exc}); falling back to direct PhysioNet URLs.",
            file=sys.stderr,
        )
        _direct_download(subjects, runs, local_root)


def _direct_download(subjects: list[int], runs: list[int], local_root: Path) -> None:
    base = "https://physionet.org/files/eegmmidb/1.0.0"
    local_root.mkdir(parents=True, exist_ok=True)
    for subject in subjects:
        subject_dir = local_root / f"S{subject:03d}"
        subject_dir.mkdir(parents=True, exist_ok=True)
        for run in runs:
            name = f"S{subject:03d}R{run:02d}.edf"
            target = subject_dir / name
            if target.exists() and target.stat().st_size > 0:
                continue
            url = f"{base}/S{subject:03d}/{name}"
            try:
                print(f"Downloading {url} -> {target}", file=sys.stderr)
                urllib.request.urlretrieve(url, target)
            except Exception as exc:
                if target.exists() and target.stat().st_size == 0:
                    target.unlink()
                raise SystemExit(
                    f"Explicit PhysioNet download failed for {url}: {exc}\n"
                    "Check internet access or place EDF files manually under data/external/eegbci."
                ) from exc


def _build_config(
    local_root: Path,
    local_root_config: str,
    subjects: list[int],
    runs: list[int],
) -> dict[str, object]:
    files = []
    for subject in subjects:
        for run in runs:
            expected = f"S{subject:03d}R{run:02d}.edf"
            matches = sorted(local_root.rglob(expected))
            path = matches[0] if matches else local_root / f"S{subject:03d}" / expected
            files.append({
                "subject_id": f"S{subject:03d}",
                "run_id": run,
                "task_context": PHYSIONET_EEGBCI_RUN_CONTEXTS.get(run, "unknown"),
                "path": (
                    str(path.relative_to(local_root))
                    if path.is_relative_to(local_root)
                    else str(path)
                ),
                "exists": path.exists(),
            })
    return {
        "dataset_id": "physionet_eegbci_local",
        "dataset_name": "PhysioNet EEG Motor Movement/Imagery local files",
        "source": "physionet_eegbci",
        "local_root": local_root_config,
        "subjects": [f"S{subject:03d}" for subject in subjects],
        "runs": runs,
        "task_type": "event_locked_motor_task_classification",
        "event_mapping": {
            "T0": "REST"
        },
        "run_contexts": PHYSIONET_EEGBCI_RUN_CONTEXTS,
        "files": files,
        "notes": [
            CITATION_NOTE,
            "T1/T2 labels are normalized by run context during feature extraction.",
            "Closed-loop adaptation remains disabled by default.",
        ],
    }


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
