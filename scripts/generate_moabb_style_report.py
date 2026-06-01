"""Generate a MOABB-style report from a benchmark output."""

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    generate_moabb_report(Path(args.benchmark_dir), Path(args.output_dir))


def generate_moabb_report(benchmark_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(benchmark_dir / "benchmark_summary.json") as f:
        summary = json.load(f)
        
    best_model = summary.get("best_model", {})
    metrics = best_model.get("metrics", {})
    loso = summary.get("loso", {})
    
    report = {
        "dataset": summary.get("epochs"),
        "paradigm": "MotorImagery",
        "subjects": len(summary.get("subjects", [])),
        "sessions": len(summary.get("runs", [])),
        "evaluation_type": "WithinSession / CrossSubject",
        "pipeline": best_model.get("model"),
        "score": metrics.get("balanced_accuracy"),
        "per_subject_score": loso.get("mean_balanced_accuracy"),
        "statistical_summary": {
            "group_run_balanced_accuracy": metrics.get("balanced_accuracy"),
            "loso_mean_balanced_accuracy": loso.get("mean_balanced_accuracy")
        },
        "reproducibility": {
            "seed": 42,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    }
    
    with open(output_dir / "physionet_eegbci_moabb_style_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    with open(output_dir / "physionet_eegbci_moabb_style_report.md", "w") as f:
        f.write("# MOABB-Style Compatibility Report\n\n")
        f.write(f"- Dataset: {report['dataset']}\n")
        f.write(f"- Paradigm: {report['paradigm']}\n")
        f.write(f"- Subjects: {report['subjects']}\n")
        f.write(f"- Pipeline: {report['pipeline']}\n")
        f.write(f"- Group Score: {report['score']}\n")
        f.write(f"- LOSO Score: {report['per_subject_score']}\n\n")
        f.write("Note: This is a MOABB-style compatibility report generated from internal benchmarks, not an official MOABB integration.\n")

if __name__ == "__main__":
    main()
