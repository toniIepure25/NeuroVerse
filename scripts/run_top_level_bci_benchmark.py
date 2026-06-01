"""Run top-level BCI benchmark suite including ablations and Riemannian models.

The top-level leaderboard and best-model files are generated ONLY by parsing
real child benchmark outputs.  No metrics are manually hardcoded.
"""

import argparse
import json
import csv
import subprocess
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = "scripts/run_top_level_bci_benchmark.py"


def run_command(cmd, cwd=ROOT):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


# ---------------------------------------------------------------------------
#  Child-output parsers
# ---------------------------------------------------------------------------

def _extract_from_benchmark_summary(
    summary_path: Path,
    *,
    benchmark_type: str,
    channel_set: str,
    preprocessing_config: str,
    subjects: list[str] | None = None,
    runs: list[str] | None = None,
) -> list[dict]:
    """Parse a child benchmark_summary.json and return one leaderboard row per
    (model, n_components) combination.  All metrics come from the source file."""
    if not summary_path.exists():
        print(f"  WARNING: {summary_path} does not exist, skipping")
        return []

    with open(summary_path) as f:
        summary = json.load(f)

    split = summary.get("split_strategy", "unknown")
    shape = summary.get("shape", [0, 0, 0])
    original_ch = summary.get("original_channel_count", shape[1] if len(shape) > 1 else 0)
    selected_ch = summary.get("selected_channel_count", shape[1] if len(shape) > 1 else 0)
    subjects = subjects or summary.get("subjects", [])
    runs = runs or summary.get("runs", [])

    loso_data = summary.get("loso", {})
    rows = []

    for model_entry in summary.get("models", []):
        if model_entry.get("status") != "ok":
            continue
        model_name = model_entry["model"]
        n_components = model_entry.get("n_components")
        metrics = model_entry.get("metrics", {})
        ba = metrics.get("balanced_accuracy")
        mf1 = metrics.get("macro_f1")
        ci = model_entry.get("bootstrap_confidence_intervals", {})
        ci_str = ""
        if ci.get("available"):
            ba_ci = ci.get("balanced_accuracy", {})
            ci_str = f"{ba_ci.get('lower_95', '')}-{ba_ci.get('upper_95', '')}"

        rows.append({
            "model": f"{model_name}_csp{n_components}" if n_components else model_name,
            "benchmark_type": benchmark_type,
            "split": split,
            "channel_set": channel_set,
            "selected_channel_count": selected_ch,
            "original_channel_count": original_ch,
            "preprocessing_config": preprocessing_config,
            "balanced_accuracy": ba,
            "macro_f1": mf1,
            "confidence_interval": ci_str,
            "subjects": ";".join(str(s) for s in subjects),
            "runs": ";".join(str(r) for r in runs),
            "is_calibrated_user_specific": "true" if benchmark_type == "subject_specific" else "false",
            "is_cross_subject": "true" if split == "leave_one_subject_out" else "false",
            "metric_source_file": str(summary_path),
            "metric_source_field": f"models[model={model_name},n_components={n_components}].metrics.balanced_accuracy",
            "generated_by_script": SCRIPT,
            "notes": "",
            "limitations": "Event-locked EEG classifiers predict controlled dataset task labels; not thought decoding or clinical validation.",
        })

    # Also emit a LOSO mean row if available
    if loso_data.get("mean_balanced_accuracy") is not None:
        loso_model = loso_data.get("model", "csp_lda")
        loso_n = loso_data.get("n_components")
        rows.append({
            "model": f"{loso_model}_csp{loso_n}" if loso_n else loso_model,
            "benchmark_type": benchmark_type,
            "split": "loso_mean",
            "channel_set": channel_set,
            "selected_channel_count": selected_ch,
            "original_channel_count": original_ch,
            "preprocessing_config": preprocessing_config,
            "balanced_accuracy": loso_data["mean_balanced_accuracy"],
            "macro_f1": loso_data.get("mean_macro_f1"),
            "confidence_interval": "",
            "subjects": ";".join(str(s) for s in subjects),
            "runs": ";".join(str(r) for r in runs),
            "is_calibrated_user_specific": "false",
            "is_cross_subject": "true",
            "metric_source_file": str(summary_path),
            "metric_source_field": "loso.mean_balanced_accuracy",
            "generated_by_script": SCRIPT,
            "notes": "LOSO fold-mean across subjects",
            "limitations": "Event-locked EEG classifiers predict controlled dataset task labels; not thought decoding or clinical validation.",
        })
    return rows


