"""Tests for Fusion Validation, Sensor Adapters, Calibration, and IMAGINA Bridge."""

from __future__ import annotations

import httpx

from app.api.routes_fusion import build_demo_fusion_input
from app.fusion.adapters.csv_replay import CSVReplayAdapter
from app.fusion.adapters.registry import get_adapter_statuses, list_adapters
from app.fusion.adapters.self_report import SelfReportAdapter
from app.fusion.adapters.simulated import (
    SimulatedGazeAdapter,
    SimulatedPhysiologyAdapter,
)
from app.fusion.calibration import (
    calibrate_from_packets,
    create_default_calibration_profile,
    deserialize_profile,
    save_calibration_report,
    serialize_profile,
)
from app.fusion.imagina_dataset_bridge import (
    convert_imagina_sample_to_fusion_input,
    load_imagina_manifest,
    validate_imagina_manifest,
)
from app.fusion.late_fusion import LateFusionV1
from app.fusion.models import FusionInput, ModalityFeaturePacket
from app.fusion.validation import run_fusion_validation
from app.main import create_app
from app.protocols.registry import get_protocol

# ---------------------------------------------------------------------------
#  1. Simulated gaze adapter returns packet
# ---------------------------------------------------------------------------


def test_simulated_gaze_adapter_returns_packet() -> None:
    adapter = SimulatedGazeAdapter(seed=42)
    assert adapter.is_available()
    packet = adapter.read_packet()
    assert packet.modality_id == "gaze"
    assert packet.source == "simulated"
    assert packet.quality_score is not None
    assert 0 <= packet.quality_score <= 1
    assert "fixation_stability" in packet.features
    assert "blink_rate" in packet.features
    assert "pupil_diameter_proxy" in packet.features


# ---------------------------------------------------------------------------
#  2. Simulated physiology adapter returns packet
# ---------------------------------------------------------------------------


def test_simulated_physiology_adapter_returns_packet() -> None:
    adapter = SimulatedPhysiologyAdapter(seed=42)
    assert adapter.is_available()
    packet = adapter.read_packet()
    assert packet.modality_id == "physiology"
    assert packet.source == "simulated"
    assert "rmssd_proxy" in packet.features
    assert "eda_phasic" in packet.features
    assert "stress_index" in packet.features
    assert "heart_rate" in packet.features


# ---------------------------------------------------------------------------
#  3. Self-report adapter returns packet
# ---------------------------------------------------------------------------


def test_self_report_adapter_returns_packet() -> None:
    adapter = SelfReportAdapter(demo_mode=True, seed=42)
    assert adapter.is_available()
    packet = adapter.read_packet()
    assert packet.modality_id == "self_report"
    assert "vividness" in packet.features
    assert "effort" in packet.features
    assert "perceived_focus" in packet.features


def test_self_report_adapter_accepts_user_report() -> None:
    adapter = SelfReportAdapter(demo_mode=False)
    adapter.submit_report({"focus": 0.8, "relaxation": 0.6, "imagery_vividness": 0.9})
    packet = adapter.read_packet()
    assert packet.source == "user_input"
    assert packet.features["focus"] == 0.8


# ---------------------------------------------------------------------------
#  4. Calibration profile creation/serialization
# ---------------------------------------------------------------------------


def test_calibration_profile_creation() -> None:
    profile = create_default_calibration_profile()
    assert profile.profile_id.startswith("default_")
    assert profile.proxy_estimates_only is True
    assert profile.closed_loop_allowed is False
    assert "focus" in profile.baseline_features


def test_calibration_profile_serialization() -> None:
    profile = create_default_calibration_profile()
    serialized = serialize_profile(profile)
    deserialized = deserialize_profile(serialized)
    assert deserialized.profile_id == profile.profile_id
    assert deserialized.baseline_features == profile.baseline_features


def test_calibration_from_packets() -> None:
    payload = build_demo_fusion_input()
    profile = calibrate_from_packets(payload.packets)
    assert profile.profile_id.startswith("calibrated_")
    assert "eeg" in profile.modality_baselines


