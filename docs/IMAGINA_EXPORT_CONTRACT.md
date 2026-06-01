# IMAGINA Export Contract & import Validator - Version 1.0

This document defines the formal, versioned cross-repository contract interface between the **IMAGINA** modeling/research platform and the **NeuroVerse** BCI runtime platform.

---

## 1. Architectural Responsibility

```
[ IMAGINA Research Workspace ]
   - Model Training (PyTorch/Scikit-Learn)
   - curriculum & SQLite Event logs
   - Scientific Evaluations
   - Offline Metrics
              ↓
  Exports Artifact Package: exports/neuroverse/latest/
              ↓
[ NeuroVerse Gated Runtime Workspace ]
   - Path Detection & Signature Discovery
   - Package Validation (Safety & Compliance Checks)
   - Safe Import Copying (gated reports folder)
   - Fusion Engine Injection (proxy estimations only)
   - Dashboard Telemetry Presentation
```

---

## 2. Manifest Schema: `neuroverse_imagina_export.json`

Every export package must contain a top-level manifest file named `neuroverse_imagina_export.json`. 

### Required Fields & Types

| Field | Type | Description | Required / Optional |
|---|---|---|---|
| `contract_version` | String | Must be `"1.0"` | **Required** |
| `export_id` | String | Unique string identifier | **Required** |
| `generated_at` | String | ISO 8601 UTC timestamp | **Required** |
| `source_project` | String | `"external_imagina"` or `"neuroverse_fixture"` | **Required** |
| `export_type` | String | `"model_evaluation"`, `"prediction_batch"`, `"model_card_only"`, `"report_only"`, `"fixture_demo"` | **Required** |
| `modality` | String | `"eeg"`, `"fmri"`, `"feature_table"`, `"multimodal"`, `"unknown"` | **Required** |
| `paradigm` | String | `"perception_vs_imagery"`, `"rest_vs_imagery"`, `"imagery_quality"`, `"imagined_symbol"`, `"dream_proxy"`, `"unknown"` | **Required** |
| `safety` | Object | Mandatory safety compliance definitions (see below) | **Required** |
| `model` | Object | Contains model details (IDs, types, local paths) | Optional |
| `metrics` | Object | Scientific metrics dictionary and bounds | Optional |
| `predictions` | Object | Active predictions stream file details | Optional |
| `reports` | Array of Strings | Relative paths to scientific reports | Optional |

---

## 3. Strict Safety Declarations (Non-Negotiable)

The `safety` block in the manifest **MUST** match the following criteria:

```json
"safety": {
  "proxy_estimates_only": true,
  "not_decoded_content": true,
  "closed_loop_allowed": false,
  "intended_use": "Offline analysis, visual dashboard simulation, pipeline debugging.",
  "not_intended_use": "Real-time BCI closed-loop adaptiveness, raw thought decoding, raw dream interpretation."
}
```

> [!WARNING]
> If any of the following occur:
> 1. The `safety` block is missing.
> 2. `proxy_estimates_only` is set to `false`.
> 3. `not_decoded_content` is set to `false`.
> 4. `closed_loop_allowed` is set to `true`.
> 
> **The NeuroVerse Import Validator will immediately reject the package, block import actions, and generate high-severity safety audits.**

---

## 4. Import & Late Fusion Behaviors

### Case A: Only Metrics and Model Cards Exist
- **Action**: NeuroVerse registers the model card and scientific metrics in the dashboard.
- **Fusion Injection**: Inserts a `ModalityFeaturePacket` with `missing = True`, `quality_score = 0.80`, `confidence = 0.80`, and limitations stating no active prediction file was supplied. **NO fake predictions are fabricated.**

### Case B: Predictions Batch File Exists
- **Action**: NeuroVerse validates the prediction stream file.
- **Fusion Injection**: Inserts a `ModalityFeaturePacket` with `missing = False`, reading features `imagery_quality_proxy`, `imagery_engagement_proxy`, and `imagery_stability_proxy` directly from the validated file.
