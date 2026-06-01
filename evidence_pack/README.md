# NeuroVerse Evidence Pack

## 1. Executive Summary
This evidence pack summarizes the validation artifacts of the NeuroVerse / Dream Corridor prototype. It is generated for portfolio review, interviews, and technical walkthroughs. The system operates primarily in shadow-mode for safety. Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present.

## 2. What Was Validated
- A. Real public EEG evidence (PhysioNet EEGBCI, CSP/FBCSP, LOSO / group split metrics)
- B. Streaming evidence (LSL validation, EEG replay over LSL, live shadow inference)
- C. Hardware readiness evidence (BrainFlow SyntheticBoard, physical trial synthetic protocol)
- D. Safety evidence (shadow-only inference, zero real adaptation actions, closed-loop locked)
- E. Multimodal Fusion / IMAGINA proxy evidence (simulated proxy fusion, uncertainty, proposed shadow-only visual mapping)
- F. IMAGINA v1 Baseline Evidence (dataset adapters, training metrics, cross-validation metrics, and registered baseline models)
- G. Launch / Reviewer Readiness Evidence (Reviewer Demo Flow, Static Portfolio health, Frontend Route checkers)
- H. Public Launch Readiness Evidence (Vite bundle budget, static accessibility checks, visual assets verification, threat model)

## 3. What Remains Unvalidated
- Physical EEG hardware validation. Physical OpenBCI path is prepared but not yet physically validated.
- Any clinical claims or mental state decoding.
- IMAGINA outputs are experimental imagery-quality proxies, not decoded thoughts or dreams.

## 4. Key Artifacts
Refer to `artifact_inventory.md` for a full breakdown and [Security & Privacy Threat Model](file:///home/tonystark/Desktop/NeuroVerse/docs/SECURITY_AND_PRIVACY_THREAT_MODEL.md) for vulnerability assessments.

## 5. Benchmark Evidence by Context

All metrics are sourced from real benchmark outputs with full provenance.
See `top_level_best_models_by_context.json` and `top_level_leaderboard.csv`.

### A. Cross-Subject / Zero-Calibration Evidence (LOSO)
| Model | Channel Set | Balanced Accuracy | Source |
|-------|-------------|-------------------|--------|
| Riem TS LogReg | motor_subset (7ch) | ~0.699 | channel_ablation_motor_subset/benchmark_summary.json |
| CSP LDA | minimal_motor (3ch) | ~0.594 | LOSO fold-mean |
| CSP LDA | all_channels (64ch) | ~0.484 | LOSO fold-mean |

### B. Run-Generalization Evidence (Group Run)
| Model | Preprocessing | Balanced Accuracy | Source |
|-------|--------------|-------------------|--------|
| FBCSP LogReg | 1.0-4.0s, 8-35Hz | ~0.636 | fw_ablation benchmark_summary.json |

### C. Subject-Specific Calibration Evidence
| Model | Train/Test | Balanced Accuracy | Source |
|-------|-----------|-------------------|--------|
| Riemannian MDM | runs 4,8 / run 12 | ~0.651 | subject_specific_summary.json |

### D. Channel Ablation Evidence
| Channel Set | #Channels | Best LOSO BA |
|-------------|-----------|-------------|
| all_channels | 64 | ~0.484 |
| motor_subset | 7 | ~0.585 |
| minimal_motor | 3 | ~0.594 |

> Subject-specific ~0.65 and LOSO ~0.48-0.70 are **different evaluation contexts** and should not be compared as equivalent. See `comparison_vs_LOSO.md`.

## 6. Hardware Readiness Table
| Interface | Validated? | Notes |
|-----------|------------|-------|
| Synthetic Simulator | Yes | Default workflow |
| LSL Replay | Yes | Uses pylsl / pyxdf |
| BrainFlow Synthetic | Yes | Native synthetic board |
| OpenBCI Cyton | No | Prepared but physical headset not yet validated |
| OpenBCI Ganglion | No | Prepared but physical headset not yet validated |

## 7. Safety Lock Explanation
NeuroVerse maintains a hardcoded Safety Gate that defaults to blocking adaptation if SQI drops, confidence is low, or physical hardware is connected without explicit overrides. The system runs real data in "shadow mode," executing inference without affecting the 3D visualizer, resulting in zero real adaptation actions.

## 8. Launch / Reviewer Readiness Evidence
- **Reviewer Demo Flow**: Statically and dynamically validates route wiring, safety states, and data schemas across components to ensure zero runtime lock leakage or interface breakage.
- **Static Portfolio Health**: Checks complete presence of static artifacts and guarantees that `closed_loop_allowed: false` is uniformly maintained in all JSON snapshot templates.
- **Frontend Route Checker**: Verifies 100% integrity of App navigation header matching physical page file presence.
- **What it Proves**: Guarantees that both live backend execution and static portfolio fallback modes operate with absolute structural integrity, perfect E501 lints, and robust type safety.
- **What it does NOT Claim**: Does not represent physical sensor attachment or live human trial validation.
- **Commands to Regenerate**: `make reviewer-ready-check` (complete) or `make reviewer-ready-fast` (non-expensive checks).

## 9. Public Launch Readiness Evidence
- **Bundle Performance Budget**: Audits production asset files size under `frontend/dist` to guard initial load speeds against regression (warn budget: 1.25 MB, fail budget: 2.5 MB).
- **A11y & Usability Compliance**: Pragmatically verifies semantic heading structure, focus reachability, and visible safety warnings to ensure strict accessibility compliance.
- **Visual Documentation**: Audits screenshot presence (under `assets/screenshots/`) representing all pages and sub-panels of the reviewer demo path.
- **Security & Privacy Posture**: Maps neural data boundaries, local-first sandbox model, and secure static public hosting guidelines under `docs/SECURITY_AND_PRIVACY_THREAT_MODEL.md`.
- **What it Proves**: Validates that static portfolio assets are complete, bundle size matches target thresholds, page usability standards are passed, and data privacy boundaries are documented.
- **What it does NOT Claim**: Does not prove clinical efficacy, HIPAA compliance certification, or production authentication manager presence.

## 10. Commands to Reproduce
```bash
make top-level-bci-benchmark
make audit-bci-benchmark
make generate-evidence-pack
make release-check
make check-frontend-bundle
make check-accessibility
make check-screenshot-assets
```

## 11. Recruiter Summary
Please refer to `docs/RECRUITER_TECHNICAL_SUMMARY.md` or `docs/NEUROTECH_APPLICATION_PACKAGE.md`.

## 12. Interview Q&A
Please refer to `docs/INTERVIEW_QA.md`.

## 13. Limitations
The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics. Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present. No benchmark result implies thought reading or clinical inference.
