"""Bake provenance-derived evidence into frontend public assets.

This script copies the latest generated evidence pack files into
frontend/public/evidence for static portfolio deployments. It does not invent
metrics or rewrite report claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "evidence_pack"
TARGET_DIR = ROOT / "frontend" / "public" / "evidence"

REQUIRED_FILES = [
    "latest_auto_run_protocol.json",
    "latest_completion_report.json",
]

OPTIONAL_FILES = [
    "data_source_readiness_snapshot.json",
    "latest_fusion_report.json",
    "latest_fusion_calibration_profile.json",
    "latest_fusion_validation_summary.json",
    "latest_fusion_ablation_table.csv",
    "external_imagina_status.json",
    "external_imagina_artifacts.json",
    "imagina_source_separation.md",
    "latest_contract_import_summary.json",
    "latest_contract_import_summary.md",
    "reviewer_demo_flow_summary.json",
    "static_portfolio_check.json",
    "frontend_route_check.json",
    "frontend_bundle_check.json",
    "accessibility_check.json",
    "screenshot_assets_check.json",
    "latest_public_launch_validation.json",
    "latest_public_launch_validation.md",
]


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing required evidence file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON evidence file: {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Evidence file is not a JSON object: {path.relative_to(ROOT)}")
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return None


def _validate_evidence_file(path: Path) -> dict[str, Any]:
    data = _load_json(path)
    if data.get("closed_loop_allowed") is not False:
        raise SystemExit(
            f"{path.relative_to(ROOT)} must preserve closed_loop_allowed=false"
        )
    if data.get("mode") == "physical_hardware":
        artifact_paths = [str(p).lower() for p in data.get("artifact_paths", [])]
        if not any("openbci" in p or "physical" in p for p in artifact_paths):
            raise SystemExit(
                f"{path.relative_to(ROOT)} claims physical hardware mode without physical artifacts"
            )
    return data


def _source_manifest() -> dict[str, Any]:
    files = []
    for name in REQUIRED_FILES:
        source = SOURCE_DIR / name
        data = _validate_evidence_file(source)
        files.append(
            {
                "name": name,
                "source_path": str(source.relative_to(ROOT)),
                "sha256": _sha256(source),
                "run_id": data.get("run_id"),
                "protocol_id": data.get("protocol_id"),
                "mode": data.get("mode"),
                "status": data.get("status"),
                "closed_loop_allowed": data.get("closed_loop_allowed"),
                "generated_at": data.get("generated_at"),
            }
        )
    return {
        "baked_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "source": "evidence_pack",
        "portfolio_mode": "static_baked_snapshot",
        "scientific_note": (
            "Static evidence is a baked snapshot, not live runtime evidence. "
            "Closed-loop from real EEG is disabled by default."
        ),
        "fusion_validation_available": (SOURCE_DIR / "latest_fusion_validation_summary.json").exists(),
        "fusion_calibration_available": (SOURCE_DIR / "latest_fusion_calibration_profile.json").exists(),
        "fusion_ablation_available": (SOURCE_DIR / "latest_fusion_ablation_table.csv").exists(),
        "imagina_bridge_available": (SOURCE_DIR / "latest_fusion_report.json").exists(),
        "files": files,
    }


def bake() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    manifest = _source_manifest()
    for name in REQUIRED_FILES:
        shutil.copy2(SOURCE_DIR / name, TARGET_DIR / name)
    for name in OPTIONAL_FILES:
        source = SOURCE_DIR / name
        if source.exists():
            shutil.copy2(source, TARGET_DIR / name)
            manifest["files"].append(
                {
                    "name": name,
                    "source_path": str(source.relative_to(ROOT)),
                    "sha256": _sha256(source),
                    "optional": True,
                }
            )
    (TARGET_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print(f"Static evidence baked to {TARGET_DIR.relative_to(ROOT)}")


def check() -> None:
    manifest_path = TARGET_DIR / "manifest.json"
    manifest = _load_json(manifest_path)
    files = manifest.get("files")
    if not isinstance(files, list):
        raise SystemExit("Static evidence manifest missing files list")

    by_name = {item.get("name"): item for item in files if isinstance(item, dict)}
    for name in REQUIRED_FILES:
        target = TARGET_DIR / name
        source = SOURCE_DIR / name
        _validate_evidence_file(target)
        _validate_evidence_file(source)
        expected = by_name.get(name, {}).get("sha256")
        actual = _sha256(target)
        source_hash = _sha256(source)
        if actual != source_hash:
            raise SystemExit(
                f"Static evidence drift: {target.relative_to(ROOT)} differs from {source.relative_to(ROOT)}"
            )
        if expected and actual != expected:
            raise SystemExit(f"Static evidence manifest hash mismatch for {name}")
    for name in OPTIONAL_FILES:
        target = TARGET_DIR / name
        source = SOURCE_DIR / name
        if target.exists() and source.exists() and _sha256(target) != _sha256(source):
            raise SystemExit(
                f"Static evidence drift: {target.relative_to(ROOT)} differs from {source.relative_to(ROOT)}"
            )
    print("Static evidence check passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bake/check static portfolio evidence")
    parser.add_argument("--check", action="store_true", help="check baked evidence only")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        bake()


if __name__ == "__main__":
    main()
