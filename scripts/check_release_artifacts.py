import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent

def check_artifacts():
    required_files = [
        "README.md",
        "VERSION",
        "REVIEWER_START_HERE.md",
        "evidence_pack/README.md",
        "evidence_pack/artifact_inventory.json",
        "evidence_pack/artifact_inventory.md",
        "docs/API_REFERENCE.md",
        "docs/openapi.json",
        "docs/RECRUITER_TECHNICAL_SUMMARY.md",
        "docs/NEUROTECH_APPLICATION_PACKAGE.md",
        "docs/INTERVIEW_QA.md",
        "docs/RELEASE_NOTES_v1.0.md",
        "docs/SCREENSHOT_AND_DEMO_ASSETS.md",
        "docs/DEPLOYMENT.md"
    ]

    expected_globs = {
        "PhysioNet benchmark": "reports/bci_benchmark/*/benchmark_summary.json",
        "raw CSP/FBCSP benchmark": "reports/bci_raw_epoch_benchmark/*/benchmark_summary.json",
        "LSL validation": "reports/hardware_validation/*lsl*_validation.md",
        "BrainFlow synthetic validation": "reports/hardware_validation/*brainflow*_validation.md",
        "physical trial synthetic": "reports/hardware_trials/*/physical_eeg_trial_summary.json",
    }

    optional_globs = {
        "physical OpenBCI real report": "reports/hardware_trials/*openbci*/physical_eeg_trial_summary.json",
        "Galea report": "reports/hardware_trials/*galea*/physical_eeg_trial_summary.json",
        "pyxdf/XDF report": "reports/eeg_lsl_validation/*/eeg_lsl_validation_summary.json",
    }

    results = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "required": {},
        "expected": {},
        "optional": {},
        "passed": True
    }

    print("--- NeuroVerse v1.1.0-rc1 Release Check ---")

    for f in required_files:
        path = ROOT / f
        exists = path.exists()
        results["required"][f] = exists
        if not exists:
            results["passed"] = False
            print(f"[FAIL] Required file missing: {f}")
        else:
            print(f"[PASS] {f}")

    for name, pattern in expected_globs.items():
        matches = list(ROOT.glob(pattern))
        if matches:
            results["expected"][name] = True
            print(f"[PASS] Expected {name} found: {matches[0].relative_to(ROOT)}")
        else:
            results["expected"][name] = False
            results["passed"] = False
            print(f"[FAIL] Expected {name} missing. You must run the evidence generation commands.")

    for name, pattern in optional_globs.items():
        matches = list(ROOT.glob(pattern))
        if matches:
            results["optional"][name] = True
            print(f"[PASS] Optional {name} found: {matches[0].relative_to(ROOT)}")
        else:
            results["optional"][name] = False
            print(f"[WARN] Optional {name} missing. (This is expected if physical hardware is absent).")

    out_dir = ROOT / "reports/release_check"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "release_check.json", "w") as f:
        json.dump(results, f, indent=2)

    md_lines = ["# Release Check Report\n"]
    md_lines.append(f"**Checked at**: {results['checked_at']}")
    md_lines.append(f"**Overall Status**: {'PASS' if results['passed'] else 'FAIL'}\n")
    
    md_lines.append("## Required Artifacts")
    for f, status in results['required'].items():
        md_lines.append(f"- [{'x' if status else ' '}] {f}")

    md_lines.append("\n## Expected Artifacts (Must be generated before release)")
    for f, status in results['expected'].items():
        md_lines.append(f"- [{'x' if status else ' '}] {f}")

    md_lines.append("\n## Optional Artifacts (Physical Hardware / Extras)")
    for f, status in results['optional'].items():
        md_lines.append(f"- [{'x' if status else ' '}] {f}")

    with open(out_dir / "release_check.md", "w") as f:
        f.write("\n".join(md_lines))

    if not results["passed"]:
        print("\nRelease check failed. Missing required or expected artifacts.")
        exit(1)
    else:
        print("\nRelease check passed.")

if __name__ == "__main__":
    check_artifacts()
