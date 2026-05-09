from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from app.datasets.clare_adapter import ClareLikeAdapter
from app.datasets.generic_csv_adapter import GenericCSVAdapter
from app.datasets.physionet_mi_adapter import PhysioNetMIAdapter
from app.datasets.schemas import WindowedSample
from app.datasets.synthetic_dataset import SyntheticDatasetAdapter
from app.datasets.windowing import align_point_labels, window_starts
from app.ml.feature_dataset import build_feature_dataset, load_feature_dataset, save_feature_dataset

FIXTURES = Path(__file__).parent / "fixtures"


def test_synthetic_adapter_deterministic() -> None:
    cfg = {
        "dataset_id": "syn",
        "type": "synthetic",
        "duration_seconds": 4,
        "tick_seconds": 1,
        "seed": 7,
    }
    a = list(SyntheticDatasetAdapter(cfg).iter_windows())
    b = list(SyntheticDatasetAdapter(cfg).iter_windows())
    assert [x.labels["phase_label"] for x in a] == [x.labels["phase_label"] for x in b]
    assert (
        a[0].data_by_modality["multimodal"]["data"][0][:5]
        == b[0].data_by_modality["multimodal"]["data"][0][:5]
    )


def test_generic_csv_fixture_loads() -> None:
    adapter = GenericCSVAdapter({
        "dataset_id": "generic",
        "path": str(FIXTURES / "generic_features.csv"),
        "timestamp_col": "timestamp",
        "label_col": "phase_label",
        "feature_cols": ["eeg_alpha_power", "physio_heart_rate", "gaze_fixation_stability"],
        "window_size_seconds": 2,
        "overlap": 0,
    })
    samples = list(adapter.iter_windows())
    assert samples
    assert samples[0].features
    assert samples[0].labels["phase_label"] == "baseline"


def test_clare_like_fixture_maps_workload() -> None:
    adapter = ClareLikeAdapter({
        "dataset_id": "clare",
        "path": str(FIXTURES / "clare_like"),
        "feature_cols": ["eeg_theta_power", "physio_heart_rate"],
        "window_size_seconds": 2,
        "overlap": 0,
    })
    samples = list(adapter.iter_windows())
    assert {sample.labels["workload_class"] for sample in samples} >= {"low", "medium"}
    assert all(0 <= sample.labels["workload_score"] <= 1 for sample in samples)


def test_physionet_missing_mne_is_graceful() -> None:
    adapter = PhysioNetMIAdapter({"dataset_id": "mi", "path": str(FIXTURES / "does-not-exist")})
    status = adapter.validate()
    assert "mne_available" in status
    if not status["mne_available"]:
        with pytest.raises(RuntimeError, match="requires optional dependency mne"):
            list(adapter.iter_windows())


def test_windowing_and_label_alignment() -> None:
    assert window_starts(0, 10, 2, 0.5) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    label = align_point_labels([0, 1, 2, 3], ["a", "a", "b", "b"], 0, 2, "majority")
    assert label == "a"
    center = align_point_labels([0, 1, 2, 3], ["a", "a", "b", "b"], 1.5, 3.5, "center")
    assert center == "b"


def test_feature_dataset_generation_save_load_and_prefixes(tmp_path: Path) -> None:
    sample = WindowedSample(
        sample_id="s0",
        dataset_id="fixture",
        subject_id="s1",
        session_id="a",
        start_time=0,
        end_time=1,
        modalities=["features"],
        features={"eeg_alpha_power": 0.6, "physio_heart_rate": 0.4},
        labels={"phase_label": "baseline"},
    )
    dataset = build_feature_dataset([sample], target="phase_label")
    assert dataset.X.shape == (1, 2)
    assert all(name.startswith(("eeg_", "physio_")) for name in dataset.feature_names)
    out = save_feature_dataset(dataset, tmp_path / "features.csv")
    loaded = load_feature_dataset(out)
    np.testing.assert_allclose(loaded.X, dataset.X)
