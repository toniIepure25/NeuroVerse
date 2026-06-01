from __future__ import annotations

import httpx

from app.api.routes_fusion import build_demo_fusion_input
from app.fusion.imagina_plugin import ImaginaProxyPluginV1
from app.fusion.late_fusion import LateFusionV1
from app.fusion.models import FusionInput, ModalityFeaturePacket
from app.fusion.report import generate_fusion_report
from app.main import create_app
from app.protocols.registry import get_protocol


def test_fusion_model_handles_all_modalities() -> None:
    output = LateFusionV1().evaluate(build_demo_fusion_input())
    assert output.proxy_estimates_only is True
    assert output.closed_loop_allowed is False
    assert output.overall_confidence < 0.8
    assert output.imagery_quality_proxy is not None
    assert output.safety_recommendation in {"allow_shadow", "wait", "block"}


def test_fusion_model_handles_missing_modalities() -> None:
    payload = FusionInput(
        context={"mode": "simulated"},
        packets=[
            ModalityFeaturePacket(
                modality_id="eeg",
                source="simulated",
                features={"engagement_index": 0.6},
                quality_score=0.7,
            )
        ],
    )
    output = LateFusionV1().evaluate(payload)
    assert "gaze" in output.missing_modalities
    assert output.uncertainty > 0.3


def test_low_quality_modality_increases_uncertainty() -> None:
    high = build_demo_fusion_input()
    low = build_demo_fusion_input()
    low.packets[0].quality_score = 0.05
    low.packets[0].confidence = 0.05
    assert LateFusionV1().evaluate(low).uncertainty > LateFusionV1().evaluate(high).uncertainty


def test_imagina_plugin_returns_not_decoded_content() -> None:
    payload = build_demo_fusion_input()
    packets = {p.modality_id: p for p in payload.packets}
    output = ImaginaProxyPluginV1().evaluate(
        eeg_packet=packets["eeg"],
        self_report_packet=packets["self_report"],
        task_metadata=payload.context,
    )
    assert output.not_decoded_content is True
    assert output.confidence < 0.8


def test_imagina_no_imagery_task_low_confidence() -> None:
    output = ImaginaProxyPluginV1().evaluate(task_metadata={})
    assert output.confidence < 0.25
    assert output.not_decoded_content is True


async def test_fusion_api_returns_proxy_estimates_only() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/fusion/evaluate",
            json=build_demo_fusion_input().model_dump(mode="json"),
        )
    assert response.status_code == 200
    body = response.json()
    assert body["proxy_estimates_only"] is True
    assert body["closed_loop_allowed"] is False


async def test_fusion_demo_sample_returns_closed_loop_false() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/fusion/demo-sample")
    assert response.status_code == 200
    body = response.json()
    assert body["closed_loop_allowed"] is False
    assert body["output"]["closed_loop_allowed"] is False


def test_visual_mapping_is_proposed_not_executed() -> None:
    output = LateFusionV1().evaluate(build_demo_fusion_input())
    mapping = output.proposed_visual_mapping
    assert mapping["mapping_mode"] == "proposed_shadow_only"
    assert mapping["executed_real_action"] is False
    assert mapping["blocked_for_real_eeg_closed_loop"] is True


def test_multimodal_fusion_protocol_registered() -> None:
    protocol = get_protocol("multimodal_fusion_demo_protocol")
    assert protocol is not None
    assert protocol.closed_loop_allowed_default is False
    assert protocol.supports_auto_run is True


def test_fusion_report_generation_works(tmp_path, monkeypatch) -> None:
    import app.fusion.report as report_mod

    monkeypatch.setattr(report_mod, "ROOT", tmp_path)
    payload = build_demo_fusion_input()
    output = LateFusionV1().evaluate(payload)
    report = generate_fusion_report(payload, output, run_id="fusion_test")
    assert report["json_path"].endswith("fusion_report.json")
    assert (tmp_path / "reports" / "fusion" / "fusion_test" / "fusion_report.md").exists()
