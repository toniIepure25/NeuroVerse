from __future__ import annotations

from pathlib import Path

from app.datasets.registry import create_dataset_adapter
from app.ml.feature_dataset import build_feature_dataset
from app.safety.safety_gate import SafetyGate
from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


def test_dataset_replay_script_produces_jsonl(tmp_path: Path) -> None:
    import subprocess

    root = Path(__file__).resolve().parents[3]
    cmd = [
        "python3",
        str(root / "scripts" / "replay_dataset.py"),
        "--dataset-config",
        str(root / "configs" / "datasets" / "synthetic.yaml"),
        "--session-id",
        "unit_replay",
        "--output-dir",
        str(tmp_path),
    ]
    result = subprocess.run(cmd, cwd=root, check=True, capture_output=True, text=True)
    assert "replay events" in result.stdout
    path = tmp_path / "unit_replay.jsonl"
    assert path.exists()
    assert "neuroverse.state.predicted" in path.read_text()


def test_safety_gate_consumes_learned_confidence() -> None:
    gate = SafetyGate()
    low_confidence_state = StatePredictionPayload(
        focus=0.5,
        relaxation=0.5,
        workload=0.5,
        stress=0.2,
        fatigue=0.2,
        imagery_engagement=0.2,
        confidence=0.1,
        model_version="learned:test",
    )
    result = gate.evaluate(
        low_confidence_state,
        {"eeg": 0.9, "physio": 0.9, "gaze": 0.9, "multimodal": 0.9},
    )
    assert result.decision == "BLOCKED"


def test_missing_modality_feature_generation_is_safe() -> None:
    adapter = create_dataset_adapter({
        "dataset_id": "generic",
        "type": "generic_csv",
        "path": str(Path(__file__).parent / "fixtures" / "generic_features.csv"),
        "timestamp_col": "timestamp",
        "label_col": "phase_label",
        "feature_cols": ["eeg_alpha_power"],
        "window_size_seconds": 2,
        "overlap": 0,
    })
    dataset = build_feature_dataset(list(adapter.iter_windows()), target="phase_label")
    payload = FeaturePayload(eeg={"alpha_power": float(dataset.X[0, 0])})
    assert payload.physio == {}
