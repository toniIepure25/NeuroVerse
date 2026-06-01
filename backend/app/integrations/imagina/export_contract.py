"""IMAGINA export contract models.

Declares the formal versioned schemas for exporting modeling research outputs
from the Imagina repository into NeuroVerse.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ExportModelDetails(BaseModel):
    model_id: str
    model_name: str
    model_type: str
    checkpoint_path: str | None = None
    model_card_path: str | None = None


class ExportMetricsDetails(BaseModel):
    metrics_path: str | None = None
    primary_metric: str | None = None
    primary_metric_value: float | None = None
    split_strategy: str | None = None
    subject_count: int | None = None
    sample_count: int | None = None
    limitations: list[str] = Field(default_factory=list)


class ExportPredictionsDetails(BaseModel):
    predictions_path: str | None = None
    prediction_schema: dict[str, Any] = Field(default_factory=dict)
    sample_count: int | None = None


class ExportSafetyDetails(BaseModel):
    proxy_estimates_only: bool = True
    not_decoded_content: bool = True
    closed_loop_allowed: bool = False
    intended_use: str | None = None
    not_intended_use: str | None = None


class NeuroVerseImaginaExportManifest(BaseModel):
    contract_version: str = "1.0"
    export_id: str
    generated_at: str
    source_project: str = "external_imagina"
    source_project_root: str | None = None
    imagina_version: str | None = "1.0"
    export_type: str  # model_evaluation, prediction_batch, fixture_demo, etc.
    modality: str = "unknown"  # eeg, fmri, feature_table, unknown
    paradigm: str = "unknown"  # perception_vs_imagery, rest_vs_imagery, etc.

    model: ExportModelDetails | None = None
    metrics: ExportMetricsDetails | None = None
    predictions: ExportPredictionsDetails | None = None
    reports: list[str] = Field(default_factory=list)
    safety: ExportSafetyDetails = Field(default_factory=ExportSafetyDetails)

    limitations: list[str] = Field(default_factory=list)
    artifact_hashes: dict[str, str] = Field(default_factory=dict)
    provenance: dict[str, Any] = Field(default_factory=dict)
