from __future__ import annotations

from pathlib import Path

import pytest

from app.api.routes_evaluation import api_get_report, api_latest_report, api_list_reports
from app.api.routes_models import api_activate_model, api_deactivate_model, api_get_active_model
from app.api.routes_runtime import api_runtime_status
from app.api.routes_sessions import get_summary
from app.datasets.validation import validate_dataset_config
from app.inference.model_loader import (
    ModelActivationError,
    validate_model_for_activation,
)
from app.ml.baselines import create_baseline_model
from app.ml.registry import register_model
from app.ml.reports import write_experiment_report
from app.schemas.events import BaseEvent
from app.schemas.state import StatePredictionPayload
from app.sessions.recorder import SessionRecorder
from app.sessions.summary import summarize_session

ROOT = Path(__file__).resolve().parents[3]


def test_dataset_validation_report_generated_for_synthetic(tmp_path: Path) -> None:
    report = validate_dataset_config(
        ROOT / "configs" / "datasets" / "synthetic.yaml",
        target="phase_label",
        output_dir=tmp_path,
    )
    assert report["ok"]
    assert report["window_count"] > 0
    assert (tmp_path / "synthetic_phase_demo_validation.json").exists()
    assert (tmp_path / "synthetic_phase_demo_validation.md").exists()


def test_dataset_validation_warns_on_one_subject_leakage(tmp_path: Path) -> None:
    report = validate_dataset_config(
        ROOT / "configs" / "datasets" / "synthetic.yaml",
        target="phase_label",
        output_dir=tmp_path,
    )
    assert any("Only one subject" in warning for warning in report["warnings"])
    assert any("group split" in warning for warning in report["warnings"])


def test_dataset_validation_detects_constant_features(tmp_path: Path) -> None:
    csv_path = tmp_path / "constant.csv"
    csv_path.write_text(
        "\n".join(
            [
                "timestamp,subject_id,session_id,label,eeg_constant,physio_signal",
                "0,s1,a,low,1,0.1",
                "1,s1,a,low,1,0.2",
                "2,s1,a,high,1,0.9",
                "3,s1,a,high,1,1.0",
                "4,s1,a,high,1,0.8",
                "5,s1,a,high,1,0.7",
            ]
        )
    )
    report = validate_dataset_config(
        {
            "dataset_id": "constant_fixture",
            "type": "generic_csv",
            "path": str(csv_path),
            "timestamp_col": "timestamp",
            "label_col": "label",
            "feature_cols": ["eeg_constant", "physio_signal"],
            "window_size_seconds": 2,
            "overlap": 0,
        },
        target="label",
        output_dir=tmp_path,
    )
    assert "eeg_constant" in report["feature_analysis"]["constant_columns"]


def test_model_activation_validation_succeeds_for_compatible_synthetic_model() -> None:
    status = validate_model_for_activation("synthetic_phase_rf", models_dir=ROOT / "models")
    assert status["active_estimator"] == "learned"
    assert status["prediction_semantics"] == "phase_proxy"


def test_model_activation_validation_fails_for_missing_model(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        validate_model_for_activation("missing", models_dir=tmp_path)


def test_model_activation_validation_fails_for_incompatible_features(tmp_path: Path) -> None:
    model = create_baseline_model("random_forest", {"n_estimators": 2}, ["bad_feature"])
    model.fit([[0], [1]], ["a", "b"])
    register_model(
        model,
        "bad_model",
        {
            "dataset_id": "unit",
            "target": "label",
            "prediction_semantics": "phase_proxy",
            "feature_names": ["bad_feature"],
        },
        models_dir=tmp_path,
    )
    with pytest.raises(ModelActivationError):
        validate_model_for_activation("bad_model", models_dir=tmp_path)


@pytest.mark.asyncio
async def test_model_active_and_deactivate_endpoints() -> None:
    activated = await api_activate_model("synthetic_phase_rf")
    assert activated["active_estimator"] == "learned"
    deactivate = await api_deactivate_model()
    assert deactivate["active_estimator"] == "heuristic"
    active = await api_get_active_model()
    assert active["active_estimator"] == "heuristic"


@pytest.mark.asyncio
async def test_runtime_status_endpoint() -> None:
    data = await api_runtime_status()
    assert "active_estimator" in data
    assert "current_data_source" in data


def _write_summary_fixture(tmp_path: Path, session_id: str = "summary_fixture") -> None:
    recorder = SessionRecorder(session_id, base_dir=tmp_path)
    state = StatePredictionPayload(
        focus=0.7,
        relaxation=0.4,
        workload=0.3,
        stress=0.2,
        fatigue=0.1,
        imagery_engagement=0.2,
        confidence=0.8,
    )
    recorder.record(
        BaseEvent(
            session_id=session_id,
            event_type="neuroverse.state.predicted",
            timestamp=0,
            source="test",
            payload=state.model_dump(),
        )
    )
    recorder.record(
        BaseEvent(
            session_id=session_id,
            event_type="neuroverse.safety.decision",
            timestamp=0,
            source="test",
            payload={"decision": "ALLOWED", "reason": "test", "confidence": 0.8},
        )
    )
    recorder.record(
        BaseEvent(
            session_id=session_id,
            event_type="neuroverse.adaptation.action",
            timestamp=0,
            source="test",
            payload={"action": "MaintainBaseline", "intensity": 0, "duration_ms": 0},
        )
    )
    recorder.close()


def test_replay_summary_contains_required_metrics(tmp_path: Path) -> None:
    _write_summary_fixture(tmp_path)
    summary = summarize_session("summary_fixture", base_dir=tmp_path)
    assert summary["total_events"] == 3
    assert summary["total_state_predictions"] == 1
    assert summary["safety_block_rate"] == 0
    assert summary["maintain_baseline_events"] == 1
    assert (tmp_path / "summary_fixture_summary.json").exists()


@pytest.mark.asyncio
async def test_session_summary_endpoint_works() -> None:
    session_id = "api_summary_fixture"
    recorder = SessionRecorder(session_id)
    recorder.record(
        BaseEvent(
            session_id=session_id,
            event_type="neuroverse.adaptation.action",
            timestamp=0,
            source="test",
            payload={"action": "MaintainBaseline", "intensity": 0, "duration_ms": 0},
        )
    )
    recorder.close()
    summary = await get_summary(session_id)
    assert summary["session_id"] == session_id


@pytest.mark.asyncio
async def test_evaluation_reports_latest_and_detail_endpoints(tmp_path: Path) -> None:
    report_dir = ROOT / "reports" / "experiments" / "9999_test_phase25"
    write_experiment_report(
        report_dir,
        title="Phase 2.5 Test Report",
        dataset_metadata={"dataset_id": "unit", "source": "test"},
        model_metadata={"model_id": "unit", "model_type": "rf", "target": "label"},
        metrics={"accuracy": 1.0, "balanced_accuracy": 1.0, "macro_f1": 1.0},
    )
    reports = await api_list_reports()
    assert any(item["report_id"] == "9999_test_phase25" for item in reports)
    latest = await api_latest_report()
    assert latest["report_id"] == "9999_test_phase25"
    detail = await api_get_report("9999_test_phase25")
    assert "Phase 2.5 Test Report" in detail["markdown"]
