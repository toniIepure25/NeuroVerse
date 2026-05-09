"""Train an event-locked EEG baseline classifier and register it locally."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from sklearn.model_selection import GroupShuffleSplit, LeaveOneGroupOut, train_test_split

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.baselines import create_baseline_model  # noqa: E402
from app.ml.event_epochs import read_feature_csv  # noqa: E402
from app.ml.metrics import evaluate_classification, measure_inference_latency  # noqa: E402
from app.ml.registry import register_model  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Train EEG event-locked classifier")
    parser.add_argument("--features", required=True)
    parser.add_argument("--model", default="logistic_regression")
    parser.add_argument("--target", default="event_label")
    parser.add_argument("--output", default="models/eeg_event_classifier_fixture")
    parser.add_argument("--split", default="stratified")
    parser.add_argument("--train-runs", default=None)
    parser.add_argument("--test-runs", default=None)
    parser.add_argument("--test-size", type=float, default=0.35)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    result = train_event_classifier(
        features_path=_resolve(args.features),
        model_type=args.model,
        output=args.output,
        split=args.split,
        train_runs=_split_csv(args.train_runs),
        test_runs=_split_csv(args.test_runs),
        test_size=args.test_size,
        random_state=args.random_state,
    )
    print(json.dumps(result, indent=2, default=str))


def train_event_classifier(
    *,
    features_path: Path,
    model_type: str,
    output: str,
    split: str = "stratified",
    train_runs: list[str] | None = None,
    test_runs: list[str] | None = None,
    test_size: float = 0.35,
    random_state: int = 42,
) -> dict[str, object]:
    x, y, feature_names, rows = read_feature_csv(features_path)
    labels = sorted(np.unique(y).tolist())
    train_idx, test_idx, split_warnings = _split_indices(
        y,
        rows,
        split=split,
        train_runs=train_runs,
        test_runs=test_runs,
        test_size=test_size,
        random_state=random_state,
    )
    x_train, x_test, y_train, y_test = x[train_idx], x[test_idx], y[train_idx], y[test_idx]
    model = create_baseline_model(
        model_type,
        params={"random_state": random_state},
        feature_names=feature_names,
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)
    metrics = evaluate_classification(y_test, predictions, probabilities, class_labels=labels)
    metrics["latency"] = measure_inference_latency(model, x_test)
    metrics["split_strategy"] = split
    metrics["split_warnings"] = split_warnings
    test_rows = [rows[i] for i in test_idx]
    metrics["per_subject"] = _group_metrics(
        model,
        x_test,
        y_test,
        test_rows,
        "subject_id",
        labels,
    )
    metrics["per_run"] = _group_metrics(model, x_test, y_test, test_rows, "run_id", labels)
    model_id = Path(output).name
    model_dir = register_model(
        model,
        model_id=model_id,
        metadata={
            "dataset_id": Path(features_path).stem,
            "target": "event_label",
            "prediction_semantics": "event_label_classifier",
            "event_labels": labels,
            "subjects": sorted({str(row.get("subject_id", "")) for row in rows}),
            "runs": sorted({str(row.get("run_id", "")) for row in rows}),
            "split_strategy": split,
            "feature_names": feature_names,
            "epoch_feature_file": str(features_path),
            "intended_use": "Event-locked controlled EEG task-label classification.",
            "not_intended_use": (
                "Not for thought reading, clinical diagnosis, unrestricted mental-state inference, "
                "or direct closed-loop control."
            ),
            "limitations": (
                "Fixture or local dataset annotations define labels; performance is not clinical "
                "validation and may not generalize across subjects or hardware."
            ),
        },
        metrics=metrics,
    )
    _write_extra_artifacts(model_dir, metrics, labels, rows)
    return {"model_dir": str(model_dir), "metrics": metrics, "labels": labels}


def _split_indices(
    y: np.ndarray,
    rows: list[dict[str, object]],
    *,
    split: str,
    train_runs: list[str] | None,
    test_runs: list[str] | None,
    test_size: float,
    random_state: int,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    indices = np.arange(len(y))
    warnings: list[str] = []
    if len(indices) < 3:
        return indices, indices, ["Very small dataset; train and test reuse all rows."]
    if train_runs or test_runs:
        train_set = set(train_runs or [])
        test_set = set(test_runs or [])
        train_idx = np.asarray([
            i for i, row in enumerate(rows) if str(row.get("run_id", "")) in train_set
        ])
        test_idx = np.asarray([
            i for i, row in enumerate(rows) if str(row.get("run_id", "")) in test_set
        ])
        if len(train_idx) and len(test_idx):
            return train_idx, test_idx, _leakage_warnings(rows, train_idx, test_idx, "run_id")
        warnings.append("Requested train/test runs did not produce non-empty splits; falling back.")
    if split == "group_subject":
        return _group_shuffle(y, rows, "subject_id", test_size, random_state)
    if split == "group_run":
        return _group_shuffle(y, rows, "group_run", test_size, random_state)
    if split == "within_subject":
        subjects = sorted({str(row.get("subject_id", "")) for row in rows})
        if len(subjects) == 1:
            warnings.append("Within-subject split uses a single subject.")
        return _stratified_split(y, test_size, random_state, warnings)
    if split == "leave_one_subject_out":
        groups = np.asarray([str(row.get("subject_id", "")) for row in rows])
        unique = sorted(set(groups))
        if len(unique) < 2:
            warnings.append("Leave-one-subject-out unavailable with fewer than two subjects.")
            return _stratified_split(y, test_size, random_state, warnings)
        logo = LeaveOneGroupOut()
        train_idx, test_idx = next(logo.split(indices, y, groups))
        return train_idx, test_idx, _leakage_warnings(rows, train_idx, test_idx, "subject_id")
    return _stratified_split(y, test_size, random_state, warnings)


def _group_shuffle(
    y: np.ndarray,
    rows: list[dict[str, object]],
    group_key: str,
    test_size: float,
    random_state: int,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    groups = np.asarray([str(row.get(group_key, "")) for row in rows])
    if len(set(groups)) < 2:
        warnings = [f"{group_key} split unavailable with fewer than two groups."]
        return _stratified_split(y, test_size, random_state, warnings)
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(splitter.split(np.arange(len(y)), y, groups))
    return train_idx, test_idx, _leakage_warnings(rows, train_idx, test_idx, group_key)


def _stratified_split(
    y: np.ndarray,
    test_size: float,
    random_state: int,
    warnings: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    indices = np.arange(len(y))
    _, counts = np.unique(y, return_counts=True)
    stratify = y if len(counts) > 1 and np.all(counts >= 2) else None
    if stratify is None:
        warnings.append("Stratified split unavailable because at least one class is too small.")
    train_idx, test_idx = train_test_split(
        indices,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    return train_idx, test_idx, warnings


def _leakage_warnings(
    rows: list[dict[str, object]],
    train_idx: np.ndarray,
    test_idx: np.ndarray,
    group_key: str,
) -> list[str]:
    train_groups = {str(rows[i].get(group_key, "")) for i in train_idx}
    test_groups = {str(rows[i].get(group_key, "")) for i in test_idx}
    overlap = sorted(train_groups & test_groups)
    if overlap:
        return [f"Group leakage detected for {group_key}: {overlap[:5]}"]
    return []


def _group_metrics(
    model: object,
    x_test: np.ndarray,
    y_test: np.ndarray,
    rows: list[dict[str, object]],
    group_key: str,
    labels: list[str],
) -> dict[str, object]:
    result: dict[str, object] = {}
    groups = sorted({str(row.get(group_key, "")) for row in rows})
    for group in groups:
        idx = np.asarray([i for i, row in enumerate(rows) if str(row.get(group_key, "")) == group])
        if len(idx) == 0:
            continue
        preds = model.predict(x_test[idx])
        result[group or "unknown"] = evaluate_classification(y_test[idx], preds, None, labels)
    return result


def _write_extra_artifacts(
    model_dir: Path,
    metrics: dict[str, object],
    labels: list[str],
    rows: list[dict[str, object]],
) -> None:
    confusion = metrics.get("confusion_matrix") or []
    with open(model_dir / "confusion_matrix.csv", "w", encoding="utf-8") as f:
        f.write("," + ",".join(labels) + "\n")
        for label, row in zip(labels, confusion, strict=False):
            f.write(label + "," + ",".join(str(value) for value in row) + "\n")
    (model_dir / "training_rows_preview.json").write_text(
        json.dumps(rows[:5], indent=2),
        encoding="utf-8",
    )
    _write_group_csv(model_dir / "per_subject_metrics.csv", metrics.get("per_subject") or {})
    _write_group_csv(model_dir / "per_run_metrics.csv", metrics.get("per_run") or {})


def _write_group_csv(path: Path, grouped: dict[str, object]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("group,accuracy,balanced_accuracy,macro_f1,row_count\n")
        for group, metrics in grouped.items():
            if not isinstance(metrics, dict):
                continue
            per_class = (
                metrics.get("per_class") if isinstance(metrics.get("per_class"), dict) else {}
            )
            row_count = int(
                (per_class.get("macro avg") or {}).get("support", 0)
            ) if isinstance(per_class.get("macro avg"), dict) else 0
            f.write(
                f"{group},{metrics.get('accuracy')},{metrics.get('balanced_accuracy')},"
                f"{metrics.get('macro_f1')},{row_count}\n"
            )


def _split_csv(value: str | None) -> list[str] | None:
    if not value:
        return None
    return [item.strip() for item in value.split(",") if item.strip()]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
