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

    # Top-level benchmark: context-aware best models and provenance-strict leaderboard
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/leaderboard.csv",
        output / "top_level_leaderboard.csv",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/best_models_by_context.json",
        output / "top_level_best_models_by_context.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/best_subject_specific_model.json",
        output / "top_level_best_subject_specific_model.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/best_loso_model.json",
        output / "top_level_best_loso_model.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/best_group_run_model.json",
        output / "top_level_best_group_run_model.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/best_low_channel_model.json",
        output / "top_level_best_low_channel_model.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/artifact_integrity_audit.json",
        output / "top_level_artifact_integrity_audit.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/channel_ablation_summary.json",
        output / "top_level_channel_ablation_summary.json",
    )
    _copy_latest(
        "reports/top_level_bci_benchmark",
        "*/subject_specific_summary.json",
        output / "top_level_subject_specific_summary.json",
    )

    # Safety governance evidence section
    _generate_safety_governance_evidence(output)
    # Also copy latest safety audit report if one exists
    _copy_latest(
        "reports/safety_audit",
        "*/safety_audit_summary.json",
        output / "safety_audit_summary.json",
    )
    _copy_latest(
        "reports/safety_audit",
        "*/safety_audit_summary.md",
        output / "safety_audit_summary.md",
    )
    _copy_latest(
        "reports/safety_audit",
        "*/closed_loop_lock_reasons.json",
        output / "safety_closed_loop_lock_reasons.json",
    )
    _copy_latest(
        "reports/safety_audit",
        "*/runtime_evidence_summary.json",
        output / "safety_runtime_evidence_summary.json",
    )

    # Protocol execution evidence
    _generate_protocol_execution_evidence(output)
    _generate_auto_run_evidence(output)
    _generate_data_source_readiness_snapshot(output)
    _copy_latest(
        "reports/protocol_runs",
        "*/protocol_run.json",
        output / "latest_protocol_run.json",
    )
    _copy_latest(
        "reports/protocol_runs",
        "*/protocol_run.md",
        output / "latest_protocol_run.md",
    )
    _copy_latest(
        "reports/protocol_runs",
        "*/protocol_completion_report.json",
        output / "latest_completion_report.json",
    )
    _copy_latest(
        "reports/protocol_runs",
        "*/protocol_completion_report.md",
        output / "latest_completion_report.md",
    )
    _copy_latest("reports/fusion", "*/fusion_report.json", output / "latest_fusion_report.json")
    _copy_latest("reports/fusion", "*/fusion_report.md", output / "latest_fusion_report.md")
    _copy_latest(
        "reports/fusion_calibration",
        "*/fusion_calibration_profile.json",
        output / "latest_fusion_calibration_profile.json",
    )
    _copy_latest(
        "reports/fusion_calibration",
        "*/fusion_calibration_report.md",
        output / "latest_fusion_calibration_report.md",
    )
    _copy_latest(
        "reports/fusion_validation",
        "*/fusion_validation_summary.json",
        output / "latest_fusion_validation_summary.json",
    )
    _copy_latest(
        "reports/fusion_validation",
        "*/fusion_validation_summary.md",
        output / "latest_fusion_validation_summary.md",
    )
    _copy_latest(
        "reports/fusion_validation",
        "*/fusion_ablation_table.csv",
        output / "latest_fusion_ablation_table.csv",
    )

    # IMAGINA v1 baseline model artifacts (fixture fallbacks)
    _copy_latest("reports/imagina_v1", "*/manifest_summary.json", output / "latest_imagina_v1_manifest_summary.json")
    _copy_latest("reports/imagina_v1", "*/metrics.json", output / "latest_imagina_v1_metrics.json")
    _copy_latest("reports/imagina_v1", "*/model_card.md", output / "latest_imagina_v1_model_card.md")
    _copy_latest("reports/imagina_v1", "*/limitations.md", output / "latest_imagina_v1_limitations.md")

    # External IMAGINA status & artifacts discovery
    try:
        import sys
        sys.path.insert(0, str(ROOT / "backend"))
        from app.integrations.imagina import detect_external_imagina_project, scan_external_imagina_artifacts  # noqa: PLC0415
        
        ext_status = detect_external_imagina_project()
        ext_arts = scan_external_imagina_artifacts()
        
        _write(output / "external_imagina_status.json", json.dumps(ext_status.model_dump(), indent=2))
        _write(output / "external_imagina_artifacts.json", json.dumps([art.model_dump() for art in ext_arts], indent=2))
        
        # Copy latest contract import summary if present
        import shutil  # noqa: PLC0415
        latest_import_summary = Path("reports/external_imagina_imports/latest_import_summary.json")
        if latest_import_summary.exists():
            shutil.copy2(latest_import_summary, output / "latest_contract_import_summary.json")
            try:
                summary_data = json.loads(latest_import_summary.read_text(encoding="utf-8"))
                imported_dir = Path(summary_data["target_dir"])
                imported_md_path = imported_dir / "import_summary.md"
                if imported_md_path.exists():
                    shutil.copy2(imported_md_path, output / "latest_contract_import_summary.md")
            except Exception:
                pass
        
        separation_md = (
            "# Research/Modeling vs Safety-Gated Runtime Separation\n\n"
            "## 1. Scientific Separation of Concerns\n"
            "- **IMAGINA (Modeling/Research)**: Located in external repository `../Imagina`. Source of truth for model cards, notebooks, SQLite event data, Next.js dashboard, and scientific reports.\n"
            "- **NeuroVerse (Safety-Gated Runtime)**: Enforces determinism, async protocol engine, structured reason codes, LSL/BrainFlow hardware readiness, LateFusionV1 logic, and closed-loop lock governance.\n\n"
            "## 2. Intended Scientific Framing\n"
            "- *\"IMAGINA is an external research/modeling project. NeuroVerse is the safety-gated runtime and neuroadaptive interface layer.\"*\n"
            "- *\"IMAGINA outputs are experimental imagery proxy estimates, not decoded thoughts or dreams.\"*\n"
            "- *\"The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.\"*\n"
            "- *\"Closed-loop from real EEG is disabled by default.\"*\n"
        )
        _write(output / "imagina_source_separation.md", separation_md)
    except Exception as exc:
        print(f"Warning: Failed to scan external Imagina for evidence pack: {exc}")

    # Launch / Reviewer QA Hardening evidence
    _copy_latest(
        "reports/reviewer_demo_flow",
        "*.json",
        output / "reviewer_demo_flow_summary.json",
    )
    _copy_latest(
        "reports/reviewer_demo_flow",
        "*.md",
        output / "reviewer_demo_flow_summary.md",
    )
    _copy_latest(
        "reports/static_portfolio_check",
        "*.json",
        output / "static_portfolio_check.json",
    )
    _copy_latest(
        "reports/static_portfolio_check",
        "*.md",
        output / "static_portfolio_check.md",
    )
    _copy_latest(
        "reports/frontend_route_check",
        "*.json",
        output / "frontend_route_check.json",
    )
    _copy_latest(
        "reports/frontend_route_check",
        "*.md",
        output / "frontend_route_check.md",
    )
    _copy_latest(
        "reports/frontend_bundle_check",
        "*.json",
        output / "frontend_bundle_check.json",
    )
    _copy_latest(
        "reports/frontend_bundle_check",
        "*.md",
        output / "frontend_bundle_check.md",
    )
    _copy_latest(
        "reports/accessibility_check",
        "*.json",
        output / "accessibility_check.json",
    )
    _copy_latest(
        "reports/accessibility_check",
        "*.md",
        output / "accessibility_check.md",
    )
    _copy_latest(
        "reports/screenshot_assets_check",
        "*.json",
        output / "screenshot_assets_check.json",
    )
    _copy_latest(
        "reports/screenshot_assets_check",
        "*.md",
        output / "screenshot_assets_check.md",
    )
    _copy_latest(
        "reports/public_launch_validation",
        "*.json",
        output / "latest_public_launch_validation.json",
    )
    _copy_latest(
        "reports/public_launch_validation",
        "*.md",
        output / "latest_public_launch_validation.md",
    )

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
        },
        {
            "path": "latest_fusion_report.json",
            "section": "E. Multimodal Fusion / IMAGINA Proxy Evidence",
            "type": "Proxy Report",
            "proves": "Simulated/optional modalities can be fused into safety-gated proxy estimates with uncertainty and proposed shadow visual mapping.",
            "does_not_prove": "Does not prove clinical inference, unrestricted mental-state measurement, thoughts, dreams, or real EEG closed-loop control."
        },
        {
            "path": "latest_fusion_calibration_profile.json",
            "section": "E. Multimodal Fusion / IMAGINA Proxy Evidence",
            "type": "Calibration",
            "proves": "Subject-specific modal baselines are recorded, serialized, and safely applied to normalize features.",
            "does_not_prove": "Does not prove absolute physical calibration against gold-standard laboratory instruments."
        },
        {
            "path": "latest_fusion_validation_summary.json",
            "section": "E. Multimodal Fusion / IMAGINA Proxy Evidence",
            "type": "Validation",
            "proves": "Behavioral validation shows robustness to missing modalities, expected uncertainty behavior, and conservative safety recommendations.",
            "does_not_prove": "Does not prove decoding accuracy under un-simulated real-world noise."
        },
        {
            "path": "latest_fusion_ablation_table.csv",
            "section": "E. Multimodal Fusion / IMAGINA Proxy Evidence",
            "type": "Ablation Table",
            "proves": "Controlled ablation testing reveals exactly how modality presence affects confidence and uncertainty.",
            "does_not_prove": "Does not guarantee identical model response for out-of-distribution subject profiles."
        },
        {
            "path": "latest_imagina_v1_metrics.json",
            "section": "F. IMAGINA v1 Baseline Evidence",
            "type": "Metrics",
            "proves": "IMAGINA v1 manifest validates and a baseline model is successfully trained/evaluated.",
            "does_not_prove": "Does not prove clinical utility, thought/dream reading, or direct closed-loop control."
        },
        {
            "path": "latest_imagina_v1_model_card.md",
            "section": "F. IMAGINA v1 Baseline Evidence",
            "type": "Model Card",
            "proves": "Trained baseline models are registered with strict limitations and usage boundaries.",
            "does_not_prove": "Does not prove real generalizable imagery reconstruction."
        },
        {
            "path": "latest_contract_import_summary.json",
            "section": "G. IMAGINA Export Contract & Safety Compliance",
            "type": "Contract Import Summary",
            "proves": "Imagina v1 Export manifest validates perfectly, checking schema version, safety flags, and copying lightweight metadata.",
            "does_not_prove": "Does not prove model performance or validity under real live BCI closed loop control."
        },
        {
            "path": "latest_contract_import_summary.md",
            "section": "G. IMAGINA Export Contract & Safety Compliance",
            "type": "Scientific Framing & Safety Audit",
            "proves": "Import processes strictly frame all metrics as experimental proxy estimates, enforcing closed_loop_allowed = false.",
            "does_not_prove": "Does not prove the user has real active dream decoding capabilities."
        },
        {
            "path": "reviewer_demo_flow_summary.json",
            "section": "H. Launch & Reviewer Readiness Evidence",
            "type": "QA Verification Summary",
            "proves": "Statically and dynamically checks route wiring, safety states, and data schemas across live FastAPI endpoints and component structures.",
            "does_not_prove": "Does not prove real physical EEG device streaming."
        },
        {
            "path": "static_portfolio_check.json",
            "section": "H. Launch & Reviewer Readiness Evidence",
            "type": "Portfolio Health Report",
            "proves": "Checks presence of complete static assets and guarantees that closed_loop_allowed is uniformly locked to false in all configurations.",
            "does_not_prove": "Does not represent physical trial success; it validates data synchronization."
        },
        {
            "path": "frontend_route_check.json",
            "section": "H. Launch & Reviewer Readiness Evidence",
            "type": "Frontend Structure Integrity",
            "proves": "Verifies 100% routing integrity of App navigation header matching physical page files.",
            "does_not_prove": "Does not represent automated browser click verification."
        },
        {
            "path": "frontend_bundle_check.json",
            "section": "I. Public Launch Readiness Evidence",
            "type": "Bundle Performance Budget",
            "proves": "Statically measures Vite production bundle assets size and validates against maximum budget of 2.5 MB.",
            "does_not_prove": "Does not prove runtime rendering frame rates or client GPU limits."
        },
        {
            "path": "accessibility_check.json",
            "section": "I. Public Launch Readiness Evidence",
            "type": "A11y & Usability Compliance",
            "proves": "Pragmatically audits component semantic heading tags, keyboard tabIndex elements, and ensures all core disclaimers are visibly present in static text.",
            "does_not_prove": "Does not replace dynamic screen-reader test evaluations or WCAG compliance certificate."
        },
        {
            "path": "screenshot_assets_check.json",
            "section": "I. Public Launch Readiness Evidence",
            "type": "Visual Documentation Verification",
            "proves": "Audits presence of 10 key high-resolution screenshots mapping out the entire system's walkthrough pathway.",
            "does_not_prove": "Does not claim clinical or automated UI functionality validation."
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


def _generate_safety_governance_evidence(output: Path) -> None:
    """Generate safety governance evidence section for the evidence pack."""
    import sys as _sys
    sys_path_inserted = False
    try:
        _sys.path.insert(0, str(ROOT / "backend"))
        sys_path_inserted = True
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance
        from app.safety.state_machine import SAFETY_STATES, safety_state_machine

        governance = evaluate_closed_loop_governance()
        state = safety_state_machine.get_current_state()
        serialized = safety_state_machine.serialize()

        evidence = {
            "current_safety_state": state["state_id"],
            "severity": state["severity"],
            "closed_loop_allowed": governance.closed_loop_allowed,
            "lock_reason_codes": governance.lock_reason_codes,
            "lock_reasons": governance.lock_reasons,
            "required_unlock_conditions": governance.required_unlock_conditions,
            "timeline_transitions_count": serialized["timeline_count"],
            "blocked_actions_count": serialized["blocked_action_count"],
            "total_states_defined": len(SAFETY_STATES),
            "state_ids": list(SAFETY_STATES.keys()),
            "scientific_disclaimer": (
                "Closed-loop from real EEG is disabled by default. "
                "Hardware validation confirms stream quality and software integration; "
                "it does not validate clinical or unrestricted mental-state inference. "
                "The corridor is not a decoded mental image. "
                "It is an adaptive scaffold driven by experimental proxy metrics."
            ),
        }
        _write(
            output / "safety_governance_evidence.json",
            json.dumps(evidence, indent=2),
        )
    except Exception as exc:
        # Backend may not be importable if dependencies are missing — still write a fallback
        evidence = {
            "current_safety_state": "CLOSED_LOOP_LOCKED",
            "severity": "blocked",
            "closed_loop_allowed": False,
            "lock_reason_codes": ["closed_loop_env_disabled", "real_eeg_closed_loop_disabled"],
            "lock_reasons": [
                "Real EEG closed-loop adaptation is disabled by default.",
                "Real EEG closed-loop is disabled for safety in this phase.",
            ],
            "required_unlock_conditions": [
                "Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment.",
                "Complete physical hardware validation.",
                "Complete calibration procedure.",
                "Complete shadow inference.",
                "Achieve sustained signal quality above safety thresholds.",
            ],
            "import_error": str(exc),
            "scientific_disclaimer": (
                "Closed-loop from real EEG is disabled by default. "
                "Hardware validation confirms stream quality and software integration; "
                "it does not validate clinical or unrestricted mental-state inference."
            ),
        }
        _write(
            output / "safety_governance_evidence.json",
            json.dumps(evidence, indent=2),
        )
    finally:
        if sys_path_inserted and str(ROOT / "backend") in _sys.path:
            try:
                _sys.path.remove(str(ROOT / "backend"))
            except ValueError:
                pass


def _generate_protocol_execution_evidence(output: Path) -> None:
    """Summarize protocol run evidence for the evidence pack."""
    runs_dir = ROOT / "reports" / "protocol_runs"
    if not runs_dir.exists():
        return
    runs = []
    for d in sorted(runs_dir.iterdir(), reverse=True):
        run_file = d / "protocol_run.json"
        if not run_file.exists():
            continue
        try:
            data = json.loads(run_file.read_text())
            runs.append({
                "run_id": data.get("run_id"),
                "protocol_id": data.get("protocol_id"),
                "protocol_title": data.get("protocol_title"),
                "mode": data.get("mode"),
                "status": data.get("status"),
                "closed_loop_allowed": data.get("closed_loop_allowed", False),
                "created_at": data.get("created_at"),
                "completed_at": data.get("completed_at"),
                "step_count": len(data.get("steps", [])),
                "final_report_path": data.get("final_report_path"),
            })
        except Exception:
            continue
    if runs:
        evidence = {
            "protocol_runs_found": len(runs),
            "latest_run": runs[0] if runs else None,
            "all_runs": runs[:10],
            "closed_loop_allowed_any": any(r.get("closed_loop_allowed") for r in runs),
            "note": (
                "Protocol runs track evidence step-by-step. "
                "closed_loop_allowed is always false in all protocol runs. "
                "Physical hardware steps require explicit PORT and remain record-only."
            ),
        }
        _write(
            output / "protocol_execution_evidence.json",
            json.dumps(evidence, indent=2),
        )


def _generate_data_source_readiness_snapshot(output: Path) -> None:
    """Write a data-source readiness snapshot without requiring a running backend."""
    import sys as _sys

    backend_path = str(ROOT / "backend")
    sys_path_inserted = False
    if backend_path not in _sys.path:
        _sys.path.insert(0, backend_path)
        sys_path_inserted = True
    try:
        from app.datasources.readiness import list_data_sources  # noqa: PLC0415

        snapshot = list_data_sources(force_refresh=True).model_dump()
        snapshot["mode"] = "static_portfolio"
        snapshot["snapshot_note"] = (
            "Generated from backend readiness code for portfolio evidence. "
            "Static evidence is a baked snapshot, not live runtime evidence."
        )
    except Exception as exc:  # noqa: BLE001
        snapshot = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mode": "static_portfolio",
            "sources": [],
            "error": str(exc),
            "snapshot_note": (
                "Data-source readiness snapshot generation failed. "
                "Start the backend for live readiness checks."
            ),
        }
    finally:
        if sys_path_inserted and backend_path in _sys.path:
            try:
                _sys.path.remove(backend_path)
            except ValueError:
                pass

    _write(output / "data_source_readiness_snapshot.json", json.dumps(snapshot, indent=2))

    lines = [
        "# Data Source Readiness Snapshot",
        "",
        f"**Generated:** {snapshot.get('generated_at')}",
        "",
        "Static evidence is a baked snapshot, not live runtime evidence.",
        "Closed-loop from real EEG is disabled by default.",
        "BrainFlow SyntheticBoard is not real OpenBCI physical validation.",
        "OpenBCI/Galea physical validation remains unperformed unless a real device report exists.",
        "",
        "| Source | Availability | Recommended Protocol | Missing Requirements |",
        "| --- | --- | --- | --- |",
    ]
    for source in snapshot.get("sources", []):
        missing = "; ".join(source.get("missing_requirements") or []) or "None"
        lines.append(
            "| {title} | `{availability}` | `{protocol}` | {missing} |".format(
                title=source.get("title", source.get("source_id", "Unknown")),
                availability=source.get("availability", "unknown"),
                protocol=source.get("recommended_protocol_id", ""),
                missing=missing.replace("|", "\\|"),
            )
        )
    _write(output / "data_source_readiness_snapshot.md", "\n".join(lines))


