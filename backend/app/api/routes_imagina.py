"""IMAGINA v1 API Routes.

Exposes status, validation, preparation, training, evaluation, predictions,
and external Imagina integration layers.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.fusion.imagina_plugin import ImaginaProxyPluginV1
from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    ModalityFeaturePacket,
)
from app.imagina.baseline_model import train_imagina_baseline
from app.imagina.dataset_adapter import load_manifest, summarize_manifest, validate_manifest
from app.imagina.registry import (
    get_latest_imagina_model,
    list_imagina_models,
    load_imagina_model,
    register_imagina_model,
)
from app.integrations.imagina import (
    detect_external_imagina_project,
    external_imagina_to_fusion_packet,
    get_latest_external_imagina_artifacts,
    imagina_export_to_fusion_packet,
    import_imagina_export,
    scan_external_imagina_artifacts,
    validate_imagina_export_package,
)

router = APIRouter(prefix="/api/v1/imagina", tags=["imagina"])
_PROXY_FALLBACK = ImaginaProxyPluginV1()


class ManifestValidatePayload(BaseModel):
    manifest_path: str = Field(default="configs/imagina/example_imagina_manifest.json")


class TrainBaselinePayload(BaseModel):
    manifest_path: str = Field(default="configs/imagina/example_imagina_manifest.json")
    model_type: str = Field(default="logistic_regression")
    split_strategy: str = Field(default="fixture")
    target_type: str = Field(default="classification")


class PredictProxyPayload(BaseModel):
    eeg_packet: ModalityFeaturePacket | None = None
    self_report_packet: ModalityFeaturePacket | None = None
    task_metadata: dict[str, Any] | None = None
    calibration_baseline: dict[str, Any] | None = None


class ExportPayload(BaseModel):
    manifest_path: str = Field(default="exports/neuroverse/latest/neuroverse_imagina_export.json")


@router.get("/status")
async def imagina_status() -> dict[str, Any]:
    """Retrieve IMAGINA plugin status, latest model, and limitations."""
    ext_status = detect_external_imagina_project()
    latest_internal = get_latest_imagina_model()

    # Check for latest valid import
    latest_import = None
    latest_import_path = Path("reports/external_imagina_imports/latest_import_summary.json")
    if latest_import_path.exists():
        try:
            latest_import = json.loads(latest_import_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # active_source precedence: external_contract > external_imagina > internal_fixture_fallback
    if latest_import and latest_import.get("valid"):
        active_source = "external_contract"
    elif ext_status.exists:
        active_source = "external_imagina"
    else:
        active_source = "internal_fixture_fallback"

    # Enforce strict scientific and product framing
    limitations = [
        "IMAGINA is an external research/modeling project. NeuroVerse is the safety-gated runtime and neuroadaptive interface layer.",
        "IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams.",
        "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.",
        CLOSED_LOOP_LIMITATION,
        PROXY_LIMITATION,
    ]

    return {
        "status": "active",
        "plugin_id": "imagina_v1",
        "active_source": active_source,
        "contract_supported": True,
        "latest_valid_import": latest_import,
        "external_project_status": ext_status.model_dump(),
        "internal_fixture_status": {
            "available": True,
            "latest_model": latest_internal,
            "warnings": [
                "Internal fixture model is only intended for pipeline demo / smoke testing.",
                "It does not represent the real Imagina research model."
            ]
        },
        "proxy_estimates_only": True,
        "not_decoded_content": True,
        "closed_loop_allowed": False,
        "limitations": limitations,
        "provenance": {
            "version": "1.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "scientific_framing": limitations[0],
        }
    }


@router.get("/external/status")
async def get_external_status() -> dict[str, Any]:
    """Get status of the external Imagina project."""
    ext = detect_external_imagina_project()
    return ext.model_dump()


@router.get("/external/artifacts")
async def get_external_artifacts() -> dict[str, Any]:
    """Get list of scanned external model and report artifacts."""
    ext = detect_external_imagina_project()
    if not ext.exists:
        raise HTTPException(
            status_code=404,
            detail=f"External Imagina project not found at: {ext.project_root}"
        )
    arts = scan_external_imagina_artifacts()
    return {
        "project_root": ext.project_root,
        "artifacts": [art.model_dump() for art in arts]
    }


@router.get("/external/latest")
async def get_external_latest() -> dict[str, Any]:
    """Get latest scanned external artifacts."""
    ext = detect_external_imagina_project()
    if not ext.exists:
        raise HTTPException(
            status_code=404,
            detail=f"External Imagina project not found at: {ext.project_root}"
        )
    return get_latest_external_imagina_artifacts()


@router.post("/external/refresh")
async def refresh_external_status() -> dict[str, Any]:
    """Force rescan of external project artifacts and return updated status."""
    ext = detect_external_imagina_project()
    arts = scan_external_imagina_artifacts()
    return {
        "status": "refreshed",
        "external_project_status": ext.model_dump(),
        "artifact_count": len(arts)
    }


def resolve_payload_manifest_path(payload_path: str) -> Path:
    p = Path(payload_path)
    if p.is_absolute():
        return p
    # Try local first
    if p.exists():
        return p.resolve()
    # Try relative to NEUROVERSE_IMAGINA_ROOT
    from app.integrations.imagina.external_client import resolve_external_imagina_root
    ext_root = resolve_external_imagina_root()
    ext_p = ext_root / p
    if ext_p.exists():
        return ext_p.resolve()
    return p.resolve()


@router.post("/external/to-fusion-packet")
async def convert_to_fusion_packet() -> dict[str, Any]:
    """Convert latest external Imagina prediction or report into a Fusion modality packet."""
    packet = external_imagina_to_fusion_packet()
    return packet.model_dump()


@router.get("/external/contract")
async def get_external_contract_template() -> dict[str, Any]:
    """Retrieve versioned template schema for the Imagina export contract v1."""
    return {
        "contract_version": "1.0",
        "description": "Cross-repository schema contract between IMAGINA and NeuroVerse.",
        "template": {
            "contract_version": "1.0",
            "export_id": "imagina_export_session_001",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_project": "external_imagina",
            "export_type": "model_evaluation",
            "modality": "eeg",
            "paradigm": "perception_vs_imagery",
            "model": {
                "model_id": "imagina_rf_v1",
                "model_name": "Random Forest Vividness Classifier",
                "model_type": "random_forest",
                "checkpoint_path": "models/imagina_rf_v1.pkl",
                "model_card_path": "models/model_card.md"
            },
            "metrics": {
                "metrics_path": "reports/scientific_report.json",
                "primary_metric": "accuracy",
                "primary_metric_value": 0.88,
                "split_strategy": "leave_one_subject_out",
                "subject_count": 10,
                "sample_count": 240,
                "limitations": [
                    "Requires strict LSL jitter calibration.",
                    "Only trained on alpha-rhythm power bands."
                ]
            },
            "predictions": {
                "predictions_path": "data/latest_predictions.json",
                "prediction_schema": {
                    "imagery_quality_proxy": "float 0-1",
                    "imagery_engagement_proxy": "float 0-1",
                    "imagery_stability_proxy": "float 0-1",
                    "confidence": "float 0-1"
                },
                "sample_count": 1
            },
            "reports": [
                "reports/session_123_curriculum_ablation.md"
            ],
            "safety": {
                "proxy_estimates_only": True,
                "not_decoded_content": True,
                "closed_loop_allowed": False,
                "intended_use": "Offline modeling, visualization pipeline testing, academic publication reporting.",
                "not_intended_use": "Real-time BCI closed-loop motor control, real-time thought decoding, commercial applications."
            },
            "limitations": [
                "IMAGINA exports are experimental imagery proxy artifacts, not decoded thoughts or dreams.",
                "NeuroVerse validates and consumes IMAGINA artifacts; it does not train the source-of-truth IMAGINA model."
            ]
        }
    }


@router.post("/external/validate-export")
async def api_validate_export(payload: ExportPayload) -> dict[str, Any]:
    """Validate a given export package manifest JSON structure and referenced files."""
    resolved_path = resolve_payload_manifest_path(payload.manifest_path)
    res = validate_imagina_export_package(resolved_path)
    return res.model_dump()


@router.post("/external/import-export")
async def api_import_export(payload: ExportPayload) -> dict[str, Any]:
    """Import a validated IMAGINA export manifest and its associated artifact package."""
    resolved_path = resolve_payload_manifest_path(payload.manifest_path)
    res = import_imagina_export(resolved_path)
    return res


@router.post("/external/export-to-fusion-packet")
async def api_export_to_fusion_packet(payload: ExportPayload) -> dict[str, Any]:
    """Convert a validated IMAGINA export manifest into a standard ModalityFeaturePacket."""
    resolved_path = resolve_payload_manifest_path(payload.manifest_path)
    res = validate_imagina_export_package(resolved_path)
    if not res.valid or not res.manifest:
        raise HTTPException(
            status_code=400,
            detail=f"Export manifest is invalid or missing: {res.errors}"
        )
    packet = imagina_export_to_fusion_packet(res.manifest, resolved_path)
    return packet.model_dump()


@router.get("/external/imports/latest")
async def get_latest_import() -> dict[str, Any]:
    """Retrieve the latest successfully imported export summary from the imports registry."""
    latest_path = Path("reports/external_imagina_imports/latest_import_summary.json")
    if not latest_path.exists():
        return {
            "available": False,
            "message": "No external IMAGINA export packages have been imported yet.",
            "instructions": "Run 'make imagina-import-export' or call POST /api/v1/imagina/external/import-export with your manifest path."
        }

    try:
        summary = json.loads(latest_path.read_text(encoding="utf-8"))

        # Load human-readable markdown import summary if present next to the manifest
        summary_dir = Path(summary["target_dir"])
        md_path = summary_dir / "import_summary.md"
        summary_md = ""
        if md_path.exists():
            summary_md = md_path.read_text(encoding="utf-8")

        return {
            "available": True,
            "summary": summary,
            "summary_md": summary_md,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load latest import summary: {e}"
        )


@router.post("/manifest/validate")
async def api_validate_manifest(payload: ManifestValidatePayload) -> dict[str, Any]:
    """Validate a given JSON manifest file path (fixture only)."""
    res = validate_manifest(payload.manifest_path)
    return {
        **res,
        "manifest_path": payload.manifest_path,
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "not_decoded_content": True,
    }


@router.post("/dataset/prepare")
async def api_prepare_dataset(payload: ManifestValidatePayload) -> dict[str, Any]:
    """Validate and prepare a feature-level dataset summary from a manifest (fixture only)."""
    try:
        summary = summarize_manifest(payload.manifest_path)
        return {
            "status": "prepared",
            "manifest_path": payload.manifest_path,
            "dataset_summary": summary,
            "proxy_estimates_only": True,
            "closed_loop_allowed": False,
            "limitations": [IMAGINA_LIMITATION],
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to prepare dataset: {exc}")


@router.post("/train-baseline")
async def api_train_baseline(payload: TrainBaselinePayload) -> dict[str, Any]:
    """Train a conservative baseline fixture model (demo only)."""
    run_id = f"imagina_v1_fixture_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    output_dir = Path("reports/imagina_v1") / run_id

    try:
        # Run training
        res = train_imagina_baseline(
            manifest_path=payload.manifest_path,
            output_dir=output_dir,
            split_strategy=payload.split_strategy,  # type: ignore
            model_type=payload.model_type,
            target_type=payload.target_type,  # type: ignore
        )

        # Register in central folder
        register_imagina_model(run_id, res)

        return {
            "status": "success",
            "run_id": run_id,
            "metrics": res["metrics"],
            "leakage_warnings": [
                "Internal NeuroVerse baseline: Trained on synthetic/fixture demo data for pipeline verification only.",
                *res["leakage_warnings"]
            ],
            "artifact_paths": res["artifacts"],
            "proxy_estimates_only": True,
            "closed_loop_allowed": False,
            "limitations": [
                "IMAGINA v1 outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.",
                IMAGINA_LIMITATION,
            ]
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Training failed: {exc}")


@router.post("/evaluate")
async def api_evaluate_manifest(payload: ManifestValidatePayload) -> dict[str, Any]:
    """Load and perform a workflow prediction evaluation on a prepared dataset (fixture only)."""
    try:
        manifest = load_manifest(payload.manifest_path)
        latest = get_latest_imagina_model()
        if not latest:
            raise HTTPException(
                status_code=404,
                detail="No trained baseline model is registered. Please call POST /api/v1/imagina/train-baseline first."
            )

        model = load_imagina_model(latest["model_id"])

        predictions = []
        for sample in manifest.samples:
            feat_dict = dict(sample.features)
            row = [float(feat_dict.get(fname, 0.0)) for fname in model.feature_names]
            import numpy as np
            pred_idx = int(model.predict(np.array([row]))[0])
            pred_label = model.classes[pred_idx] if model.classes else str(pred_idx)

            predictions.append({
                "sample_id": sample.sample_id,
                "true_label": sample.label or sample.task,
                "predicted_label": pred_label,
            })

        return {
            "model_id": latest["model_id"],
            "predictions": predictions,
            "proxy_estimates_only": True,
            "not_decoded_content": True,
            "closed_loop_allowed": False,
            "limitations": [IMAGINA_LIMITATION]
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Evaluation failed: {exc}")


@router.get("/models")
async def api_list_imagina_models() -> dict[str, Any]:
    """List both external Imagina model artifacts and internal fixture stubs."""
    # List internal models first
    internals = list_imagina_models()
    for m in internals:
        m["source_project"] = "neuroverse_fixture"
        if "metrics" in m and isinstance(m["metrics"], dict):
            m["metrics"]["leakage_warnings"] = [
                "Internal fixture baseline only. Trained on synthetic/fixture demo data.",
                *(m["metrics"].get("leakage_warnings") or [])
            ]

    # Scan external artifacts
    externals: list[dict[str, Any]] = []
    try:
        scanned = scan_external_imagina_artifacts()
        for art in scanned:
            if art.artifact_type == "model":
                externals.append({
                    "model_id": art.model_id,
                    "path": art.path,
                    "model_type": art.metrics.get("model_type", "scikit-learn") if art.metrics else "scikit-learn",
                    "dataset_id": art.metrics.get("dataset_id", "external_dataset") if art.metrics else "external_dataset",
                    "target": art.target,
                    "registered_at": art.created_at,
                    "imagina_model": True,
                    "source_project": "external_imagina",
                    "metrics": art.metrics,
                })
    except Exception:
        pass

    return {
        "models": externals + internals,
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
    }


@router.get("/models/{model_id}")
async def api_get_imagina_model(model_id: str) -> dict[str, Any]:
    """Retrieve details of a model by its ID (from external or internal sources)."""
    # Check internal first
    internals = list_imagina_models()
    for m in internals:
        if m["model_id"] == model_id:
            m["source_project"] = "neuroverse_fixture"
            return m

    # Check external second
    scanned = scan_external_imagina_artifacts()
    for art in scanned:
        if art.model_id == model_id:
            return {
                "model_id": art.model_id,
                "path": art.path,
                "model_type": art.metrics.get("model_type", "scikit-learn") if art.metrics else "scikit-learn",
                "dataset_id": art.metrics.get("dataset_id", "external_dataset") if art.metrics else "external_dataset",
                "target": art.target,
                "registered_at": art.created_at,
                "imagina_model": True,
                "source_project": "external_imagina",
                "metrics": art.metrics,
                "model_card": art.model_card,
            }

    raise HTTPException(status_code=404, detail="Model not found")


@router.post("/predict-proxy")
async def api_predict_proxy(payload: PredictProxyPayload) -> dict[str, Any]:
    """Inference proxy endpoint.

    Uses external Imagina prediction if available, otherwise falls back to
    internal trained model, and finally the rule-based proxy plugin.
    """
    # 1. Try external Imagina prediction first
    try:
        packet = external_imagina_to_fusion_packet()
        if not packet.missing and "imagery_quality_proxy" in packet.features:
            features = packet.features
            return {
                "imagery_quality_proxy": features.get("imagery_quality_proxy"),
                "imagery_stability_proxy": features.get("imagery_stability_proxy"),
                "imagery_engagement_proxy": features.get("imagery_engagement_proxy"),
                "confidence": packet.confidence or 0.70,
                "not_decoded_content": True,
                "source": "external_imagina",
                "model_id": packet.provenance.get("model_id"),
                "limitations": packet.limitations,
                "provenance": packet.provenance,
            }
    except Exception:
        pass

    # 2. Try internal trained model
    latest = get_latest_imagina_model()
    if latest and payload.eeg_packet and not payload.eeg_packet.missing:
        try:
            model = load_imagina_model(latest["model_id"])
            feat_dict = payload.eeg_packet.features
            row = [float(feat_dict.get(fname, 0.5)) for fname in model.feature_names]
            import numpy as np
            pred = model.predict(np.array([row]))[0]

            if model.target_type == "classification":
                score = 0.75 if int(pred) == 1 else 0.35
            else:
                score = float(pred)

            prob = model.predict_proba(np.array([row]))
            confidence = float(prob[0][int(pred)]) if prob is not None else 0.65

            return {
                "imagery_quality_proxy": score,
                "imagery_stability_proxy": score * 0.90,
                "imagery_engagement_proxy": score * 0.95,
                "confidence": confidence,
                "not_decoded_content": True,
                "source": "internal_fixture_fallback",
                "model_id": latest["model_id"],
                "limitations": [
                    "IMAGINA outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.",
                    IMAGINA_LIMITATION,
                ],
                "provenance": {
                    "source": "imagina_v1_baseline_prediction",
                    "model_id": latest["model_id"],
                }
            }
        except Exception:
            pass

    # 3. Fallback to the rule-based proxy plugin
    output = _PROXY_FALLBACK.evaluate(
        eeg_packet=payload.eeg_packet,
        self_report_packet=payload.self_report_packet,
        task_metadata=payload.task_metadata,
        calibration_baseline=payload.calibration_baseline,
    )
    return {
        "imagery_quality_proxy": output.imagery_quality_proxy,
        "imagery_stability_proxy": output.imagery_stability_proxy,
        "imagery_engagement_proxy": output.imagery_engagement_proxy,
        "confidence": output.confidence,
        "not_decoded_content": output.not_decoded_content,
        "source": "proxy_plugin",
        "limitations": output.limitations,
        "provenance": output.provenance,
    }
