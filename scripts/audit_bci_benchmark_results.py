"""Audit BCI benchmark results for provenance integrity, leakage, and consistency.

Exits with non-zero status if any provenance or integrity check fails.
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-dir", required=True)
    args = parser.parse_args()

    ok = audit(Path(args.benchmark_dir))
    sys.exit(0 if ok else 1)


def audit(benchmark_dir: Path) -> bool:
    if not benchmark_dir.exists():
        print(f"ERROR: Directory {benchmark_dir} does not exist.")
        return False

    # Check for latest run
    subdirs = [d for d in benchmark_dir.iterdir() if d.is_dir()]
    if not subdirs:
        print("ERROR: No benchmark runs found.")
        return False
    latest_run = max(subdirs, key=lambda d: d.name)

    print(f"Auditing run: {latest_run.name}")

    errors: list[str] = []
    warnings: list[str] = []

    # ---------------------------------------------------------------
    # 1. Required files
    # ---------------------------------------------------------------
    required_files = [
        "leaderboard.csv",
        "best_models_by_context.json",
        "channel_ablation_summary.json",
    ]

    optional_files = [
        "subject_specific_summary.json",
        "subject_specific_summary.md",
        "moabb_style/physionet_eegbci_moabb_style_report.json",
    ]

    for f in required_files:
        if not (latest_run / f).exists():
            errors.append(f"Missing required file: {f}")

    for f in optional_files:
        if not (latest_run / f).exists():
            warnings.append(f"Missing optional file: {f}")

    # ---------------------------------------------------------------
    # 2. Leaderboard provenance validation
    # ---------------------------------------------------------------
    leaderboard_path = latest_run / "leaderboard.csv"
    leaderboard_rows = []

    required_columns = {
        "model", "benchmark_type", "split", "channel_set",
        "selected_channel_count", "original_channel_count",
        "preprocessing_config", "balanced_accuracy",
        "metric_source_file", "metric_source_field",
        "generated_by_script",
    }

    if leaderboard_path.exists():
        with open(leaderboard_path) as f:
            reader = csv.DictReader(f)
            headers = set(reader.fieldnames or [])
            missing_cols = required_columns - headers
            if missing_cols:
                errors.append(f"Leaderboard missing required columns: {sorted(missing_cols)}")

            for i, row in enumerate(reader):
                leaderboard_rows.append(row)
                row_id = f"Row {i+1} ({row.get('model', '?')})"

                # metric_source_file must exist
                msf = row.get("metric_source_file", "")
                if not msf:
                    errors.append(f"{row_id}: metric_source_file is empty")
                elif not Path(msf).exists():
                    errors.append(f"{row_id}: metric_source_file does not exist: {msf}")

                # metric_source_field must be present
                if not row.get("metric_source_field"):
                    errors.append(f"{row_id}: metric_source_field is empty")

                # balanced_accuracy validation
                ba_str = row.get("balanced_accuracy", "")
                if not ba_str:
                    errors.append(f"{row_id}: balanced_accuracy is missing")
                else:
                    try:
                        ba = float(ba_str)
                        if ba != ba:  # NaN check
                            errors.append(f"{row_id}: balanced_accuracy is NaN")
                        elif ba < 0.0 or ba > 1.0:
                            errors.append(f"{row_id}: balanced_accuracy {ba} outside [0, 1]")
                    except ValueError:
                        errors.append(f"{row_id}: balanced_accuracy is not numeric: {ba_str}")

                # macro_f1 validation (if present)
                mf1_str = row.get("macro_f1", "")
                if mf1_str:
                    try:
                        mf1 = float(mf1_str)
                        if mf1 < 0.0 or mf1 > 1.0:
                            errors.append(f"{row_id}: macro_f1 {mf1} outside [0, 1]")
                    except ValueError:
                        pass  # empty or non-numeric is OK

                # Check for mock/manual/hardcoded markers
                row_str = str(row).lower()
                for suspect in ["mock", "manual", "hardcoded"]:
                    if suspect in row_str:
                        errors.append(f"{row_id}: contains suspicious marker '{suspect}' in provenance or notes")

                # Subject-specific mislabeled as LOSO
                if row.get("benchmark_type") == "loso" and row.get("is_calibrated_user_specific") == "true":
                    errors.append(f"{row_id}: subject_specific result mislabeled as LOSO")

                # benchmark_type present
                if not row.get("benchmark_type"):
                    errors.append(f"{row_id}: benchmark_type is missing")

        if not leaderboard_rows:
            errors.append("Leaderboard has no data rows")

    # ---------------------------------------------------------------
    # 3. Channel ablation sanity
    # ---------------------------------------------------------------
    ablation_json = latest_run / "channel_ablation_summary.json"
    if ablation_json.exists():
        with open(ablation_json) as f:
            ablations = json.load(f)

        full_count = None
        for a in ablations:
            sc = a.get("selected_channel_count")
            cs = a.get("channel_set", "")
            if cs == "all_channels":
                full_count = sc

        if full_count is not None:
            for a in ablations:
                cs = a.get("channel_set", "")
                sc = a.get("selected_channel_count")
                if cs == "motor_subset" and sc == full_count:
                    errors.append(f"channel_ablation motor_subset has selected_channel_count == full ({full_count})")
                if cs == "minimal_motor" and sc == full_count:
                    errors.append(f"channel_ablation minimal_motor has selected_channel_count == full ({full_count})")

        counts = [a.get("selected_channel_count") for a in ablations if a.get("selected_channel_count") is not None]
        if len(set(counts)) == 1 and len(ablations) > 1:
            errors.append("Channel counts are identical across all ablations. This likely indicates a bug.")
    else:
        warnings.append("channel_ablation_summary.json not found")

    # ---------------------------------------------------------------
    # 4. best_models_by_context.json validation
    # ---------------------------------------------------------------
    best_ctx_path = latest_run / "best_models_by_context.json"
    if best_ctx_path.exists():
        with open(best_ctx_path) as f:
            best_ctx = json.load(f)

        for ctx_name, ctx_data in best_ctx.items():
            msf = ctx_data.get("metric_source_file", "")
            if msf and not Path(msf).exists():
                errors.append(f"best_models_by_context.{ctx_name}: metric_source_file does not exist: {msf}")
    else:
        errors.append("best_models_by_context.json not found")

    # ---------------------------------------------------------------
    # 5. Leakage audit (reused from old script)
    # ---------------------------------------------------------------
    leakage_report = {
        "status": "PASS",
        "checks": []
    }

    def check_split(name, path, expected_split):
        if not path.exists():
            return
        with open(path) as f:
            data = json.load(f)
            split = data.get("split_strategy")
            leak_warnings = data.get("leakage_warnings", [])

            leakage_report["checks"].append({
                "name": name,
                "expected_split": expected_split,
                "actual_split": split,
                "warnings": leak_warnings,
                "pass": split == expected_split and not leak_warnings
            })
            if leak_warnings:
                leakage_report["status"] = "FAIL"
                errors.append(f"Leakage detected in {name}: {leak_warnings}")

    check_split("channel_ablation_all_channels",
                latest_run / "channel_ablation_all_channels/benchmark_summary.json",
                "leave_one_subject_out")
    check_split("channel_ablation_motor_subset",
                latest_run / "channel_ablation_motor_subset/benchmark_summary.json",
                "leave_one_subject_out")
    check_split("channel_ablation_minimal_motor",
                latest_run / "channel_ablation_minimal_motor/benchmark_summary.json",
                "leave_one_subject_out")

    for fw_dir in sorted(latest_run.glob("fw_ablation_*")):
        if fw_dir.is_dir():
            check_split(fw_dir.name,
                        fw_dir / "benchmark_summary.json",
                        "group_run")

    # Write leakage reports
    with open(latest_run / "leakage_audit.json", "w") as f:
        json.dump(leakage_report, f, indent=2)

    with open(latest_run / "leakage_audit.md", "w") as f:
        f.write("# Leakage Audit Report\n\n")
        f.write(f"Status: **{leakage_report['status']}**\n\n")
        for check in leakage_report["checks"]:
            f.write(f"### {check['name']}\n")
            f.write(f"- Expected Split: {check['expected_split']}\n")
            f.write(f"- Actual Split: {check['actual_split']}\n")
            f.write(f"- Pass: {check['pass']}\n")
            if check['warnings']:
                f.write("- Warnings:\n")
                for w in check['warnings']:
                    f.write(f"  - {w}\n")
            f.write("\n")

    # ---------------------------------------------------------------
    # 6. Write integrity audit report
    # ---------------------------------------------------------------
    audit_report = {
        "run_id": latest_run.name,
        "audit_timestamp": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "leaderboard_row_count": len(leaderboard_rows),
        "leakage_status": leakage_report["status"],
    }

    with open(latest_run / "artifact_integrity_audit.json", "w") as f:
        json.dump(audit_report, f, indent=2)

    with open(latest_run / "artifact_integrity_audit.md", "w") as f:
        f.write("# Artifact Integrity Audit Report\n\n")
        f.write(f"Run: {latest_run.name}\n\n")
        f.write(f"Status: **{audit_report['status']}**\n\n")
        f.write(f"Leaderboard rows: {len(leaderboard_rows)}\n\n")
        if errors:
            f.write("## Errors\n\n")
            for e in errors:
                f.write(f"- ❌ {e}\n")
            f.write("\n")
        if warnings:
            f.write("## Warnings\n\n")
            for w in warnings:
                f.write(f"- ⚠️ {w}\n")
            f.write("\n")
        if not errors:
            f.write("All provenance checks passed. ✅\n")

    # Print summary
    print(f"\n{'='*60}")
    print(f"Audit Status: {audit_report['status']}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Leaderboard rows: {len(leaderboard_rows)}")
    print(f"Leakage: {leakage_report['status']}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  ❌ {e}")
    print(f"{'='*60}\n")

    return len(errors) == 0


if __name__ == "__main__":
    main()
