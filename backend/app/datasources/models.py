"""Typed models for data source readiness."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

DataSourceMode = Literal[
    "simulator",
    "public_eeg_replay",
    "lsl_stream",
    "brainflow_synthetic",
    "physical_openbci",
]

Availability = Literal["available", "partially_available", "unavailable", "unknown"]


class DataSourceDefinition(BaseModel):
    source_id: str
    title: str
    mode: DataSourceMode
    description: str
    recommended_protocol_id: str
    required_inputs: list[str] = Field(default_factory=list)
    commands: list[str] = Field(default_factory=list)
    what_it_proves: list[str] = Field(default_factory=list)
    what_it_does_not_prove: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class DataSourcePreflightSummary(BaseModel):
    protocol_id: str
    protocol_title: str | None = None
    can_start: bool = False
    can_auto_run: bool = False
    missing_inputs: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    auto_run_policy: str = "disabled"


class DataSourceStatus(BaseModel):
    source_id: str
    title: str
    mode: DataSourceMode
    description: str
    availability: Availability = "unknown"
    can_run_now: bool = False
    can_validate_now: bool = False
    can_auto_run_protocol: bool = False
    recommended_protocol_id: str
    required_inputs: list[str] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    installed_dependencies: dict[str, bool] = Field(default_factory=dict)
    detected_resources: dict[str, Any] = Field(default_factory=dict)
    latest_evidence_paths: dict[str, str | None] = Field(default_factory=dict)
    safety_status: dict[str, Any] = Field(default_factory=dict)
    closed_loop_allowed: bool = False
    physical_hardware_validated: bool = False
    what_it_proves: list[str] = Field(default_factory=list)
    what_it_does_not_prove: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    commands: list[str] = Field(default_factory=list)
    protocol_preflight: DataSourcePreflightSummary | None = None


class DataSourceListResponse(BaseModel):
    generated_at: str
    mode: Literal["live_backend"] = "live_backend"
    sources: list[DataSourceStatus]
    static_portfolio_note: str = (
        "Static portfolio mode is informational only. Start the backend for live checks."
    )
