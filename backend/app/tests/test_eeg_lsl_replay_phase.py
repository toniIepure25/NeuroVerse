from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from app.acquisition.artifacts import merge_artifact_summaries, summarize_eeg_artifacts
from app.acquisition.channel_mapping import get_profile, validate_profile_against_stream
from app.acquisition.markers import MarkerEvent, align_markers_to_windows, empty_marker_report

ROOT = Path(__file__).resolve().parents[3]


def test_marker_alignment_counts_labels_inside_windows() -> None:
    markers = [
        MarkerEvent("LEFT_HAND_IMAGERY", 1.2, "markers", {}),
        MarkerEvent("LEFT_HAND_IMAGERY", 1.6, "markers", {}),
        MarkerEvent("REST", 2.4, "markers", {}),
    ]
    windows = [
        {"start_time": 1.0, "end_time": 2.0},
        {"start_time": 2.0, "end_time": 3.0},
    ]

    report = align_markers_to_windows(markers, windows)

    assert report["marker_count"] == 3
    assert report["markers_per_label"] == {"LEFT_HAND_IMAGERY": 2, "REST": 1}
    assert report["aligned_window_count"] == 3
    assert report["unaligned_marker_count"] == 0
    assert report["marker_alignment_pass"] is True


def test_marker_alignment_warns_for_out_of_range_markers() -> None:
    report = align_markers_to_windows(
        [MarkerEvent("OUTSIDE", 10.0, "markers", {})],
        [{"start_time": 1.0, "end_time": 2.0}],
        tolerance_seconds=0.05,
    )

    assert report["aligned_window_count"] == 0
    assert report["unaligned_marker_count"] == 1
    assert report["marker_alignment_pass"] is False
    assert report["marker_alignment_warnings"]


def test_empty_marker_report_uses_full_schema() -> None:
    report = empty_marker_report("No marker stream detected.")

    for field in {
        "marker_stream_found",
        "marker_count",
        "marker_labels",
        "markers_per_label",
        "aligned_window_count",
        "unaligned_marker_count",
        "marker_alignment_pass",
        "marker_alignment_warnings",
        "assignments",
    }:
        assert field in report


def test_eeg_artifact_summary_flags_flatline_and_nan() -> None:
    summary = summarize_eeg_artifacts(
        [[1.0, 2.0, 3.0], [0.0, 0.0, 0.0], [float("nan"), 1.0, 2.0]],
        ["C3", "C4", "Pz"],
    )

    assert summary["channel_count"] == 3
    assert summary["nan_inf_count"] == 1
    assert "C4" in summary["bad_channel_candidates"]
    assert "Pz" in summary["bad_channel_candidates"]
    assert "clinical quality" in summary["warnings"][0]


def test_eeg_artifact_merge_preserves_bad_channels() -> None:
    merged = merge_artifact_summaries([
        summarize_eeg_artifacts([[0.0, 0.0, 0.0]], ["C3"]),
        summarize_eeg_artifacts([[1.0, 2.0, 3.0]], ["C4"]),
    ])

    assert merged["window_count"] == 2
    assert merged["bad_channel_candidates"] == ["C3"]


def test_eeg_lsl_10_20_profile_matches_fixture_stream() -> None:
    profile = get_profile("eeg_lsl_10_20_fixture")
    stream = {
        "name": "NeuroVerseReplayEEG",
        "type": "EEG",
        "channel_count": 10,
        "nominal_srate": 250,
        "channel_names": ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"],
    }

    validation = validate_profile_against_stream(profile, stream)

    assert validation["ok"] is True
    assert validation["observed_channel_count"] == 10


def test_eeg_lsl_10_20_profile_rejects_wrong_stream_type() -> None:
    profile = get_profile("eeg_lsl_10_20_fixture")
    stream = {
        "name": "NeuroVerseReplayEEG",
        "type": "Markers",
        "channel_count": 10,
        "nominal_srate": 250,
        "channel_names": ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"],
    }

    validation = validate_profile_against_stream(profile, stream)

    assert validation["ok"] is False
    assert any("stream type" in error for error in validation["errors"])


def test_eeg_replay_scripts_expose_help() -> None:
    for script in ["eeg_lsl_replay_streamer.py", "run_eeg_lsl_validation_suite.py"]:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script), "--help"],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout
