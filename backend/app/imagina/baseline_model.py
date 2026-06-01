"""IMAGINA v1 Baseline Model.

Trains and evaluates a conservative baseline model on mental imagery datasets.
IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge, RidgeClassifier
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import GroupKFold, KFold, LeaveOneGroupOut, StratifiedKFold
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.imagina.dataset_adapter import build_feature_table, load_manifest

REPO_ROOT = Path(__file__).resolve().parents[3]


class ImaginaBaselineModelAdapter:
    """Adapter wrapping an scikit-learn pipeline for IMAGINA baseline inference."""

    def __init__(
        self,
        model_type: str,
        estimator: Any,
        target_type: Literal["classification", "regression"],
        feature_names: list[str],
        classes: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.model_type = model_type
        self.estimator = estimator
        self.target_type = target_type
        self.feature_names = feature_names
        self.classes = classes or []
        self.metadata = metadata or {}

    def fit(self, X: np.ndarray, y: np.ndarray) -> ImaginaBaselineModelAdapter:
        self.estimator.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.estimator.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray | None:
        if self.target_type == "classification" and hasattr(self.estimator, "predict_proba"):
            return self.estimator.predict_proba(X)
        return None

    def save(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, out)
        return out

    @classmethod
    def load(cls, path: str | Path) -> ImaginaBaselineModelAdapter:
        return joblib.load(path)


def create_imagina_model(
    model_type: str,
    target_type: Literal["classification", "regression"],
    feature_names: list[str],
    classes: list[str] | None = None,
    random_state: int = 42,
) -> ImaginaBaselineModelAdapter:
    """Factory to create a standardized baseline model pipeline."""
    model_key = model_type.lower()

    if target_type == "classification":
        if model_key in {"logistic_regression", "logistic"}:
            clf = LogisticRegression(max_iter=1000, random_state=random_state)
        elif model_key in {"ridge_classifier", "ridge"}:
            clf = RidgeClassifier(random_state=random_state)
        elif model_key in {"random_forest", "rf"}:
            clf = RandomForestClassifier(random_state=random_state)
        elif model_key in {"mlp", "mlp_classifier"}:
            clf = MLPClassifier(max_iter=500, random_state=random_state)
        else:
            raise ValueError(f"Unknown classification model type: {model_type}")

        estimator = Pipeline([
            ("impute", SimpleImputer(strategy="mean")),
            ("scale", StandardScaler()),
            ("clf", clf),
        ])
    else:
        # Regression
        if model_key in {"ridge_regression", "ridge"}:
            reg = Ridge()
        elif model_key in {"random_forest", "rf"}:
            reg = RandomForestRegressor(random_state=random_state)
        elif model_key in {"mlp", "mlp_regressor"}:
            reg = MLPRegressor(max_iter=500, random_state=random_state)
        else:
            raise ValueError(f"Unknown regression model type: {model_type}")

        estimator = Pipeline([
            ("impute", SimpleImputer(strategy="mean")),
            ("scale", StandardScaler()),
            ("reg", reg),
        ])

    return ImaginaBaselineModelAdapter(
        model_type=model_key,
        estimator=estimator,
        target_type=target_type,
        feature_names=feature_names,
        classes=classes,
    )


def train_imagina_baseline(
    manifest_path: str | Path,
    output_dir: str | Path,
    split_strategy: Literal["stratified", "group_subject", "leave_one_subject_out", "fixture"] = "fixture",
    model_type: str = "logistic_regression",
    target_type: Literal["classification", "regression"] = "classification",
) -> dict[str, Any]:
    """Train and evaluate the baseline model on the specified manifest."""
    manifest = load_manifest(manifest_path)
    table = build_feature_table(manifest, target_type=target_type)

    X = table["X"]
    y = table["y"]
    feature_names = table["feature_names"]
    subject_ids = table["subject_ids"]
    classes = table["classes"]

    unique_subjects = set(subject_ids)

    # Check for potential data leakage
    leakage_warnings = []
    if len(unique_subjects) > 1:
        # Multiple subjects present
        samples_per_subject = {}
        for s in subject_ids:
            samples_per_subject[s] = samples_per_subject.get(s, 0) + 1

        has_multiple_samples = any(count > 1 for count in samples_per_subject.values())
        if has_multiple_samples and split_strategy in {"stratified"}:
            leakage_warnings.append(
                "Data leakage risk: Multiple samples from the same subject are present. "
                "Using a 'stratified' (random) split may leak subject-specific patterns into the validation set. "
                "Use 'group_subject' or 'leave_one_subject_out' split strategy instead."
            )

    # Label as fixture/demo if manifest specifies it
    is_fixture = bool(
        "example" in str(manifest_path)
        or "fixture" in str(manifest_path)
        or manifest.dataset_name == "example_imagery_dataset"
    )

    if is_fixture:
        leakage_warnings.append("Fixture validation metrics: This model is trained on synthetic/fixture demo data for workflow verification only. No scientific validity is claimed.")

    # Execute splits and cross-validation
    metrics = {}

    if split_strategy == "fixture" or len(X) < 4:
        # Fixture evaluation: simple train-test or train on all
        model = create_imagina_model(model_type, target_type, feature_names, classes)
        model.fit(X, y)
        preds = model.predict(X)

        if target_type == "classification":
            acc = float(accuracy_score(y, preds))
            bal_acc = float(balanced_accuracy_score(y, preds))
            macro_f1 = float(f1_score(y, preds, average="macro"))
            cm = confusion_matrix(y, preds).tolist()

            metrics = {
                "accuracy": acc,
                "balanced_accuracy": bal_acc,
                "macro_f1": macro_f1,
                "confusion_matrix": cm,
            }
        else:
            mae = float(mean_absolute_error(y, preds))
            rmse = float(np.sqrt(mean_squared_error(y, preds)))
            r2 = float(r2_score(y, preds))

            metrics = {
                "mae": mae,
                "rmse": rmse,
                "r2": r2,
            }
    else:
        # Cross-validation
        model = create_imagina_model(model_type, target_type, feature_names, classes)

        cv_preds = np.zeros_like(y, dtype=np.float32) if target_type == "regression" else np.zeros_like(y)

        if split_strategy == "stratified":
            cv = StratifiedKFold(n_splits=min(3, len(X)), shuffle=True, random_state=42)
            splits = list(cv.split(X, y))
        elif split_strategy == "group_subject":
            cv = GroupKFold(n_splits=min(3, len(unique_subjects)))
            splits = list(cv.split(X, y, groups=subject_ids))
        elif split_strategy == "leave_one_subject_out":
            cv = LeaveOneGroupOut()
            splits = list(cv.split(X, y, groups=subject_ids))
        else:
            cv = KFold(n_splits=min(3, len(X)), shuffle=True, random_state=42)
            splits = list(cv.split(X))

        for train_idx, val_idx in splits:
            fold_model = create_imagina_model(model_type, target_type, feature_names, classes)
            fold_model.fit(X[train_idx], y[train_idx])
            cv_preds[val_idx] = fold_model.predict(X[val_idx])

        # Fit final model on all data
        model.fit(X, y)

        # Evaluate cross-validated predictions
        if target_type == "classification":
            acc = float(accuracy_score(y, cv_preds))
            bal_acc = float(balanced_accuracy_score(y, cv_preds))
            macro_f1 = float(f1_score(y, cv_preds, average="macro"))
            cm = confusion_matrix(y, cv_preds).tolist()

            metrics = {
                "accuracy": acc,
                "balanced_accuracy": bal_acc,
                "macro_f1": macro_f1,
                "confusion_matrix": cm,
            }
        else:
            mae = float(mean_absolute_error(y, cv_preds))
            rmse = float(np.sqrt(mean_squared_error(y, cv_preds)))
            r2 = float(r2_score(y, cv_preds))

            metrics = {
                "mae": mae,
                "rmse": rmse,
                "r2": r2,
            }

    # Add general dataset and split metadata
    metrics.update({
        "sample_count": len(X),
        "subject_count": len(unique_subjects),
        "split_strategy": split_strategy,
        "leakage_warnings": leakage_warnings,
        "model_type": model_type,
        "target_type": target_type,
    })

    # Save outputs
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Save trained model joblib
    model_file = out_path / "model.joblib"
    model.save(model_file)

    # Save manifest summary
    manifest_summary = {
        "dataset_name": manifest.dataset_name,
        "dataset_version": manifest.dataset_version,
        "modality": manifest.modality,
        "paradigm": manifest.paradigm,
        "sample_count": len(manifest.samples),
        "unique_subjects": list(unique_subjects),
        "feature_schema": feature_names,
    }
    with open(out_path / "manifest_summary.json", "w") as f:
        json.dump(manifest_summary, f, indent=2)

    # Save metrics
    with open(out_path / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Save predictions.csv if classification
    predictions_file = out_path / "predictions.csv"
    with open(predictions_file, "w") as f:
        f.write("sample_id,true_label,predicted_label\n")
        preds = model.predict(X)
        for i, s in enumerate(manifest.samples):
            true_lbl = s.label or s.task
            pred_lbl = classes[preds[i]] if target_type == "classification" and classes else str(preds[i])
            f.write(f"{s.sample_id},{true_lbl},{pred_lbl}\n")

    # Save limitations.md
    limitations_file = out_path / "limitations.md"
    _write_limitations(limitations_file, leakage_warnings)

    # Save model_card.md
    model_card_file = out_path / "model_card.md"
    _write_model_card(model_card_file, model_type, target_type, split_strategy, metrics, leakage_warnings)

    return {
        "model_path": str(model_file),
        "metrics": metrics,
        "leakage_warnings": leakage_warnings,
        "manifest_summary": manifest_summary,
        "artifacts": {
            "model": str(model_file),
            "manifest_summary": str(out_path / "manifest_summary.json"),
            "metrics": str(out_path / "metrics.json"),
            "predictions_csv": str(predictions_file),
            "limitations_md": str(limitations_file),
            "model_card_md": str(model_card_file),
        }
    }


def _write_limitations(path: Path, warnings: list[str]) -> None:
    lines = [
        "# IMAGINA v1 Baseline Limitations",
        "",
        "> [!IMPORTANT]",
        "> IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.",
        "> Fusion outputs are experimental proxy estimates, not validated cognitive-state measurements.",
        "> The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
        "> Closed-loop from real EEG is disabled by default.",
        "",
        "## Scientific Boundaries",
        "- **Proxy Estimation:** The baseline model estimates supervised statistical bounds of trial annotations; it does not read mental imagery content or reconstruct thoughts.",
        "- **Closed-Loop Gating:** No mental imagery estimation translates directly into physical motor actions or visualization modifications without multiple layers of physical validation and explicit calibration baselines.",
        "- **Clinical Applicability:** None. This platform is an educational/research benchmark and should never be used as a medical diagnostics system.",
        "",
        "## Pipeline Warnings",
    ]
    if warnings:
        for w in warnings:
            lines.append(f"- **Warning:** {w}")
    else:
        lines.append("- No immediate train-time leakage warnings identified.")

    path.write_text("\n".join(lines))


def _write_model_card(
    path: Path,
    model_type: str,
    target_type: str,
    split_strategy: str,
    metrics: dict[str, Any],
    warnings: list[str],
) -> None:
    lines = [
        f"# IMAGINA Model Card: v1 {model_type.upper()} ({target_type})",
        "",
        "## Intended Use",
        "This baseline model estimates conservative mental-imagery and perception proxies under controlled task guidelines for portfolio demonstration.",
        "",
        "## Not Intended Use",
        "- Unrestricted thought decoding, dream reading, clinical diagnostic evaluation, or direct hardware closed-loop control.",
        "",
        "## Baseline Details",
        f"- **Model Type:** {model_type}",
        f"- **Target Type:** {target_type}",
        f"- **Split Strategy:** {split_strategy}",
        f"- **Sample Count:** {metrics.get('sample_count', 0)}",
        f"- **Subject Count:** {metrics.get('subject_count', 0)}",
        "",
        "## Metrics",
        "```json",
        json.dumps(metrics, indent=2),
        "```",
        "",
        "## Safety Governance",
        "- **Status:** Closed-Loop from Real EEG is Locked/Disabled.",
        "- **Pipeline Warnings:**",
    ]
    for w in warnings:
        lines.append(f"  - {w}")

    path.write_text("\n".join(lines))
