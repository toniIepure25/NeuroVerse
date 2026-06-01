"""Artifact reader for external Imagina outputs.

Scans the external project for metrics, model cards, session reports,
and prediction outputs, converting them into integration artifacts.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from app.integrations.imagina.contract import (
    ExternalImaginaModelArtifact,
    ExternalImaginaPrediction,
)
from app.integrations.imagina.external_client import resolve_external_imagina_root


def scan_external_imagina_artifacts(
    project_root: str | None = None
) -> list[ExternalImaginaModelArtifact]:
    """Robustly scan the external Imagina directories for model and report artifacts."""
    root_path = resolve_external_imagina_root(project_root)
    artifacts: list[ExternalImaginaModelArtifact] = []

    if not root_path.exists() or not root_path.is_dir():
        return artifacts

    # Define standard directories to search recursively
    search_dirs = [
        root_path / "models",
        root_path / "checkpoints",
        root_path / "reports",
        root_path / "backend" / "reports",
        root_path / "research",
        root_path / "data" / "imagina",
        root_path / "backend" / "data" / "imagina",
    ]

    seen_paths: set[str] = set()

    for directory in search_dirs:
        if not directory.exists() or not directory.is_dir():
            continue

        # Look for metrics.json or report.json or session files recursively
        for path in directory.rglob("*.json"):
            abs_str = str(path.resolve())
            if abs_str in seen_paths:
                continue
            seen_paths.add(abs_str)

            # Skip large databases or configuration definitions
            if path.name in ("pyproject.toml", "package.json", "tsconfig.json"):
                continue

            try:
                content = path.read_text()
                if not content.strip():
                    continue
                data = json.loads(content)

                # Check if it represents a model artifact or a session run
                is_model = (
                    "metrics" in data or "accuracy" in data or "model_type" in data
                )
                is_report = (
                    "session_id" in data or
                    "curriculum" in data or
                    "imagery_quality_proxy" in data
                )

                if is_model or is_report:
                    # Look for a corresponding model card markdown file next to it
                    model_card = None
                    card_path = path.with_name("model_card.md")
                    if card_path.exists():
                        model_card = card_path.read_text()

                    mtime = datetime.fromtimestamp(
                        path.stat().st_mtime, tz=timezone.utc
                    ).isoformat()

                    artifacts.append(
                        ExternalImaginaModelArtifact(
                            model_id=(
                                data.get("model_id") or
                                data.get("session_id") or
                                path.stem
                            ),
                            artifact_type="model" if is_model else "report",
                            path=str(path),
                            created_at=mtime,
                            metrics=data.get("metrics") or data if is_model else None,
                            model_card=model_card,
                            target=(
                                data.get("target") or
                                data.get("target_type") or
                                "classification"
                            ),
                            modality=data.get("modality") or "eeg",
                            paradigm=data.get("paradigm") or "perception_vs_imagery",
                            source_project="external_imagina",
                        )
                    )
            except Exception:
                # Robust: ignore unparseable files
                continue

    return sorted(artifacts, key=lambda x: x.created_at, reverse=True)


def get_latest_external_imagina_artifacts(project_root: str | None = None) -> dict[str, Any]:
    """Retrieve the latest model, metrics, report, and predictions from external Imagina."""
    artifacts = scan_external_imagina_artifacts(project_root)

    latest_model = None
    latest_metrics = None
    latest_report = None
    latest_prediction = None

    for art in artifacts:
        if art.artifact_type == "model" and not latest_model:
            latest_model = art
            latest_metrics = art.metrics
        elif art.artifact_type == "report" and not latest_report:
            latest_report = art

    # Search for latest prediction CSV or JSON under reports or data/exports
    root_path = resolve_external_imagina_root(project_root)
    prediction_path = None
    if root_path.exists():
        # Look for predictions.json or prediction.json or exported json files
        for p in root_path.rglob("*predictions*.json"):
            try:
                pred_data = json.loads(p.read_text())
                if isinstance(pred_data, dict) and (
                    "imagery_quality_proxy" in pred_data or "predictions" in pred_data
                ):
                    prediction_path = p
                    latest_prediction = ExternalImaginaPrediction(
                        imagery_quality_proxy=pred_data.get("imagery_quality_proxy"),
                        imagery_engagement_proxy=pred_data.get("imagery_engagement_proxy"),
                        imagery_stability_proxy=pred_data.get("imagery_stability_proxy"),
                        confidence=pred_data.get("confidence") or 0.70,
                        source="external_imagina_file",
                        model_id=pred_data.get("model_id"),
                        report_path=str(p),
                    )
                    break
            except Exception:
                continue

    return {
        "latest_model": latest_model,
        "latest_metrics": latest_metrics,
        "latest_report": latest_report,
        "latest_prediction": latest_prediction,
        "latest_prediction_path": str(prediction_path) if prediction_path else None,
    }