def test_calibration_report_saved(tmp_path, monkeypatch) -> None:
    import app.fusion.calibration as cal_mod

    monkeypatch.setattr(cal_mod, "_ROOT", tmp_path)
    profile = create_default_calibration_profile()
    report = save_calibration_report(profile, run_id="cal_test")
    assert report["json_path"].endswith("fusion_calibration_profile.json")
    assert (
        tmp_path / "reports" / "fusion_calibration" / "cal_test" / "fusion_calibration_report.md"
    ).exists()


# ---------------------------------------------------------------------------
#  5. Fusion validation produces report files
# ---------------------------------------------------------------------------


def test_fusion_validation_produces_reports(tmp_path, monkeypatch) -> None:
    import app.fusion.validation as val_mod

    monkeypatch.setattr(val_mod, "_ROOT", tmp_path)
    result = run_fusion_validation(run_id="val_test")
    assert result["all_checks_passed"] is True or result["all_checks_passed"] is False
    assert (
        tmp_path / "reports" / "fusion_validation" / "val_test" / "fusion_validation_summary.json"
    ).exists()
    assert (
        tmp_path / "reports" / "fusion_validation" / "val_test" / "fusion_ablation_table.csv"
    ).exists()


# ---------------------------------------------------------------------------
#  6. Missing modality increases uncertainty
# ---------------------------------------------------------------------------


