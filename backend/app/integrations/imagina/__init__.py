"""IMAGINA External Integration package."""

from __future__ import annotations

from app.integrations.imagina.adapter import (
    external_imagina_to_fusion_packet,
    imagina_export_to_fusion_packet,
)
from app.integrations.imagina.artifact_reader import (
    get_latest_external_imagina_artifacts,
    scan_external_imagina_artifacts,
)
from app.integrations.imagina.contract import (
    ExternalImaginaModelArtifact,
    ExternalImaginaPrediction,
    ExternalImaginaStatus,
    external_prediction_to_modality_packet,
)

# New export contract v1 imports
from app.integrations.imagina.export_contract import NeuroVerseImaginaExportManifest
from app.integrations.imagina.export_importer import import_imagina_export
from app.integrations.imagina.export_validator import (
    ValidationResult,
    validate_imagina_export_package,
)
from app.integrations.imagina.external_client import (
    detect_external_imagina_project,
    resolve_external_imagina_root,
)

__all__ = [
    "ExternalImaginaStatus",
    "ExternalImaginaModelArtifact",
    "ExternalImaginaPrediction",
    "external_prediction_to_modality_packet",
    "resolve_external_imagina_root",
    "detect_external_imagina_project",
    "scan_external_imagina_artifacts",
    "get_latest_external_imagina_artifacts",
    "external_imagina_to_fusion_packet",

    # Export Contract v1
    "NeuroVerseImaginaExportManifest",
    "validate_imagina_export_package",
    "ValidationResult",
    "import_imagina_export",
    "imagina_export_to_fusion_packet",
]

