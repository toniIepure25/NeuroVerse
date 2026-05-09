from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.ml.reports import summarize_report_dir

REPO_ROOT = Path(__file__).resolve().parents[3]
REPORTS_ROOT = REPO_ROOT / "reports" / "experiments"


def create_run_dir(experiment_id: str, reports_root: str | Path = REPORTS_ROOT) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = Path(reports_root) / f"{stamp}_{experiment_id}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_reports(reports_root: str | Path = REPORTS_ROOT) -> list[dict[str, str]]:
    root = Path(reports_root)
    if not root.exists():
        return []
    reports = []
    for path in sorted(root.glob("*/report.md"), reverse=True):
        reports.append(summarize_report_dir(path.parent))
    return reports


def latest_report(reports_root: str | Path = REPORTS_ROOT) -> dict | None:
    reports = list_reports(reports_root)
    return reports[0] if reports else None
