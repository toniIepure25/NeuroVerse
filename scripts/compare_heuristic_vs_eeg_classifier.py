"""Compare heuristic LSL shadow output with an event-locked EEG classifier report."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare heuristic proxy and EEG classifier reports")
    parser.add_argument("--heuristic-shadow", required=True)
    parser.add_argument("--classifier-shadow", required=True)
    parser.add_argument("--validation-report", default=None)
    parser.add_argument("--calibration-report", default=None)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output = _resolve(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    result = compare_reports(
        heuristic=_read(args.heuristic_shadow),
        classifier=_read(args.classifier_shadow),
        validation=_read(args.validation_report) if args.validation_report else {},
        calibration=_read(args.calibration_report) if args.calibration_report else {},
    )
    (output / "heuristic_vs_classifier_comparison.json").write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )
    (output / "heuristic_vs_classifier_comparison.md").write_text(
        _markdown(result),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


def compare_reports(
    *,
    heuristic: dict[str, Any],
    classifier: dict[str, Any],
    validation: dict[str, Any],
    calibration: dict[str, Any],
) -> dict[str, Any]:
    predictions = classifier.get("predictions") or []
    marker_labels = [str(row.get("marker_label")) for row in predictions if row.get("marker_label")]
    pred_labels = [str(row.get("predicted_label")) for row in predictions if row.get("predicted_label")]
    proxy_by_marker = heuristic.get("marker_conditioned_summary") or {}
    return {
        "marker_labels": dict(Counter(marker_labels)),
        "classifier_predictions": dict(Counter(pred_labels)),
        "classifier_accuracy": classifier.get("accuracy"),
        "classifier_model_id": classifier.get("model_id"),
        "heuristic_proxy_by_marker": proxy_by_marker,
        "sqi_summary": heuristic.get("sqi_summary"),
        "timing": (validation or heuristic).get("timing"),
        "calibration_id": calibration.get("calibration_id"),
        "real_adaptation_actions_emitted": heuristic.get("real_adaptation_actions_emitted", 0),
        "interpretation": (
            "Heuristic output is a cognitive proxy summary. The learned classifier predicts "
            "dataset task labels from event-locked EEG epochs. Neither is mind reading."
        ),
        "closed_loop_allowed": False,
    }


def _markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Heuristic vs EEG Event Classifier",
        "",
        f"- Classifier model: `{result.get('classifier_model_id')}`",
        f"- Classifier accuracy on available labels: `{result.get('classifier_accuracy')}`",
        f"- Real adaptation actions emitted: `{result.get('real_adaptation_actions_emitted')}`",
        f"- Closed-loop allowed: `{result.get('closed_loop_allowed')}`",
        "",
        "## Marker Labels",
        "```json",
        json.dumps(result.get("marker_labels"), indent=2),
        "```",
        "",
        "## Classifier Predictions",
        "```json",
        json.dumps(result.get("classifier_predictions"), indent=2),
        "```",
        "",
        "## Interpretation",
        str(result.get("interpretation")),
        "",
        (
            "Event-locked EEG classifiers predict dataset task labels under controlled "
            "conditions; they should not be interpreted as general mind-reading models."
        ),
        "",
        (
            "The corridor is not a decoded mental image. It is an adaptive scaffold "
            "driven by experimental proxy metrics."
        ),
    ]
    return "\n".join(lines)


def _read(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(_resolve(path).read_text(encoding="utf-8"))


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


if __name__ == "__main__":
    main()
