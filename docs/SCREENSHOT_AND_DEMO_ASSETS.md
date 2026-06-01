# Screenshot and Demo Asset Guide

This guide maps out the key visual screens, interactive paths, and verification scripts for the **NeuroVerse CommandCenter** and BCI validation layers. It serves as a visual index for auditors, reviewers, and engineering stakeholders.

---

## 1. Interactive Dashboard Map & Screenshot Anchors

Below is the layout map of the CommandCenter. Each of the 8 health sectors in the grid corresponds to an auditable component in the live backend.

```
+---------------------------------------------------------------------------------+
|                               NEUROVERSE COMMAND CENTER                         |
+---------------------------------------------------------------------------------+
| [ Guided 5-Minute Tour Banner: Step 1/7 - Welcome (Start / Next / Skip) ]       |
+---------------------------------------------------------------------------------+
|  SECTOR 1: Safety State     |  SECTOR 2: Real EEG Lock   |  SECTOR 3: Data Sources |
|  - Invariant: Locked        |  - Status: Gated           |  - Simulator: Running   |
|  - State ID: SAFE_SHADOW    |  - closed_loop_allowed=0   |  - Channels: 64         |
+-----------------------------+----------------------------+-------------------------+
|  SECTOR 4: Protocol Runs    |  SECTOR 5: External IMAGINA|  SECTOR 6: Fusion Layer |
|  - Demo Run: COMPLETED      |  - Detected: Yes (../)     |  - Latency: 24ms        |
|  - Steps: 6/6 Passed        |  - Export Contract: Valid  |  - Modalities: EEG+fMRI |
+-----------------------------+----------------------------+-------------------------+
|  SECTOR 7: Observability    |  SECTOR 8: Disclaimers     |
|  - Endpoint: /api/.../view  |  - Dream Corridor Proxy    |
|  - Latency check: 14ms      |  - Static Portfolio status |
+----------------------------------------------------------+-------------------------+
| [ ProvenanceGraph: IMAGINA Research modeling -> NeuroVerse Safety adaptation ]  |
+---------------------------------------------------------------------------------+
| [ Shadow-Explainability Panel: Prediction Cosine, Gated Weights, Uncertainty ] |
+---------------------------------------------------------------------------------+
```

### Standard Screenshot Deliverables & Expected Filenames
Auditors and visual checkers expect the following files to be present:
* `assets/screenshots/01_landing.png` - Initial polished LandingPage and regulatory disclaimers.
* `assets/screenshots/02_command_center.png` - CommandCenter grid displaying all 8 health sectors in green.
* `assets/screenshots/03_provenance_graph.png` - The interactive SVG separating external modeling research from sandboxed visual adaptations.
* `assets/screenshots/04_evidence_center_section_h.png` - Dual-pane evidence panel highlighting external Imagina export status.
* `assets/screenshots/05_protocol_center_auto_run.png` - Protocol Center displaying completion reports and auto-run step passes.
* `assets/screenshots/06_data_source_wizard.png` - Ingestion wizard showcasing Lab Streaming Layer emulators and preflight check.
* `assets/screenshots/07_dream_corridor.png` - Dynamic React three-dimensional Dream Corridor visualization.
* `assets/screenshots/08_safety_governance.png` - Safety State Machine timeline panels and audit governance summaries.
* `assets/screenshots/09_fusion_imagina_proxy.png` - Late-fusion prediction variances and modality-quality proxy gauges.
* `assets/screenshots/10_hiring_page.png` - Technical hiring onboarding dashboard and task links.

---

## 2. Interactive Features & Verification Path

To demonstrate the full capability of the CommandCenter to a recruiter or auditor, follow this **2-Minute Walkthrough**:

### Step 1: Guided Tour Interaction
- **Action**: Click the **"Next"** button in the guided tour banner.
- **Expected UI Reaction**: The banner shifts context to Step 2, highlighting Sector 1 (Safety State) with an animated blue pulse border.
- **Console Log / Mock Log**:
  `[CommandCenter] Step changed from 1 to 2. Focusing on Safety State.`

### Step 2: Live-to-Static Fallback Toggle
- **Action**: Simulate a backend outage or start the UI in offline mode.
- **Expected UI Reaction**: The top bar status indicator turns from `🟢 Live Backend` to `🟠 Baked Snapshot Fallback`. The grid remains fully populated from local baked `evidence_pack/` JSON assets without throwing raw API errors.
- **Console Log / Mock Log**:
  `[API Client] Live system/overview failed. Falling back to static baked portfolio assets.`

### Step 3: Hovering the ProvenanceGraph
- **Action**: Hover over the `Modeling Research` node.
- **Expected UI Reaction**: A card pops up explaining the exact file path and contract verification results.
- **Console Log / Mock Log**:
  `[ProvenanceGraph] Focused on external modeling research node.`

---

## 3. Walkthrough Profiles for Interviewers & Stakeholders

