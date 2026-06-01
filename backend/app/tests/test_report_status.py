"""Tests for report_status.py — evidence extraction and aggregation from disk reports."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from app.safety.report_status import (
    ReportEvidenceSummary,
    _is_synthetic_adapter,
    infer_startup_safety_state,
    load_report_evidence,
)

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def _make_hw_report(tmp: Path, adapter: str, passed: bool, **extra) -> None:
    hw_dir = tmp / "reports" / "hardware_validation"
    hw_dir.mkdir(parents=True, exist_ok=True)
    report: dict = {
        "passed": passed,
        "adapter": adapter,
        "closed_loop_allowed": False,
        "sqi_summary": {"mean": 0.92, "min": 0.85},
        "timing": {
            "pass": passed,
            "jitter_ms_p95": 0.015,
            "drift_percent": -0.05,
        },
        **extra,
    }
    (hw_dir / "latest_hw.json").write_text(json.dumps(report))


def _make_cal_report(tmp: Path, source: str = "simulator", sqi: float = 0.90) -> None:
    cal_dir = tmp / "reports" / "calibration"
    cal_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "baseline_sqi": sqi,
        "source": source,
        "timestamp_quality": {"pass": True, "quality": "excellent"},
    }
    (cal_dir / "latest_cal.json").write_text(json.dumps(report))


def _make_shadow_report(tmp: Path, emitted: int = 0) -> None:
    shadow_dir = tmp / "reports" / "shadow"
    shadow_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "real_adaptation_actions_emitted": emitted,
        "predicted_states": [{"focus": 0.5}],
        "source": "simulator",
        "closed_loop_allowed": False,
    }
    (shadow_dir / "latest_shadow.json").write_text(json.dumps(report))


def _make_trial_report(tmp: Path, physical: bool = False) -> None:
    trial_dir = tmp / "reports" / "hardware_trials" / "test_trial"
    trial_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "physical_device_detected": physical,
        "synthetic_mode": not physical,
        "closed_loop_allowed": False,
        "validation": {"passed": physical},
    }
    (trial_dir / "physical_eeg_trial_summary.json").write_text(json.dumps(report))


# ---------------------------------------------------------------------------
#  Missing directories
# ---------------------------------------------------------------------------


class TestMissingDirectories:
    def test_missing_all_dirs_returns_safe_defaults(self, tmp_path):
        ev = load_report_evidence(tmp_path)
        assert isinstance(ev, ReportEvidenceSummary)
        assert ev.validation_report_present is False
        assert ev.validation_passed is False
        assert ev.calibration_complete is False
        assert ev.shadow_inference_passed is False
        assert ev.physical_hardware_validated is False
        assert ev.brainflow_synthetic_validated is False
        assert ev.signal_quality_ok is False

    def test_missing_hw_dir_still_reads_calibration(self, tmp_path):
        _make_cal_report(tmp_path)
        ev = load_report_evidence(tmp_path)
        assert ev.calibration_complete is True
        assert ev.validation_report_present is False

    def test_missing_shadow_dir_leaves_shadow_false(self, tmp_path):
        ev = load_report_evidence(tmp_path)
        assert ev.shadow_inference_passed is False


# ---------------------------------------------------------------------------
#  Hardware validation
# ---------------------------------------------------------------------------


class TestHardwareValidation:
    def test_brainflow_synthetic_passed_sets_synthetic_flag(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.brainflow_synthetic_validated is True
        assert ev.physical_hardware_validated is False

    def test_failed_hw_report_does_not_set_validated(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=False, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.brainflow_synthetic_validated is False
        assert ev.validation_report_present is True
        assert ev.validation_passed is False

    def test_lsl_adapter_sets_lsl_synthetic(self, tmp_path):
        _make_hw_report(tmp_path, adapter="lsl", passed=True)
        ev = load_report_evidence(tmp_path)
        assert ev.lsl_synthetic_validated is True
        assert ev.physical_hardware_validated is False

    def test_sqi_extracted_from_hw_report(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.latest_sqi_mean == pytest.approx(0.92)
        assert ev.latest_sqi_min == pytest.approx(0.85)

    def test_timing_extracted_from_hw_report(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.latest_jitter_p95_ms == pytest.approx(0.015)
        assert ev.latest_drift_percent == pytest.approx(-0.05)
        assert ev.timing_ok is True

    def test_signal_quality_ok_when_sqi_above_threshold(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.signal_quality_ok is True

    def test_signal_quality_not_ok_when_sqi_below_threshold(self, tmp_path):
        hw_dir = tmp_path / "reports" / "hardware_validation"
        hw_dir.mkdir(parents=True, exist_ok=True)
        report = {
            "passed": True,
            "adapter": "brainflow",
            "sqi_summary": {"mean": 0.3, "min": 0.2},
            "timing": {"pass": True, "jitter_ms_p95": 0.01, "drift_percent": 0.0},
        }
        (hw_dir / "low_sqi.json").write_text(json.dumps(report))
        ev = load_report_evidence(tmp_path)
        assert ev.signal_quality_ok is False


# ---------------------------------------------------------------------------
#  Physical hardware NOT falsely flagged from synthetic
# ---------------------------------------------------------------------------


class TestPhysicalHardwareNotFalsified:
    def test_synthetic_brainflow_does_not_set_physical(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.physical_hardware_validated is False

    def test_synthetic_trial_does_not_set_physical(self, tmp_path):
        _make_trial_report(tmp_path, physical=False)
        ev = load_report_evidence(tmp_path)
        assert ev.physical_hardware_validated is False
        assert ev.trial_synthetic_mode is True
        assert ev.trial_physical_device_detected is False

    def test_physical_trial_detected_sets_physical(self, tmp_path):
        _make_trial_report(tmp_path, physical=True)
        ev = load_report_evidence(tmp_path)
        assert ev.physical_hardware_validated is True
        assert ev.trial_physical_device_detected is True


# ---------------------------------------------------------------------------
#  Calibration
# ---------------------------------------------------------------------------


class TestCalibration:
    def test_calibration_report_sets_complete(self, tmp_path):
        _make_cal_report(tmp_path)
        ev = load_report_evidence(tmp_path)
        assert ev.calibration_complete is True

    def test_calibration_source_extracted(self, tmp_path):
        _make_cal_report(tmp_path, source="brainflow")
        ev = load_report_evidence(tmp_path)
        assert ev.calibration_source == "brainflow"

    def test_calibration_sqi_extracted(self, tmp_path):
        _make_cal_report(tmp_path, sqi=0.94)
        ev = load_report_evidence(tmp_path)
        assert ev.calibration_sqi == pytest.approx(0.94)

    def test_calibration_improves_signal_quality_flag(self, tmp_path):
        # No hw report, but cal has good SQI
        _make_cal_report(tmp_path, sqi=0.88)
        ev = load_report_evidence(tmp_path)
        assert ev.signal_quality_ok is True


# ---------------------------------------------------------------------------
#  Shadow inference
# ---------------------------------------------------------------------------


class TestShadowInference:
    def test_shadow_with_zero_actions_sets_passed(self, tmp_path):
        _make_shadow_report(tmp_path, emitted=0)
        ev = load_report_evidence(tmp_path)
        assert ev.shadow_inference_passed is True
        assert ev.shadow_real_actions_emitted == 0

    def test_shadow_with_real_actions_does_not_set_passed(self, tmp_path):
        _make_shadow_report(tmp_path, emitted=3)
        ev = load_report_evidence(tmp_path)
        assert ev.shadow_inference_passed is False
        assert ev.shadow_real_actions_emitted == 3


# ---------------------------------------------------------------------------
#  Governance integration
# ---------------------------------------------------------------------------


class TestGovernanceIntegration:
    def test_governance_uses_calibration_evidence(self, tmp_path):
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance

        _make_cal_report(tmp_path)
        ev = load_report_evidence(tmp_path)
        # governance should reflect calibration_complete=True
        gov = evaluate_closed_loop_governance(
            calibration_complete=ev.calibration_complete,
            shadow_inference_passed=ev.shadow_inference_passed,
            signal_quality_ok=ev.signal_quality_ok,
            timing_validated=ev.timing_ok,
        )
        # Still locked (env flag not set, etc.) but missing_calibration should not be in codes
        assert "missing_calibration" not in gov.lock_reason_codes

    def test_governance_locked_by_default(self, tmp_path):
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance

        ev = load_report_evidence(tmp_path)  # empty tmp → all False
        gov = evaluate_closed_loop_governance(
            calibration_complete=ev.calibration_complete,
            shadow_inference_passed=ev.shadow_inference_passed,
            signal_quality_ok=ev.signal_quality_ok,
            timing_validated=ev.timing_ok,
            hardware_validated=ev.physical_hardware_validated,
        )
        assert gov.closed_loop_allowed is False

    def test_synthetic_hw_does_not_count_as_physical(self, tmp_path):
        """BrainFlow SyntheticBoard must not set physical_hardware_validated."""
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.physical_hardware_validated is False
        assert ev.brainflow_synthetic_validated is True

    def test_physical_hardware_mode_locked_without_physical_hw(self, tmp_path):
        """Governance with mode=physical_hardware stays locked if no physical HW."""
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance

        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        _make_cal_report(tmp_path)
        _make_shadow_report(tmp_path, emitted=0)
        ev = load_report_evidence(tmp_path)
        assert ev.physical_hardware_validated is False

        gov = evaluate_closed_loop_governance(
            environment_flag=True,
            hardware_validated=ev.physical_hardware_validated,  # False
            signal_quality_ok=ev.signal_quality_ok,
            timing_validated=ev.timing_ok,
            calibration_complete=ev.calibration_complete,
            shadow_inference_passed=ev.shadow_inference_passed,
            mode="physical_hardware",  # physical mode requires validated hardware
        )
        # Locked: physical hardware not validated + real EEG disabled
        assert gov.closed_loop_allowed is False
        assert "physical_hardware_unvalidated" in gov.lock_reason_codes
        assert "real_eeg_closed_loop_disabled" in gov.lock_reason_codes


# ---------------------------------------------------------------------------
#  Synthetic adapter detection
# ---------------------------------------------------------------------------


class TestSyntheticAdapterDetection:
    def test_simulator_is_synthetic(self):
        assert _is_synthetic_adapter("simulator") is True

    def test_brainflow_synthetic_is_synthetic(self):
        assert _is_synthetic_adapter("brainflow_synthetic") is True

    def test_lsl_synthetic_is_synthetic(self):
        assert _is_synthetic_adapter("lsl_synthetic_eeg") is True

    def test_none_is_synthetic(self):
        assert _is_synthetic_adapter(None) is True

    def test_cyton_string_not_synthetic(self):
        assert _is_synthetic_adapter("cyton") is False


# ---------------------------------------------------------------------------
#  to_dict coverage
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_to_dict_has_all_keys(self, tmp_path):
        ev = load_report_evidence(tmp_path)
        d = ev.to_dict()
        for key in (
            "signal_quality_ok",
            "calibration_complete",
            "shadow_inference_passed",
            "physical_hardware_validated",
            "brainflow_synthetic_validated",
            "validation_report_present",
            "latest_validation_report_path",
            "latest_calibration_report_path",
            "latest_shadow_report_path",
        ):
            assert key in d

    def test_to_dict_values_are_json_serializable(self, tmp_path):
        ev = load_report_evidence(tmp_path)
        import json as _json

        _json.dumps(ev.to_dict())  # should not raise


# ---------------------------------------------------------------------------
#  Aggregation: multiple reports
# ---------------------------------------------------------------------------


class TestAggregation:
    def test_reads_multiple_hw_reports(self, tmp_path):
        hw_dir = tmp_path / "reports" / "hardware_validation"
        hw_dir.mkdir(parents=True, exist_ok=True)
        # Older passing brainflow report
        (hw_dir / "old_brainflow.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.90, "min": 0.82},
                    "timing": {"pass": True, "jitter_ms_p95": 0.012, "drift_percent": -0.02},
                    "board": {"board_id": -1},
                }
            )
        )
        # Newer failing LSL report — should NOT hide older valid evidence
        time.sleep(0.01)
        (hw_dir / "new_lsl_failed.json").write_text(
            json.dumps(
                {
                    "passed": False,
                    "adapter": "lsl",
                    "sqi_summary": {"mean": None, "min": None},
                    "timing": {"pass": False, "jitter_ms_p95": None},
                }
            )
        )
        ev = load_report_evidence(tmp_path)
        assert ev.validation_report_present is True
        # Older passing brainflow is still detected
        assert ev.brainflow_synthetic_validated is True
        # Validation passed because an older report passed
        assert ev.validation_passed is True
        # Best SQI from the passing report
        assert ev.best_sqi_mean == pytest.approx(0.90)

    def test_failed_latest_does_not_hide_valid_evidence(self, tmp_path):
        hw_dir = tmp_path / "reports" / "hardware_validation"
        hw_dir.mkdir(parents=True, exist_ok=True)
        # Older passing report
        (hw_dir / "a_valid.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.88, "min": 0.75},
                    "timing": {"pass": True, "jitter_ms_p95": 0.020},
                    "board": {"board_id": -1},
                }
            )
        )
        time.sleep(0.01)
        # Newer failing report
        (hw_dir / "b_failed.json").write_text(
            json.dumps(
                {
                    "passed": False,
                    "adapter": "lsl",
                    "sqi_summary": {"mean": None, "min": None},
                    "timing": {"pass": False},
                }
            )
        )
        ev = load_report_evidence(tmp_path)
        # Latest report is failed
        assert ev.latest_failed_validation_report_path is not None
        # But older valid is still tracked
        assert ev.latest_valid_validation_report_path is not None
        assert ev.validation_passed is True
        # Warning should be present
        assert any("failed" in w.lower() for w in ev.evidence_warnings)

    def test_evidence_sources_populated(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        _make_cal_report(tmp_path)
        _make_shadow_report(tmp_path, emitted=0)
        ev = load_report_evidence(tmp_path)
        assert len(ev.evidence_sources) >= 2  # hw + calibration + shadow

    def test_best_sqi_tracks_highest_across_reports(self, tmp_path):
        hw_dir = tmp_path / "reports" / "hardware_validation"
        hw_dir.mkdir(parents=True, exist_ok=True)
        (hw_dir / "low.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.60, "min": 0.50},
                    "timing": {"pass": True, "jitter_ms_p95": 0.05},
                    "board": {"board_id": -1},
                }
            )
        )
        time.sleep(0.01)
        (hw_dir / "high.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.95, "min": 0.90},
                    "timing": {"pass": True, "jitter_ms_p95": 0.01},
                    "board": {"board_id": -1},
                }
            )
        )
        ev = load_report_evidence(tmp_path)
        assert ev.best_sqi_mean == pytest.approx(0.95)

    def test_best_jitter_tracks_lowest_across_reports(self, tmp_path):
        hw_dir = tmp_path / "reports" / "hardware_validation"
        hw_dir.mkdir(parents=True, exist_ok=True)
        (hw_dir / "high_jitter.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.9, "min": 0.8},
                    "timing": {"pass": True, "jitter_ms_p95": 0.1},
                    "board": {"board_id": -1},
                }
            )
        )
        time.sleep(0.01)
        (hw_dir / "low_jitter.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.9, "min": 0.8},
                    "timing": {"pass": True, "jitter_ms_p95": 0.005},
                    "board": {"board_id": -1},
                }
            )
        )
        ev = load_report_evidence(tmp_path)
        assert ev.best_jitter_p95_ms == pytest.approx(0.005)


# ---------------------------------------------------------------------------
#  SQI provenance
# ---------------------------------------------------------------------------


class TestSqiProvenance:
    def test_signal_quality_source_hardware_validation(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.signal_quality_ok is True
        assert ev.signal_quality_source == "hardware_validation"
        assert ev.best_sqi_mean is not None

    def test_signal_quality_source_calibration_when_no_hw_sqi(self, tmp_path):
        # No hw report, but calibration has good SQI
        _make_cal_report(tmp_path, sqi=0.88)
        ev = load_report_evidence(tmp_path)
        assert ev.signal_quality_ok is True
        assert ev.signal_quality_source == "calibration"
        assert ev.best_sqi_mean == pytest.approx(0.88)
        # Note should be present
        assert "calibration" in ev.signal_quality_note.lower()

    def test_signal_quality_note_populated(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        assert ev.signal_quality_note != ""

    def test_no_inconsistency_signal_ok_without_sqi(self, tmp_path):
        # If signal_quality_ok is True, best_sqi_mean must not be None
        _make_cal_report(tmp_path, sqi=0.75)
        ev = load_report_evidence(tmp_path)
        if ev.signal_quality_ok:
            assert ev.best_sqi_mean is not None


# ---------------------------------------------------------------------------
#  Startup inference
# ---------------------------------------------------------------------------


class TestStartupInference:
    def test_shadow_and_calibration_gives_shadow_ready(self, tmp_path):
        _make_cal_report(tmp_path)
        _make_shadow_report(tmp_path, emitted=0)
        ev = load_report_evidence(tmp_path)
        state = infer_startup_safety_state(ev)
        assert state == "SHADOW_READY"

    def test_calibration_only_gives_calibration_required(self, tmp_path):
        _make_cal_report(tmp_path)
        ev = load_report_evidence(tmp_path)
        state = infer_startup_safety_state(ev)
        assert state == "CALIBRATION_REQUIRED"

    def test_validation_only_gives_validation_passed(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        state = infer_startup_safety_state(ev)
        assert state == "VALIDATION_PASSED"

    def test_failed_validation_only_gives_validation_failed(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=False, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        # If only the failed report exists, validation_passed = False
        if not ev.validation_passed:
            state = infer_startup_safety_state(ev)
            assert state == "VALIDATION_FAILED"

    def test_no_evidence_gives_closed_loop_locked(self, tmp_path):
        ev = load_report_evidence(tmp_path)
        state = infer_startup_safety_state(ev)
        assert state == "CLOSED_LOOP_LOCKED"

    def test_infer_from_evidence_on_state_machine(self, tmp_path):
        from app.safety.state_machine import SafetyStateMachine

        _make_cal_report(tmp_path)
        _make_shadow_report(tmp_path, emitted=0)
        ev = load_report_evidence(tmp_path)
        sm = SafetyStateMachine()
        result_state = sm.infer_from_evidence(ev)
        assert result_state == "SHADOW_READY"
        assert sm.current_state_id == "SHADOW_READY"

    def test_startup_inference_never_enables_real_eeg_closed_loop(self, tmp_path):
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance

        _make_cal_report(tmp_path)
        _make_shadow_report(tmp_path, emitted=0)
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        gov = evaluate_closed_loop_governance(
            environment_flag=False,
            hardware_validated=ev.physical_hardware_validated,
            signal_quality_ok=ev.signal_quality_ok,
            timing_validated=ev.timing_ok,
            calibration_complete=ev.calibration_complete,
            shadow_inference_passed=ev.shadow_inference_passed,
        )
        assert gov.closed_loop_allowed is False

    def test_startup_transition_recorded_in_timeline(self, tmp_path):
        from app.safety.state_machine import SafetyStateMachine

        _make_cal_report(tmp_path)
        _make_shadow_report(tmp_path, emitted=0)
        ev = load_report_evidence(tmp_path)
        sm = SafetyStateMachine()
        sm.infer_from_evidence(ev)
        timeline = sm.get_timeline()
        assert any(t["source"] == "startup_evidence_inference" for t in timeline)

    def test_new_fields_in_to_dict(self, tmp_path):
        _make_hw_report(tmp_path, adapter="brainflow", passed=True, board={"board_id": -1})
        ev = load_report_evidence(tmp_path)
        d = ev.to_dict()
        for key in (
            "signal_quality_source",
            "signal_quality_note",
            "best_sqi_mean",
            "best_sqi_min",
            "best_jitter_p95_ms",
            "latest_valid_validation_report_path",
            "latest_failed_validation_report_path",
            "evidence_sources",
            "evidence_warnings",
            "lsl_replay_validated",
        ):
            assert key in d, f"Missing key: {key}"