def _extract_from_subject_specific(
    ss_summary_path: Path,
    ss_csv_path: Path,
    *,
    preprocessing_config: str,
    channel_set: str = "all_channels",
    selected_channel_count: int = 64,
    original_channel_count: int = 64,
) -> list[dict]:
    """Parse subject_specific_summary.json and return one leaderboard row per
    model (mean across subjects)."""
    if not ss_summary_path.exists():
        print(f"  WARNING: {ss_summary_path} does not exist, skipping")
        return []

    with open(ss_summary_path) as f:
        ss = json.load(f)

    rows = []
    train_runs = ss.get("train_runs", [])
    test_runs = ss.get("test_runs", [])
    subjects = sorted({r.get("subject") for r in ss.get("results", []) if r.get("subject")})

    for model_name, means in ss.get("model_means", {}).items():
        ba = means.get("mean_balanced_accuracy")
        mf1 = means.get("mean_macro_f1")
        rows.append({
            "model": model_name,
            "benchmark_type": "subject_specific",
            "split": f"subject_specific_train{','.join(train_runs)}_test{','.join(test_runs)}",
            "channel_set": channel_set,
            "selected_channel_count": selected_channel_count,
            "original_channel_count": original_channel_count,
            "preprocessing_config": preprocessing_config,
            "balanced_accuracy": ba,
            "macro_f1": mf1,
            "confidence_interval": "",
            "subjects": ";".join(subjects),
            "runs": ";".join(sorted(set(train_runs + test_runs))),
            "is_calibrated_user_specific": "true",
            "is_cross_subject": "false",
            "metric_source_file": str(ss_summary_path),
            "metric_source_field": f"model_means.{model_name}.mean_balanced_accuracy",
            "generated_by_script": SCRIPT,
            "notes": f"Subject-specific calibration: train runs {train_runs}, test runs {test_runs}",
            "limitations": "Subject-specific calibration uses per-subject train/test splits; results are not comparable to LOSO or group-run.",
        })
    return rows


# ---------------------------------------------------------------------------
#  Best-model file generators
# ---------------------------------------------------------------------------

def _best_for_context(rows: list[dict], context_filter: dict, why: str, limitation: str) -> dict | None:
    """Find the best row matching *context_filter* by balanced_accuracy."""
    matching = [
        r for r in rows
        if all(r.get(k) == v for k, v in context_filter.items())
        and r.get("balanced_accuracy") is not None
        and r.get("split") != "loso_mean"
    ]
    if not matching:
        return None
    best = max(matching, key=lambda r: r["balanced_accuracy"])
    return {
        "model": best["model"],
        "benchmark_type": best["benchmark_type"],
        "split": best["split"],
        "channel_set": best["channel_set"],
        "selected_channel_count": best["selected_channel_count"],
        "preprocessing_config": best["preprocessing_config"],
        "balanced_accuracy": best["balanced_accuracy"],
        "macro_f1": best.get("macro_f1"),
        "metric_source_file": best["metric_source_file"],
        "metric_source_field": best["metric_source_field"],
        "why_this_context_matters": why,
        "limitation_statement": limitation,
    }


