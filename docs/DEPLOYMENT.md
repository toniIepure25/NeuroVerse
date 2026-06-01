# NeuroVerse CommandCenter Deployment and Hydration Guide

This document describes how to deploy the NeuroVerse CommandCenter, set up the live-to-static fallback pipelines, and configure the runtime environments for audits, technical reviews, and recruiter walkthroughs.

---

## 1. Deployment Environments

The CommandCenter supports two primary hydration modes, automatically determined at runtime based on backend accessibility:

```
+-----------------------------------------------------------+
|                      Client Web Browser                   |
+-----------------------------------------------------------+
                              |
              Does Live Backend Respond (GET /overview)?
             /                                         \
          [Yes]                                       [No]
           /                                             \
          v                                               v
+-----------------------+                       +-----------------------+
|  🟢 Live Backend Mode  |                       | 🟠 Baked Snapshot Mode|
|  - Queries FastAPI    |                       | - Fetches public/     |
|    routes in real-time|                       |   evidence/*.json     |
+-----------------------+                       +-----------------------+
```

### A. Live Backend Environment (`live_backend`)
Used during active local development, live simulator testing, or live hardware validation trials.

* **Backend Server**: Uvicorn running on port 8000.
* **Database / Cache**: Aggregates live protocol engine state, LSL streaming buffers, and external Imagina imports.
* **Deployment Steps**:
  1. Boot the backend server:
     ```bash
     cd backend && uvicorn app.main:create_app --factory --port 8000
     ```
  2. Boot the frontend dev server:
     ```bash
     cd frontend && npm run dev
     ```
  3. The client queries `/api/v1/system/overview` every 10 seconds to update all sectors in real-time.

### B. Static Portfolio Environment (`static_portfolio`)
Used for serverless deployments (such as GitHub Pages or static S3 hosting) where no live Python backend is running, allowing reviewers to browse the interface fully hydrated from historical snapshots.

* **Frontend Server**: Vite static assets bundle serving standard HTML/JS/CSS.
* **Snapshot Storage**: Files under `frontend/public/evidence/`.
* **Deployment Steps**:
  1. Generate all validation evidence and QA checklists on a development machine:
     ```bash
     make reviewer-ready-check
     ```
  2. Build the optimized static distribution folder:
     ```bash
     cd frontend && npm run build
     ```
  3. Deploy the resulting `frontend/dist/` folder to any static hosting provider.
  4. The client automatically detects the absence of the live FastAPI port, triggers the fallback handler `getStaticSystemOverview()`, and loads the baked JSON assets, providing a seamless zero-server interactive portfolio.

---

## 2. Client-Side Hydration Mechanics

The fallback logic is implemented inside the client-side API handler `frontend/src/api/client.ts`.

### Fallback Lifecycle
1. The `CommandCenter.tsx` page calls `getSystemOverview()`.
2. `getSystemOverview()` attempts to fetch `http://localhost:8000/api/v1/system/overview`.
3. If the fetch is successful:
   - Sets the state `source` to `"live_backend"`.
   - Returns the live system status payload.
4. If the fetch fails (due to connection timeout or 404/500 errors):
   - Triggers `getStaticSystemOverview()`.
   - Fetches the baked manifest from `/evidence/manifest.json`.
   - Fetches all required sector documents (`latest_auto_run_protocol.json`, `data_source_readiness_snapshot.json`, etc.) from `/evidence/`.
   - Resolves a synthesized payload mapping these static files into the corresponding sectors, setting the state `source` to `"static_snapshot"`.
   - Updates the dashboard with a visual warning: `"Baked Snapshot Fallback"`.

---

## 3. Operations & Maintenance

### How to Manually Force Static Mode in Development
If you are developing components and want to force the dashboard to run in offline/static mode even if your backend is running:
- Open `frontend/src/api/client.ts`.
- Locate `getSystemOverview()`.
- Add `throw new Error("Forced static mode dev test");` at the top of the `try` block.
- The UI will immediately switch to static fallback mode on refresh.

### Troubleshooting Missing Sector Data in Static Mode
If some sectors in the CommandCenter display `[Missing Data]` in static mode:
1. Run `make check-static-portfolio` to see which files are missing.
2. Regenerate the missing evidence by running the appropriate make targets:
   - Protocol runs: `make protocol-run-demo`
   - Calibration: `make fusion-calibrate`
   - External Imagina contract: `make imagina-import-export`
3. Run `make generate-evidence-pack` followed by `make bake-static-evidence` to copy the fresh snapshots into the `public/evidence` folder.
4. Re-run `make check-static-portfolio` to confirm completeness.
