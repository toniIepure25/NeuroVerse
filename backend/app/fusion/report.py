"""Fusion report generation."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.fusion.models import (
    CLOSED_LOOP_LIMITATION,
    CORRIDOR_LIMITATION,
    IMAGINA_LIMITATION,
    PROXY_LIMITATION,
    FusionInput,
    FusionOutput,
)

ROOT = Path(__file__).resolve().parent.parent.parent.parent


def generate_fusion_report(
    fusion_input: FusionInput,
    output: FusionOutput,
    *,
    run_id: str | None = None,
) -> dict[str, Any]:
    run_id = (
        run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "_" + str(uuid.uuid4())[:8]
    )
    report_dir = ROOT / "reports" / "fusion" / run_id
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / "fusion_report.json"
    md_path = report_dir / "fusion_report.md"
    payload = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "proxy_estimates_only": True,
        "closed_loop_allowed": False,
        "input": fusion_input.model_dump(mode="json"),
        "fusion_output": output.model_dump(mode="json"),
        "modality_availability": {
            packet.modality_id: not packet.missing for packet in fusion_input.packets
        },
        "limitations": [
            PROXY_LIMITATION,
            CORRIDOR_LIMITATION,
            CLOSED_LOOP_LIMITATION,
            IMAGINA_LIMITATION,
        ],
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(_markdown(payload), encoding="utf-8")
    return {
        "run_id": run_id,
        "report_dir": str(report_dir),
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "report": payload,
    }


def _markdown(report: dict[str, Any]) -> str:
    output = report["fusion_output"]
    lines = [
        "# Multimodal Fusion / IMAGINA Proxy Report",
        "",
        f"Run ID: `{report['run_id']}`",
        f"Generated: `{report['generated_at']}`",
        "",
        "> Multimodal fusion outputs are experimental proxy estimates, not clinical "
        "or unrestricted mental-state measurements.",
        "> The corridor is not a decoded mental image. It is an adaptive scaffold "
        "driven by experimental proxy metrics.",
        "> Closed-loop from real EEG is disabled by default.",
        "> IMAGINA plugin outputs are experimental imagery-quality proxies, not "
        "decoded thoughts or dreams.",
        "",
        "## Fusion Output",
        "",
        f"- Focus proxy: `{output['focus_proxy']:.3f}`",
        f"- Relaxation proxy: `{output['relaxation_proxy']:.3f}`",
        f"- Workload proxy: `{output['workload_proxy']:.3f}`",
        f"- Stress/arousal proxy: `{output['stress_arousal_proxy']:.3f}`",
        f"- Fatigue proxy: `{output['fatigue_proxy']:.3f}`",
        f"- Imagery engagement proxy: `{output['imagery_engagement_proxy']:.3f}`",
        f"- Imagery quality proxy: `{output.get('imagery_quality_proxy')}`",
        f"- Confidence: `{output['overall_confidence']:.3f}`",
        f"- Uncertainty: `{output['uncertainty']:.3f}`",
        f"- Safety recommendation: `{output['safety_recommendation']}`",
        "",
        "## Modalities",
    ]
    for modality, present in report["modality_availability"].items():
        lines.append(f"- `{modality}`: {'present' if present else 'missing'}")
    lines += [
        "",
        "## Proposed Dream Corridor Mapping",
        "",
        "This mapping is proposed for simulated/shadow display only and does not "
        "execute real adaptation.",
        "",
        "```json",
        json.dumps(output["proposed_visual_mapping"], indent=2),
        "```",
    ]
    return "\n".join(lines) + "\n"
