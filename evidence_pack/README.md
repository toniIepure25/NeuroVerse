# NeuroVerse Evidence Pack

## 1. Executive Summary
This evidence pack summarizes the validation artifacts of the NeuroVerse / Dream Corridor prototype. It is generated for portfolio review, interviews, and technical walkthroughs. For a comprehensive technical overview, see the [NeuroVerse Technical Whitepaper](../docs/NEUROVERSE_WHITEPAPER.md) and [One-Page Summary](../docs/NEUROVERSE_ONE_PAGE_SUMMARY.md). The system operates primarily in shadow-mode for safety. Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present.

## 2. What Was Validated
- A. Real public EEG evidence (PhysioNet EEGBCI, CSP/FBCSP, LOSO / group split metrics)
- B. Streaming evidence (LSL validation, EEG replay over LSL, live shadow inference)
- C. Hardware readiness evidence (BrainFlow SyntheticBoard, physical trial synthetic protocol)
- D. Safety evidence (shadow-only inference, zero real adaptation actions, closed-loop locked)

## 3. What Remains Unvalidated
- Physical EEG hardware validation. Physical OpenBCI path is prepared but not yet physically validated.
- Any clinical claims or mental state decoding.

## 4. Key Artifacts
Refer to `artifact_inventory.md` for a full breakdown.

## 5. Metrics Table (Example)
| Target | Model | Split | Balanced Accuracy |
|--------|-------|-------|-------------------|
| Motor Imagery | FBCSP + LogReg | Group Run | ~0.576 |
| Motor Imagery | FBCSP + LogReg | LOSO | ~0.488 |

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

## 8. Commands to Reproduce
```bash
make bci-benchmark-small
make raw-bci-benchmark-small
make lsl-live-validation-suite
make validate-brainflow-synthetic
make generate-evidence-pack
```

## 9. Recruiter Summary
Please refer to `docs/RECRUITER_TECHNICAL_SUMMARY.md` or `docs/NEUROTECH_APPLICATION_PACKAGE.md`.

## 10. Interview Q&A
Please refer to `docs/INTERVIEW_QA.md`.

## 11. Limitations
The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics. Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; they should not be interpreted as general mind-reading models. Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present.
