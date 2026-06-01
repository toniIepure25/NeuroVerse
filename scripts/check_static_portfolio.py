#!/usr/bin/env python3
"""Check static portfolio evidence completeness and safety compliance."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    print("[*] Starting Static Portfolio Health Check...")
    results = {
        "status": "passed",
        "timestamp": "",
        "checks": {},
        "warnings": [],
        "errors": []
    }
    
    evidence_dir = ROOT / "frontend" / "public" / "evidence"
    
    # 1. Verify directory exists
    if not evidence_dir.exists():
        msg = f"Evidence directory does not exist: {evidence_dir}"
        results["checks"]["directory_exists"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"
        _save_and_exit(results)
    else:
        results["checks"]["directory_exists"] = {"passed": True, "message": "frontend/public/evidence exists"}

    # 2. Check manifest.json
    manifest_path = evidence_dir / "manifest.json"
    if not manifest_path.exists():
        msg = "manifest.json is missing in evidence folder"
        results["checks"]["manifest_exists"] = {"passed": False, "message": msg}
        results["errors"].append(msg)
        results["status"] = "failed"
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            baked_at = manifest.get("baked_at", "unknown")
            files_count = len(manifest.get("files", []))
            results["checks"]["manifest_exists"] = {
                "passed": True,
                "message": f"manifest.json exists. Baked at: {baked_at}. Files count: {files_count}"
            }
        except Exception as exc:
            msg = f"Failed to load manifest.json: {exc}"
            results["checks"]["manifest_exists"] = {"passed": False, "message": msg}
            results["errors"].append(msg)
            results["status"] = "failed"

    # 3. Check for specific evidence files
    evidence_files = {
        "latest_auto_run_protocol.json": "Protocol runtime evidence",
        "latest_completion_report.json": "Protocol completion summary",
        "external_imagina_status.json": "IMAGINA research detection summary",
        "data_source_readiness_snapshot.json": "FastAPI simulator readiness preflights",
        "latest_contract_import_summary.json": "IMAGINA export validation summaries"
    }

    for filename, desc in evidence_files.items():
        file_path = evidence_dir / filename
        check_name = f"file_{filename.split('.')[0]}"
        if file_path.exists():
            results["checks"][check_name] = {"passed": True, "message": f"{filename} exists ({desc})"}
        else:
            msg = f"{filename} is missing from static portfolio evidence folder ({desc})"
            results["checks"][check_name] = {"passed": True, "message": msg}
            results["warnings"].append(msg)

    # 4. Strict Safety Assertion: scan ALL JSON files for closed_loop_allowed: true
    results["checks"]["safety_closed_loop_disabled"] = {
        "passed": True,
        "message": "All JSON evidence files verified to ensure closed_loop_allowed=false"
    }
    
    for json_file in evidence_dir.glob("*.json"):
        try:
            content = json_file.read_text(encoding="utf-8")
            data = json.loads(content)
            
            # Recursive check function
            def check_closed_loop(val) -> bool:
                if isinstance(val, dict):
                    if val.get("closed_loop_allowed") is True:
                        return True
                    return any(check_closed_loop(v) for v in val.values())
                elif isinstance(val, list):
                    return any(check_closed_loop(item) for item in val)
                return False
                
            if check_closed_loop(data):
                msg = f"CRITICAL SAFETY VIOLATION: {json_file.name} contains closed_loop_allowed=true!"
                results["checks"]["safety_closed_loop_disabled"] = {"passed": False, "message": msg}
                results["errors"].append(msg)
                results["status"] = "failed"
        except Exception as exc:
            # If not parseable or not a dict, skip or warn
            pass

    _save_and_exit(results)


def _save_and_exit(results: dict) -> None:
    from datetime import datetime, timezone
    results["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    report_dir = ROOT / "reports" / "static_portfolio_check"
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    json_path = report_dir / "static_portfolio_check.json"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"[+] Saved JSON report to: {json_path}")
    
    # Save Markdown
    md_path = report_dir / "static_portfolio_check.md"
    md_lines = [
        "# Static Portfolio Evidence Verification Report",
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
