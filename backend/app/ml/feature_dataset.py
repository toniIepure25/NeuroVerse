from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from app.datasets.schemas import FeatureDataset, WindowedSample
from app.features.eeg_features import extract_eeg_features
from app.features.gaze_features import extract_gaze_features
from app.features.multimodal_features import extract_multimodal_features
from app.features.physio_features import extract_physio_features
from app.signal_quality.eeg_sqi import compute_eeg_sqi
from app.signal_quality.gaze_sqi import compute_gaze_sqi
from app.signal_quality.physio_sqi import compute_physio_sqi
from app.signal_quality.sqi import compute_multimodal_sqi

_EEG_CHANNELS = {"Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"}
_PHYSIO_CHANNELS = {"HR", "HRV_RMSSD", "EDA_tonic", "EDA_phasic"}
_GAZE_CHANNELS = {"gaze_x", "gaze_y", "pupil_diameter", "blink"}


def build_feature_dataset(
    samples: list[WindowedSample],
    target: str | None = None,
) -> FeatureDataset:
    if not samples:
        raise ValueError("No samples supplied")
    target_name = target or _first_label(samples)
    rows = [_features_for_sample(sample) for sample in samples]
    feature_names = sorted({key for row in rows for key in row})
    x_values = np.array(
        [[float(row.get(name, 0.0)) for name in feature_names] for row in rows], dtype=float
    )
    y = np.array([sample.labels.get(target_name) for sample in samples], dtype=object)
    groups = [f"{sample.subject_id}:{sample.session_id}" for sample in samples]
    return FeatureDataset(
        X=x_values,
        y=y,
        feature_names=feature_names,
        label_names=[target_name],
        groups=groups,
        metadata={
            "dataset_id": samples[0].dataset_id,
            "target": target_name,
            "sample_count": len(samples),
            "feature_version": "phase2-feature-v1",
        },
    )


def _first_label(samples: list[WindowedSample]) -> str:
    preferred = ["phase_label", "workload_class", "label", "workload_score"]
    keys = set().union(*(sample.labels.keys() for sample in samples))
    for key in preferred:
        if key in keys:
            return key
    if keys:
        return sorted(keys)[0]
    raise ValueError("Samples do not contain labels")


def _split_channels(
    data: list[list[float]],
    channel_names: list[str],
) -> tuple[
    list[list[float]],
    list[str],
    list[list[float]],
    list[str],
    list[list[float]],
    list[str],
]:
    eeg_data, eeg_names = [], []
    physio_data, physio_names = [], []
    gaze_data, gaze_names = [], []
    for i, name in enumerate(channel_names):
        if i >= len(data):
            break
        if name in _EEG_CHANNELS:
            eeg_data.append(data[i])
            eeg_names.append(name)
        elif name in _PHYSIO_CHANNELS:
            physio_data.append(data[i])
            physio_names.append(name)
        elif name in _GAZE_CHANNELS:
            gaze_data.append(data[i])
            gaze_names.append(name)
    return eeg_data, eeg_names, physio_data, physio_names, gaze_data, gaze_names


def _features_for_sample(sample: WindowedSample) -> dict[str, float]:
    if sample.features is not None:
        return {str(k): float(v) for k, v in sample.features.items()}

    eeg: dict[str, float] = {}
    physio: dict[str, float] = {}
    gaze: dict[str, float] = {}
    sqi: dict[str, float] = {}

    if "multimodal" in sample.data_by_modality:
        data = sample.data_by_modality["multimodal"]
        eeg_d, eeg_n, physio_d, physio_n, gaze_d, gaze_n = _split_channels(
            data.get("data", []),
            data.get("channel_names", []),
        )
        sr = float(data.get("sampling_rate", 1.0))
        eeg = extract_eeg_features(eeg_d, eeg_n, sr)
        physio = extract_physio_features(physio_d, physio_n)
        gaze = extract_gaze_features(gaze_d, gaze_n)
        sqi["eeg"] = compute_eeg_sqi(eeg_d, eeg_n)
        sqi["physio"] = compute_physio_sqi(physio_d, physio_n)
        sqi["gaze"] = compute_gaze_sqi(gaze_d, gaze_n)
    else:
        if "eeg" in sample.data_by_modality:
            item = sample.data_by_modality["eeg"]
            eeg = extract_eeg_features(
                item.get("data", []),
                item.get("channel_names", []),
                float(item.get("sampling_rate", 1.0)),
            )
            sqi["eeg"] = compute_eeg_sqi(item.get("data", []), item.get("channel_names", []))
        if "physio" in sample.data_by_modality:
            item = sample.data_by_modality["physio"]
            physio = extract_physio_features(item.get("data", []), item.get("channel_names", []))
            sqi["physio"] = compute_physio_sqi(item.get("data", []), item.get("channel_names", []))
        if "gaze" in sample.data_by_modality:
            item = sample.data_by_modality["gaze"]
            gaze = extract_gaze_features(item.get("data", []), item.get("channel_names", []))
            sqi["gaze"] = compute_gaze_sqi(item.get("data", []), item.get("channel_names", []))

    multimodal = extract_multimodal_features(eeg, physio, gaze)
    if sqi:
        sqi["multimodal"] = compute_multimodal_sqi(
            sqi.get("eeg", 0.5),
            sqi.get("physio", 0.5),
            sqi.get("gaze", 0.5),
        )

    out: dict[str, float] = {}
    for prefix, values in (
        ("eeg", eeg),
        ("physio", physio),
        ("gaze", gaze),
        ("multimodal", multimodal),
        ("sqi", sqi),
    ):
        out.update({f"{prefix}_{key}": float(value) for key, value in values.items()})
    return out


def save_feature_dataset(dataset: FeatureDataset, path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    meta_path = out.with_suffix(out.suffix + ".metadata.json")
    metadata = {
        "feature_names": dataset.feature_names,
        "label_names": dataset.label_names,
        "metadata": dataset.metadata,
    }
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
    if out.suffix == ".npz":
        return dataset.save_npz(out)
    frame = dataset.to_frame()
    if out.suffix == ".parquet":
        try:
            frame.to_parquet(out, index=False)
            return out
        except Exception:
            out = out.with_suffix(".csv")
    frame.to_csv(out, index=False)
    return out


def load_feature_dataset(path: str | Path) -> FeatureDataset:
    src = Path(path)
    if src.suffix == ".npz":
        return FeatureDataset.load_npz(src)
    meta_path = src.with_suffix(src.suffix + ".metadata.json")
    with open(meta_path) as f:
        metadata = json.load(f)
    frame = pd.read_parquet(src) if src.suffix == ".parquet" else pd.read_csv(src)
    return FeatureDataset.from_frame(
        frame,
        feature_names=list(metadata["feature_names"]),
        label_names=list(metadata["label_names"]),
        metadata=dict(metadata.get("metadata") or {}),
    )
