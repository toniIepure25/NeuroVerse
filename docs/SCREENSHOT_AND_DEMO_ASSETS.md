# Screenshot and Demo Asset Guide

This document outlines the required assets for the final public portfolio launch. If the assets do not currently exist in the repository, they should be captured locally and placed in the designated directory before promoting the repository on LinkedIn or CVs.

## 1. Directory Structure

Place all assets in a new `assets/screenshots/` directory at the root of the repository.

```
assets/
└── screenshots/
    ├── 01_landing.png
    ├── 02_evidence_center.png
    ├── 03_dream_corridor.png
    ├── 04_research_panel.png
    ├── 05_hiring_page.png
    ├── 06_evidence_pack.png
    └── 07_benchmark_report.png
```

## 2. Required Screenshots

Please capture the following screenshots using `make dev`:

- **`01_landing.png`**: The main Landing Page showing the Hero section, "Scientific Disclaimer", and Architecture overview.
- **`02_evidence_center.png`**: The Evidence Center tab showing the A/B/C/D evidence blocks and the copyable terminal commands.
- **`03_dream_corridor.png`**: A wide shot of the 3D Dream Corridor running with the Research Panel and Biosignal Panel open on the side.
- **`04_research_panel.png`**: A zoomed-in shot of the Research Panel specifically showing the "NeuroVerse v1.1.0-rc1 | public EEG + simulated hardware + safety-locked" badge.
- **`05_hiring_page.png`**: The Hiring / Interview page showing the 90-second pitch and FAQ.
- **`06_evidence_pack.png`**: A screenshot of the terminal running `make generate-evidence-pack`, or the `evidence_pack/README.md` rendered on GitHub.
- **`07_benchmark_report.png`**: Terminal output of `make raw-bci-benchmark-small` showing the dataset split, class balance, and the final FBCSP + LogReg accuracy metrics.

## 3. Demo Video Outline

For recruiters and portfolio platforms, a screen-recorded demo video is highly recommended.

### 2-Minute Demo Flow
1. **[0:00 - 0:20] Landing Page**: Open the UI. Briefly state: "This is NeuroVerse, a safety-gated neuroadaptive interface. It focuses on honest ML baselines rather than unproven mind-reading."
2. **[0:20 - 0:50] Evidence Center**: Click into the Evidence Center. "Every pipeline is validated offline before ever reaching the UI. Here you can see our CSP/FBCSP benchmarks against the PhysioNet dataset."
3. **[0:50 - 1:20] Terminal Benchmark**: Open the terminal and run `make raw-bci-benchmark-small` to prove the signal processing works live.
4. **[1:20 - 1:50] Dream Corridor**: Open the Dream Corridor tab. Point out the LSL stream running in the background. "Notice the 3D scene is static. The safety gate is locking adaptation because the hardware is simulated."
5. **[1:50 - 2:00] Conclusion**: "The platform is fully open-source and reproducible."

### 5-Minute Technical Demo Flow
*(Follow the 2-Minute flow, then add:)*
1. **[2:00 - 3:00] Data Leakage**: Explain the difference between the Group Run metrics and the LOSO (Leave-One-Subject-Out) metrics in the Evidence Center, highlighting why generalization is hard in BCI.
2. **[3:00 - 4:00] LSL Shadow Mode**: Run `make lsl-live-validation-suite` in the terminal to show jitter and drift validation on the incoming stream.
3. **[4:00 - 5:00] Code Walkthrough**: Briefly show `backend/app/safety/gate.py` to demonstrate the hardcoded SQI (Signal Quality Index) thresholds.

### What NOT to Claim in the Video
- Do not claim the corridor is reacting to your real thoughts unless you have a physical OpenBCI connected and have turned off the safety gate.
- Do not claim the system can diagnose medical conditions.
- Do not imply that the PhysioNet LOSO accuracy is high enough for consumer-grade plug-and-play control (be honest that it's a proxy baseline).
