"""Generate a local NeuroVerse portfolio evidence pack."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a NeuroVerse evidence pack")
    parser.add_argument("--output", default="evidence_pack")
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.mkdir(parents=True, exist_ok=True)

    _write(output / "README.md", _readme())
    _write(output / "architecture_summary.md", _architecture_summary())
    _write(
        output / "demo_script.md",
        _copy_or_fallback("docs/DEMO_SCRIPT.md", _demo_script()),
    )
    _write(
        output / "safety_and_ethics.md",
        _copy_or_fallback("docs/SAFETY_AND_ETHICS.md", _safety_and_ethics()),
    )
    _write(
        output / "recruiter_summary.md",
        _copy_or_fallback(
            "docs/RECRUITER_TECHNICAL_SUMMARY.md",
            _recruiter_summary(),
        ),
    )
    _write(output / "screenshots_placeholder.md", _screenshots_placeholder())
    _generate_artifact_inventory(output)

    _copy_latest("data/sessions", "*_summary.json", output / "latest_session_report.json")
    _copy_latest("data/sessions", "*_summary.md", output / "latest_session_report.md")
    _copy_latest("reports/datasets", "*_validation.md", output / "dataset_validation.md")
    _copy_latest(
        "reports/hardware_validation",
        "*.md",
        output / "hardware_validation.md",
    )
    _copy_latest(
        "reports/hardware_validation",
        "*brainflow*.md",
        output / "brainflow_hardware_validation.md",
    )
    _copy_latest(
        "reports/hardware_validation",
        "*lsl*validation.md",
        output / "lsl_validation.md",
    )
    _copy_latest("reports/calibration", "*.json", output / "calibration_profile.json")
    _copy_latest(
        "reports/calibration",
        "*brainflow*.json",
        output / "brainflow_calibration_profile.json",
    )
    _copy_latest("reports/calibration", "*lsl*.json", output / "lsl_calibration_profile.json")
    _copy_latest("reports/shadow", "*.json", output / "shadow_report.json")
    _copy_latest("reports/shadow", "*brainflow*.json", output / "brainflow_shadow_report.json")
    _copy_latest("reports/shadow", "*lsl*.json", output / "lsl_shadow_report.json")
    _copy_latest(
        "reports/hardware_trials",
        "*/physical_eeg_trial_summary.md",
        output / "physical_eeg_trial_summary.md",
    )
    _copy_latest(
        "reports/hardware_trials",
        "*/physical_eeg_trial_summary.json",
        output / "physical_eeg_trial_summary.json",
    )
    _copy_latest(
        "reports/hardware_trials",
        "*/alpha_reactivity_report.md",
        output / "alpha_reactivity_report.md",
    )
    _copy_latest(
        "reports/hardware_trials",
        "*/alpha_reactivity_report.json",
        output / "alpha_reactivity_report.json",
    )
    _copy_latest(
        "reports/lsl_live_validation",
        "*/live_validation_summary.md",
        output / "lsl_live_validation_summary.md",
    )
    _copy_latest(
        "reports/lsl_live_validation",
        "*/live_validation_summary.json",
        output / "lsl_live_validation_summary.json",
    )
    _copy_latest(
        "reports/eeg_lsl_validation",
        "*/eeg_lsl_validation_summary.md",
        output / "eeg_lsl_validation_summary.md",
    )
    _copy_latest(
        "reports/eeg_lsl_validation",
        "*/eeg_lsl_validation_summary.json",
        output / "eeg_lsl_validation_summary.json",
    )
    _copy_latest(
        "reports/public_eeg_validation",
        "*/public_eeg_validation_summary.md",
        output / "public_eeg_validation_summary.md",
    )
    _copy_latest(
        "reports/public_eeg_validation",
        "*/public_eeg_validation_summary.json",
        output / "public_eeg_validation_summary.json",
    )
    _copy_latest(
        "reports/public_eeg_validation",
        "*/classifier_model_card.md",
        output / "eeg_classifier_model_card.md",
    )
    _copy_latest(
        "reports/public_eeg_validation",
        "*/heuristic_vs_classifier_comparison.md",
        output / "heuristic_vs_eeg_classifier_comparison.md",
    )
    _copy_latest(
        "reports/real_public_eeg_validation",
        "*/real_public_eeg_validation_summary.md",
        output / "real_public_eeg_validation_summary.md",
    )
    _copy_latest(
        "reports/real_public_eeg_validation",
        "*/real_public_eeg_validation_summary.json",
        output / "real_public_eeg_validation_summary.json",
    )
    _copy_latest(
        "reports/real_public_eeg_validation",
        "*/dataset_inspection.md",
        output / "real_public_eeg_dataset_inspection.md",
    )
    _copy_latest(
        "reports/real_public_eeg_validation",
        "*/classifier_model_card.md",
        output / "real_public_eeg_classifier_model_card.md",
    )
    _copy_latest(
        "reports/real_public_eeg_validation",
        "*/heuristic_vs_classifier_comparison.md",
        output / "real_public_eeg_heuristic_vs_classifier.md",
    )
    _copy_latest(
        "reports/bci_benchmark",
        "*/benchmark_summary.md",
        output / "bci_benchmark_summary.md",
    )
    _copy_latest(
        "reports/bci_benchmark",
        "*/benchmark_summary.json",
        output / "bci_benchmark_summary.json",
    )
    _copy_latest(
        "reports/bci_benchmark",
        "*/model_comparison.csv",
        output / "bci_model_comparison.csv",
    )
    _copy_latest(
        "reports/bci_benchmark",
        "*/best_model.json",
        output / "bci_best_model.json",
    )
    _copy_latest(
        "reports/bci_benchmark",
        "*/bootstrap_confidence_intervals.json",
        output / "bci_bootstrap_confidence_intervals.json",
    )
    _copy_latest(
        "reports/bci_benchmark",
        "*/leakage_warnings.json",
        output / "bci_leakage_warnings.json",
    )
    _copy_latest(
        "reports/bci_raw_epoch_benchmark",
        "*/benchmark_summary.md",
        output / "raw_bci_benchmark_summary.md",
    )
    _copy_latest(
        "reports/bci_raw_epoch_benchmark",
        "*/benchmark_summary.json",
        output / "raw_bci_benchmark_summary.json",
    )
    _copy_latest(
        "reports/bci_raw_epoch_benchmark",
        "*/model_comparison.csv",
        output / "raw_bci_model_comparison.csv",
    )
    _copy_latest(
        "reports/bci_raw_epoch_benchmark",
        "*/best_model.json",
        output / "raw_bci_best_model.json",
    )
    _copy_latest(
        "reports/bci_raw_epoch_benchmark",
        "*/loso_summary.json",
        output / "raw_bci_loso_summary.json",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_small/benchmark_summary.md",
        output / "raw_bci_group_run_summary.md",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_small/benchmark_summary.json",
        output / "raw_bci_group_run_summary.json",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_small_loso/benchmark_summary.md",
        output / "raw_bci_loso_benchmark_summary.md",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium/benchmark_summary.md",
        output / "medium_raw_bci_group_run_summary.md",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium/benchmark_summary.json",
        output / "medium_raw_bci_group_run_summary.json",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_group_subject/benchmark_summary.md",
        output / "medium_raw_bci_group_subject_summary.md",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_group_subject/benchmark_summary.json",
        output / "medium_raw_bci_group_subject_summary.json",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_loso/benchmark_summary.md",
        output / "medium_raw_bci_loso_summary.md",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_loso/benchmark_summary.json",
        output / "medium_raw_bci_loso_summary.json",
    )
    _copy_if_exists(
        "reports/bci_raw_epoch_benchmark/physionet_eegbci_medium_loso/loso_summary.json",
        output / "medium_raw_bci_loso_fold_summary.json",
    )
    _copy_latest(
        "reports/bci_benchmark_comparison",
        "*/comparison.md",
        output / "bci_raw_vs_flattened_comparison.md",
    )
    _copy_latest(
        "reports/raw_bci_shadow",
        "*.md",
        output / "raw_bci_shadow_report.md",
    )
    _copy_latest(
        "reports/raw_bci_shadow",
        "*/live_shadow_summary.md",
        output / "raw_bci_live_shadow_summary.md",
    )
    _copy_latest("models", "*/model_card.md", output / "model_card.md")
    _write(output / "hardware_safety_protocol.md", _hardware_safety_protocol())
    _write(output / "lsl_demo_instructions.md", _lsl_demo_instructions())

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "contents": sorted(path.name for path in output.iterdir() if path.is_file()),
        "scientific_note": (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
    }
    _write(output / "manifest.json", json.dumps(manifest, indent=2))
    print(f"Evidence pack written to {output}")

def _generate_artifact_inventory(output: Path) -> None:
    artifacts = [
        {
            "path": "bci_benchmark_summary.json",
            "section": "A. Real Public EEG Evidence",
            "type": "Benchmark",
            "proves": "Classical models can decode controlled proxy tasks (e.g. motor imagery) from the PhysioNet subset.",
            "does_not_prove": "Does not prove high accuracy on unseen subjects (LOSO is lower) or general mind-reading."
        },
        {
            "path": "raw_bci_benchmark_summary.json",
            "section": "A. Real Public EEG Evidence",
            "type": "Benchmark",
            "proves": "Raw epoch CSP/FBCSP baseline works and avoids data leakage.",
            "does_not_prove": "Does not prove clinical utility."
        },
        {
            "path": "raw_bci_loso_summary.json",
            "section": "A. Real Public EEG Evidence",
            "type": "Benchmark",
            "proves": "Provides realistic cross-subject (LOSO) metrics.",
            "does_not_prove": "Does not prove zero-shot reliability."
        },
        {
            "path": "lsl_live_validation_summary.json",
            "section": "B. Streaming Evidence",
            "type": "Validation",
            "proves": "Platform streams LSL continuously with low jitter/drift and maintains a safety lock.",
            "does_not_prove": "Does not prove the LSL stream contains real human EEG unless physically attached."
        },
        {
            "path": "eeg_lsl_validation_summary.json",
            "section": "B. Streaming Evidence",
            "type": "Validation",
            "proves": "Platform can replay EDF datasets dynamically over LSL and align markers correctly.",
            "does_not_prove": "Does not prove real-time closed-loop control or mind-reading."
        },
        {
            "path": "raw_bci_shadow_report.md",
            "section": "B. Streaming Evidence",
            "type": "Validation",
            "proves": "Live shadow inference processes streaming markers and builds epochs.",
            "does_not_prove": "Does not prove closed-loop control."
        },
        {
            "path": "brainflow_hardware_validation.md",
            "section": "C. Hardware Readiness Evidence",
            "type": "Validation",
            "proves": "BrainFlow SyntheticBoard integration works properly through the system's acquisition layer.",
            "does_not_prove": "Does not prove real OpenBCI Cyton/Ganglion performance. Physical OpenBCI path is prepared but not yet physically validated."
        },
        {
            "path": "physical_eeg_trial_summary.json",
            "section": "C. Hardware Readiness Evidence",
            "type": "Validation",
            "proves": "Physical trial protocol executes properly and computes eyes-open/closed alpha reactivity.",
            "does_not_prove": "Does not prove clinical results; it is an offline sanity check."
        },
        {
            "path": "shadow_report.json",
            "section": "D. Safety Evidence",
            "type": "Validation",
            "proves": "System runs in shadow-only inference and produces zero real adaptation actions while locked.",
            "does_not_prove": "Does not prove safety under un-gated physical conditions."
        }
    ]

    for item in artifacts:
        p = output / item["path"]
        if p.exists():
            item["created_at"] = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()
        else:
            item["created_at"] = None

    _write(output / "artifact_inventory.json", json.dumps(artifacts, indent=2))

    md_lines = ["# Evidence Pack Artifact Inventory\n"]
    sections = {}
    for item in artifacts:
        sec = item["section"]
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(item)

    for sec, items in sorted(sections.items()):
        md_lines.append(f"## {sec}\n")
        for item in items:
            md_lines.append(f"### {item['path']}")
            md_lines.append(f"- **Type**: {item['type']}")
            md_lines.append(f"- **Created At**: {item['created_at'] or 'Missing (Optional/Not Run)'}")
            md_lines.append(f"- **What it proves**: {item['proves']}")
            md_lines.append(f"- **What it does not prove**: {item['does_not_prove']}\n")

    _write(output / "artifact_inventory.md", "\n".join(md_lines))


def _readme() -> str:
    return """# NeuroVerse Evidence Pack