def test_missing_modality_increases_uncertainty() -> None:
    full = build_demo_fusion_input()
    sparse = FusionInput(
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
    engine = LateFusionV1()
    full_out = engine.evaluate(full)
    sparse_out = engine.evaluate(sparse)
    assert sparse_out.uncertainty > full_out.uncertainty


# ---------------------------------------------------------------------------
#  7. Low quality increases uncertainty
# ---------------------------------------------------------------------------


def test_low_quality_increases_uncertainty() -> None:
    high = build_demo_fusion_input()
    low = build_demo_fusion_input()
    low.packets[0].quality_score = 0.05
    low.packets[0].confidence = 0.05
    engine = LateFusionV1()
    assert engine.evaluate(low).uncertainty > engine.evaluate(high).uncertainty


# ---------------------------------------------------------------------------
#  8. Contradictory modalities
# ---------------------------------------------------------------------------


def test_contradictory_modalities_effect() -> None:
    # Contradictory inputs should not crash and should produce valid output
    normal = build_demo_fusion_input()
    contradictory = build_demo_fusion_input()
    # Make self-report contradict EEG
    for p in contradictory.packets:
        if p.modality_id == "self_report":
            p.features["focus"] = 0.95
            p.features["relaxation"] = 0.05
            p.features["stress"] = 0.95
    engine = LateFusionV1()
    normal_out = engine.evaluate(normal)
    contra_out = engine.evaluate(contradictory)
    # Both should be valid; stress should differ
    assert contra_out.proxy_estimates_only is True
    assert contra_out.closed_loop_allowed is False
    # Stress proxy should be different (contradictory self-report pushes it)
    assert abs(contra_out.stress_arousal_proxy - normal_out.stress_arousal_proxy) > 0.001


# ---------------------------------------------------------------------------
#  9. IMAGINA manifest validates
# ---------------------------------------------------------------------------


def test_imagina_manifest_validates() -> None:
    result = validate_imagina_manifest("configs/imagina/example_imagina_manifest.json")
    assert result["valid"] is True
    assert result["sample_count"] == 3
    assert result["not_a_trained_model"] is True


# ---------------------------------------------------------------------------
#  10. IMAGINA sample converts to FusionInput
# ---------------------------------------------------------------------------


def test_imagina_sample_converts_to_fusion_input() -> None:
    spec = load_imagina_manifest("configs/imagina/example_imagina_manifest.json")
    assert len(spec.samples) > 0
    fusion_input = convert_imagina_sample_to_fusion_input(
        spec.samples[0], dataset_spec=spec
    )
    assert fusion_input.session_id.startswith("imagina_")
    assert len(fusion_input.packets) > 0
    assert fusion_input.context["not_a_trained_model"] is True
    # Should be evaluable
    output = LateFusionV1().evaluate(fusion_input)
    assert output.proxy_estimates_only is True
    assert output.closed_loop_allowed is False


# ---------------------------------------------------------------------------
#  11. Fusion validation API returns artifact paths
# ---------------------------------------------------------------------------


async def test_fusion_validation_api_returns_artifacts() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/fusion/validate")
    assert response.status_code == 200
    body = response.json()
    assert body["proxy_estimates_only"] is True
    assert body["closed_loop_allowed"] is False
    assert "artifact_paths" in body


async def test_fusion_adapters_api() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/fusion/adapters")
    assert response.status_code == 200
    body = response.json()
    assert "adapters" in body
    assert body["closed_loop_allowed"] is False


async def test_fusion_calibrate_api() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/fusion/calibrate")
    assert response.status_code == 200
    body = response.json()
    assert body["proxy_estimates_only"] is True
    assert body["closed_loop_allowed"] is False
    assert "report_paths" in body


async def test_imagina_manifest_validate_api() -> None:
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/fusion/imagina/manifest/validate")
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True
    assert body["closed_loop_allowed"] is False


# ---------------------------------------------------------------------------
#  12. Fusion protocols are registered
# ---------------------------------------------------------------------------


def test_fusion_validation_protocol_registered() -> None:
    protocol = get_protocol("fusion_validation_protocol")
    assert protocol is not None
    assert protocol.closed_loop_allowed_default is False
    assert protocol.supports_auto_run is True


def test_imagina_bridge_validation_protocol_registered() -> None:
    protocol = get_protocol("imagina_bridge_validation_protocol")
    assert protocol is not None
    assert protocol.closed_loop_allowed_default is False
    assert protocol.supports_auto_run is True


# ---------------------------------------------------------------------------
#  13. closed_loop_allowed remains false
# ---------------------------------------------------------------------------


def test_closed_loop_always_false_in_fusion() -> None:
    output = LateFusionV1().evaluate(build_demo_fusion_input())
    assert output.closed_loop_allowed is False
    assert output.proxy_estimates_only is True


def test_closed_loop_false_in_protocols() -> None:
    for pid in [
        "fusion_validation_protocol",
        "imagina_bridge_validation_protocol",
        "multimodal_fusion_demo_protocol",
    ]:
        protocol = get_protocol(pid)
        assert protocol is not None
        assert protocol.closed_loop_allowed_default is False


# ---------------------------------------------------------------------------
#  Adapter registry
# ---------------------------------------------------------------------------


def test_adapter_registry_lists_adapters() -> None:
    adapters = list_adapters()
    assert len(adapters) >= 3
    ids = [a["adapter_id"] for a in adapters]
    assert "simulated_gaze_v1" in ids
    assert "simulated_physiology_v1" in ids
    assert "self_report_v1" in ids


def test_adapter_statuses() -> None:
    statuses = get_adapter_statuses()
    assert "simulated_gaze_v1" in statuses
    assert statuses["simulated_gaze_v1"]["source_type"] == "simulated"


# ---------------------------------------------------------------------------
#  CSV replay adapter
# ---------------------------------------------------------------------------


def test_csv_replay_adapter_not_available_without_file() -> None:
    adapter = CSVReplayAdapter()
    assert adapter.is_available() is False
    packet = adapter.read_packet()
    assert packet.missing is True


def test_csv_replay_adapter_loads_csv(tmp_path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "alpha_power,beta_power,quality_score\n0.5,0.6,0.7\n0.55,0.65,0.75\n"
    )
    adapter = CSVReplayAdapter(
        file_path=csv_file,
        target_modality="eeg",
    )
    assert adapter.is_available()
    loaded = adapter.load()
    assert loaded == 2
    packet = adapter.read_packet()
    assert packet.modality_id == "eeg"
    assert packet.source == "replay"
    assert "alpha_power" in packet.features
