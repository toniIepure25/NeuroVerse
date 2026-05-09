from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

from run_live_raw_bci_shadow import epoch_from_buffer

from app.acquisition.eeg_fixture import create_eeg_fixture_raw
from app.acquisition.marker_collector import BackgroundMarkerCollector
from app.ml.event_epochs import (
    extract_epoch_features,
    inspect_eeg_dataset_config,
    inspect_raw_source,
    prepare_event_feature_dataset,
    read_feature_csv,
)
from app.ml.event_label_mapping import normalize_event_label
from app.ml.raw_epoch_models import RawEpochModelAdapter, create_raw_epoch_model

ROOT = Path(__file__).resolve().parents[3]


def test_eeg_fixture_inspection_reports_annotations() -> None:
    report = inspect_raw_source(fixture_mode=True, duration_seconds=26)

    assert report["channel_count"] == 10
    assert report["sampling_rate_hz"] == 250.0
    assert "LEFT_HAND_IMAGERY" in report["annotation_labels"]
    assert "RIGHT_HAND_IMAGERY" in report["annotation_labels"]


def test_event_locked_feature_dataset_fixture(tmp_path: Path) -> None:
    output = tmp_path / "features.csv"
    summary = prepare_event_feature_dataset(fixture_mode=True, output_path=output)
    x, y, feature_names, rows = read_feature_csv(output)

    assert output.exists()
    assert summary["row_count"] == len(rows)
    assert x.shape[0] == len(y)
    assert feature_names
    assert all(name.startswith("eeg_") for name in feature_names)


def test_epoch_feature_extraction_has_bandpower_prefixes() -> None:
    data = np.vstack([
        np.sin(np.linspace(0, 20, 250)),
        np.cos(np.linspace(0, 20, 250)),
    ])
    features = extract_epoch_features(data, 250.0, ["C3", "C4"])

    assert "eeg_C3_alpha_relpower" in features
    assert "eeg_global_beta_relpower" in features


def test_event_feature_config_supports_preprocessing(tmp_path: Path) -> None:
    output = tmp_path / "features.csv"
    summary = prepare_event_feature_dataset(
        fixture_mode=True,
        output_path=output,
        tmin=0.5,
        tmax=1.5,
        bandpass_low=7.0,
        bandpass_high=35.0,
        baseline_correction=True,
        reject_amplitude_uv=500.0,
        feature_set="combined",
    )
    _x, _y, feature_names, rows = read_feature_csv(output)

    assert summary["preprocessing"]["bandpass_low"] == 7.0
    assert summary["feature_set"] == "combined"
    assert "epoch_quality_pass" in rows[0]
    assert any("lateral_c3_c4" in name for name in feature_names)


def test_marker_collector_empty_path_is_safe() -> None:
    collector = BackgroundMarkerCollector(stream_name="definitely_missing_stream", timeout=0.01)
    collector.start()
    events = collector.stop()

    assert events == []


def test_event_classifier_script_help() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "train_eeg_event_classifier.py"), "--help"],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "usage:" in result.stdout


def test_bci_benchmark_script_runs_and_defers_csp(tmp_path: Path) -> None:
    features = tmp_path / "features.csv"
    prepare_event_feature_dataset(fixture_mode=True, output_path=features)
    output = tmp_path / "benchmark"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_bci_benchmark.py"),
            "--features",
            str(features),
            "--models",
            "logistic_regression",
            "ridge_classifier",
            "csp_lda",
            "--split",
            "stratified",
            "--output",
            str(output),
            "--n-bootstrap",
            "20",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    summary = yaml.safe_load((output / "benchmark_summary.json").read_text())
    assert (output / "model_comparison.csv").exists()
    assert summary["best_model"]["status"] == "ok"
    assert any(item["status"] == "deferred" for item in summary["models"])


def test_raw_epoch_benchmark_script_runs_csp(tmp_path: Path) -> None:
    fif_paths = []
    for subject, run in (("S001", "4"), ("S002", "8")):
        raw = create_eeg_fixture_raw(duration=26, seed=int(run))
        path = tmp_path / f"{subject}R{run}_raw.fif"
        raw.save(path, overwrite=True, verbose=False)
        fif_paths.append((subject, run, path))
    cfg_path = tmp_path / "raw_epoch_fixture.yaml"
    cfg_path.write_text(
        yaml.safe_dump({
            "dataset_id": "raw_epoch_fixture",
            "dataset_name": "raw epoch fixture",
            "source": "fixture",
            "local_root": str(tmp_path),
            "files": [
                {"subject_id": subject, "run_id": run, "path": path.name}
                for subject, run, path in fif_paths
            ],
        }),
        encoding="utf-8",
    )
    epochs = tmp_path / "raw_epochs.npz"
    prep = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "prepare_raw_epoch_dataset.py"),
            "--dataset-config",
            str(cfg_path),
            "--labels",
            "LEFT_HAND_IMAGERY",
            "RIGHT_HAND_IMAGERY",
            "--exclude-rest",
            "--output",
            str(epochs),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert prep.returncode == 0, prep.stderr
    output = tmp_path / "raw_benchmark"
    bench = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "run_raw_epoch_bci_benchmark.py"),
            "--epochs",
            str(epochs),
            "--models",
            "csp_lda",
            "--n-components-grid",
            "2",
            "--split",
            "group_run",
            "--output",
            str(output),
            "--n-bootstrap",
            "5",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert bench.returncode == 0, bench.stderr
    summary = yaml.safe_load((output / "benchmark_summary.json").read_text())
    assert summary["best_model"]["model"] == "csp_lda"
    assert summary["best_model"]["metadata"]["raw_epoch_model"] is True
    assert not summary["closed_loop_allowed"]