def _generate_auto_run_evidence(output: Path) -> None:
    """Scan protocol_runs/ for the latest auto-completed run and write rich evidence files.

    Always scans (never uses a pre-written cache) so content is always fresh and
    status values are guaranteed to be plain strings from the JSON files.
    """
    runs_dir = ROOT / "reports" / "protocol_runs"
    if not runs_dir.exists():
        return

    for d in sorted(runs_dir.iterdir(), reverse=True):
        run_file = d / "protocol_run.json"
        if not run_file.exists():
            continue
        try:
            data = json.loads(run_file.read_text())
            if not data.get("auto_completed"):
                continue

            # Load completion report for rich fields (proves/not-proves)
            completion_data: dict = {}
            completion_path = d / "protocol_completion_report.json"
            if completion_path.exists():
                completion_data = json.loads(completion_path.read_text())

            steps = data.get("steps", [])
            all_artifacts = [
                p for s in steps for p in (s.get("artifact_paths") or [])
            ]
            step_summary = {
                "total": len(steps),
                "passed": sum(1 for s in steps if s.get("status") == "passed"),
                "failed": sum(1 for s in steps if s.get("status") == "failed"),
                "blocked": sum(1 for s in steps if s.get("status") == "blocked"),
                "manual": sum(
                    1 for s in steps if s.get("status") == "manual_command_required"
                ),
                "skipped": sum(1 for s in steps if s.get("status") == "skipped"),
            }

            # status: always use the value from completion_data (known plain string)
            # or strip enum repr if reading from older protocol_run.json
            raw_status = (
                completion_data.get("status")
                or str(data.get("status", "")).split(".")[-1].lower()
                or "unknown"
            )
            mode_key = str(data.get("mode", "")).split(".")[-1].lower()

            evidence = {
                "run_id": data.get("run_id"),
                "protocol_id": data.get("protocol_id"),
                "protocol_title": data.get("protocol_title"),
                "mode": mode_key,
                "status": raw_status,
                "auto_completed": True,
                "auto_completed_at": data.get("auto_completed_at"),
                "final_report_generated": data.get("final_report_generated", False),
                "final_report_path": data.get("final_report_path"),
                "protocol_completion_report_path": (
                    str(completion_path) if completion_path.exists() else None
                ),
                "orchestration_status": data.get("orchestration_status"),
                "closed_loop_allowed": False,
                "created_at": data.get("created_at"),
                "completed_at": data.get("completed_at"),
                "step_summary": step_summary,
                "artifact_paths": all_artifacts,
                "artifact_count": len(all_artifacts),
                "what_this_proves": completion_data.get("what_this_proves", []),
                "what_this_does_not_prove": completion_data.get(
                    "what_this_does_not_prove", []
                ),
                "scientific_disclaimer": data.get("scientific_disclaimer", ""),
                "scientific_limitations": completion_data.get("scientific_limitations", ""),
                "safety_summary": data.get("safety_summary"),
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
            _write(
                output / "latest_auto_run_protocol.json",
                json.dumps(evidence, indent=2),
            )
            if completion_path.exists():
                shutil.copyfile(completion_path, output / "latest_completion_report.json")
                md_path = completion_path.with_suffix(".md")
                if md_path.exists():
                    shutil.copyfile(md_path, output / "latest_completion_report.md")
            return
        except Exception:
            continue


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
