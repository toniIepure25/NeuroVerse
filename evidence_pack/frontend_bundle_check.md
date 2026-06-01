# Frontend Bundle Performance Audit

**Audit Status**: PASS
**Checked At**: 2026-06-01T22:50:18.531074+00:00

## Core Metrics
- **Total Dist Directory Size**: 1.63 MB
- **Main JS Bundle Size**: 1.18 MB (Path: `assets/AppShell-DjCogLXy.js`)
- **Total CSS Assets Size**: 32.35 KB
- **Largest Single Asset**: `assets/AppShell-DjCogLXy.js` (1.18 MB)

## Complete Asset Inventory
| Asset Path | Size | Bytes |
|---|---|---|
| `assets/AppShell-DjCogLXy.js` | 1.18 MB | 1,237,454 |
| `assets/index-DhZR0pcX.js` | 144.21 KB | 147,671 |
| `assets/EvidenceCenter-veM80zu9.js` | 77.92 KB | 79,787 |
| `evidence/external_imagina_artifacts.json` | 42.08 KB | 43,087 |
| `assets/CommandCenter-DBPmlyJQ.js` | 32.56 KB | 33,338 |
| `assets/index-vSPF2GHd.css` | 32.35 KB | 33,123 |
| `evidence/data_source_readiness_snapshot.json` | 22.94 KB | 23,490 |
| `assets/ProtocolCenter--_1zlQMJ.js` | 20.12 KB | 20,608 |
| `assets/DataSourceWizard-BsaSbeo5.js` | 17.94 KB | 18,371 |
| `assets/client-CnKMY-vh.js` | 13.78 KB | 14,115 |
| `evidence/latest_fusion_validation_summary.json` | 9.89 KB | 10,124 |
| `evidence/latest_fusion_report.json` | 7.83 KB | 8,021 |
| `evidence/latest_completion_report.json` | 7.26 KB | 7,430 |
| `assets/LandingPage-Dfumhsi_.js` | 6.91 KB | 7,080 |
| `assets/neuroverseStore-B-43wwGG.js` | 5.93 KB | 6,075 |
| `assets/HiringPage-C0ECXnGl.js` | 5.18 KB | 5,307 |
| `evidence/manifest.json` | 3.89 KB | 3,987 |
| `evidence/latest_auto_run_protocol.json` | 3.09 KB | 3,169 |
| `evidence/frontend_route_check.json` | 2.42 KB | 2,481 |
| `evidence/latest_fusion_calibration_profile.json` | 2.38 KB | 2,435 |
| `evidence/static_portfolio_check.json` | 1.50 KB | 1,532 |
| `evidence/latest_fusion_ablation_table.csv` | 1.23 KB | 1,261 |
| `evidence/reviewer_demo_flow_summary.json` | 1.10 KB | 1,122 |
| `evidence/imagina_source_separation.md` | 0.89 KB | 912 |
| `evidence/external_imagina_status.json` | 0.60 KB | 618 |
| `index.html` | 0.55 KB | 562 |

## Scientific Context & Large Dependency Disclaimer
NeuroVerse relies on extensive visual frameworks (such as Three.js, React Three Fiber, React Three Drei, and Recharts) 
to deliver high-fidelity immersive biofeedback loops. These essential scientific visualization dependencies 
represent the majority of the code footprint. Code splitting is configured to isolate heavy rendering logic 
from main app configuration entrypoints.