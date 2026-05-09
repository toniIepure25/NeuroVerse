from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.adaptation import AdaptationActionPayload
from app.schemas.events import BaseEvent
from app.schemas.safety import SafetyDecisionPayload
from app.schemas.session import FeaturePayload, SessionSummaryPayload
from app.schemas.signals import RawSignalPayload
from app.schemas.state import StatePredictionPayload


class TestBaseEvent:
    def test_valid_event(self):
        e = BaseEvent(
            session_id="test-001",
            event_type="neuroverse.session.started",
            timestamp=1.0,
            source="test",
        )
        assert e.session_id == "test-001"
        assert e.event_id  # auto-generated

    def test_invalid_event_type(self):
        with pytest.raises(ValidationError):
            BaseEvent(
                session_id="test",
                event_type="invalid.type",
                timestamp=0,
                source="test",
            )


class TestStatePrediction:
    def test_valid_state(self):
        s = StatePredictionPayload(
            focus=0.8, relaxation=0.5, workload=0.3,
            stress=0.2, fatigue=0.1, imagery_engagement=0.4,
            confidence=0.9,
        )
        assert s.focus == 0.8

    def test_rejects_out_of_range(self):
        with pytest.raises(ValidationError):
            StatePredictionPayload(
                focus=1.5, relaxation=0.5, workload=0.3,
                stress=0.2, fatigue=0.1, imagery_engagement=0.4,
                confidence=0.9,
            )

    def test_rejects_negative(self):
        with pytest.raises(ValidationError):
            StatePredictionPayload(
                focus=-0.1, relaxation=0.5, workload=0.3,
                stress=0.2, fatigue=0.1, imagery_engagement=0.4,
                confidence=0.9,
            )


class TestSafetyDecision:
    def test_valid_decision(self):
        d = SafetyDecisionPayload(
            decision="ALLOWED",
            reason="No safety issue",
            confidence=0.85,
        )
        assert d.decision == "ALLOWED"

    def test_invalid_decision(self):
        with pytest.raises(ValidationError):
            SafetyDecisionPayload(
                decision="INVALID",
                reason="test",
                confidence=0.5,
            )


class TestAdaptationAction:
    def test_valid_action(self):
        a = AdaptationActionPayload(
            action="IncreaseSceneClarity",
            intensity=0.7,
            duration_ms=2000,
        )
        assert a.intensity == 0.7

    def test_rejects_negative_intensity(self):
        with pytest.raises(ValidationError):
            AdaptationActionPayload(action="test", intensity=-0.1, duration_ms=0)


class TestRawSignalPayload:
    def test_valid_signal(self):
        s = RawSignalPayload(
            modality="eeg",
            sampling_rate=250.0,
            channel_names=["Fp1", "Fp2"],
            data=[[0.1, 0.2], [0.3, 0.4]],
            window_size_ms=500,
        )
        assert s.modality == "eeg"

    def test_rejects_invalid_modality(self):
        with pytest.raises(ValidationError):
            RawSignalPayload(
                modality="invalid",
                sampling_rate=250.0,
                channel_names=["x"],
                data=[[1.0]],
                window_size_ms=500,
            )


class TestFeaturePayload:
    def test_defaults(self):
        f = FeaturePayload()
        assert f.eeg == {}
        assert f.sqi_scores == {}


class TestSessionSummary:
    def test_valid(self):
        s = SessionSummaryPayload(
            session_id="s1", started_at=0.0, ended_at=180.0,
            total_events=100, average_focus=0.7,
        )
        assert s.total_events == 100

    def test_rejects_out_of_range_scores(self):
        with pytest.raises(ValidationError):
            SessionSummaryPayload(
                session_id="s1", started_at=0, ended_at=1,
                average_focus=1.5,
            )
