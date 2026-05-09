"""Learned attention-based multimodal fusion (future implementation).

Architecture:
- Input: per-modality state vectors (or raw feature embeddings) before late averaging
- Modality encoders: small MLP per modality projecting to d_fuse
- Stacked cross-modal attention: L layers, each with multi-head attention across 3 modality tokens
- Gating: learnable scalar gates per modality (or per dimension) from SQI embeddings
- Output head: linear map to 6 cognitive dimensions + optional confidence logits

Expected tensor shapes:
- Per-modality inputs: (batch, n_modalities=3, state_dim=7) or (batch, 3, embed_dim=32)
- SQI conditioning: (batch, n_modalities) or (batch, 3, sqi_dim=4)
- After encoders: (batch, 3, d_fuse=64)
- Attention output: (batch, 3, d_fuse) then pooled to (batch, d_fuse) via attention pooling or mean
- Fused state: (batch, 6) for focus, relaxation, workload, stress, fatigue, imagery_engagement
- Confidence: (batch, 1) from an auxiliary head (optionally monotone in pooled SQI)

Training / integration TODO:
- Supervised loss against labels or teacher heuristic outputs;
  optional ranking / contrastive loss
- Train with modality dropout for robustness; mask modalities at inference when SQI is low
- Export ONNX or TorchScript for low-latency serving
- Wire SQI as prior weights in the attention mask (soft mask from normalized SQI)
"""

from __future__ import annotations

from app.schemas.state import StatePredictionPayload


class AttentionMultimodalFusion:
    def fuse(
        self,
        predictions: dict[str, StatePredictionPayload],
        sqi_scores: dict[str, float],
    ) -> StatePredictionPayload:
        raise NotImplementedError(
            "Attention-based fusion not yet implemented; use late_fusion or bayesian_fusion."
        )
