"""Unit and integration tests for Imagina Export Contract, Validator, Importer, and API routes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.integrations.imagina import (
    import_imagina_export,
    validate_imagina_export_package,
)
from app.integrations.imagina.adapter import imagina_export_to_fusion_packet
from app.main import create_app


@pytest.fixture
def temp_export_dir(tmp_path: Path) -> Path:
    """Fixture to create a temporary compliant export package."""
    export_dir = tmp_path / "imagina_export"
    export_dir.mkdir()

    # Write mock predictions file
    predictions_file = export_dir / "predictions.json"
    predictions_file.write_text(json.dumps({
        "imagery_quality_proxy": 0.85,
        "imagery_engagement_proxy": 0.90,
        "imagery_stability_proxy": 0.88,
        "confidence": 0.89,
        "not_decoded_content": True
    }), encoding="utf-8")

    # Write mock metrics file
    metrics_file = export_dir / "metrics.json"
    metrics_file.write_text(json.dumps({
        "model_id": "test_model_v1",
        "primary_metric": "accuracy",
        "primary_metric_value": 0.88
    }), encoding="utf-8")

    # Write compliant manifest
    manifest_data = {
        "contract_version": "1.0",
        "export_id": "test_export_001",
        "generated_at": "2026-06-01T12:00:00Z",
        "source_project": "external_imagina",
        "export_type": "model_evaluation",
        "modality": "eeg",
        "paradigm": "perception_vs_imagery",
        "model": {
            "model_id": "test_model_v1",
            "model_name": "Test Model",
            "model_type": "Ridge"
        },
        "metrics": {
            "metrics_path": "metrics.json",
            "primary_metric": "accuracy",
            "primary_metric_value": 0.88,
            "split_strategy": "leave_one_subject_out"
        },
        "predictions": {
            "predictions_path": "predictions.json",
            "prediction_schema": {
                "imagery_quality_proxy": "float"
            },
            "sample_count": 1
        },
        "safety": {
            "proxy_estimates_only": True,
            "not_decoded_content": True,
            "closed_loop_allowed": False
        }
    }

    manifest_path = export_dir / "neuroverse_imagina_export.json"
    manifest_path.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    return export_dir


def test_validator_compliant_manifest(temp_export_dir: Path) -> None:
    """Ensure a compliant export package passes validation successfully."""
    manifest_path = temp_export_dir / "neuroverse_imagina_export.json"
    res = validate_imagina_export_package(manifest_path)

    assert res.valid is True
    assert len(res.errors) == 0
    assert res.safety_flags_ok is True
    assert res.can_convert_to_fusion_packet is True
    assert res.manifest is not None
    assert res.manifest.export_id == "test_export_001"


def test_validator_missing_manifest(tmp_path: Path) -> None:
    """Ensure missing manifest handles gracefully and returns valid = False."""
    res = validate_imagina_export_package(tmp_path / "nonexistent.json")
    assert res.valid is False
    assert "not found" in res.errors[0]


def test_validator_safety_violations(temp_export_dir: Path) -> None:
    """Ensure safety violations trigger immediate validation failure."""
    manifest_path = temp_export_dir / "neuroverse_imagina_export.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Trigger closed loop violation
    data["safety"]["closed_loop_allowed"] = True
    manifest_path.write_text(json.dumps(data), encoding="utf-8")

    res = validate_imagina_export_package(manifest_path)
    assert res.valid is False
    assert res.safety_flags_ok is False
    assert any("closed_loop_allowed" in err for err in res.errors)


def test_importer_copies_correctly(temp_export_dir: Path, tmp_path: Path) -> None:
    """Ensure valid packages copy lightweight files and generate summary records."""
    manifest_path = temp_export_dir / "neuroverse_imagina_export.json"
    output_dir = tmp_path / "imports"

    res = import_imagina_export(manifest_path, output_base_dir=output_dir)
    assert res["success"] is True

    import_dir = Path(res["import_dir"])
    assert (import_dir / "validated_export_manifest.json").exists()
    assert (import_dir / "import_summary.json").exists()
    assert (import_dir / "import_summary.md").exists()

    # Verify predictions file got copied
    assert (import_dir / "predictions.json").exists()

    # Check warning text
    summary_md = (import_dir / "import_summary.md").read_text(encoding="utf-8")
    assert "experimental imagery proxy artifacts" in summary_md


def test_adapter_converts_export_packet(temp_export_dir: Path) -> None:
    """Ensure adapter converts imported manifest into a ModalityFeaturePacket."""
    manifest_path = temp_export_dir / "neuroverse_imagina_export.json"
    res = validate_imagina_export_package(manifest_path)

    assert res.manifest is not None
    packet = imagina_export_to_fusion_packet(res.manifest, manifest_path)

    assert packet.modality_id == "imagina"
    assert packet.features["imagery_quality_proxy"] == 0.85
    assert packet.features["proxy_estimates_only"] is True
    assert packet.features["not_decoded_content"] is True
    assert packet.missing is False


def test_api_endpoints_integration(temp_export_dir: Path, tmp_path: Path) -> None:
    """Test full integration across API endpoints using FastAPI TestClient."""
    app = create_app()
    client = TestClient(app)
    manifest_path = temp_export_dir / "neuroverse_imagina_export.json"

    # 1. Test GET contract template
    r = client.get("/api/v1/imagina/external/contract")
    assert r.status_code == 200
    assert r.json()["contract_version"] == "1.0"

    # 2. Test POST validate
    r = client.post("/api/v1/imagina/external/validate-export", json={
        "manifest_path": str(manifest_path.resolve())
    })
    assert r.status_code == 200
    assert r.json()["valid"] is True

    # 3. Test POST convert to fusion packet
    r = client.post("/api/v1/imagina/external/export-to-fusion-packet", json={
        "manifest_path": str(manifest_path.resolve())
    })
    assert r.status_code == 200
    assert r.json()["modality_id"] == "imagina"
    assert r.json()["features"]["imagery_quality_proxy"] == 0.85
