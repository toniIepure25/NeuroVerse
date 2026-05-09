from __future__ import annotations

import numpy as np
import pytest

from app.acquisition.simulator import BiosignalSimulator
from app.features.eeg_features import extract_eeg_features
from app.features.gaze_features import extract_gaze_features
from app.features.multimodal_features import extract_multimodal_features
from app.features.physio_features import extract_physio_features

_EEG_NAMES = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"]
_PHYSIO_NAMES = ["HR", "HRV_RMSSD", "EDA_tonic", "EDA_phasic"]
_GAZE_NAMES = ["gaze_x", "gaze_y", "pupil_diameter", "blink"]


def _make_data(n_channels: int, n_samples: int = 125) -> list[list[float]]:
    rng = np.random.default_rng(0)
    return [rng.normal(0, 1, n_samples).tolist() for _ in range(n_channels)]


class TestEEGFeatures:
    def test_all_keys_present(self):
        data = _make_data(10)
        feats = extract_eeg_features(data, _EEG_NAMES, 250.0)
        expected = {
            "alpha_power", "beta_power", "theta_power", "delta_power",
            "gamma_power", "engagement_index", "relaxation_index",
            "fatigue_index", "spectral_entropy_proxy", "p300_proxy",
        }
        assert set(feats.keys()) == expected

    def test_values_bounded(self):
        data = _make_data(10)
        feats = extract_eeg_features(data, _EEG_NAMES, 250.0)
        for v in feats.values():
            assert 0.0 <= v <= 1.0, f"Value {v} out of bounds"

    def test_empty_data(self):
        feats = extract_eeg_features([], [], 250.0)
        assert all(v == 0.0 for v in feats.values())


class TestPhysioFeatures:
    def test_all_keys_present(self):
        data = [
            np.random.default_rng(0).normal(72, 2, 50).tolist(),
            np.random.default_rng(1).normal(45, 5, 50).tolist(),
            np.random.default_rng(2).normal(2.5, 0.2, 50).tolist(),
            np.random.default_rng(3).normal(0.1, 0.05, 50).tolist(),
        ]
        feats = extract_physio_features(data, _PHYSIO_NAMES)
        expected = {
            "heart_rate", "rmssd_proxy", "hrv_stability",
            "eda_tonic", "eda_phasic", "eda_peak_rate", "stress_index",
        }
        assert set(feats.keys()) == expected

    def test_values_bounded(self):
        data = [
            np.random.default_rng(0).normal(72, 2, 50).tolist(),
            np.random.default_rng(1).normal(45, 5, 50).tolist(),
            np.random.default_rng(2).normal(2.5, 0.2, 50).tolist(),
            np.random.default_rng(3).normal(0.1, 0.05, 50).tolist(),
        ]
        feats = extract_physio_features(data, _PHYSIO_NAMES)
        for v in feats.values():
            assert 0.0 <= v <= 1.0


class TestGazeFeatures:
    def test_values_bounded(self):
        data = _make_data(4, 100)
        feats = extract_gaze_features(data, _GAZE_NAMES)
        for v in feats.values():
            assert 0.0 <= v <= 1.0


class TestMultimodalFeatures:
    def test_values_bounded(self):
        eeg = extract_eeg_features(_make_data(10), _EEG_NAMES, 250.0)
        physio = extract_physio_features(
            [np.random.default_rng(i).normal(0, 1, 50).tolist() for i in range(4)],
            _PHYSIO_NAMES,
        )
        gaze = extract_gaze_features(_make_data(4, 100), _GAZE_NAMES)
        multi = extract_multimodal_features(eeg, physio, gaze)
        for v in multi.values():
            assert 0.0 <= v <= 1.0


class TestEndToEndFeatures:
    @pytest.mark.asyncio
    async def test_simulator_to_features(self):
        sim = BiosignalSimulator(duration_s=5, tick_interval_ms=100, rng=np.random.default_rng(42))
        await sim.start()
        w = await sim.get_window()
        await sim.stop()

        eeg_idx = [i for i, n in enumerate(w.channel_names) if n in set(_EEG_NAMES)]
        eeg_data = [w.data[i] for i in eeg_idx]
        eeg_names = [w.channel_names[i] for i in eeg_idx]
        feats = extract_eeg_features(eeg_data, eeg_names, w.sampling_rate)
        for v in feats.values():
            assert 0.0 <= v <= 1.0
