#!/usr/bin/env python3
import os
import json
import glob
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "frontend" / "dist"
REPORT_DIR = ROOT / "reports" / "frontend_bundle_check"

# Budgets in bytes
WARN_MAIN_JS = 1.25 * 1024 * 1024  # 1.25 MB
FAIL_MAIN_JS = 2.5 * 1024 * 1024   # 2.5 MB
WARN_TOTAL_DIST = 5.0 * 1024 * 1024 # 5.0 MB

def get_directory_size(path: Path) -> int:
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            total += os.path.getsize(fp)
    return total

def format_size(bytes_size: int) -> str:
    if bytes_size >= 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.2f} MB"
    return f"{bytes_size / 1024:.2f} KB"

def run_bundle_check():
    print("[*] Starting Frontend Bundle Budget Check...")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if not DIST_DIR.exists():
        print(f"[FAIL] frontend/dist directory does not exist. Please run 'cd frontend && npm run build' first.")
        # Create a mock report for clean execution without hard crashes
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "FAIL",
            "error": "frontend/dist not found. Build is required.",
            "total_dist_size_bytes": 0,
            "main_js_size_bytes": 0,
            "css_size_bytes": 0,
            "largest_asset": None,
            "assets": []
        }
        write_reports(summary)
        return False

    assets = []
    total_dist_size = get_directory_size(DIST_DIR)
    
    # Locate JS and CSS assets
    js_files = glob.glob(str(DIST_DIR / "assets" / "*.js"))
    css_files = glob.glob(str(DIST_DIR / "assets" / "*.css"))
    
    main_js_path = None
    main_js_size = 0
    if js_files:
        # Find the largest JS file which usually represents the main index chunk
        main_js_path = max(js_files, key=os.path.getsize)
        main_js_size = os.path.getsize(main_js_path)
        
    css_size = sum(os.path.getsize(f) for f in css_files)

    largest_asset_path = None
    largest_asset_size = 0
    
    # Scan all files under dist to build asset list
    for root, _, files in os.walk(DIST_DIR):
        for f in files:
            fp = Path(root) / f
            rel_path = fp.relative_to(DIST_DIR)
            sz = fp.stat().st_size
            assets.append({
                "path": str(rel_path),
                "size_bytes": sz,
                "size_formatted": format_size(sz)
            })
            if sz > largest_asset_size:
                largest_asset_size = sz
                largest_asset_path = rel_path

    # Assess budgets
    status = "PASS"
    warnings = []
    
    if main_js_size > FAIL_MAIN_JS:
        status = "FAIL"
        warnings.append(f"Main JS bundle size ({format_size(main_js_size)}) exceeds the maximum hard failure budget of {format_size(int(FAIL_MAIN_JS))}.")
    elif main_js_size > WARN_MAIN_JS:
        status = "WARN"
        warnings.append(f"Main JS bundle size ({format_size(main_js_size)}) exceeds the soft warning budget of {format_size(int(WARN_MAIN_JS))}. Consider code-splitting.")
        
    if total_dist_size > WARN_TOTAL_DIST:
        if status == "PASS":
            status = "WARN"
        warnings.append(f"Total dist directory size ({format_size(total_dist_size)}) exceeds the soft budget of {format_size(int(WARN_TOTAL_DIST))}.")

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "total_dist_size_bytes": total_dist_size,
        "total_dist_size_formatted": format_size(total_dist_size),
        "main_js_size_bytes": main_js_size,
        "main_js_size_formatted": format_size(main_js_size),
        "main_js_path": str(Path(main_js_path).relative_to(DIST_DIR)) if main_js_path else None,
        "css_size_bytes": css_size,
        "css_size_formatted": format_size(css_size),
        "largest_asset": str(largest_asset_path) if largest_asset_path else None,
        "largest_asset_size_bytes": largest_asset_size,
        "largest_asset_size_formatted": format_size(largest_asset_size),
        "warnings": warnings,
        "assets": sorted(assets, key=lambda x: x["size_bytes"], reverse=True)
    }

    write_reports(summary)
    
    print(f"[+] Bundle check completed with status: {status}")
    if warnings:
        for w in warnings:
            print(f"    [!] {w}")
            
    return status != "FAIL"

def write_reports(summary: dict):
    # Save JSON report
    with open(REPORT_DIR / "frontend_bundle_check.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    # Save Markdown report
    md_content = []
    md_content.append("# Frontend Bundle Performance Audit\n")
    md_content.append(f"**Audit Status**: {summary['status']}")
    md_content.append(f"**Checked At**: {summary['timestamp']}\n")
    
    md_content.append("## Core Metrics")
    md_content.append(f"- **Total Dist Directory Size**: {summary.get('total_dist_size_formatted', '0 B')}")
    md_content.append(f"- **Main JS Bundle Size**: {summary.get('main_js_size_formatted', '0 B')} (Path: `{summary.get('main_js_path')}`)")
    md_content.append(f"- **Total CSS Assets Size**: {summary.get('css_size_formatted', '0 B')}")
    md_content.append(f"- **Largest Single Asset**: `{summary.get('largest_asset')}` ({summary.get('largest_asset_size_formatted', '0 B')})\n")
    
    if summary.get("warnings"):
        md_content.append("## Budgets & Warnings")
        for w in summary["warnings"]:
            md_content.append(f"- ⚠️ {w}")
        md_content.append("")
        
    md_content.append("## Complete Asset Inventory")
    md_content.append("| Asset Path | Size | Bytes |")
    md_content.append("|---|---|---|")
    for asset in summary.get("assets", []):
        md_content.append(f"| `{asset['path']}` | {asset['size_formatted']} | {asset['size_bytes']:,} |")
        
    md_content.append("\n## Scientific Context & Large Dependency Disclaimer")
    md_content.append("NeuroVerse relies on extensive visual frameworks (such as Three.js, React Three Fiber, React Three Drei, and Recharts) ")
    md_content.append("to deliver high-fidelity immersive biofeedback loops. These essential scientific visualization dependencies ")
    md_content.append("represent the majority of the code footprint. Code splitting is configured to isolate heavy rendering logic ")
    md_content.append("from main app configuration entrypoints.")

    (REPORT_DIR / "frontend_bundle_check.md").write_text("\n".join(md_content), encoding="utf-8")
    print(f"[+] Saved JSON report to: {REPORT_DIR / 'frontend_bundle_check.json'}")
    print(f"[+] Saved Markdown report to: {REPORT_DIR / 'frontend_bundle_check.md'}")

if __name__ == "__main__":
    import sys
    success = run_bundle_check()
    sys.exit(0 if success else 1)
