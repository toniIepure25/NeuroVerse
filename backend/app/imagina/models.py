"""Pydantic models for IMAGINA v1.

Scientifically honest mental-imagery proxy data structures.
IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

ImaginaModality = Literal["eeg", "fmri", "feature_table", "multimodal"]
ImaginaParadigm = Literal["perception_vs_imagery", "rest_vs_imagery", "imagery_quality", "imagined_symbol", "unknown"]


class ImaginaSample(BaseModel):
    sample_id: str
    subject_id: str | None = None
    session_id: str | None = None
    task: str = "imagery"
    label: str | None = None
    features_path: str | None = None
    features: dict[str, float] = Field(default_factory=dict)
    self_report: dict[str, float] = Field(default_factory=dict)
    source: str = "imagina_v1_fixture"
    limitations: list[str] = Field(default_factory=list)


class ImaginaDatasetManifest(BaseModel):
    dataset_name: str
    dataset_version: str = "1.0"
    modality: ImaginaModality = "feature_table"
    paradigm: ImaginaParadigm = "unknown"
    labels: list[str] = Field(default_factory=list)
    feature_schema: list[str] = Field(default_factory=list)
    subject_column: str | None = None
    session_column: str | None = None
    task_column: str | None = None
    self_report_fields: list[str] = Field(default_factory=list)
    samples: list[ImaginaSample] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)
    not_a_trained_model: bool = True
