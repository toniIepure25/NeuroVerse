"""Tests for data source readiness assistant."""

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


async def test_list_data_sources_returns_expected_sources(async_client):
    resp = await async_client.get("/api/v1/data-sources")
    assert resp.status_code == 200
    body = resp.json()
    ids = {source["source_id"] for source in body["sources"]}
    assert {
        "simulator",
        "physionet_eegbci_replay",
        "lsl_stream",
        "brainflow_synthetic",
        "openbci_cyton",
        "openbci_ganglion",
    }.issubset(ids)


async def test_simulator_is_available(async_client):
    resp = await async_client.get("/api/v1/data-sources/simulator")
    assert resp.status_code == 200
    body = resp.json()
    assert body["availability"] == "available"
    assert body["can_run_now"] is True
    assert body["closed_loop_allowed"] is False
    assert body["recommended_protocol_id"] == "synthetic_demo_protocol"


async def test_brainflow_synthetic_never_marks_physical_validated(async_client, monkeypatch):
    import app.datasources.readiness as readiness

    monkeypatch.setattr(
        readiness.BrainFlowAcquisition,
        "is_available",
        staticmethod(lambda: True),
    )
    resp = await async_client.get("/api/v1/data-sources/brainflow_synthetic")
    assert resp.status_code == 200
    body = resp.json()
    assert body["availability"] == "available"
    assert body["detected_resources"]["physical_or_synthetic"] == "synthetic"
    assert body["physical_hardware_validated"] is False
    assert (
        "BrainFlow SyntheticBoard is not real OpenBCI physical validation."
        in body["limitations"]
    )


async def test_openbci_unavailable_without_serial_device(async_client, monkeypatch):
    import app.datasources.readiness as readiness

    monkeypatch.setattr(
        readiness.BrainFlowAcquisition,
        "is_available",
        staticmethod(lambda: False),
    )
    monkeypatch.setattr(
        readiness,
        "discover_brainflow_devices",
        lambda: {
            "pyserial_available": False,
            "devices": [],
            "warnings": ["No serial devices detected."],
            "next_commands": {},
        },
    )
    resp = await async_client.get("/api/v1/data-sources/openbci_cyton")
    assert resp.status_code == 200
    body = resp.json()
    assert body["availability"] == "unavailable"
    assert body["can_auto_run_protocol"] is False
    assert body["closed_loop_allowed"] is False
    assert body["physical_hardware_validated"] is False
    assert any("PORT" in item for item in body["missing_requirements"])


async def test_each_source_has_recommended_protocol_and_missing_requirements(async_client):
    resp = await async_client.get("/api/v1/data-sources")
    assert resp.status_code == 200
    for source in resp.json()["sources"]:
        assert source["recommended_protocol_id"]
        assert source["protocol_preflight"] is not None
        if source["availability"] == "unavailable":
            assert source["missing_requirements"]


async def test_data_source_preflight_accepts_inputs(async_client):
    resp = await async_client.post(
        "/api/v1/data-sources/openbci_cyton/preflight",
        json={"inputs": {"PORT": "/dev/ttyUSB0", "PROFILE_ID": "openbci_cyton_8ch"}},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["source_id"] == "openbci_cyton"
    assert body["protocol_preflight"]["protocol_id"] == "physical_openbci_trial_protocol"
    assert body["protocol_preflight"]["can_auto_run"] is False
