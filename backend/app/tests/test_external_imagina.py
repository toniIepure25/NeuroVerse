"""Tests for the External Imagina Integration Layer."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

import httpx
import pytest

from app.integrations.imagina.adapter import external_imagina_to_fusion_packet
from app.integrations.imagina.artifact_reader import scan_external_imagina_artifacts
from app.integrations.imagina.external_client import detect_external_imagina_project
from app.main import create_app


@pytest.fixture
def mock_imagina_root():
    """Create a temporary directory structure matching the Imagina contract."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create signature directories
        (temp_path / "backend").mkdir()
        (temp_path / "frontend").mkdir()
        (temp_path / "research").mkdir()
        (temp_path / "scripts").mkdir()

        # Create files
        (temp_path / "README.md").write_text("Mock Imagina Readme", encoding="utf-8")

        # Create model artifact
        model_dir = temp_path / "models"
        model_dir.mkdir()
        (model_dir / "external_model.pkl").write_text("model_bytes", encoding="utf-8")
        (model_dir / "external_model_metrics.json").write_text(json.dumps({
            "model_id": "external_model_01",
            "model_type": "random_forest",
            "metrics": {
                "accuracy": 0.89,
                "macro_f1": 0.88,
                "confusion_matrix": [[10, 1], [1, 9]]
            }
        }), encoding="utf-8")

        # Create report artifact
        report_dir = temp_path / "reports"
        report_dir.mkdir()
        (report_dir / "scientific_report.json").write_text(json.dumps({
            "session_id": "session_research_456",
            "subject_id": "subject_01",
            "curriculum": "imagination_v1"
        }), encoding="utf-8")

        # Create prediction artifact
        data_dir = temp_path / "data"
        data_dir.mkdir()
        (data_dir / "latest_predictions.json").write_text(json.dumps({
            "imagery_quality_proxy": 0.78,
            "imagery_engagement_proxy": 0.85,
            "imagery_stability_proxy": 0.82,
            "confidence": 0.90,
            "model_id": "external_model_01"
        }), encoding="utf-8")

        # Yield the root path
        yield temp_path


def test_detect_external_imagina_not_found(monkeypatch) -> None:
    """Ensure detect returns false and default root when project does not exist."""
    monkeypatch.setenv("NEUROVERSE_IMAGINA_ROOT", "/nonexistent/path/to/imagina")
    status = detect_external_imagina_project()
    assert status.exists is False
    assert status.integration_ready is False


def test_detect_external_imagina_discovered(mock_imagina_root, monkeypatch) -> None:
    """Ensure detect returns true and passes contract validations when directories exist."""
    monkeypatch.setenv("NEUROVERSE_IMAGINA_ROOT", str(mock_imagina_root))
    status = detect_external_imagina_project()
    assert status.exists is True
    assert status.integration_ready is True
    assert len(status.warnings) == 0


def test_detect_external_imagina_partial_compliance(mock_imagina_root, monkeypatch) -> None:
    """Ensure warnings are emitted when signature folders are missing."""
    # Delete backend folder
    shutil.rmtree(mock_imagina_root / "backend")

    monkeypatch.setenv("NEUROVERSE_IMAGINA_ROOT", str(mock_imagina_root))
    status = detect_external_imagina_project()
    assert status.exists is True
    assert status.integration_ready is False
    assert len(status.warnings) > 0
    assert any("backend" in w for w in status.warnings)


def test_scan_external_artifacts(mock_imagina_root, monkeypatch) -> None:
    """Ensure artifact scanner finds models, reports, and predictions recursively."""
    monkeypatch.setenv("NEUROVERSE_IMAGINA_ROOT", str(mock_imagina_root))
    artifacts = scan_external_imagina_artifacts()

    types = [a.artifact_type for a in artifacts]
    assert "model" in types
    assert "report" in types

    model_art = next(a for a in artifacts if a.artifact_type == "model")
    assert model_art.path.endswith("external_model_metrics.json")


def test_adapter_converts_to_packet(mock_imagina_root, monkeypatch) -> None:
    """Ensure fusion adapter successfully parses prediction artifacts and produces a ModalityFeaturePacket."""
    monkeypatch.setenv("NEUROVERSE_IMAGINA_ROOT", str(mock_imagina_root))
    packet = external_imagina_to_fusion_packet()

    assert packet.modality_id == "imagina"
    assert packet.source == "derived"
    assert packet.features["imagery_quality_proxy"] == 0.78
    assert packet.features["imagery_engagement_proxy"] == 0.85


async def test_imagina_external_api_endpoints(mock_imagina_root, monkeypatch) -> None:
    """Ensure all external Imagina API routes return valid status and artifacts."""
    monkeypatch.setenv("NEUROVERSE_IMAGINA_ROOT", str(mock_imagina_root))

    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Status
        res_status = await client.get("/api/v1/imagina/external/status")
        assert res_status.status_code == 200
        assert res_status.json()["exists"] is True
        assert res_status.json()["integration_ready"] is True

        # 2. Artifacts
        res_arts = await client.get("/api/v1/imagina/external/artifacts")
        assert res_arts.status_code == 200
        assert len(res_arts.json()["artifacts"]) >= 2

        # 3. Refresh
        res_ref = await client.post("/api/v1/imagina/external/refresh")
        assert res_ref.status_code == 200
        assert res_ref.json()["status"] == "refreshed"

        # 4. Adapt to fusion packet
        res_pkt = await client.post("/api/v1/imagina/external/to-fusion-packet")
        assert res_pkt.status_code == 200
        assert res_pkt.json()["modality_id"] == "imagina"
        assert res_pkt.json()["source"] == "derived"
