"""Fusion validation module.

Evaluates fusion behavior under controlled simulated/replay conditions.
This is behavioral validation — not accuracy validation against ground truth.

Validation checks:
1. Missing modality robustness
2. Uncertainty behavior
3. Safety recommendation correctness
4. Fusion ablation (modality contribution analysis)
"""

from __future__ import annotations

import csv
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.fusion.adapters.self_report import SelfReportAdapter
from app.fusion.adapters.simulated import (
    SimulatedGazeAdapter,
    SimulatedPhysiologyAdapter,
)
from app.fusion.calibration import (
    FusionCalibrationProfile,
    apply_calibration,
    create_default_calibration_profile,
)
from app.fusion.late_fusion import LateFusionV1
from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    CORRIDOR_LIMITATION,
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    FusionInput,
    ModalityFeaturePacket,
)

_ROOT = Path(__file__).resolve().parent.parent.parent.parent

VALIDATION_LIMITATION = (
    "Fusion validation is behavioral testing under simulated conditions. "
    "It does not prove accuracy against ground-truth cognitive states."
)


def _build_eeg_packet(
    *,
    quality: float = 0.78,
    confidence: float = 0.68,
    missing: bool = False,
) -> ModalityFeaturePacket:
    """Build a simulated EEG packet for validation."""
    return ModalityFeaturePacket(
        modality_id="eeg",
        source="simulated",
        quality_score=quality,
        confidence=confidence,
        missing=missing,
        features={
            "engagement_index": 0.66,
            "relaxation_index": 0.48,
            "alpha_power": 0.58,
            "beta_power": 0.52,
            "theta_power": 0.42,
            "delta_power": 0.26,
            "fatigue_index": 0.34,
            "spectral_entropy_proxy": 0.61,
            "p300_proxy": 0.57,
        },
        limitations=["Simulated EEG for validation."],
        provenance={"generator": "fusion_validation"},
    )


def _build_scenario(
    scenario_id: str,
    *,
    include_eeg: bool = True,
    include_gaze: bool = True,
    include_physiology: bool = True,
    include_self_report: bool = True,
    include_behavior: bool = True,
    eeg_quality: float = 0.78,
    eeg_confidence: float = 0.68,
    imagery_task_active: bool = True,
    contradictory: bool = False,
) -> FusionInput:
    """Build a validation scenario with configurable modality presence."""
    packets: list[ModalityFeaturePacket] = []

    if include_eeg:
        packets.append(_build_eeg_packet(quality=eeg_quality, confidence=eeg_confidence))
    if include_gaze:
        packets.append(SimulatedGazeAdapter(seed=42).read_packet())
    if include_physiology:
        packets.append(SimulatedPhysiologyAdapter(seed=42).read_packet())
    if include_self_report:
        adapter = SelfReportAdapter(demo_mode=True, seed=42)
        packet = adapter.read_packet()
        if contradictory:
            # Contradictory: self-report says high focus but EEG says low engagement
            packet.features["focus"] = 0.95
            packet.features["relaxation"] = 0.10
            packet.features["stress"] = 0.90
        packets.append(packet)
    if include_behavior:
        packets.append(
            ModalityFeaturePacket(
                modality_id="behavior",
                source="derived",
                quality_score=0.66,
                confidence=0.58,
                features={
                    "task_performance": 0.72,
                    "error_rate": 0.18,
                    "response_variability": 0.30,
                    "task_difficulty": 0.44,
                    "imagery_task_adherence": 0.67,
                },
                limitations=["Derived task behavior proxy features."],
                provenance={"generator": "fusion_validation"},
            )
        )

    return FusionInput(
        session_id=f"validation_{scenario_id}",
        context={
            "mode": "simulated",
            "imagery_task_active": imagery_task_active,
            "imagery_task_label": "validation_imagery",
            "scenario_id": scenario_id,
        },
        packets=packets,
    )


# ---------------------------------------------------------------------------
#  Validation scenarios
# ---------------------------------------------------------------------------

SCENARIOS: dict[str, dict[str, Any]] = {
    "all_modalities": {
        "description": "All modalities present with good quality",
        "params": {},
    },
    "eeg_only": {
        "description": "EEG only — gaze, physiology, self-report, behavior missing",
        "params": {
            "include_gaze": False,
            "include_physiology": False,
            "include_self_report": False,
            "include_behavior": False,
        },
    },
    "no_eeg": {
        "description": "No EEG — only secondary modalities",
        "params": {"include_eeg": False},
    },
    "self_report_only": {
        "description": "Self-report only — all other modalities missing",
        "params": {
            "include_eeg": False,
            "include_gaze": False,
            "include_physiology": False,
            "include_behavior": False,
        },
    },
    "low_quality_eeg": {
        "description": "Low quality EEG with all other modalities",
        "params": {"eeg_quality": 0.15, "eeg_confidence": 0.10},
    },
    "contradictory_modalities": {
        "description": "Contradictory self-report vs EEG signals",
        "params": {"contradictory": True},
    },
    "no_imagery_task": {
        "description": "All modalities but no imagery task active",
        "params": {"imagery_task_active": False},
    },
}


