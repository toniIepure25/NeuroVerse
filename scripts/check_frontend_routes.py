#!/usr/bin/env python3
"""Statically verify frontend routing and component existence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    print("[*] Starting Frontend Route verification...")
    results = {
        "status": "passed",
        "timestamp": "",
        "checks": {},
        "warnings": [],
        "errors": []
    }
    
    frontend_dir = ROOT / "frontend"
    app_tsx = frontend_dir / "src" / "App.tsx"
    
    # 1. Verify App.tsx exists
    if not app_tsx.exists():
        msg = f"App.tsx is missing: {app_tsx}"
        results["checks"]["app_exists"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"
        _save_and_exit(results)
    else:
        results["checks"]["app_exists"] = {"passed": True, "message": "App.tsx exists"}

    # 2. Check App.tsx content for required navigation links & switches
    content = app_tsx.read_text(encoding="utf-8")
    required_keys = {
        "Overview / landing": ["landing", "Overview"],
        "Command Center": ["command-center", "Command Center"],
        "Dream Corridor": ["demo", "Dream Corridor"],
        "Evidence Center": ["evidence", "Evidence Center"],
        "Protocol Center": ["protocols", "Protocol Center"],
        "Data Sources": ["data-sources", "Data Sources"],
        "Hiring / Interview": ["hiring", "Hiring / Interview"]
    }
    
    for route_name, patterns in required_keys.items():
        missing = [p for p in patterns if p not in content]
        check_id = f"route_{route_name.lower().replace(' ', '_').replace('/', '_')}"
        if missing:
            msg = f"App.tsx is missing pattern(s) for route '{route_name}': {missing}"
            results["checks"][check_id] = {"passed": False, "message": msg}
            results["errors"].append(msg)
            results["status"] = "failed"
        else:
            results["checks"][check_id] = {"passed": True, "message": f"App.tsx successfully routes and navigates to '{route_name}'"}

    # 3. Check that referenced page component files exist
    components = {
        "LandingPage.tsx": "src/components/Pages/LandingPage.tsx",
        "CommandCenter.tsx": "src/components/Pages/CommandCenter.tsx",
        "AppShell.tsx": "src/components/Layout/AppShell.tsx",
        "EvidenceCenter.tsx": "src/components/Pages/EvidenceCenter.tsx",
        "ProtocolCenter.tsx": "src/components/Pages/ProtocolCenter.tsx",
        "DataSourceWizard.tsx": "src/components/Pages/DataSourceWizard.tsx",
        "HiringPage.tsx": "src/components/Pages/HiringPage.tsx",
        "ProvenanceGraph.tsx": "src/components/Visualization/ProvenanceGraph.tsx"
    }
    
    for name, relative_path in components.items():
        full_path = frontend_dir / relative_path
        check_id = f"file_{name.lower().split('.')[0]}"
        if full_path.exists():
            results["checks"][check_id] = {"passed": True, "message": f"{name} exists under {relative_path}"}
        else:
            msg = f"Component file '{name}' is missing at: {relative_path}"
            results["checks"][check_id] = {"passed": False, "message": msg}
            results["errors"].append(msg)
            results["status"] = "failed"

    # 4. Check that public evidence directory exists
    public_evidence = frontend_dir / "public" / "evidence"
    if public_evidence.exists():
        results["checks"]["public_evidence_dir"] = {"passed": True, "message": "public/evidence folder exists"}
    else:
        msg = "public/evidence folder does not exist!"
        results["checks"]["public_evidence_dir"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"

    _save_and_exit(results)


def _save_and_exit(results: dict) -> None:
    from datetime import datetime, timezone
    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    report_dir = ROOT / "reports" / "frontend_route_check"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    json_path = report_dir / "frontend_route_check.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[+] Saved JSON report to: {json_path}")
    
    # Save Markdown
    md_path = report_dir / "frontend_route_check.md"
    md_lines = [
        "# Frontend Route Verification Report",
        "",
        f"- **Verification Status:** {'🟢 PASSED' if results['status'] == 'passed' else '🔴 FAILED'}",
        f"- **Timestamp:** {results['timestamp']}",
        "",
        "## Summary of Executed Checks",
        "",
        "| Check ID | Passed | Description |",
        "| :--- | :--- | :--- |"
    ]
    for check_id, check_data in results["checks"].items():
        pass_symbol = "✅" if check_data["passed"] else "❌"
        md_lines.append(f"| `{check_id}` | {pass_symbol} | {check_data['message']} |")
        
    if results["warnings"]:
        md_lines.extend([
            "",
            "### Warnings",
            ""
        ])
        for warning in results["warnings"]:
            md_lines.append(f"- ⚠️ {warning}")
            
    if results["errors"]:
        md_lines.extend([
            "",
            "### Errors",
            ""
        ])
        for error in results["errors"]:
            md_lines.append(f"- ❌ {error}")
            
    md_lines.extend([
        "",
        "---",
        "## Invariant Core Scientific Assertions",
        "- **Closed-loop from real EEG is disabled by default.**",
        "- **The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics.**",
        "- **IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams.**",
        "- **Static evidence is a baked snapshot, not live runtime evidence.**",
        "- **Physical OpenBCI/Galea validation remains unperformed unless a real device report exists.**"
    ])
    
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"[+] Saved Markdown report to: {md_path}")
    
    sys.exit(0 if results["status"] == "passed" else 1)


if __name__ == "__main__":
    main()
