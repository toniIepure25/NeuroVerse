# NeuroVerse Phase 2.5 Report

## What Phase 2.5 Adds

Phase 2.5 hardens the research workflow around the existing Phase 2 backend:

- dataset validation reports;
- safe model activation and deactivation;
- runtime status APIs;
- standardized experiment report artifacts;
- replay/session summary reports;
- a minimal frontend Research Panel;
- Makefile workflow targets for repeatable demos.

The Phase 1 synthetic live demo remains intact, and the heuristic estimator remains the default.

## Backend APIs

New or hardened endpoints:

- `GET /api/runtime/status`
- `GET /api/models/active`
- `POST /api/models/{model_id}/activate`
- `POST /api/models/deactivate`
- `POST /api/datasets/validate`
- `GET /api/evaluation/latest`
- `GET /api/sessions/{session_id}/summary`

Model activation validates artifact presence, metadata, prediction semantics, and feature names. It is
rejected while a live session is running.

## Frontend Research Panel

The Research Panel shows:

- runtime estimator/source status;
- active model and registry entries;
- latest evaluation metrics;
- configured datasets;
- a visible research-only disclaimer.

It does not replace the Meditation Chamber or existing dashboard cards.

## Dataset Validation

Validation reports are written to `reports/datasets/` and include label distribution, feature health,
group/leakage warnings, and windowing metadata. These reports are engineering checks, not scientific
validation of cognitive state.

## Replay Summary

Replay/session summaries include event counts, safety block rate, action distribution, state averages,
oscillation rates, and model/dataset provenance.

## Limitations

- Learned models remain proxy estimators trained on dataset-derived labels.
- No real hardware streaming, transformer training, cloud storage, or database was added.
- Dataset validation does not prove scientific validity or clinical utility.
- The platform remains a research prototype and is not a medical device.

## Next Phase

Validate the adapters against real local dataset copies, add richer cross-subject evaluation protocols,
and consider a small heuristic-vs-learned comparison workflow.
