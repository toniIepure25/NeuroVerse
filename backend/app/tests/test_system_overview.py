"""Tests for the unified system overview endpoint."""

from __future__ import annotations

import httpx
import pytest


@pytest.fixture
async def async_client():
    from app.main import create_app

    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


async def test_system_overview_endpoint_returns_valid_aggregated_structure(async_client):
    resp = await async_client.get("/api/v1/system/overview")
    assert resp.status_code == 200
    body = resp.json()

    # Base Fields
    assert body["source"] == "live_backend"
    assert "generated_at" in body
    assert isinstance(body["warnings"], list)
    assert isinstance(body["limitations"], list)
    assert body["closed_loop_allowed"] is False

    # Limitations contain the scientific/product wording
    assert any(
        "Closed-loop from real EEG is disabled by default." in item
        for item in body["limitations"]
    )
    assert any(
        "The corridor is not a decoded mental image." in item
        for item in body["limitations"]
    )
    assert any(
        "IMAGINA outputs are experimental imagery proxy artifacts" in item
        for item in body["limitations"]
    )
    assert any(
        "Static evidence is a baked snapshot" in item
        for item in body["limitations"]
    )
    assert any(
        "Physical OpenBCI/Galea validation remains unperformed" in item
        for item in body["limitations"]
    )

    # Safety Section
    assert "safety" in body
    safety = body["safety"]
    assert "current_state" in safety
    assert "severity" in safety
    assert safety["closed_loop_allowed"] is False
    assert isinstance(safety["lock_reasons"], list)
    assert "emergency_stop_active" in safety
    assert "adaptation_frozen" in safety
    assert "evidence_summary" in safety

    # Data Sources Section
    assert "data_sources" in body
    assert "sources" in body["data_sources"]

    # Protocol Section
    assert "protocol" in body

    # Imagina Section
    assert "imagina" in body
    assert "external_detected" in body["imagina"]

    # Fusion Section
    assert "fusion" in body
    assert body["fusion"]["imagina_proxy_status"] == "proxy_estimates_only"

    # Evidence Health Section
    assert "evidence_health" in body
    assert "artifact_count" in body["evidence_health"]
    assert "evidence_sources" in body["evidence_health"]
