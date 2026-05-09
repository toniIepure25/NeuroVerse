from __future__ import annotations

from typing import Any

from app.ml.trainer import train_baseline_from_configs


def run_training_experiment(
    dataset_config: dict[str, Any],
    experiment_config: dict[str, Any],
) -> dict[str, Any]:
    return train_baseline_from_configs(dataset_config, experiment_config)
