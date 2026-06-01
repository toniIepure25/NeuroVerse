# NeuroVerse Final Release Checklist (v1.2.0)

This checklist outlines the absolute engineering quality gates and validation steps required before tagging the repository as `v1.2.0-public-launch`.

---

## 1. Safety & Data Privacy Gates (Non-Negotiable)
* [x] **Closed-Loop Assertions**: Verify that `closed_loop_allowed = false` is enforced in Uvicorn backend runs and static portfolio snapshots.
* [x] **Limitations Alignment**: Verify that the FastAPI `/api/v1/system/overview` endpoint and the frontend LandingPage display the 5 mandatory scientific safety disclaimers.
* [x] **Local LAN Isolation**: Ensure the backend's default socket binding defaults strictly to localhost (`127.0.0.1:8000`) in local development profiles.
* [x] **Anonymization Verification**: Scan all historical datasets inside `data/` and `reports/` to ensure 100% anonymized PhysioNet motor imagery references only.

---

## 2. Pre-Release Validation Pipelines
* [x] **Vite Bundle Check**: Run bundle sizing analysis and assert that the main JS chunk remains below the `2.5 MB` budget limits.
* [x] **A11y & Usability Auditing**: Execute accessibility audits on dynamic React route elements to verify focus reachability and header structures.
* [x] **TypeScript Type-Safety**: Ensure typescript compiler validates all lazy-loaded paths cleanly with `tsc --noEmit` (0 errors).
* [x] **API Route Completeness**: Run FastAPI smoke test and verify 63 system routes map cleanly matching expected endpoint lists.

---

## 3. Static Portfolio Baking & Portability
* [x] **Evidence Harvesting**: Run `make generate-evidence-pack` to sync all new validation checkers into standard evidence packs.
* [x] **Static Baking Sync**: Run `make static-evidence-bake` to populate the public Vite folder `/evidence` cleanly.
* [x] **Manifest Hash Drift check**: Execute `make static-evidence-check` and ensure zero file drift or configuration tampering is present.

---

## 4. Release Tagging & Packaging Steps
1. Verify the release version is correctly set:
   ```bash
   cat VERSION  # Should return v1.2.0-public-launch
   ```
2. Run final launch checklist:
   ```bash
   make public-launch-fast
   ```
3. Commit and tag:
   ```bash
   git add .
   git commit -m "chore: finalize v1.2.0 public launch packaging"
   git tag -a v1.2.0-public-launch -m "NeuroVerse v1.2.0 Public Launch Release"
   ```
4. Push static distribution to hosting provider (Github Pages/S3):
   ```bash
   cd frontend && npm run build
   # Upload frontend/dist to secure static file host
   ```
