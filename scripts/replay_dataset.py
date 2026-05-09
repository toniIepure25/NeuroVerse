"""Replay dataset windows through the NeuroVerse feature/state/safety/policy pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.datasets.registry import create_dataset_adapter
from app.inference.heuristic_model import HeuristicStateEstimator
from app.ml.feature_dataset import build_feature_dataset
from app.policy.adaptation_policy import AdaptationPolicy
from app.safety.safety_gate import SafetyGate
from app.schemas.events import BaseEvent
from app.schemas.session import FeaturePayload
from app.sessions.recorder import SessionRecorder
from app.sessions.summary import summarize_session


def _payload_from_flat(row: dict[str, float]) -> FeaturePayload:
    buckets = {"eeg": {}, "physio": {}, "gaze": {}, "multimodal": {}, "sqi": {}}
    for key, value in row.items():
        prefix, _, name = key.partition("_")
        if prefix == "sqi":
            buckets["sqi"][name] = value
        elif prefix in buckets and name:
            buckets[prefix][name] = value
    return FeaturePayload(
        eeg=buckets["eeg"],
        physio=buckets["physio"],
        gaze=buckets["gaze"],
        multimodal=buckets["multimodal"],
        sqi_scores=buckets["sqi"],
    )


def _learned_estimator(model_dir: str):
    from app.inference.learned_model import LearnedModelEstimator

    return LearnedModelEstimator.from_model_dir(model_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a dataset through NeuroVerse offline")
    parser.add_argument("--dataset-config", required=True)
    parser.add_argument(
        "--speed", type=float, default=1.0, help="Recorded as metadata only for offline replay"
    )
    parser.add_argument("--use-model", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--session-id", default=None)
    args = parser.parse_args()

    adapter = create_dataset_adapter(args.dataset_config)
    samples = list(adapter.iter_windows())
    dataset = build_feature_dataset(samples)
    estimator = (
        _learned_estimator(args.use_model)
        if args.use_model
        else HeuristicStateEstimator()
    )
    gate = SafetyGate()
    policy = AdaptationPolicy()
    session_id = args.session_id or f"dataset-{adapter.dataset_id}"
    recorder = SessionRecorder(
        session_id, base_dir=Path(args.output_dir) if args.output_dir else None
    )
    recorder.record(
        BaseEvent(
            session_id=session_id,
            event_type="neuroverse.replay.started",
            timestamp=0.0,
            source="dataset_replay",
            payload={"dataset_id": adapter.dataset_id, "speed": args.speed},
        )
    )
    for i, sample in enumerate(samples):
        row = {name: float(dataset.X[i, j]) for j, name in enumerate(dataset.feature_names)}
        features = _payload_from_flat(row)
        ts = float(sample.start_time)
        recorder.record(
            BaseEvent(
                session_id=session_id,
                event_type="neuroverse.features.extracted",
                timestamp=ts,
                source="dataset_replay",
                payload=features.model_dump(),
                metadata={"sample_id": sample.sample_id, "labels": sample.labels},
            )
        )
        prediction = estimator.predict(features)
        recorder.record(
            BaseEvent(
                session_id=session_id,
                event_type="neuroverse.state.predicted",
                timestamp=ts,
                source="dataset_replay",
                payload=prediction.model_dump(),
                metadata={"sample_id": sample.sample_id},
            )
        )
        safety = gate.evaluate(prediction, features.sqi_scores, policy.action_history)
        recorder.record(
            BaseEvent(
                session_id=session_id,
                event_type="neuroverse.safety.decision",
                timestamp=ts,
                source="dataset_replay",
                payload=safety.model_dump(),
            )
        )
        action = policy.decide(prediction, safety)
        recorder.record(
            BaseEvent(
                session_id=session_id,
                event_type="neuroverse.adaptation.action",
                timestamp=ts,
                source="dataset_replay",
                payload=action.model_dump(),
            )
        )
    recorder.record(
        BaseEvent(
            session_id=session_id,
            event_type="neuroverse.replay.completed",
            timestamp=float(samples[-1].end_time if samples else 0.0),
            source="dataset_replay",
            payload={"dataset_id": adapter.dataset_id, "samples": len(samples)},
        )
    )
    recorder.close()
    summarize_session(
        session_id,
        base_dir=Path(args.output_dir) if args.output_dir else None,
        write_report=True,
    )
    print(f"Wrote {recorder.event_count} replay events to {recorder.file_path}")


if __name__ == "__main__":
    main()
