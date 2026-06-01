#!/usr/bin/env python3
import os
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_DIR = ROOT / "assets" / "screenshots"
REPORT_DIR = ROOT / "reports" / "screenshot_assets_check"

EXPECTED_SCREENSHOTS = [
    "01_landing.png",
    "02_command_center.png",
    "03_provenance_graph.png",
    "04_evidence_center_section_h.png",
    "05_protocol_center_auto_run.png",
    "06_data_source_wizard.png",
    "07_dream_corridor.png",
    "08_safety_governance.png",
    "09_fusion_imagina_proxy.png",
    "10_hiring_page.png"
]

def run_screenshot_check():
    print("[*] Starting Screenshot Assets Verification...")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create the assets/screenshots directory if it doesn't exist
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    found_assets = []
    missing_assets = []
    
    for filename in EXPECTED_SCREENSHOTS:
        fp = SCREENSHOTS_DIR / filename
        if fp.exists():
            found_assets.append({
                "filename": filename,
                "path": str(fp.relative_to(ROOT)),
                "size_bytes": fp.stat().st_size
            })
        else:
            missing_assets.append(filename)
            
    # Exit state: Warn if any expected screenshots are missing, but exit with 0 by default.
    status = "PASS"
    warnings = []
    if missing_assets:
        status = "WARN"
        warnings.append(f"Missing {len(missing_assets)} of {len(EXPECTED_SCREENSHOTS)} expected launch screenshots. Recruiter packages require these assets prior to public landing hosting.")
        
    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "total_expected": len(EXPECTED_SCREENSHOTS),
        "total_found": len(found_assets),
        "total_missing": len(missing_assets),
        "found_assets": found_assets,
        "missing_assets": missing_assets,
        "warnings": warnings
    }
    
    write_reports(summary)
    
    print(f"[+] Screenshot assets check completed with status: {status} ({len(found_assets)} found, {len(missing_assets)} missing)")
    if missing_assets:
        for m in missing_assets:
            print(f"    [-] Missing asset: {m}")
            
    return True  # Exit 0 by default so we don't break the release build in clean environments

def write_reports(summary: dict):
    # Save JSON report
    with open(REPORT_DIR / "screenshot_assets_check.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    # Save Markdown report
    md_content = []
    md_content.append("# Recruiter & Reviewer Portfolio Screenshot Verification\n")
    md_content.append(f"**Verification Status**: {summary['status']}")
    md_content.append(f"**Checked At**: {summary['timestamp']}\n")
    
    md_content.append("## Screen Verification Summary")
    md_content.append(f"- **Expected Visual Assets**: {summary['total_expected']}")
    md_content.append(f"- **Found and Verified**: {summary['total_found']}")
    md_content.append(f"- **Missing Visual Assets**: {summary['total_missing']}\n")
    
    if summary.get("warnings"):
        md_content.append("### ⚠️ Auditing Cautions")
        for w in summary["warnings"]:
            md_content.append(f"- {w}")
        md_content.append("")
        
    md_content.append("## Verified Visual Assets")
    if summary["found_assets"]:
        md_content.append("| Screenshot | Local File Path | File Size |")
        md_content.append("|---|---|---|")
        for asset in summary["found_assets"]:
            md_content.append(f"| `{asset['filename']}` | `{asset['path']}` | {asset['size_bytes'] / 1024:.1f} KB |")
    else:
        md_content.append("*No screenshot assets have been generated yet. Please refer to `docs/SCREENSHOT_AND_DEMO_ASSETS.md` for generation details.*")
    md_content.append("")
    
    md_content.append("## Missing Visual Assets")
    if summary["missing_assets"]:
        for asset in summary["missing_assets"]:
            md_content.append(f"- ❌ `{asset}` (Reviewers will see descriptive placeholders in the portfolio inventory)")
    else:
        md_content.append("🟢 *All expected screenshot visual assets are present and ready.*")
        
    md_content.append("\n## Manual Visual Hydration Guide")
    md_content.append("Auditors or portfolio administrators can generate these assets by booting the system via `make dev`, ")
    md_content.append("and capturing high-resolution window frames using browser devtools or OS capture tools. ")
    md_content.append("Once saved to `assets/screenshots/`, rerun `make check-screenshot-assets` to re-verify compliance.")

    (REPORT_DIR / "screenshot_assets_check.md").write_text("\n".join(md_content), encoding="utf-8")
    print(f"[+] Saved JSON report to: {REPORT_DIR / 'screenshot_assets_check.json'}")
    print(f"[+] Saved Markdown report to: {REPORT_DIR / 'screenshot_assets_check.md'}")

if __name__ == "__main__":
    run_screenshot_check()