## 1. Executive Summary
This evidence pack summarizes the validation artifacts of the NeuroVerse / Dream Corridor prototype. It is generated for portfolio review, interviews, and technical walkthroughs. The system operates primarily in shadow-mode for safety. Physical OpenBCI/Galea hardware remains unvalidated unless a real device report is present.

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
"""


def _architecture_summary() -> str:
    return """# Architecture Summary

NeuroVerse combines an acquisition layer, feature extraction, SQI, state proxy
estimation, safety gating, adaptation policy, event recording, replay, reports,
and a cinematic frontend.

Productionization additions include runtime health, latency metrics, acquisition
diagnostics, dataset/model workflow visibility, and evidence-pack generation.
"""


def _demo_script() -> str:
    return """# Demo Script

1. Start backend and frontend.
2. Open the Dream Corridor.
3. Start a synthetic session.
4. Show state proxy values, SQI, safety decisions, and adaptation actions.
5. Stop the session and open the generated summary/report.
6. Show dataset validation, model registry, and hardware diagnostics.

The corridor is not a decoded mental image. It is an adaptive scaffold driven by
experimental proxy metrics.
"""


def _safety_and_ethics() -> str:
    return """# Safety And Ethics

NeuroVerse estimates cognitive proxies from simulated or dataset-derived signals.
It is a research prototype, not clinically validated, not a medical device, and
not a thought decoder.
"""


def _recruiter_summary() -> str:
    return """# Recruiter Technical Summary