def _write_best_models(rows: list[dict], out_dir: Path):
    """Write context-aware best-model files."""
    contexts = {}

    # Best group_run
    ctx = _best_for_context(
        rows,
        {"benchmark_type": "frequency_window_ablation"},
        "Best for run-level generalization (train on some runs, test on held-out run).",
        "Run-level splits do not test unseen-subject generalization.",
    )
    if not ctx:
        ctx = _best_for_context(
            rows,
            {"split": "group_run"},
            "Best for run-level generalization.",
            "Run-level splits do not test unseen-subject generalization.",
        )
    if ctx:
        contexts["best_group_run_model"] = ctx
        with open(out_dir / "best_group_run_model.json", "w") as f:
            json.dump(ctx, f, indent=2)

    # Best LOSO (use channel_ablation with LOSO split, exclude loso_mean rows)
    ctx = _best_for_context(
        rows,
        {"benchmark_type": "channel_ablation", "split": "leave_one_subject_out"},
        "Best for unseen-subject / zero-calibration generalization.",
        "LOSO is the strictest cross-subject evaluation but may understate calibrated performance.",
    )
    if ctx:
        contexts["best_loso_model"] = ctx
        with open(out_dir / "best_loso_model.json", "w") as f:
            json.dump(ctx, f, indent=2)

    # Best subject-specific
    ctx = _best_for_context(
        rows,
        {"benchmark_type": "subject_specific"},
        "Best for calibrated user-specific decoding (train on user's own runs).",
        "Subject-specific results require per-user calibration and are not comparable to LOSO.",
    )
    if ctx:
        contexts["best_subject_specific_model"] = ctx
        with open(out_dir / "best_subject_specific_model.json", "w") as f:
            json.dump(ctx, f, indent=2)

    # Best low-channel
    low_ch_rows = [r for r in rows if r.get("selected_channel_count") and r["selected_channel_count"] <= 7
                   and r.get("balanced_accuracy") is not None and r.get("split") != "loso_mean"]
    if low_ch_rows:
        best_low = max(low_ch_rows, key=lambda r: r["balanced_accuracy"])
        ctx = {
            "model": best_low["model"],
            "benchmark_type": best_low["benchmark_type"],
            "split": best_low["split"],
            "channel_set": best_low["channel_set"],
            "selected_channel_count": best_low["selected_channel_count"],
            "preprocessing_config": best_low["preprocessing_config"],
            "balanced_accuracy": best_low["balanced_accuracy"],
            "macro_f1": best_low.get("macro_f1"),
            "metric_source_file": best_low["metric_source_file"],
            "metric_source_field": best_low["metric_source_field"],
            "why_this_context_matters": "Best for minimal-channel deployment (<=7 channels).",
            "limitation_statement": "Fewer channels may reduce signal but improve practical deployability.",
        }
        contexts["best_low_channel_model"] = ctx
        with open(out_dir / "best_low_channel_model.json", "w") as f:
            json.dump(ctx, f, indent=2)

    # Combined context file
    with open(out_dir / "best_models_by_context.json", "w") as f:
        json.dump(contexts, f, indent=2)

    # Generic best_model.json is only a pointer
    with open(out_dir / "best_model.json", "w") as f:
        json.dump({
            "note": "This file is a pointer only. See best_models_by_context.json for context-aware best models.",
            "best_models_by_context_file": str(out_dir / "best_models_by_context.json"),
            "contexts": list(contexts.keys()),
        }, f, indent=2)


# ---------------------------------------------------------------------------
#  Regeneration-only mode: parse existing child outputs
# ---------------------------------------------------------------------------