def test_fbcsp_trains_and_save_load_preserves_prediction_shape(tmp_path: Path) -> None:
    rng = np.random.default_rng(7)
    x = rng.normal(size=(16, 4, 128))
    y = np.asarray(["LEFT_HAND_IMAGERY"] * 8 + ["RIGHT_HAND_IMAGERY"] * 8)
    x[:8, 0, :] += np.sin(np.linspace(0, 20, 128))
    x[8:, 1, :] += np.sin(np.linspace(0, 20, 128))
    model = create_raw_epoch_model(
        "fbcsp_logreg",
        n_components=2,
        sampling_rate=128.0,
        bands=[(8.0, 12.0), (12.0, 16.0)],
    )

    model.fit(x, y)
    preds = model.predict(x)
    path = tmp_path / "fbcsp.joblib"
    model.save(path)
    loaded = RawEpochModelAdapter.load(path)
    loaded_preds = loaded.predict(x)

    assert preds.shape == y.shape
    assert loaded_preds.shape == y.shape
    assert loaded.metadata()["spatial_filter"] == "filter_bank_mne.decoding.CSP"


def test_live_raw_shadow_epoch_from_buffer_interpolates_marker_window() -> None:
    timestamps = np.linspace(10.0, 14.0, 81)
    samples = np.column_stack([
        np.sin(timestamps),
        np.cos(timestamps),
    ])

    epoch, reason = epoch_from_buffer(
        samples,
        timestamps,
        marker_timestamp=11.0,
        tmin=0.5,
        tmax=2.5,
        expected_samples=40,
        expected_channels=2,
    )

    assert reason is None
    assert epoch is not None
    assert epoch.shape == (2, 40)


def test_live_raw_shadow_epoch_from_buffer_reports_missed_epoch() -> None:
    timestamps = np.linspace(10.0, 10.2, 5)
    samples = np.column_stack([timestamps, timestamps])

    epoch, reason = epoch_from_buffer(
        samples,
        timestamps,
        marker_timestamp=11.0,
        tmin=0.5,
        tmax=2.5,
        expected_samples=40,
        expected_channels=2,
    )

    assert epoch is None
    assert reason == "insufficient_samples_in_epoch_window"


def test_physionet_run_aware_event_mapping() -> None:
    left = normalize_event_label("T1", run_id=4)
    right = normalize_event_label("T2", run_id=4)
    feet = normalize_event_label("T2", run_id=6)

    assert left["event_label"] == "LEFT_HAND_IMAGERY"
    assert right["event_label"] == "RIGHT_HAND_IMAGERY"
    assert feet["event_label"] == "BOTH_FEET_IMAGERY"
    assert normalize_event_label("custom", run_id=4)["original_label"] == "custom"


def test_dataset_config_feature_generation_from_local_fif(tmp_path: Path) -> None:
    raw = create_eeg_fixture_raw(duration=24, seed=7)
    fif_path = tmp_path / "S001R04_raw.fif"
    raw.save(fif_path, overwrite=True, verbose=False)
    cfg_path = tmp_path / "physionet_local.yaml"
    cfg_path.write_text(
        yaml.safe_dump({
            "dataset_id": "test_physionet_local",
            "dataset_name": "test",
            "source": "physionet_eegbci",
            "local_root": str(tmp_path),
            "files": [{
                "subject_id": "S001",
                "run_id": 4,
                "path": fif_path.name,
                "task_context": "motor_imagery_left_right",
            }],
        }),
        encoding="utf-8",
    )
    output = tmp_path / "features.csv"

    inspection = inspect_eeg_dataset_config(cfg_path)
    summary = prepare_event_feature_dataset(dataset_config=cfg_path, output_path=output)
    _x, _y, _features, rows = read_feature_csv(output)

    assert inspection["inspected_file_count"] == 1
    assert summary["row_count"] == len(rows)
    assert {row["subject_id"] for row in rows} == {"S001"}
    assert "LEFT_HAND_IMAGERY" in {row["event_label"] for row in rows}


def test_physionet_config_script_local_mode(tmp_path: Path) -> None:
    output = tmp_path / "physionet.yaml"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "prepare_physionet_eegbci.py"),
            "--local-root",
            str(tmp_path / "eegbci"),
            "--subjects",
            "1",
            "--runs",
            "4",
            "--output-config",
            str(output),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert output.exists()
    assert "citation_note" in result.stdout