NeuroVerse demonstrates real-time systems engineering, BCI/ML workflow design,
safety-gated adaptation, deterministic replay, and production-minded
frontend/backend architecture for neurotechnology prototyping.
"""


def _screenshots_placeholder() -> str:
    return """# Screenshots Placeholder

Recommended captures:

- Dream Corridor live session
- Research dashboard with runtime/model/dataset status
- Evaluation report view
- Hardware diagnostics panel
"""


def _hardware_safety_protocol() -> str:
    return """# Hardware Safety Protocol

NeuroVerse uses a staged path: simulator, adapter diagnostics, record-only
hardware validation, timestamp/channel/SQI report, baseline calibration, shadow
inference, and only then explicitly enabled closed-loop mode.

Hardware closed-loop adaptation is disabled by default.
"""


def _lsl_demo_instructions() -> str:
    return """# LSL Demo Instructions

Terminal 1:

```bash
make lsl-stream-demo
```

Terminal 2:

```bash
make discover-lsl
make validate-lsl-demo
make calibration-lsl-demo
make shadow-lsl-demo
```

Or run the one-command suite after installing `pylsl`:

```bash
make lsl-live-validation-suite
```

EEG replay-over-LSL fixture suite:

```bash
make eeg-lsl-live-suite
```

The demo LSL stream is simulated. It validates real streaming mechanics while
closed-loop adaptation remains locked by default.
"""


def _copy_or_fallback(relative_path: str, fallback: str) -> str:
    path = ROOT / relative_path
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def _copy_latest(source_dir: str, pattern: str, target: Path) -> None:
    base = ROOT / source_dir
    if not base.exists():
        return
    matches = sorted(base.glob(pattern), key=lambda path: path.stat().st_mtime, reverse=True)
    if matches:
        shutil.copyfile(matches[0], target)


def _copy_if_exists(relative_path: str, target: Path) -> None:
    source = ROOT / relative_path
    if source.exists():
        shutil.copyfile(source, target)


def _write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
            check=True,
            capture_output=True,
        )
        return result.stdout.strip()
    except Exception:
        return None


if __name__ == "__main__":
    main()
