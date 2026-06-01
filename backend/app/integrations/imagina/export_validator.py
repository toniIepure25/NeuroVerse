"""IMAGINA export validator.

Implements manifest loading, schema checks, referenced artifact existence checks,
and safety parameter verification.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from app.integrations.imagina.export_contract import NeuroVerseImaginaExportManifest


class ValidationResult(BaseModel):
    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    manifest: NeuroVerseImaginaExportManifest | None = None
    resolved_artifacts: list[str] = Field(default_factory=list)
    missing_artifacts: list[str] = Field(default_factory=list)
    safety_flags_ok: bool = False
    can_convert_to_fusion_packet: bool = False
    limitations: list[str] = Field(default_factory=list)


def validate_imagina_export_package(export_dir_or_manifest_path: str | Path) -> ValidationResult:
    """Validate an external IMAGINA export package manifest and referenced files."""
    errors: list[str] = []
    warnings: list[str] = []
    resolved: list[str] = []
    missing: list[str] = []

    target = Path(export_dir_or_manifest_path)
    manifest_path = target

    # If the target is a directory, assume the manifest name is neuroverse_imagina_export.json
    if target.is_dir():
        manifest_path = target / "neuroverse_imagina_export.json"

    if not manifest_path.exists():
        return ValidationResult(
            valid=False,
            errors=[f"Manifest file not found: {manifest_path}"],
            warnings=[],
            manifest=None,
            resolved_artifacts=[],
            missing_artifacts=[],
            safety_flags_ok=False,
            can_convert_to_fusion_packet=False,
            limitations=["Export manifest missing."]
        )

    manifest_root = manifest_path.parent

    # 1. Load JSON manifest
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        return ValidationResult(
            valid=False,
            errors=[f"Failed to parse manifest JSON: {e}"],
            warnings=[],
            manifest=None,
            resolved_artifacts=[],
            missing_artifacts=[],
            safety_flags_ok=False,
            can_convert_to_fusion_packet=False,
            limitations=["Invalid JSON structure."]
        )

    # 2. Validate schema using Pydantic
    try:
        manifest = NeuroVerseImaginaExportManifest.model_validate(data)
    except Exception as e:
        return ValidationResult(
            valid=False,
            errors=[f"Manifest schema validation failed: {e}"],
            warnings=[],
            manifest=None,
            resolved_artifacts=[],
            missing_artifacts=[],
            safety_flags_ok=False,
            can_convert_to_fusion_packet=False,
            limitations=["Schema non-compliant."]
        )

    # 3. Check Safety Flags (Non-Negotiable)
    safety = manifest.safety
    safety_ok = True

    if not safety.proxy_estimates_only:
        errors.append("Safety violation: safety.proxy_estimates_only must be true.")
        safety_ok = False

    if not safety.not_decoded_content:
        errors.append("Safety violation: safety.not_decoded_content must be true.")
        safety_ok = False

    if safety.closed_loop_allowed:
        errors.append("Safety violation: safety.closed_loop_allowed must be false.")
        safety_ok = False

    # 4. Verify referenced artifact files
    def verify_file(rel_path: str | None, required: bool, field_name: str) -> None:
        if not rel_path:
            if required:
                errors.append(f"Required path is missing: {field_name}")
            return

        full_path = manifest_root / rel_path
        if full_path.exists() and full_path.is_file():
            resolved.append(str(full_path.resolve()))
        else:
            if required:
                errors.append(f"Required artifact file missing: {field_name} at {rel_path}")
                missing.append(rel_path)
            else:
                warnings.append(f"Optional artifact file missing: {field_name} at {rel_path}")
                missing.append(rel_path)

    # Verify model details
    if manifest.model:
        verify_file(
            manifest.model.checkpoint_path,
            required=False,
            field_name="model.checkpoint_path"
        )
        verify_file(
            manifest.model.model_card_path,
            required=False,
            field_name="model.model_card_path"
        )

    # Verify metrics details
    if manifest.metrics:
        verify_file(
            manifest.metrics.metrics_path,
            required=False,
            field_name="metrics.metrics_path"
        )

    # Verify predictions details
    if manifest.predictions:
        verify_file(
            manifest.predictions.predictions_path,
            required=False,
            field_name="predictions.predictions_path"
        )

    # Verify reports
    for i, rep_path in enumerate(manifest.reports):
        verify_file(rep_path, required=False, field_name=f"reports[{i}]")

    # 5. Check if it can be converted to fusion packet
    can_convert = False
    if safety_ok and len(errors) == 0:
        # We need predictions file containing prediction schema or values to stream live predictions
        if manifest.predictions and manifest.predictions.predictions_path:
            full_pred = manifest_root / manifest.predictions.predictions_path
            if full_pred.exists():
                can_convert = True
            else:
                warnings.append(
                    "Export has predictions, but predictions file is physically missing."
                )
        else:
            warnings.append(
                "No active predictions. Importing metrics/metadata only."
            )

    # 6. Specific validation for fixture demo exports
    if manifest.export_type == "fixture_demo":
        if manifest.source_project != "neuroverse_fixture":
            warnings.append(
                "export_type is fixture_demo but project is not neuroverse_fixture."
            )
        manifest.limitations.append(
            "Fixture demo export: for workflow/pipeline integration only."
        )

    valid = len(errors) == 0

    return ValidationResult(
        valid=valid,
        errors=errors,
        warnings=warnings,
        manifest=manifest,
        resolved_artifacts=resolved,
        missing_artifacts=missing,
        safety_flags_ok=safety_ok,
        can_convert_to_fusion_packet=can_convert,
        limitations=manifest.limitations + [
            "IMAGINA exports are experimental imagery proxy artifacts.",
            "NeuroVerse validates and consumes artifacts; it does not train the model."
        ]
    )
