#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = ROOT / "frontend" / "src" / "components" / "Pages"
REPORT_DIR = ROOT / "reports" / "accessibility_check"

# Required BCI warnings pattern check to ensure they are present in visible text
REQUIRED_PATTERNS = [
    ("Closed-loop from real EEG is disabled by default", r"Closed-loop from real EEG is disabled by default"),
    ("The corridor is not a decoded mental image. It is an adaptive scaffold driven by experimental proxy metrics", r"The corridor is not a decoded mental image"),
    ("IMAGINA outputs are experimental imagery proxy artifacts, not decoded thoughts or dreams", r"IMAGINA outputs are.*imagery proxy")
]

def analyze_tsx_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    issues = []
    
    # Check 1: Audit div/span tags with onClick but without role="button" or tabIndex or keyboard triggers
    for idx, line in enumerate(lines, 1):
        if "onClick" in line:
            # Check if it's a div, span, or section with onClick but missing role="button"
            if re.search(r"<(div|span|section|aside|p|h\d)\s", line) and not "role=" in line:
                issues.append({
                    "line": idx,
                    "type": "Interactive Role Missing",
                    "severity": "WARN",
                    "code": line.strip(),
                    "suggestion": "Add role=\"button\" and tabIndex={0} to div/span elements with onClick handlers to make them keyboard accessible."
                })
            # Check if role="button" exists but tabIndex is missing
            if "role=\"button\"" in line and not "tabIndex" in line:
                issues.append({
                    "line": idx,
                    "type": "Keyboard Focus Missing",
                    "severity": "WARN",
                    "code": line.strip(),
                    "suggestion": "Add tabIndex={0} to role=\"button\" elements so screen readers and keyboard users can navigate to them."
                })

    # Check 2: Audit button elements missing text or aria-label
    # Find <button ... > tags
    for idx, line in enumerate(lines, 1):
        if "<button" in line:
            # Simple check if there's an onClick or button tag but no label or text
            if "className=" in line and "aria-label=" not in line and "aria-labelledby=" not in line:
                # If the button tag closes on same line with icon only (e.g. no visible text inside tag)
                if re.search(r"<button[^>]*>\s*<[A-Z][a-zA-Z0-9]*\s*(?:/>|></[A-Z][a-zA-Z0-9]*>)\s*</button>", line):
                    issues.append({
                        "line": idx,
                        "type": "Button Missing Text Label",
                        "severity": "FAIL",
                        "code": line.strip(),
                        "suggestion": "Buttons containing only icons must have a descriptive aria-label attribute."
                    })

    # Check 3: Check standard headings structure
    # Check if page component contains at least one heading tag (h1, h2, h3)
    has_heading = any(re.search(r"<h[1-6]\b", line) for line in lines)
    if not has_heading:
        issues.append({
            "line": 1,
            "type": "Semantic Heading Structure Missing",
            "severity": "WARN",
            "code": f"Component: {file_path.name}",
            "suggestion": "Ensure the main page component has a semantic heading structure (<h1-6>) to aid screen reader navigation."
        })

    # Check 4: Check if safety disclaimers are visibly present in text (especially in EvidenceCenter/CommandCenter/LandingPage)
    if file_path.name in ["EvidenceCenter.tsx", "CommandCenter.tsx", "LandingPage.tsx"]:
        for text_desc, pattern in REQUIRED_PATTERNS:
            if not re.search(pattern, content, re.IGNORECASE):
                # Only warn/fail on specific files where disclaimers are expected to be highly visible
                issues.append({
                    "line": 1,
                    "type": "Safety Disclaimer Missing",
                    "severity": "WARN",
                    "code": f"Missing disclaimer: '{text_desc}'",
                    "suggestion": f"Ensure the precise safety disclaimer is visibly displayed in the page's markdown or text blocks."
                })

    return issues

def run_accessibility_check():
    print("[*] Starting Frontend Accessibility Check...")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if not PAGES_DIR.exists():
        print(f"[FAIL] components/Pages directory not found at: {PAGES_DIR}")
        summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "FAIL",
            "error": "components/Pages directory not found.",
            "total_issues": 0,
            "failed_assertions": 0,
            "audited_files": []
        }
        write_reports(summary)
        return False

    audited_files = []
    total_issues = 0
    failed_assertions = 0

    tsx_files = list(PAGES_DIR.glob("*.tsx"))
    for tsx in tsx_files:
        issues = analyze_tsx_file(tsx)
        total_issues += len(issues)
        failed_assertions += sum(1 for i in issues if i["severity"] == "FAIL")
        
        audited_files.append({
            "file": tsx.name,
            "issues_count": len(issues),
            "issues": issues
        })

    status = "PASS"
    if failed_assertions > 0:
        status = "FAIL"
    elif total_issues > 0:
        status = "WARN"

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "total_issues": total_issues,
        "failed_assertions": failed_assertions,
        "audited_files": audited_files
    }

    write_reports(summary)
    
    print(f"[+] Accessibility check completed with status: {status} ({total_issues} issues found, {failed_assertions} critical failures)")
    
    return status != "FAIL"

def write_reports(summary: dict):
    # Save JSON report
    with open(REPORT_DIR / "accessibility_check.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    # Save Markdown report
    md_content = []
    md_content.append("# Frontend Accessibility (a11y) & Usability Audit\n")
    md_content.append(f"**Audit Status**: {summary['status']}")
    md_content.append(f"**Checked At**: {summary['timestamp']}\n")
    
    md_content.append("## Executive Audit Summary")
    md_content.append(f"- **Total Pages Audited**: {len(summary.get('audited_files', []))}")
    md_content.append(f"- **Total Accessibility Warnings/Failures**: {summary.get('total_issues', 0)}")
    md_content.append(f"- **Critical failures preventing release**: {summary.get('failed_assertions', 0)}\n")
    
    md_content.append("## Details by Component File")
    
    for item in summary.get("audited_files", []):
        md_content.append(f"### Component: `{item['file']}` ({item['issues_count']} issues)")
        if not item["issues"]:
            md_content.append("🟢 *No issues found in this file.*")
        else:
            md_content.append("| Line | Type | Severity | Code Snippet | Suggestion |")
            md_content.append("|---|---|---|---|---|")
            for issue in item["issues"]:
                code_escaped = issue["code"].replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;")
                md_content.append(f"| L{issue['line']} | {issue['type']} | **{issue['severity']}** | `{code_escaped}` | {issue['suggestion']} |")
        md_content.append("")
        
    md_content.append("\n## Regulatory visible warning safety compliance note")
    md_content.append("To support high-integrity Recruiter/Reviewer walkthroughs and protect neurofeedback safety standards, ")
    md_content.append("all warnings regarding physical device non-validation, shadow-only mode bounds, ")
    md_content.append("and closed-loop locks must be perfectly visible in default text elements, ")
    md_content.append("rather than isolated within interactive custom widgets or dynamic hover panels.")

    (REPORT_DIR / "accessibility_check.md").write_text("\n".join(md_content), encoding="utf-8")
    print(f"[+] Saved JSON report to: {REPORT_DIR / 'accessibility_check.json'}")
    print(f"[+] Saved Markdown report to: {REPORT_DIR / 'accessibility_check.md'}")

if __name__ == "__main__":
    import sys
    success = run_accessibility_check()
    sys.exit(0 if success else 1)
