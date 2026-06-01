# NeuroVerse Demonstration Script

This script provides a step-by-step technical narration, mock terminal logs, and exact expected UI reactions for presenting the NeuroVerse CommandCenter to auditors, reviewers, and engineering recruiters.

---

## Narration Part 1: System Boot & Live Observability (0:00 - 0:45)

**Narration**:
> *"Welcome to the NeuroVerse Command Center. I will show you how our system architecture enforces a clean separation between external modeling research and our safety-gated runtime."*
> *"Let's boot the system using our standard backend orchestrator. We will see the live observability stream hydrate the UI."*

### Step 1: Boot Backend
- **Action**: Run `cd backend && uvicorn app.main:create_app --factory --port 8000` (or `make dev`).
- **Expected Terminal Output**:
  ```
  INFO:     Started server process [12345]
  INFO:     Waiting for application startup.
  [INFO] BCI Safety Governance Layer initialized in shadow-only mode.
  [INFO] Invariant check: closed_loop_allowed = False.
  INFO:     Application startup complete.
  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
  ```

### Step 2: Query Overview API
- **Action**: Query the overview API at `/api/v1/system/overview` using `curl`.
- **Expected API Response (Truncated for readability)**:
  ```json
  {
    "source": "live_backend",
    "generated_at": "2026-06-02T01:10:00.123Z",
    "warnings": [],
    "limitations": [
      "Closed-loop from real EEG is disabled by default.",
      "The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics."
    ],
    "closed_loop_allowed": false,
    "safety": {
      "current_state": "SAFE_SHADOW",
      "severity": "NORMAL",
      "closed_loop_allowed": false
    }
  }
  ```

---

## Narration Part 2: Interactive Reviewer Tour & Invariants (0:45 - 1:30)

**Narration**:
> *"Next, we'll walk through our 5-Minute Guided Reviewer Tour, designed to guide auditors through every element of our compliance structure."*
> *"Notice the Safety State and Real EEG Lock sectors. These sectors explicitly show that the closed-loop system is hard-locked to false, ensuring absolute protection against live model adaptation during testing."*

### Step 3: Advance Guided Tour
- **Action**: Click "Next" in the guided tour banner in the UI.
- **Expected UI Reaction**:
  - The banner highlights Sector 1 (Safety State) with a pulsate animation.
  - Text updates: *"Sector 1: Safety State displays the current safety state machine level. It shows 'SAFE_SHADOW', proving the system is running in shadow mode."*
- **Underlying Console Log**:
  `[CommandCenter] Reviewer tour advanced to Step 2: Focus on Safety State.`

### Step 4: Hovering the ProvenanceGraph
- **Action**: Hover over the `Modeling Research (../Imagina)` node in the ProvenanceGraph svg.
- **Expected UI Reaction**: Tooltip displays:
  - **Artifact**: `neuroverse_imagina_export.json`
  - **Contract Version**: `v1.0.0`
  - **Status**: `Verified Compliant`
- **Underlying Console Log**:
  `[ProvenanceGraph] Focused on modeling research node. Contract validation status: Valid.`

---

## Narration Part 3: Offline Resiliency & Fallback (1:30 - 2:00)

**Narration**:
> *"Finally, we'll demonstrate offline resilience. If the live backend is shut down, the dashboard switches instantly to Baked Snapshot Fallback mode."*
> *"This allows recruiters and auditors to explore our complete validation history, code schemas, and artifact inventory completely offline without any system degradation."*

### Step 5: Shut Down Backend & Trigger Fallback
- **Action**: Press `CTRL+C` in the backend terminal to simulate outage.
- **Expected Terminal Output**:
  ```
  INFO:     Shutting down
  INFO:     Waiting for application shutdown.
  INFO:     Application shutdown complete.
  INFO:     Finished server process [12345]
  ```
- **Expected UI Reaction**:
  - Top status pill updates to: `🟠 Baked Snapshot Fallback`.
  - Grid data remains fully interactive, hydrated from `evidence_pack/` JSON snapshot files.
- **Underlying Console Log**:
  `[API Client] Live overview query failed: Network Error. Hydrating dashboard via getStaticSystemOverview() fallback assets.`
