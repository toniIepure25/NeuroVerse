from __future__ import annotations

from app.core.engine import _split_channels
from app.features.eeg_features import extract_eeg_features
from app.features.gaze_features import extract_gaze_features
from app.features.multimodal_features import extract_multimodal_features
from app.features.physio_features import extract_physio_features
from app.schemas.session import FeaturePayload
from app.schemas.signals import RawSignalPayload
from app.signal_quality.eeg_sqi import compute_eeg_sqi
from app.signal_quality.gaze_sqi import compute_gaze_sqi
from app.signal_quality.physio_sqi import compute_physio_sqi
from app.signal_quality.sqi import compute_multimodal_sqi


def extract_features_and_sqi(window: RawSignalPayload) -> FeaturePayload:
    eeg_d, eeg_n, physio_d, physio_n, gaze_d, gaze_n = _split_channels(
        window.data,
        window.channel_names,
    )
    if window.modality == "eeg" and not eeg_d and window.data:
        eeg_d = window.data
        eeg_n = window.channel_names
    eeg_feats = extract_eeg_features(eeg_d, eeg_n, window.sampling_rate)
    physio_feats = extract_physio_features(physio_d, physio_n)
    gaze_feats = extract_gaze_features(gaze_d, gaze_n)
    multi_feats = extract_multimodal_features(eeg_feats, physio_feats, gaze_feats)

    eeg_sqi = compute_eeg_sqi(eeg_d, eeg_n)
    physio_sqi = compute_physio_sqi(physio_d, physio_n)
    gaze_sqi = compute_gaze_sqi(gaze_d, gaze_n)
    multimodal_sqi = compute_multimodal_sqi(eeg_sqi, physio_sqi, gaze_sqi)
    return FeaturePayload(
        eeg=eeg_feats,
        physio=physio_feats,
        gaze=gaze_feats,
        multimodal=multi_feats,
        sqi_scores={
            "eeg": round(eeg_sqi, 4),
            "physio": round(physio_sqi, 4),
            "gaze": round(gaze_sqi, 4),
            "multimodal": round(multimodal_sqi, 4),
        },
    )
