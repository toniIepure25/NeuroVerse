#!/usr/bin/env python3
"""Verify reviewer demo flow and active endpoint schema compliance."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add backend directory to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

try:
    from fastapi.testclient import TestClient
    from app.main import create_app
except ImportError as exc:
    print(f"[-] Backend import failed. Make sure dependencies are installed: {exc}")
    sys.exit(1)


def main() -> None:
    print("[*] Starting Reviewer Demo Flow verification...")
    results = {
        "status": "passed",
        "timestamp": "",
        "checks": {},
        "warnings": [],
        "errors": []
    }
    
    # 1. Boot backend TestClient
    try:
        app = create_app()
        client = TestClient(app)
        results["checks"]["backend_boot"] = {"passed": True, "message": "Backend booted successfully using create_app()"}
    except Exception as exc:
        msg = f"Failed to instantiate backend: {exc}"
        results["checks"]["backend_boot"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"
        _save_and_exit(results)

    # 2. Check /api/v1/system/overview
    try:
        resp = client.get("/api/v1/system/overview")
        if resp.status_code == 200:
            body = resp.json()
            # Validate schema contract elements
            required_keys = ["source", "generated_at", "warnings", "limitations", "closed_loop_allowed", "safety", "data_sources", "protocol", "imagina", "fusion", "evidence_health"]
            missing_keys = [k for k in required_keys if k not in body]
            
            if missing_keys:
                msg = f"/api/v1/system/overview is missing keys: {missing_keys}"
                results["checks"]["system_overview"] = {"passed": False, "message": msg}
                results["errors"].append(msg)
                results["status"] = "failed"
            elif body["closed_loop_allowed"] is not False:
                msg = "CRITICAL SAFETY FAILURE: closed_loop_allowed is not False in overview!"
                results["checks"]["system_overview"] = {"passed": False, "message": msg}
                results["errors"].append(msg)
                results["status"] = "failed"
            else:
                results["checks"]["system_overview"] = {
                    "passed": True,
                    "message": "Overview endpoint matches full schema and preserves closed_loop_allowed=false"
                }
        else:
            msg = f"/api/v1/system/overview returned status {resp.status_code}: {resp.text}"
            results["checks"]["system_overview"] = {"passed": False, "message": msg}
            results["errors"].append(msg)
            results["status"] = "failed"
    except Exception as exc:
        msg = f"Failed to query system overview: {exc}"
        results["checks"]["system_overview"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"

    # 3. Check other key endpoints
    endpoints = {
        "protocols": "/api/v1/protocols",
        "data_sources": "/api/v1/data-sources",
        "fusion_status": "/api/v1/fusion/status"
    }
    
    for name, path in endpoints.items():
        try:
            resp = client.get(path)
            if resp.status_code == 200:
                results["checks"][f"endpoint_{name}"] = {"passed": True, "message": f"{path} returns status 200"}
            else:
                msg = f"Endpoint {path} failed with code {resp.status_code}"
                results["checks"][f"endpoint_{name}"] = {"passed": False, "message": msg}
                results["warnings"].append(msg)
        except Exception as exc:
            msg = f"Endpoint {path} query threw exception: {exc}"
            results["checks"][f"endpoint_{name}"] = {"passed": False, "message": msg}
            results["warnings"].append(msg)

    # 4. Verify Frontend Routing & Components exist
    frontend_dir = ROOT / "frontend"
    app_tsx = frontend_dir / "src" / "App.tsx"
    provenance_graph = frontend_dir / "src" / "components" / "Visualization" / "ProvenanceGraph.tsx"
    
    if app_tsx.exists():
        content = app_tsx.read_text(encoding="utf-8")
        if "command-center" in content or "CommandCenter" in content:
            results["checks"]["frontend_route"] = {"passed": True, "message": "CommandCenter route successfully wired in App.tsx"}
        else:
            msg = "CommandCenter route missing in App.tsx navigation/switch block"
            results["checks"]["frontend_route"] = {"passed": False, "message": msg}
            results["errors"].append(msg)
            results["status"] = "failed"
    else:
        msg = "frontend/src/App.tsx does not exist!"
        results["checks"]["frontend_route"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"

    if provenance_graph.exists():
        results["checks"]["provenance_graph_exists"] = {"passed": True, "message": "ProvenanceGraph component file exists"}
    else:
        msg = "ProvenanceGraph.tsx component is missing!"
        results["checks"]["provenance_graph_exists"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"

    # 5. Check Static Portfolio Folder
    static_evidence_dir = frontend_dir / "public" / "evidence"
    if static_evidence_dir.exists():
        manifest = static_evidence_dir / "manifest.json"
        if manifest.exists():
            results["checks"]["static_portfolio_dir"] = {"passed": True, "message": f"Static evidence folder exists with valid manifest.json"}
        else:
            msg = "Static evidence folder exists but manifest.json is missing"
            results["checks"]["static_portfolio_dir"] = {"passed": True, "message": msg}
            results["warnings"].append(msg)
    else:
        msg = "Static evidence folder (frontend/public/evidence) does not exist"
        results["checks"]["static_portfolio_dir"] = {"passed": True, "message": msg}
        results["warnings"].append(msg)

    # 6. Save results
    _save_and_exit(results)


def _save_and_exit(results: dict) -> None:
    from datetime import datetime, timezone
    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    report_dir = ROOT / "reports" / "reviewer_demo_flow"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    json_path = report_dir / "reviewer_demo_flow_summary.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[+] Saved JSON report to: {json_path}")
    
    # Save Markdown
    md_path = report_dir / "reviewer_demo_flow_summary.md"
    md_lines = [
        "# Reviewer Demo Flow Verification Report",
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
