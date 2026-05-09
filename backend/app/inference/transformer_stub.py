"""Transformer-based multimodal fusion state estimator (future implementation).

Architecture:
- Input: temporal windows of features per modality (EEG, physio, gaze)
- Modality token embeddings: learned embeddings per sensor modality
- Temporal transformer encoder: 4-layer, 8-head attention over time steps
- Cross-modal attention: modality tokens attend to each other
- Uncertainty head: predict aleatoric + epistemic uncertainty per state
- State prediction heads: 6 linear heads for cognitive dimensions

Expected tensor shapes:
- Input: (batch, n_modalities=3, time_steps=10, feature_dim=16)
- Modality embeddings: (n_modalities, d_model=64)
- Transformer output: (batch, n_modalities, d_model)
- State predictions: (batch, 6)
- Uncertainty: (batch, 6, 2)  # mean, variance per state

Training requirements:
- Labeled neurocognitive dataset (e.g., DEAP, SEED, or custom)
- Cross-subject validation
- Calibration fine-tuning per user
"""

from __future__ import annotations

from app.inference.base import StateEstimator
from app.schemas.session import FeaturePayload
from app.schemas.state import StatePredictionPayload


class TransformerFusionEstimator(StateEstimator):
    def predict(self, features: FeaturePayload) -> StatePredictionPayload:
        raise NotImplementedError(
            "Transformer fusion model not yet implemented. "
            "Requires PyTorch and a trained checkpoint."
        )
