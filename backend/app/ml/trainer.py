from __future__ import annotations

from typing import Any

from app.datasets.registry import create_dataset_adapter
from app.datasets.validation import validate_dataset_config
from app.experiments.tracking import create_run_dir
from app.ml.ablation import filter_feature_dataset
from app.ml.baselines import create_baseline_model
from app.ml.evaluator import evaluate_model_on_dataset
from app.ml.registry import register_model
from app.ml.reports import write_experiment_report
from app.ml.splits import leakage_warnings, make_split_indices


def train_baseline_from_configs(
    dataset_config: dict[str, Any],
    experiment_config: dict[str, Any],
    model_type: str | None = None,
    target: str | None = None,
    output_model_id: str | None = None,
) -> dict[str, Any]:
    adapter = create_dataset_adapter(dataset_config)
    feature_dataset = adapter.to_feature_dataset(target=target or experiment_config.get("target"))
    splits = make_split_indices(feature_dataset, experiment_config.get("split") or {})
    model_cfg = dict(experiment_config.get("model") or {})
    configured_model = model_cfg.pop("type", "random_forest")
    selected_model = model_type or configured_model
    model = create_baseline_model(
        selected_model, model_cfg, feature_names=feature_dataset.feature_names
    )
    model.fit(feature_dataset.X[splits["train"]], feature_dataset.y[splits["train"]])
    eval_idx = splits["test"] if len(splits["test"]) else splits["val"]
    metrics = evaluate_model_on_dataset(model, feature_dataset, eval_idx)
    metrics["warnings"] = leakage_warnings(feature_dataset, splits)
    if (experiment_config.get("ablation") or {}).get("enabled"):
        metrics["ablation"] = _run_ablation(
            feature_dataset,
            splits,
            experiment_config,
            selected_model,
            model_cfg,
        )
    model_id = output_model_id or str(
        experiment_config.get("experiment_id", f"{adapter.dataset_id}_{selected_model}")
    )
    model_dir = register_model(
        model,
        model_id=model_id,
        metadata={
            "dataset_id": adapter.dataset_id,
            "target": feature_dataset.label_names[0],
            "label_mapping": "dataset_adapter",
            "prediction_semantics": experiment_config.get("prediction_semantics", "phase_proxy"),
            "limitations": "Dataset-derived proxy labels; not clinically validated.",
            "intended_use": "Offline research baseline comparison and replay experiments.",
            "not_intended_use": "Clinical diagnosis, treatment, or consequential decision making.",
        },
        metrics=metrics,
    )
    report_dir = create_run_dir(model_id)
    model_metadata = {
        "model_id": model_id,
        "model_type": selected_model,
        "dataset_id": adapter.dataset_id,
        "target": feature_dataset.label_names[0],
        "prediction_semantics": experiment_config.get("prediction_semantics", "phase_proxy"),
        "limitations": "Dataset-derived proxy labels; not clinically validated.",
        "intended_use": "Offline research baseline comparison and replay experiments.",
        "not_intended_use": "Clinical diagnosis, treatment, or consequential decision making.",
    }
    validation_summary = validate_dataset_config(
        dataset_config,
        target=feature_dataset.label_names[0],
    )
    write_experiment_report(
        report_dir,
        title=f"NeuroVerse Baseline: {model_id}",
        dataset_metadata=adapter.load_metadata().to_dict(),
        model_metadata=model_metadata,
        metrics=metrics,
        run_config={"dataset_config": dataset_config, "experiment_config": experiment_config},
        dataset_validation_summary=validation_summary,
    )
    return {
        "model_dir": str(model_dir),
        "report_dir": str(report_dir),
        "metrics": metrics,
        "splits": {k: v.tolist() for k, v in splits.items()},
    }


def _run_ablation(
    feature_dataset,
    splits,
    experiment_config: dict[str, Any],
    model_type: str,
    model_cfg: dict[str, Any],
) -> dict[str, Any]:
    results: dict[str, Any] = {}
    sets = (experiment_config.get("ablation") or {}).get(
        "sets",
        ["eeg", "physio", "gaze", "eeg+physio", "eeg+gaze", "physio+gaze", "all", "all+sqi"],
    )
    eval_idx = splits["test"] if len(splits["test"]) else splits["val"]
    for name in sets:
        subset = filter_feature_dataset(feature_dataset, str(name))
        model = create_baseline_model(
            model_type, dict(model_cfg), feature_names=subset.feature_names
        )
        model.fit(subset.X[splits["train"]], subset.y[splits["train"]])
        results[str(name)] = evaluate_model_on_dataset(model, subset, eval_idx)
    return results
