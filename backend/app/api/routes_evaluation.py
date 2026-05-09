from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.experiments.tracking import REPORTS_ROOT, latest_report, list_reports

router = APIRouter(prefix="/api")
REPO_ROOT = Path(__file__).resolve().parents[3]


@router.get("/v1/reports")
@router.get("/v1/evaluation/reports")
@router.get("/evaluation/reports")
async def api_list_reports() -> list[dict[str, str]]:
    return list_reports()


@router.get("/v1/evaluation/latest")
@router.get("/evaluation/latest")
async def api_latest_report() -> dict:
    report = latest_report()
    if report is None:
        return {"report": None}
    path = Path(report["path"])
    markdown = path.read_text() if path.exists() else ""
    return {**report, "markdown": markdown}


@router.get("/v1/reports/{report_id}")
@router.get("/v1/evaluation/reports/{report_id}")
@router.get("/evaluation/reports/{report_id}")
async def api_get_report(report_id: str) -> dict[str, str]:
    path = Path(REPORTS_ROOT) / report_id / "report.md"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report_id": report_id, "markdown": path.read_text()}


@router.get("/v1/eeg/public/latest")
async def api_latest_public_eeg_report() -> dict:
    return _latest_report_from("public_eeg_validation", "public_eeg_validation_summary")


@router.get("/v1/eeg/real-public/latest")
async def api_latest_real_public_eeg_report() -> dict:
    return _latest_report_from("real_public_eeg_validation", "real_public_eeg_validation_summary")


@router.get("/v1/eeg/bci-benchmark/latest")
async def api_latest_bci_benchmark_report() -> dict:
    return _latest_report_from("bci_benchmark", "benchmark_summary")


@router.get("/v1/eeg/raw-bci-benchmark/latest")
async def api_latest_raw_bci_benchmark_report() -> dict:
    return _latest_report_from("bci_raw_epoch_benchmark", "benchmark_summary")


@router.get("/v1/eeg/bci-benchmark-comparison/latest")
async def api_latest_bci_benchmark_comparison() -> dict:
    return _latest_report_from("bci_benchmark_comparison", "comparison")


@router.get("/v1/eeg/raw-bci-shadow/latest")
async def api_latest_raw_bci_shadow_report() -> dict:
    return _latest_report_from("raw_bci_shadow", "live_shadow_summary")


def _latest_report_from(directory: str, stem: str) -> dict:
    base = REPO_ROOT / "reports" / "public_eeg_validation"
    if directory != "public_eeg_validation":
        base = REPO_ROOT / "reports" / directory
    if not base.exists():
        return {"report": None}
    matches = sorted(
        base.glob(f"*/{stem}.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    if not matches:
        return {"report": None}
    summary_path = matches[0]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    markdown_path = summary_path.with_suffix(".md")
    return {
        "report": summary,
        "path": str(summary_path),
        "markdown": markdown_path.read_text(encoding="utf-8") if markdown_path.exists() else "",
    }