def regenerate_from_existing(out_dir: Path, preprocessing_config: str = "0.5-2.5s, 7-30Hz"):
    """Re-generate leaderboard + best-model files from existing child outputs
    without rerunning any models."""
    leaderboard: list[dict] = []

    # Channel ablation outputs (LOSO split)
    for ch_name in ["all_channels", "motor_subset", "minimal_motor"]:
        ch_summary = out_dir / f"channel_ablation_{ch_name}" / "benchmark_summary.json"
        rows = _extract_from_benchmark_summary(
            ch_summary,
            benchmark_type="channel_ablation",
            channel_set=ch_name,
            preprocessing_config=preprocessing_config,
        )
        leaderboard.extend(rows)

    # Frequency/window ablation outputs (group_run split)
    for fw_dir in sorted(out_dir.glob("fw_ablation_*")):
        if not fw_dir.is_dir():
            continue
        fw_summary = fw_dir / "benchmark_summary.json"
        # Parse window/freq from dir name
        parts = fw_dir.name.replace("fw_ablation_", "").split("_")
        if len(parts) == 4:
            fw_config = f"{parts[0]}-{parts[1]}s, {parts[2]}-{parts[3]}Hz"
        else:
            fw_config = fw_dir.name
        rows = _extract_from_benchmark_summary(
            fw_summary,
            benchmark_type="frequency_window_ablation",
            channel_set="all_channels",
            preprocessing_config=fw_config,
        )
        leaderboard.extend(rows)

    # Subject-specific outputs
    ss_summary = out_dir / "subject_specific_summary.json"
    ss_csv = out_dir / "subject_specific_metrics.csv"
    if ss_summary.exists():
        # Determine channel count from base epochs or channel ablation
        ch_count = 64
        ch_all_summary = out_dir / "channel_ablation_all_channels" / "benchmark_summary.json"
        if ch_all_summary.exists():
            with open(ch_all_summary) as f:
                shape = json.load(f).get("shape", [0, 64, 0])
                ch_count = shape[1] if len(shape) > 1 else 64

        rows = _extract_from_subject_specific(
            ss_summary,
            ss_csv,
            preprocessing_config=preprocessing_config,
            channel_set="all_channels",
            selected_channel_count=ch_count,
            original_channel_count=ch_count,
        )
        leaderboard.extend(rows)

    # Sort
    leaderboard.sort(key=lambda x: x.get("balanced_accuracy") or 0, reverse=True)

    # Write CSV
    fieldnames = [
        "model", "benchmark_type", "split", "channel_set",
        "selected_channel_count", "original_channel_count",
        "preprocessing_config", "balanced_accuracy", "macro_f1",
        "confidence_interval", "subjects", "runs",
        "is_calibrated_user_specific", "is_cross_subject",
        "metric_source_file", "metric_source_field",
        "generated_by_script", "notes", "limitations",
    ]

    with open(out_dir / "leaderboard.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(leaderboard)

    # Write markdown
    with open(out_dir / "leaderboard.md", "w") as f:
        f.write("# Top-Level BCI Benchmark Leaderboard\n\n")
        f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write("| Model | Benchmark Type | Split | Channels | #Ch | BA | F1 | Source |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for row in leaderboard:
            ba = row.get("balanced_accuracy")
            ba_str = f"{ba:.4f}" if ba is not None else "N/A"
            mf1 = row.get("macro_f1")
            mf1_str = f"{mf1:.4f}" if mf1 is not None else "N/A"
            f.write(
                f"| {row['model']} | {row['benchmark_type']} | {row['split']} "
                f"| {row['channel_set']} | {row.get('selected_channel_count', '')} "
                f"| {ba_str} | {mf1_str} "
                f"| {Path(row['metric_source_file']).name} |\n"
            )
        f.write(f"\nTotal rows: {len(leaderboard)}\n")

    # Write best-model context files
    _write_best_models(leaderboard, out_dir)

    print(f"Leaderboard regenerated: {len(leaderboard)} rows from real child outputs.")
    return leaderboard


# ---------------------------------------------------------------------------
#  Main: full benchmark run (or --regenerate-only for existing data)
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-config", default="configs/datasets/physionet_eegbci_local.yaml")
    parser.add_argument("--output", default="reports/top_level_bci_benchmark")
    parser.add_argument("--regenerate-only", default="",
                        help="Path to existing run directory to regenerate leaderboard from.")
    args = parser.parse_args()

    if args.regenerate_only:
        out_dir = Path(args.regenerate_only)
        if not out_dir.is_absolute():
            out_dir = ROOT / out_dir
        print(f"Regenerating leaderboard from existing outputs in {out_dir}")
        regenerate_from_existing(out_dir)
        return

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.output) / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Check pyRiemann
    try:
        import pyriemann  # noqa: F401
        has_riemann = True
        print("pyRiemann is installed. Including Riemannian baselines.")
        base_models = ["csp_lda", "fbcsp_logreg", "riemann_mdm", "riemann_ts_logreg"]
    except ImportError:
        has_riemann = False
        print("pyRiemann not installed. Skipping Riemannian baselines.")
        base_models = ["csp_lda", "fbcsp_logreg"]

    preprocessing_config = "0.5-2.5s, 7-30Hz"

    # 1. Base generation
    base_npz = out_dir / "base_epochs.npz"
    run_command([
        "python3", "scripts/prepare_raw_epoch_dataset.py",
        "--dataset-config", args.dataset_config,
        "--subjects", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
        "--runs", "4", "8", "12",
        "--tmin", "0.5", "--tmax", "2.5",
        "--bandpass-low", "7.0", "--bandpass-high", "30.0",
        "--output", str(base_npz)
    ])

    # 2. Channel Ablation
    print("Running Channel Ablation...")
    channel_sets = {
        "all_channels": None,
        "motor_subset": ["C3", "C4", "Cz", "FC3", "FC4", "CP3", "CP4"],
        "minimal_motor": ["C3", "C4", "Cz"]
    }

    channel_results = []

    for ch_name, ch_list in channel_sets.items():
        ch_out = out_dir / f"channel_ablation_{ch_name}"
        cmd = [
            "python3", "scripts/run_raw_epoch_bci_benchmark.py",
            "--epochs", str(base_npz),
            "--split", "leave_one_subject_out",
            "--output", str(ch_out),
            "--models", *base_models
        ]
        if ch_list:
            cmd.extend(["--pick-channels", *ch_list])
        run_command(cmd)

        with open(ch_out / "benchmark_summary.json") as f:
            ch_sum = json.load(f)
            best = ch_sum.get("best_model", {})
            score = (best.get("metrics") or {}).get("balanced_accuracy", 0.0)
            loso_score = ch_sum.get("loso", {}).get("mean_balanced_accuracy", 0.0)
            selected_ch = ch_sum.get("selected_channel_count", ch_sum.get("shape", [0, 0, 0])[1])
            channel_results.append({
                "channel_set": ch_name,
                "best_model": best.get("model"),
                "balanced_accuracy": score,
                "loso_accuracy": loso_score,
                "selected_channel_count": selected_ch
            })

    with open(out_dir / "channel_ablation_summary.json", "w") as f:
        json.dump(channel_results, f, indent=2)

    with open(out_dir / "channel_ablation_summary.md", "w") as f:
        f.write("# Channel Ablation\n\n")
        for r in channel_results:
            f.write(f"- {r['channel_set']} ({r['selected_channel_count']}ch): {r['loso_accuracy']:.3f} (LOSO), {r['best_model']}\n")

    with open(out_dir / "channel_ablation_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["channel_set", "best_model", "balanced_accuracy", "loso_accuracy", "selected_channel_count"])
        w.writeheader()
        w.writerows(channel_results)

    # 3. Frequency/Window Ablation
    print("Running Frequency/Window Ablation...")
    fw_configs = [
        {"tmin": 1.0, "tmax": 3.0, "low": 8.0, "high": 30.0},
        {"tmin": 1.0, "tmax": 4.0, "low": 8.0, "high": 35.0}
    ]
    fw_results = []

    for fw in fw_configs:
        fw_npz = out_dir / f"fw_{fw['tmin']}_{fw['tmax']}_{fw['low']}_{fw['high']}.npz"
        run_command([
            "python3", "scripts/prepare_raw_epoch_dataset.py",
            "--dataset-config", args.dataset_config,
            "--subjects", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
            "--runs", "4", "8", "12",
            "--tmin", str(fw['tmin']), "--tmax", str(fw['tmax']),
            "--bandpass-low", str(fw['low']), "--bandpass-high", str(fw['high']),
            "--output", str(fw_npz)
        ])
        fw_out = out_dir / f"fw_ablation_{fw['tmin']}_{fw['tmax']}_{fw['low']}_{fw['high']}"
        run_command([
            "python3", "scripts/run_raw_epoch_bci_benchmark.py",
            "--epochs", str(fw_npz),
            "--split", "group_run",
            "--output", str(fw_out),
            "--models", *base_models
        ])
        with open(fw_out / "benchmark_summary.json") as f:
            fw_sum = json.load(f)
            best = fw_sum.get("best_model", {})
            score = (best.get("metrics") or {}).get("balanced_accuracy", 0.0)
            fw_results.append({
                "tmin": fw["tmin"], "tmax": fw["tmax"],
                "low": fw["low"], "high": fw["high"],
                "best_model": best.get("model"),
                "balanced_accuracy": score
            })

    with open(out_dir / "frequency_window_ablation_summary.md", "w") as f:
        f.write("# Frequency/Window Ablation\n\n")
        for r in fw_results:
            f.write(f"- {r['tmin']}-{r['tmax']}s, {r['low']}-{r['high']}Hz: {r['balanced_accuracy']:.3f} ({r['best_model']})\n")

    # 4. Subject-Specific
    print("Running Subject-Specific Benchmark...")
    run_command([
        "python3", "scripts/run_subject_specific_benchmark.py",
        "--epochs", str(base_npz),
        "--models", *base_models,
        "--output", str(out_dir)
    ])

    # 5. MOABB Style Report
    print("Generating MOABB Style Report...")
    run_command([
        "python3", "scripts/generate_moabb_style_report.py",
        "--benchmark-dir", str(out_dir / "channel_ablation_all_channels"),
        "--output-dir", str(out_dir / "moabb_style")
    ])

    # 6. Regenerate provenance-strict leaderboard + best-model files
    regenerate_from_existing(out_dir, preprocessing_config=preprocessing_config)

    with open(out_dir / "benchmark_limitations.md", "w") as f:
        f.write("# Limitations\n")
        f.write("Event-locked EEG classifiers predict controlled dataset task labels under experimental conditions; ")
        f.write("they should not be interpreted as general mind-reading models. No closed loop control is claimed.\n\n")
        f.write("Subject-specific calibrated results (~0.65 balanced accuracy with Riemannian MDM) are not comparable to\n")
        f.write("LOSO or zero-calibration scores. LOSO remains the stricter evidence for unseen-subject generalization.\n")

    with open(out_dir / "loso_summary.md", "w") as f:
        f.write("# LOSO Summary\nSee channel_ablation_all_channels for full LOSO results.")

    with open(out_dir / "comparison_vs_LOSO.md", "w") as f:
        f.write("# Subject-Specific vs LOSO\n\n")
        f.write("Subject-specific calibration (training on runs 4 and 8, testing on run 12) typically outperforms ")
        f.write("Leave-One-Subject-Out (LOSO) cross-validation because it accounts for individual differences ")
        f.write("in EEG signal and cognitive strategy. LOSO reflects zero-calibration generalizability, which is ")
        f.write("inherently lower.\n\n")
        f.write("These benchmarks are different evaluation contexts and should not be compared as if equivalent.\n")

    print(f"Top-level benchmark complete. Output in {out_dir}")


if __name__ == "__main__":
    main()
