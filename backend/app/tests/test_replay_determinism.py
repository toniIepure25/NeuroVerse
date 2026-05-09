from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from app.policy.behavior_tree import evaluate_behavior_tree
from app.safety.safety_gate import SafetyGate
from app.schemas.events import BaseEvent
from app.schemas.state import StatePredictionPayload
from app.sessions.recorder import SessionRecorder
from app.sessions.replay import SessionReplayer


def _state(focus=0.5, stress=0.3, **kw) -> StatePredictionPayload:
    return StatePredictionPayload(
        focus=focus, relaxation=0.5, workload=0.5,
        stress=stress, fatigue=0.3, imagery_engagement=0.3,
        confidence=0.8, **kw,
    )


class TestReplayDeterminism:
    def test_record_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            recorder = SessionRecorder("det-test", base_dir=Path(tmpdir))
            states = [
                _state(focus=0.3, stress=0.2),
                _state(focus=0.8, stress=0.1),
                _state(focus=0.5, stress=0.85),
            ]
            gate = SafetyGate()
            sqi = {"eeg": 0.9, "physio": 0.85, "gaze": 0.88, "multimodal": 0.87}
            recorded_actions = []
            for i, st in enumerate(states):
                safety = gate.evaluate(st, sqi)
                action = evaluate_behavior_tree(st, safety)
                recorded_actions.append(action.action)
                event = BaseEvent(
                    session_id="det-test",
                    event_type="neuroverse.state.predicted",
                    timestamp=float(i),
                    source="test",
                    payload=st.model_dump(),
                )
                recorder.record(event)
                action_event = BaseEvent(
                    session_id="det-test",
                    event_type="neuroverse.adaptation.action",
                    timestamp=float(i) + 0.01,
                    source="test",
                    payload=action.model_dump(),
                )
                recorder.record(action_event)
            recorder.close()

            replayer = SessionReplayer("det-test", base_dir=Path(tmpdir))
            events = replayer.load_events()
            assert len(events) == 6

            replayed_actions = []
            for ev in events:
                if ev.event_type == "neuroverse.state.predicted":
                    st = StatePredictionPayload(**ev.payload)
                    safety = gate.evaluate(st, sqi)
                    action = evaluate_behavior_tree(st, safety)
                    replayed_actions.append(action.action)

            assert replayed_actions == recorded_actions

    def test_missing_session_raises(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(Exception):
                SessionReplayer("nonexistent", base_dir=Path(tmpdir))