### A. 5-Minute Reviewer Walkthrough (Executive Flow)
1. **Welcome & Onboarding**: Click the "Start" button on the **CommandCenter guided tour banner** to initialize the walkthrough.
2. **Safety Guard Assertions**: Step through Step 2 and 3 of the guided tour to highlight Sector 1 and 2, showcasing that `closed_loop_allowed = false` is an absolute software invariant.
3. **External Research Provenance**: Hover over the `Modeling Research` node in the ProvenanceGraph. Demonstrate how NeuroVerse integrates with `../Imagina` without duplicating modeling code.
4. **Shadow Explainability**: Click Step 5 of the guided tour to highlight the Shadow Explainability panel. Show the late-fusion prediction cosine similarities and uncertainty variance bounds.
5. **Offline Portfolio Verification**: Turn off the local server and show that the entire interface continues to operate natively from historical snapshots baked under `/evidence/manifest.json`.

### B. 10-Minute Technical Walkthrough (Deep-Dive Flow)
1. **Protocol Engine Execution**: Navigate to `/protocols`. Review the registered safety-first automated step protocols. Show how async operations complete step-by-step with safety status assertions.
2. **Lab Streaming Layer Ingestion**: Navigate to `/data-sources`. Run the streaming preflight checker. Show how the client parses synthetic signal diagnostics (SQI, channels, sample rate).
3. **Bake Code & Manifest Audit**: Open `scripts/bake_static_evidence.py` and explain the manifest generation. Show how it guarantees zero evidence drift by hashing baked assets.
4. **Release Gate Automation**: Show how the `make public-launch-fast` target acts as a gatekeeper, blocking release builds if Vite bundles exceed budgets or if accessibility is violated.

---

## 4. Communication Guidelines: "What to Say" vs "What Not to Say"

Reviewers and recruiters appreciate rigorous engineering safety posture over hype. Use these standard guidelines during presentations:

| Topic Area | 🟢 What to Say (Strict Scientific Integrity) | 🔴 What NOT to Say (Hyped Claims / Failures) |
|---|---|---|
| **Dream Corridor Mapping** | "The Dream Corridor acts as an adaptive visual scaffold driven by experimental task proxies and model-uncertainty metrics." | "The system reads your mind and decodes active mental imagery onto the screen in real-time." |
| **IMAGINA Modeling Role** | "IMAGINA is an external modeling framework. NeuroVerse imports and validates its metrics to assess imagery proxy quality." | "NeuroVerse directly decodes dreams and complex thoughts using an built-in AI brain scanner." |
| **System Safety Gating** | "The system is restricted to a shadow-inference mode where all adaptation commands are blocked by software invariants." | "The system is ready to adapt screen feedback based on live neural signals during public deployment." |
| **Hardware Readiness** | "Lab Streaming Layer and BrainFlow integrations are prepared and validated using high-fidelity synthetic signal generators." | "We have validated the full closed-loop pipeline with live human subjects and real OpenBCI CYTON/GALEA hardware." |
| **Regulatory & Clinical** | "This is an exploratory research-grade prototype demonstrating defensive software engineering and QA discipline." | "This system is a clinical-grade diagnostic utility ready for medical applications or neurological treatment." |

---

## 5. Mandatory Safety Disclaimers & Text Parity

The following disclaimers must remain visible by default in all presentation layouts:
* **Closed-Loop Isolation**: `"Closed-loop from real EEG is disabled by default."`
* **Scaffold Limits**: `"The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics."`
* **Imagina Proxies**: `"IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams."`
* **Static Nature**: `"Static evidence is a baked snapshot, not live runtime evidence."`
* **Hardware Status**: `"Physical OpenBCI/Galea validation remains unperformed unless a real device report exists."`

---

## 6. Verification Checklists

### Backend Validation Checklist
* [x] **Unit Testing**: Run `cd backend && python3 -m pytest app/tests/test_system_overview.py -v` (Must pass 100%).
* [x] **API Route Mapping**: Verify route is registered at `/api/v1/system/overview` with `closed_loop_allowed = false` safety assertion.
* [x] **Code Quality**: Verify zero ruff check errors: `python3 -m ruff check app/api/routes_health.py`.

### Frontend Validation Checklist
* [x] **TypeScript Compiles**: Run `npm run lint` inside the frontend directory (zero compilation errors).
* [x] **Production Build**: Run `npm run build` inside the frontend directory (generates a optimized index bundle under `dist/` successfully).
* [x] **Client Fetch Fallback**: Verify `client.ts` falls back gracefully to `getStaticSystemOverview()` on fetch failure.

### Static Mode Verification Checklist
* [x] **Static Baking**: Run `python3 scripts/bake_static_evidence.py` to populate `frontend/public/evidence`.
* [x] **Safety Proof**: Scan all JSON assets in `public/evidence` for `closed_loop_allowed: true` (Must be empty).
* [x] **Artifact Completeness**: Verify `manifest.json` correctly list all generated reports.