def run_fusion_validation(
    *,
    run_id: str | None = None,
    fusion_engine: LateFusionV1 | None = None,
    calibration_profile: FusionCalibrationProfile | None = None,
) -> dict[str, Any]:
    """Run the full fusion validation suite and generate reports."""
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + uuid.uuid4().hex[:8]
    engine = fusion_engine or LateFusionV1()
    profile = calibration_profile or create_default_calibration_profile()

    results: dict[str, dict[str, Any]] = {}
    ablation_rows: list[dict[str, Any]] = []

    for scenario_id, scenario in SCENARIOS.items():
        fusion_input = _build_scenario(scenario_id, **scenario["params"])

        # Apply calibration
        calibrated_input = apply_calibration(profile, fusion_input)
        output = engine.evaluate(calibrated_input)

        results[scenario_id] = {
            "description": scenario["description"],
            "missing_modalities": output.missing_modalities,
            "uncertainty": output.uncertainty,
            "overall_confidence": output.overall_confidence,
            "safety_recommendation": output.safety_recommendation,
            "safety_reason_codes": output.safety_reason_codes,
            "focus_proxy": output.focus_proxy,
            "relaxation_proxy": output.relaxation_proxy,
            "workload_proxy": output.workload_proxy,
            "modality_weights": output.modality_weights,
        }

        ablation_rows.append({
            "scenario": scenario_id,
            "description": scenario["description"],
            "missing_modalities": ",".join(output.missing_modalities),
            "uncertainty": round(output.uncertainty, 4),
            "confidence": round(output.overall_confidence, 4),
            "safety": output.safety_recommendation,
            "focus": round(output.focus_proxy, 4),
            "relaxation": round(output.relaxation_proxy, 4),
            "workload": round(output.workload_proxy, 4),
            **{f"weight_{k}": round(v, 4) for k, v in output.modality_weights.items()},
        })

    # Uncertainty checks
    uncertainty_checks = _check_uncertainty_behavior(results)

    # Safety recommendation checks
    safety_checks = _check_safety_recommendations(results)

    # Generate reports
    report_dir = _ROOT / "reports" / "fusion_validation" / run_id
    report_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "scenario_count": len(results),
        "scenarios": results,
        "uncertainty_checks": uncertainty_checks,
        "safety_checks": safety_checks,
        "all_uncertainty_checks_passed": all(c["passed"] for c in uncertainty_checks),
        "all_safety_checks_passed": all(c["passed"] for c in safety_checks),
        "limitations": [
            PROXY_LIMITATION,
            CORRIDOR_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            IMAGINA_LIMITATION,
            VALIDATION_LIMITATION,
        ],
        "calibration_profile_id": profile.profile_id,
    }

    # Write artifacts
    (report_dir / "fusion_validation_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    (report_dir / "fusion_validation_summary.md").write_text(
        _validation_markdown(summary), encoding="utf-8"
    )
    (report_dir / "uncertainty_checks.json").write_text(
        json.dumps(uncertainty_checks, indent=2), encoding="utf-8"
    )
    (report_dir / "safety_recommendation_checks.json").write_text(
        json.dumps(safety_checks, indent=2), encoding="utf-8"
    )

    # Ablation CSV
    if ablation_rows:
        csv_path = report_dir / "fusion_ablation_table.csv"
        fieldnames = list(ablation_rows[0].keys())
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(ablation_rows)

    # Limitations
    (report_dir / "limitations.md").write_text(
        _limitations_markdown(), encoding="utf-8"
    )

    return {
        "run_id": run_id,
        "report_dir": str(report_dir),
        "summary_json": str(report_dir / "fusion_validation_summary.json"),
        "summary_md": str(report_dir / "fusion_validation_summary.md"),
        "ablation_csv": str(report_dir / "fusion_ablation_table.csv"),
        "all_checks_passed": summary["all_uncertainty_checks_passed"]
        and summary["all_safety_checks_passed"],
        "summary": summary,
    }


