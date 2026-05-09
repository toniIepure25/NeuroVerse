from __future__ import annotations

from pathlib import Path

import numpy as np

from app.datasets.schemas import FeatureDataset
from app.inference.learned_model import LearnedModelEstimator
from app.ml.ablation import filter_feature_dataset
from app.ml.baselines import create_baseline_model
from app.ml.calibration import calibration_metrics
from app.ml.evaluator import evaluate_model_on_dataset
from app.ml.registry import register_model
from app.ml.splits import leakage_warnings, make_split_indices
from app.schemas.session import FeaturePayload


def _dataset() -> FeatureDataset:
    x = np.array([
        [0.8, 0.2, 0.4, 0.8],
        [0.75, 0.25, 0.42, 0.82],
        [0.2, 0.8, 0.7, 0.55],
        [0.25, 0.78, 0.72, 0.52],
        [0.6, 0.4, 0.35, 0.9],
        [0.58, 0.42, 0.36, 0.88],
    ])
    y = np.array(
        ["relaxation", "relaxation", "workload", "workload", "focus", "focus"],
        dtype=object,
    )
    return FeatureDataset(
        X=x,
        y=y,
        feature_names=[
            "eeg_alpha_power",
            "eeg_beta_power",
            "physio_heart_rate",
            "gaze_fixation_stability",
        ],
        label_names=["phase_label"],
        groups=["s1:a", "s1:a", "s2:b", "s2:b", "s3:c", "s3:c"],
        metadata={"dataset_id": "unit"},
    )


def test_baseline_save_load_preserves_predictions(tmp_path: Path) -> None:
    dataset = _dataset()
    model = create_baseline_model("random_forest", {"n_estimators": 10}, dataset.feature_names)
    model.fit(dataset.X, dataset.y)
    before = model.predict(dataset.X)
    path = model.save(tmp_path / "model.joblib")
    after = model.load(path).predict(dataset.X)
    assert before.tolist() == after.tolist()


def test_evaluation_and_calibration_metrics() -> None:
    dataset = _dataset()
    model = create_baseline_model("random_forest", {"n_estimators": 10}, dataset.feature_names)
    model.fit(dataset.X, dataset.y)
    metrics = evaluate_model_on_dataset(model, dataset)
    assert "accuracy" in metrics
    assert "macro_f1" in metrics
    cal = calibration_metrics(
        dataset.y,
        model.predict_proba(dataset.X),
        list(model.estimator.named_steps["clf"].classes_),
    )
    assert cal["available"]
    assert "ece" in cal


def test_group_split_prevents_leakage() -> None:
    dataset = _dataset()
    splits = make_split_indices(
        dataset,
        {"type": "group", "train_size": 0.5, "val_size": 0.25, "test_size": 0.25},
    )
    warnings = leakage_warnings(dataset, splits)
    assert not warnings or all("Group leakage" not in msg for msg in warnings)


def test_ablation_filtering() -> None:
    subset = filter_feature_dataset(_dataset(), "eeg")
    assert subset.feature_names == ["eeg_alpha_power", "eeg_beta_power"]


def test_learned_estimator_maps_phase_prediction(tmp_path: Path) -> None:
    dataset = _dataset()
    model = create_baseline_model("random_forest", {"n_estimators": 10}, dataset.feature_names)
    model.fit(dataset.X, dataset.y)
    model_dir = register_model(
        model,
        "unit_phase_model",
        {
            "dataset_id": "unit",
            "target": "phase_label",
            "prediction_semantics": "phase_proxy",
            "feature_names": dataset.feature_names,
        },
        models_dir=tmp_path,
    )
    estimator = LearnedModelEstimator.from_model_dir(model_dir)
    payload = FeaturePayload(
        eeg={"alpha_power": 0.2, "beta_power": 0.8},
        physio={"heart_rate": 0.7},
        gaze={"fixation_stability": 0.55},
        multimodal={},
        sqi_scores={},
    )
    state = estimator.predict(payload)
    assert 0 <= state.confidence <= 1
    assert state.model_version.startswith("learned:")
