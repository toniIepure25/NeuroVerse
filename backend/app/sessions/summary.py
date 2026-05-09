from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np

from app.core.config import settings
from app.schemas.events import BaseEvent

STATE_KEYS = [
    "focus",
    "relaxation",
    "workload",
    "stress",
    "fatigue",
    "imagery_engagement",
    "confidence",
]


def summarize_session(
    session_id: str,
    base_dir: str | Path | None = None,
    write_report: bool = True,
) -> dict[str, Any]:
    directory = Path(base_dir) if base_dir is not None else settings.sessions_dir
    path = directory / f"{session_id}.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"Session file not found: {path}")
    events = _load_events(path)
    summary = summarize_events(events, session_id=session_id)
    if write_report:
        paths = write_session_summary(summary, directory)
        summary["summary_paths"] = {key: str(value) for key, value in paths.items()}
    return summary


def summarize_events(events: list[BaseEvent], session_id: str) -> dict[str, Any]:
    states = [event.payload for event in events if event.event_type == "neuroverse.state.predicted"]
    safety = [event.payload for event in events if event.event_type == "neuroverse.safety.decision"]
    actions = [
        event.payload for event in events if event.event_type == "neuroverse.adaptation.action"
    ]
    replay_started = next(
        (event.payload for event in events if event.event_type == "neuroverse.replay.started"),
        {},
    )
    replay_completed = next(
        (event.payload for event in events if event.event_type == "neuroverse.replay.completed"),
        {},
    )
    action_names = [str(action.get("action", "")) for action in actions]
    safety_decisions = [str(item.get("decision", "")) for item in safety]
    state_averages = {
        key: _mean([_float_or_none(state.get(key)) for state in states]) for key in STATE_KEYS
    }
    summary = {
        "session_id": session_id,
        "total_events": len(events),
        "total_state_predictions": len(states),
        "total_safety_decisions": len(safety),
        "total_adaptation_actions": len(actions),
        "safety_block_rate": _rate(
            safety_decisions,
            {"BLOCKED", "WAIT"},
        ),
        "action_distribution": dict(Counter(action_names)),
        "state_averages": state_averages,
        "state_oscillation_rate": _state_oscillation_rate(states),
        "action_oscillation_rate": _oscillation_rate(action_names),
        "freeze_events": action_names.count("FreezeAdaptation"),
        "maintain_baseline_events": action_names.count("MaintainBaseline"),
        "data_source": "dataset_replay" if replay_started else "recorded_session",
        "model_used": _model_used(states),
        "dataset_id": replay_started.get("dataset_id") or replay_completed.get("dataset_id"),
    }
    return summary


def write_session_summary(
    summary: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    session_id = summary["session_id"]
    json_path = out / f"{session_id}_summary.json"
    md_path = out / f"{session_id}_summary.md"
    json_path.write_text(json.dumps(summary, indent=2, default=str))
    md_path.write_text(_summary_markdown(summary))
    return {"json": json_path, "markdown": md_path}


def _load_events(path: Path) -> list[BaseEvent]:
    events: list[BaseEvent] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(BaseEvent(**json.loads(line)))
    return events


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _mean(values: list[float | None]) -> float | None:
    clean = [value for value in values if value is not None]
    if not clean:
        return None
    return float(np.mean(clean))


def _rate(values: list[str], matches: set[str]) -> float:
    if not values:
        return 0.0
    return float(sum(value in matches for value in values) / len(values))


def _oscillation_rate(values: list[str]) -> float:
    if len(values) < 2:
        return 0.0
    transitions = sum(values[i] != values[i - 1] for i in range(1, len(values)))
    return float(transitions / (len(values) - 1))


def _state_oscillation_rate(states: list[dict[str, Any]]) -> float:
    if len(states) < 2:
        return 0.0
    dominant: list[str] = []
    for state in states:
        scores = {
            key: _float_or_none(state.get(key)) or 0.0
            for key in STATE_KEYS
            if key != "confidence"
        }
        dominant.append(max(scores.items(), key=lambda item: item[1])[0])
    return _oscillation_rate(dominant)


def _model_used(states: list[dict[str, Any]]) -> str | None:
    versions = [str(state.get("model_version")) for state in states if state.get("model_version")]
    if not versions:
        return None
    counts = Counter(versions)
    return counts.most_common(1)[0][0]


def _summary_markdown(summary: dict[str, Any]) -> str:
    averages = summary.get("state_averages") or {}
    actions = summary.get("action_distribution") or {}
    return "\n".join(
        [
            f"# Replay Summary: {summary.get('session_id')}",
            "",
            f"- Events: `{summary.get('total_events')}`",
            f"- State predictions: `{summary.get('total_state_predictions')}`",
            f"- Safety decisions: `{summary.get('total_safety_decisions')}`",
            f"- Adaptation actions: `{summary.get('total_adaptation_actions')}`",
            f"- Safety block/wait rate: `{summary.get('safety_block_rate')}`",
            f"- State oscillation rate: `{summary.get('state_oscillation_rate')}`",
            f"- Action oscillation rate: `{summary.get('action_oscillation_rate')}`",
            f"- Data source: `{summary.get('data_source')}`",
            f"- Model used: `{summary.get('model_used')}`",
            f"- Dataset: `{summary.get('dataset_id')}`",
            "",
            "## State Averages",
            json.dumps(averages, indent=2),
            "",
            "## Action Distribution",
            json.dumps(actions, indent=2),
            "",
            "## Scientific Note",
            "Replay summaries describe engineering behavior over proxy estimates. "
            "They are not clinical validation.",
            "",
        ]
    )