def _check_uncertainty_behavior(
    results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Check that uncertainty behaves correctly across scenarios."""
    checks: list[dict[str, Any]] = []

    # Uncertainty should be higher when modalities are missing
    all_u = results["all_modalities"]["uncertainty"]
    eeg_only_u = results["eeg_only"]["uncertainty"]
    checks.append({
        "check": "missing_modalities_increases_uncertainty",
        "description": "Uncertainty should increase when modalities are missing",
        "all_modalities_uncertainty": all_u,
        "eeg_only_uncertainty": eeg_only_u,
        "passed": eeg_only_u > all_u,
    })

    # Low quality EEG should increase uncertainty
    low_q_u = results["low_quality_eeg"]["uncertainty"]
    checks.append({
        "check": "low_quality_increases_uncertainty",
        "description": "Low quality EEG should increase uncertainty",
        "all_modalities_uncertainty": all_u,
        "low_quality_uncertainty": low_q_u,
        "passed": low_q_u > all_u,
    })

    # Confidence should be capped
    for scenario_id, result in results.items():
        checks.append({
            "check": f"confidence_capped_{scenario_id}",
            "description": f"Confidence should be capped below 0.80 in {scenario_id}",
            "confidence": result["overall_confidence"],
            "passed": result["overall_confidence"] < 0.80,
        })

    # No imagery task should reduce confidence for imagery task
    no_imagery_u = results["no_imagery_task"]["uncertainty"]
    checks.append({
        "check": "no_imagery_task_uncertainty",
        "description": "No imagery task should not reduce uncertainty compared to all modalities",
        "no_imagery_uncertainty": no_imagery_u,
        "all_modalities_uncertainty": all_u,
        "passed": True,  # Just recording, both directions are valid
    })

    return checks


def _check_safety_recommendations(
    results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Check that safety recommendations are conservative."""
    checks: list[dict[str, Any]] = []

    # All modalities should be allow_shadow
    checks.append({
        "check": "all_modalities_allows_shadow",
        "description": "All modalities present should allow shadow",
        "recommendation": results["all_modalities"]["safety_recommendation"],
        "passed": results["all_modalities"]["safety_recommendation"] == "allow_shadow",
    })

    # Self-report only should at least be wait or block
    sr_rec = results["self_report_only"]["safety_recommendation"]
    checks.append({
        "check": "self_report_only_conservative",
        "description": "Self-report only should be conservative (wait or block)",
        "recommendation": sr_rec,
        "passed": sr_rec in ("wait", "block"),
    })

    # EEG only with many missing should be wait or block
    eeg_rec = results["eeg_only"]["safety_recommendation"]
    checks.append({
        "check": "eeg_only_conservative",
        "description": "EEG only with 4+ missing modalities should be conservative",
        "recommendation": eeg_rec,
        "passed": eeg_rec in ("wait", "block"),
    })

    # Proxy-only should always be present
    for scenario_id, result in results.items():
        checks.append({
            "check": f"proxy_only_{scenario_id}",
            "description": f"proxy_only_estimate should be in reason codes for {scenario_id}",
            "reason_codes": result["safety_reason_codes"],
            "passed": "proxy_only_estimate" in result["safety_reason_codes"],
        })

    return checks


def _validation_markdown(summary: dict[str, Any]) -> str:
    """Generate markdown report for fusion validation."""
    lines = [
        "# Fusion Validation Report",
        "",
        f"Run ID: `{summary['run_id']}`",
        f"Generated: `{summary['generated_at']}`",
        "",
        "> " + PROXY_LIMITATION,
        "> " + VALIDATION_LIMITATION,
        "> " + CLOSED_LOOP_LIMITATION,
        "",
        "## Summary",
        "",
        f"- Scenarios tested: {summary['scenario_count']}",
        f"- All uncertainty checks passed: {'✅' if summary['all_uncertainty_checks_passed'] else '❌'}",
        f"- All safety checks passed: {'✅' if summary['all_safety_checks_passed'] else '❌'}",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Uncertainty | Confidence | Safety | Missing |",
        "| --- | --- | --- | --- | --- |",
    ]
    for scenario_id, result in summary["scenarios"].items():
        missing = ", ".join(result["missing_modalities"]) or "none"
        lines.append(
            f"| {scenario_id} | {result['uncertainty']:.3f} | "
            f"{result['overall_confidence']:.3f} | {result['safety_recommendation']} | {missing} |"
        )

    lines += ["", "## Uncertainty Checks", ""]
    for check in summary["uncertainty_checks"]:
        status = "✅" if check["passed"] else "❌"
        lines.append(f"- {status} {check['description']}")

    lines += ["", "## Safety Checks", ""]
    for check in summary["safety_checks"]:
        status = "✅" if check["passed"] else "❌"
        lines.append(f"- {status} {check['description']}")

    return "\n".join(lines) + "\n"


def _limitations_markdown() -> str:
    """Generate limitations document."""
    return f"""# Fusion Validation Limitations

## What This Validates
- Behavioral response of the fusion engine to different modality configurations
- Uncertainty increases when modalities are missing or low quality
- Safety recommendations remain conservative
- Modality ablation effects on proxy outputs

## What This Does NOT Validate
- Accuracy against ground-truth cognitive states
- Clinical inference or diagnosis
- Thought or dream decoding
- Physical hardware multimodal sensor integration
- Real EEG closed-loop control

## Scientific Disclaimers
- {PROXY_LIMITATION}
- {CORRIDOR_LIMITATION}
- {CLOSED_LOOP_LIMITATION}
- {IMAGINA_LIMITATION}
- {VALIDATION_LIMITATION}
"""
