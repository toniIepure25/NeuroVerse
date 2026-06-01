# Reviewer Start Here

## 1. 30-Second Summary
NeuroVerse is a fully integrated, real-time closed-loop Brain-Computer Interface (BCI) research platform built to validate the entire neuroadaptive pipeline—from signal acquisition and classical ML modeling on public datasets to a React Three Fiber visual interface. It acts as an executable portfolio piece demonstrating rigorous software engineering, data streaming (LSL), and a stringent safety-first approach to physical hardware integration.

## 2. What to Inspect First
- **`README.md`**: Provides the architectural summary and the scientific safety limitations.
- **Command Center (`make dev` -> CommandCenter)**: The central launch-grade dashboard featuring the 5-Minute Tour, 8-sector observability, ProvenanceGraph, and shadow explainability.
- **Frontend UI (`make dev`)**: Navigate to the Evidence Center inside the React app to see a clear breakdown of validated workflows.
- **`docs/NEUROTECH_APPLICATION_PACKAGE.md`**: Contains the GitHub topics, LinkedIn post, and an interview Q&A.
- **`evidence_pack/artifact_inventory.md`**: Proves that all metrics and benchmark runs are logged and timestamped.

## 3. Best 5-Minute Review Path
1. **README.md**: Read the *What It Is / What It Is Not* section.
2. **Command Center**: Run `make dev`, navigate to the **Command Center**, and click through the 7-step **5-Minute Guided Reviewer Tour**. Observe the 8-sector health grid, interactive **ProvenanceGraph** showing model boundaries, and **Shadow Explainability** cards.
3. **Evidence Center**: Open the hosted static portfolio or click the **Evidence Center** tab. The panel labels whether it is showing live backend evidence or a static baked snapshot.
4. **Data Sources**: Open the **Data Sources** tab to see simulator, PhysioNet replay, LSL, BrainFlow SyntheticBoard, and OpenBCI readiness without hardware claims.
5. **evidence_pack/README.md**: Review the generated evidence inventory and Launch QA checker statuses.
6. **reports/bci_raw_epoch_benchmark/physionet_eegbci_medium/benchmark_summary.json**: Verify that actual CSP/FBCSP models were trained and evaluated on real EEG dataset splits.

## 4. Best Local Demo Path
If you want to run the platform locally:
```bash
make preflight
make dev
```
Then open `http://localhost:5173` in your browser. 
Click through the **Landing Page**, walk through the **Command Center** tour, inspect the **Evidence Center**, and finally click **Dream Corridor** to view the live dashboard. (Note: Closed-loop adaptation is locked by default for safety).

For frontend-only review:
```bash
make protocol-run-demo
make generate-evidence-pack
make static-portfolio-build
```
Deploy `frontend/dist/` to Vercel, Netlify, or GitHub Pages. Static evidence is a baked snapshot, not live runtime evidence.

## Data Source Wizard Notes

The Data Source Wizard is the safest way to understand setup readiness:

- **Simulator** is the reviewer-friendly no-hardware path.
- **PhysioNet replay** requires local EDF files and remains a controlled proxy-task workflow.
- **LSL stream** requires a local stream and backend discovery.
- **BrainFlow SyntheticBoard** is not real OpenBCI physical validation.
- **OpenBCI Cyton/Ganglion** requires explicit `PORT` input and real reports before any physical validation claim.

Closed-loop from real EEG is disabled by default.

## 5. Best Evidence Commands
To reproduce the core scientific and engineering validations locally:
```bash
# 1. Run full release readiness and QA verifiers
make reviewer-ready-check

# 2. Run non-expensive verification tests only (fast)
make reviewer-ready-fast

# 3. Train CSP/FBCSP models on PhysioNet motor imagery
make raw-bci-benchmark-small

# 4. Run continuous streaming jitter/drift tests
make lsl-live-validation-suite

# 5. Test hardware ingestion pipeline (Synthetic)
make validate-brainflow-synthetic

# 6. Run physical alpha-reactivity offline trial (Synthetic)
make physical-eeg-trial-synthetic
```

## 6. What Is Validated
- **Data Engineering**: Deterministic synthetic data workflows and offline EDF dataset replay.
- **Streaming**: Live LSL runtime performance (jitter, drift, drop rates) and Replay-over-LSL.
- **Machine Learning**: Raw-epoch CSP and FBCSP baseline benchmarks using proper cross-validation (Group/LOSO) to avoid data leakage on public dataset proxy labels.
- **Hardware Integrations**: BrainFlow SyntheticBoard ingestion and OpenBCI API profiles.
- **Safety**: Hardcoded signal quality (SQI) safety gate that forces the live model into "shadow-only" inference to prevent unsafe 3D adaptations.

## 7. What Is Not Validated
- **Physical Headsets**: OpenBCI/Galea hardware remains unvalidated. The paths are prepared, but no real device was used in this repository snapshot unless a local report exists.
- **Mind Reading / Clinical Efficacy**: The platform predicts controlled experimental task labels. It does not perform general mental state decoding.
- **Unrestricted Closed-Loop**: The 3D Dream Corridor remains locked to raw simulated streams until explicitly un-gated by the user.

## 8. Why This Matters for BCI/Neurotech Roles
Translating offline EEG machine learning to a live, asynchronous environment is incredibly challenging due to signal noise and hardware unpredictability. NeuroVerse forces the evaluation of models in a live streaming context (LSL shadow mode) before trusting them. It proves strong capabilities in signal processing, systems engineering, safety gating, and reproducible ML workflows—critical skills for deploying consumer or clinical neurotechnology.
