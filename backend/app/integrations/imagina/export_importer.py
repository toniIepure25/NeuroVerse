"""IMAGINA export importer.

Validates and imports validated external IMAGINA export manifests into NeuroVerse's
gated reports environment, writing import summary files.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.integrations.imagina.export_validator import (
    ValidationResult,
    validate_imagina_export_package,
)


def import_imagina_export(
    export_manifest_path: str | Path,
    output_base_dir: str | Path = "reports/external_imagina_imports"
) -> dict[str, Any]:
    """Import a validated IMAGINA export package into NeuroVerse's local reports repository.

    Copies lightweight artifacts (metadata, CSV predictions, report cards) and
    references heavy model binaries.
    """
    manifest_path = Path(export_manifest_path)
    res: ValidationResult = validate_imagina_export_package(manifest_path)

    if not res.valid:
        return {
            "success": False,
            "errors": res.errors,
            "warnings": res.warnings,
            "imported_at": datetime.now(timezone.utc).isoformat(),
        }

    manifest = res.manifest
    assert manifest is not None

    run_id = f"import_{manifest.export_id}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    target_dir = Path(output_base_dir) / run_id
    target_dir.mkdir(parents=True, exist_ok=True)

    manifest_root = manifest_path.parent
    artifact_index: dict[str, dict[str, str]] = {}

    # Define helper to import files safely
    def import_file(rel_path: str | None, key: str, is_large_binary: bool = False) -> str | None:
        if not rel_path:
            return None
        src_path = manifest_root / rel_path
        if not src_path.exists():
            return None

        dst_rel_path = rel_path
        dst_path = target_dir / dst_rel_path

        # If it's a large checkpoint binary, DO NOT physically copy unless small, reference instead
        if is_large_binary:
            artifact_index[key] = {
                "original_path": str(src_path.resolve()),
                "imported_path": str(src_path.resolve()),
                "copied": "false",
                "reference_only": "true"
            }
            return str(src_path.resolve())

        # Copy file
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src_path, dst_path)
            artifact_index[key] = {
                "original_path": str(src_path.resolve()),
                "imported_path": str(dst_path.resolve()),
                "copied": "true",
                "reference_only": "false"
            }
            return str(dst_path.resolve())
        except Exception:
            artifact_index[key] = {
                "original_path": str(src_path.resolve()),
                "imported_path": str(src_path.resolve()),
                "copied": "false",
                "reference_only": "true"
            }
            return str(src_path.resolve())

    # Import parts
    if manifest.model:
        import_file(manifest.model.checkpoint_path, "model.checkpoint", is_large_binary=True)
        import_file(manifest.model.model_card_path, "model.model_card", is_large_binary=False)

    if manifest.metrics:
        import_file(manifest.metrics.metrics_path, "metrics.metrics", is_large_binary=False)

    if manifest.predictions:
        import_file(
            manifest.predictions.predictions_path,
            "predictions.predictions",
            is_large_binary=False
        )

    for i, rep in enumerate(manifest.reports):
        import_file(rep, f"reports.report_{i}", is_large_binary=False)

    # 1. Write validated manifest copy
    manifest_dst = target_dir / "validated_export_manifest.json"
    manifest_dst.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")

    # 2. Write artifact index
    index_dst = target_dir / "artifact_index.json"
    index_dst.write_text(json.dumps(artifact_index, indent=2), encoding="utf-8")

    # 3. Write import summary json
    summary_data = {
        "import_id": run_id,
        "export_id": manifest.export_id,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "valid": True,
        "warnings": res.warnings,
        "artifacts_count": len(artifact_index),
        "can_convert_to_fusion_packet": res.can_convert_to_fusion_packet,
        "safety_flags_ok": res.safety_flags_ok,
        "target_dir": str(target_dir.resolve()),
        "manifest_path": str(manifest_dst.resolve()),
        "artifact_index_path": str(index_dst.resolve())
    }
    summary_dst = target_dir / "import_summary.json"
    summary_dst.write_text(json.dumps(summary_data, indent=2), encoding="utf-8")

    # 4. Write human-readable Markdown summary with mandatory scientific framing
    md_content = f"""# IMAGINA Export Import Summary

- **Import ID**: `{run_id}`
- **Export ID**: `{manifest.export_id}`
- **Import Timestamp**: `{summary_data["imported_at"]}`
- **Source Project**: `{manifest.source_project}`
- **Modality**: `{manifest.modality}`
- **Paradigm**: `{manifest.paradigm}`
- **Can Stream/Convert to Fusion**: `{summary_data["can_convert_to_fusion_packet"]}`

---

## Mandatory Scientific Boundary & Safety Declarations

> [!IMPORTANT]
> - **IMAGINA exports are experimental imagery proxy artifacts, not decoded thoughts.**
> - **NeuroVerse validates and consumes IMAGINA artifacts; it does not train the model.**
> - **The corridor is not a decoded image. It is an adaptive scaffold driven by proxy metrics.**
> - **Closed-loop from real EEG is disabled by default.**

---

## Safety Flags Audit
- `proxy_estimates_only`: **{manifest.safety.proxy_estimates_only}**
- `not_decoded_content`: **{manifest.safety.not_decoded_content}**
- `closed_loop_allowed`: **{manifest.safety.closed_loop_allowed}**

---

## Artifact Files Registered
"""
    for key, info in artifact_index.items():
        copied_lbl = "Copied Locally" if info["copied"] == "true" else "Referenced Externally"
        md_content += f"- **{key}**: `{info['imported_path']}` ({copied_lbl})\n"

    if res.warnings:
        md_content += "\n## Import Warnings\n"
        for warn in res.warnings:
            md_content += f"- *Warning*: {warn}\n"

    md_dst = target_dir / "import_summary.md"
    md_dst.write_text(md_content, encoding="utf-8")

    # Register/track latest import in a static JSON file for portfolio promotion
    latest_track = Path(output_base_dir) / "latest_import_summary.json"
    latest_track.write_text(json.dumps(summary_data, indent=2), encoding="utf-8")

    return {
        "success": True,
        "import_id": run_id,
        "summary": summary_data,
        "import_dir": str(target_dir.resolve()),
        "summary_md_path": str(md_dst.resolve()),
    }
