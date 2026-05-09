from __future__ import annotations

from collections.abc import Mapping

import numpy as np

from app.inference.base import StateEstimator
from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


def _get(features_dict: Mapping[str, float], key: str, default: float = 0.5) -> float:
    raw = features_dict.get(key, default)
    try:
        v = float(raw)
    except (TypeError, ValueError):
        v = default
    return float(np.clip(v, 0.0, 1.0))


class HeuristicStateEstimator(StateEstimator):
    FEATURE_WINDOW_MS = 500
    MODEL_VERSION = "heuristic-v1"

    W_FOCUS_ENGAGEMENT_INDEX = 0.30
    W_FOCUS_BETA_POWER = 0.15
    W_FOCUS_FIXATION_STABILITY = 0.25
    W_FOCUS_ONE_MINUS_FATIGUE_INDEX = 0.15
    W_FOCUS_ONE_MINUS_BLINK_RATE = 0.15

    W_RELAX_ALPHA_POWER = 0.25
    W_RELAX_RELAXATION_INDEX = 0.25
    W_RELAX_RMSSD_PROXY = 0.20
    W_RELAX_ONE_MINUS_EDA_PHASIC = 0.15
    W_RELAX_ONE_MINUS_STRESS_INDEX = 0.15

    W_WORK_THETA_POWER = 0.25
    W_WORK_PUPIL_DIAMETER_PROXY = 0.20
    W_WORK_EDA_PHASIC = 0.20
    W_WORK_STRESS_INDEX = 0.15
    W_WORK_ENGAGEMENT_INDEX = 0.10
    W_WORK_ONE_MINUS_RELAXATION_INDEX = 0.10

    W_STRESS_EDA_PHASIC = 0.25
    W_STRESS_STRESS_INDEX = 0.25
    W_STRESS_ONE_MINUS_RMSSD_PROXY = 0.20
    W_STRESS_ONE_MINUS_FIXATION_STABILITY = 0.15
    W_STRESS_HEART_RATE = 0.15

    W_FATIGUE_FATIGUE_INDEX = 0.30
    W_FATIGUE_THETA_POWER = 0.15
    W_FATIGUE_BLINK_DURATION_PROXY = 0.20
    W_FATIGUE_ONE_MINUS_ENGAGEMENT_INDEX = 0.15
    W_FATIGUE_DELTA_POWER = 0.20

    W_IMG_SPECTRAL_ENTROPY_PROXY = 0.25
    W_IMG_P300_PROXY = 0.25
    W_IMG_FIXATION_STABILITY = 0.20
    W_IMG_ONE_MINUS_GAZE_DISPERSION = 0.15
    W_IMG_ALPHA_POWER = 0.15

    CONF_W_SQI_MEAN = 0.40
    CONF_W_MODALITY_AGREEMENT = 0.35
    CONF_W_SENSOR_CONSENSUS = 0.25
    SQI_LOW_THRESHOLD = 0.40
    SQI_LOW_PENALTY_FACTOR = 0.75

    def predict(self, features: FeaturePayload) -> StatePredictionPayload:
        eeg = features.eeg
        physio = features.physio
        gaze = features.gaze

        focus = (
            self.W_FOCUS_ENGAGEMENT_INDEX * _get(eeg, "engagement_index")
            + self.W_FOCUS_BETA_POWER * _get(eeg, "beta_power")
            + self.W_FOCUS_FIXATION_STABILITY * _get(gaze, "fixation_stability")
            + self.W_FOCUS_ONE_MINUS_FATIGUE_INDEX * (1.0 - _get(eeg, "fatigue_index"))
            + self.W_FOCUS_ONE_MINUS_BLINK_RATE * (1.0 - _get(gaze, "blink_rate"))
        )

        relaxation = (
            self.W_RELAX_ALPHA_POWER * _get(eeg, "alpha_power")
            + self.W_RELAX_RELAXATION_INDEX * _get(eeg, "relaxation_index")
            + self.W_RELAX_RMSSD_PROXY * _get(physio, "rmssd_proxy")
            + self.W_RELAX_ONE_MINUS_EDA_PHASIC * (1.0 - _get(physio, "eda_phasic"))
            + self.W_RELAX_ONE_MINUS_STRESS_INDEX * (1.0 - _get(physio, "stress_index"))
        )

        workload = (
            self.W_WORK_THETA_POWER * _get(eeg, "theta_power")
            + self.W_WORK_PUPIL_DIAMETER_PROXY * _get(gaze, "pupil_diameter_proxy")
            + self.W_WORK_EDA_PHASIC * _get(physio, "eda_phasic")
            + self.W_WORK_STRESS_INDEX * _get(physio, "stress_index")
            + self.W_WORK_ENGAGEMENT_INDEX * _get(eeg, "engagement_index")
            + self.W_WORK_ONE_MINUS_RELAXATION_INDEX * (1.0 - _get(eeg, "relaxation_index"))
        )

        stress = (
            self.W_STRESS_EDA_PHASIC * _get(physio, "eda_phasic")
            + self.W_STRESS_STRESS_INDEX * _get(physio, "stress_index")
            + self.W_STRESS_ONE_MINUS_RMSSD_PROXY * (1.0 - _get(physio, "rmssd_proxy"))
            + self.W_STRESS_ONE_MINUS_FIXATION_STABILITY * (1.0 - _get(gaze, "fixation_stability"))
            + self.W_STRESS_HEART_RATE * _get(physio, "heart_rate")
        )

        fatigue = (
            self.W_FATIGUE_FATIGUE_INDEX * _get(eeg, "fatigue_index")
            + self.W_FATIGUE_THETA_POWER * _get(eeg, "theta_power")
            + self.W_FATIGUE_BLINK_DURATION_PROXY * _get(gaze, "blink_duration_proxy")
            + self.W_FATIGUE_ONE_MINUS_ENGAGEMENT_INDEX * (1.0 - _get(eeg, "engagement_index"))
            + self.W_FATIGUE_DELTA_POWER * _get(eeg, "delta_power")
        )

        imagery_engagement = (
            self.W_IMG_SPECTRAL_ENTROPY_PROXY * _get(eeg, "spectral_entropy_proxy")
            + self.W_IMG_P300_PROXY * _get(eeg, "p300_proxy")
            + self.W_IMG_FIXATION_STABILITY * _get(gaze, "fixation_stability")
            + self.W_IMG_ONE_MINUS_GAZE_DISPERSION * (1.0 - _get(gaze, "gaze_dispersion"))
            + self.W_IMG_ALPHA_POWER * _get(eeg, "alpha_power")
        )

        if features.sqi_scores:
            sqi_mean = float(
                np.clip(
                    np.mean([_get(features.sqi_scores, k) for k in features.sqi_scores]),
                    0.0,
                    1.0,
                )
            )
        else:
            sqi_mean = 0.5

        modality_agreement = _get(features.multimodal, "modality_agreement")
        sensor_consensus = _get(features.multimodal, "sensor_consensus")

        confidence = (
            self.CONF_W_SQI_MEAN * sqi_mean
            + self.CONF_W_MODALITY_AGREEMENT * modality_agreement
            + self.CONF_W_SENSOR_CONSENSUS * sensor_consensus
        )
        if features.sqi_scores and any(
            float(v) < self.SQI_LOW_THRESHOLD for v in features.sqi_scores.values()
        ):
            confidence *= self.SQI_LOW_PENALTY_FACTOR

        return StatePredictionPayload(
            focus=float(np.clip(focus, 0.0, 1.0)),
            relaxation=float(np.clip(relaxation, 0.0, 1.0)),
            workload=float(np.clip(workload, 0.0, 1.0)),
            stress=float(np.clip(stress, 0.0, 1.0)),
            fatigue=float(np.clip(fatigue, 0.0, 1.0)),
            imagery_engagement=float(np.clip(imagery_engagement, 0.0, 1.0)),
            confidence=float(np.clip(confidence, 0.0, 1.0)),
            model_version=self.MODEL_VERSION,
            feature_window_ms=self.FEATURE_WINDOW_MS,
        )
