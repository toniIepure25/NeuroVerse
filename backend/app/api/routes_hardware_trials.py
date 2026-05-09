from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1/hardware-trials", tags=["hardware-trials"])
REPO_ROOT = Path(__file__).resolve().parents[3]
TRIAL_DIR = REPO_ROOT / "reports" / "hardware_trials"


@router.get("")
async def list_hardware_trials() -> list[dict[str, Any]]:
    return _trial_summaries()


@router.get("/latest")
async def latest_hardware_trial() -> dict[str, Any]:
    summaries = _trial_summaries()
    if not summaries:
        return {
            "report": None,
            "message": "No physical EEG hardware trial report found.",
            "next_commands": {
                "synthetic": "make physical-eeg-trial-synthetic",
                "discover": "make discover-brainflow-devices",
                "cyton": "make physical-eeg-trial-openbci-cyton PORT=/dev/ttyUSB0",
            },
        }
    return summaries[0]


@router.get("/{trial_id}")
async def get_hardware_trial(trial_id: str) -> dict[str, Any]:
    path = TRIAL_DIR / trial_id / "physical_eeg_trial_summary.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Hardware trial report not found")
    return {
        "trial_id": trial_id,
        "path": str(path),
        "report": json.loads(path.read_text(encoding="utf-8")),
    }


def _trial_summaries() -> list[dict[str, Any]]:
    if not TRIAL_DIR.exists():
        return []
    summaries: list[dict[str, Any]] = []
    for path in sorted(
        TRIAL_DIR.glob("*/physical_eeg_trial_summary.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    ):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        summaries.append({
            "trial_id": path.parent.name,
            "path": str(path),
            "report": report,
        })
    return summaries
