# NeuroVerse GitHub Presentation & Reviewer Guide

Welcome to the **NeuroVerse** repository! This guide provides technical reviewers, developers, and recruiters with a rapid quickstart to explore the platform's features, visual dashboards, and engineering artifacts.

---

## 1. Quickstart Presentation Modes

Depending on your time and local setup, choose one of the three presentation paths:

```
                    +--------------------------------------------+
                    |          Choose Presentation Mode          |
                    +--------------------------------------------+
                                          |
                +-------------------------+-------------------------+
                |                                                   |
                v                                                   v
    +-----------------------+                           +-----------------------+
    |   Serverless Static   |                           |    Live Local Dev     |
    |   (No Backend Setup)  |                           | (FastAPI + Vite React)|
    |                       |                           |                       |
    | 1. Run Vite build     |                           | 1. Install dependencies|
    | 2. Hydrate from JSON  |                           | 2. Boot up local dev  |
    | 3. Browse offline     |                           | 3. Access Live API    |
    +-----------------------+                           +-----------------------+
```

### Mode A: Serverless Static Portfolio (Fastest & Zero Setup)
Review the complete dashboard hydrated entirely from pre-baked static JSON files. Zero database configuration or backend Python packages required.
1. Run local build static hosting:
   ```bash
   make static-portfolio-build
   # Hydrates from public/evidence/manifest.json
   ```
2. Open your local browser to view the beautiful interactive dashboard with zero server dependencies!

### Mode B: Live Local Ingestion Walkthrough (Interactive)
1. Install backend and frontend dependencies:
   ```bash
   make install
   ```
2. Start the local loopback server:
   ```bash
   make dev
   ```
3. Access the Vite dashboard at `http://localhost:5173` and backend API endpoints at `http://localhost:8000`.

---

## 2. Recommended Walkthrough Paths

### The 5-Minute Executive Walkthrough
1. **Interactive Guided Tour**: Click the "Start" button on the **CommandCenter guided tour banner** at the top of the dashboard. Follow the highlighted sectores to see Safety State and LSL parameters.
2. **ProvenanceGraph Inspection**: Hover over the `Modeling Research` node. See the clean boundary isolating external `Imagina` modeling scripts from local NeuroVerse safety code.
3. **Shadow Explainability Indicators**: Review the predictions cosine similarity and uncertainty bounds under the explainability panel, showcasing how the visual adaptation is safety-gated in real-time.

### The 10-Minute Technical Walkthrough
1. **Automated Protocol Runs**: Navigate to `/protocols` in the top bar. Choose a registered protocol (e.g. Synthetic Multimodal Calibration) and execute the steps asynchronously.
2. **Lab Streaming Ingestion Preflight**: Navigate to `/data-sources`. Run the signal quality indices check and review the simulated multi-channel EEG diagnostics.
3. **Release Pipeline Audit**: Execute the release verification target locally:
   ```bash
   make public-launch-fast
   ```
   This validates the Vite bundle budget check, accessibility assertions, and screenshot checklists in a single command block.

---

## 3. Standard Repository Safety Boundaries & Non-Claims

NeuroVerse represents a **research-grade software prototype** emphasizing defensive programming, diagnostic observability, and audit transparency.

- **Non-Claims**: The system does not decode raw thought images, read active minds, or serve as a clinical/medical utility.
- **Safety Assertions**: All adaptations operate in a shadow-inference mode (`closed_loop_allowed = false`) by default, blocking visual feedback changes from raw signal streams.
- **Hardware Profile**: Live EEG hardware streaming uses simulated signal generators in standard configurations. Physical OpenBCI hardware validations are synthetic.
