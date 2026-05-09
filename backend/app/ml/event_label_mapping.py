from __future__ import annotations

from typing import Any

PHYSIONET_EEGBCI_RUN_CONTEXTS: dict[int, str] = {
    1: "baseline_eyes_open",
    2: "baseline_eyes_closed",
    3: "motor_execution_left_right",
    4: "motor_imagery_left_right",
    5: "motor_execution_hands_feet",
    6: "motor_imagery_hands_feet",
    7: "motor_execution_left_right",
    8: "motor_imagery_left_right",
    9: "motor_execution_hands_feet",
    10: "motor_imagery_hands_feet",
    11: "motor_execution_left_right",
    12: "motor_imagery_left_right",
    13: "motor_execution_hands_feet",
    14: "motor_imagery_hands_feet",
}

DIRECT_LABEL_MAP = {
    "rest": "REST",
    "baseline": "REST",
    "t0": "REST",
    "noisy": "NOISY_SEGMENT",
    "noisy_segment": "NOISY_SEGMENT",
    "recovery": "RECOVERY",
    "end": "END",
    "left": "LEFT_HAND",
    "left_hand": "LEFT_HAND",
    "left hand": "LEFT_HAND",
    "right": "RIGHT_HAND",
    "right_hand": "RIGHT_HAND",
    "right hand": "RIGHT_HAND",
    "both_hands": "BOTH_HANDS",
    "both hands": "BOTH_HANDS",
    "both_feet": "BOTH_FEET",
    "both feet": "BOTH_FEET",
    "left_hand_imagery": "LEFT_HAND_IMAGERY",
    "left hand imagery": "LEFT_HAND_IMAGERY",
    "right_hand_imagery": "RIGHT_HAND_IMAGERY",
    "right hand imagery": "RIGHT_HAND_IMAGERY",
}


def normalize_event_label(
    original_label: str,
    *,
    run_id: int | str | None = None,
    custom_mapping: dict[str, str] | None = None,
) -> dict[str, Any]:
    original = str(original_label).strip()
    key = _key(original)
    if custom_mapping and original in custom_mapping:
        return _result(original, custom_mapping[original], run_id)
    if custom_mapping and key in {_key(item) for item in custom_mapping}:
        for src, dst in custom_mapping.items():
            if _key(src) == key:
                return _result(original, dst, run_id)
    if key in DIRECT_LABEL_MAP:
        return _result(original, DIRECT_LABEL_MAP[key], run_id)
    parsed_run = _parse_run(run_id)
    context = PHYSIONET_EEGBCI_RUN_CONTEXTS.get(parsed_run, "unknown")
    if key == "t1":
        if context.endswith("left_right"):
            label = "LEFT_HAND_IMAGERY" if "imagery" in context else "LEFT_HAND"
        elif context.endswith("hands_feet"):
            label = "BOTH_HANDS_IMAGERY" if "imagery" in context else "BOTH_HANDS"
        else:
            label = "UNKNOWN"
        return _result(original, label, run_id)
    if key == "t2":
        if context.endswith("left_right"):
            label = "RIGHT_HAND_IMAGERY" if "imagery" in context else "RIGHT_HAND"
        elif context.endswith("hands_feet"):
            label = "BOTH_FEET_IMAGERY" if "imagery" in context else "BOTH_FEET"
        else:
            label = "UNKNOWN"
        return _result(original, label, run_id)
    return _result(original, "UNKNOWN", run_id)


def event_mapping_report(labels: list[str], *, run_id: int | str | None = None) -> dict[str, Any]:
    mapped = [normalize_event_label(label, run_id=run_id) for label in labels]
    return {
        "run_id": run_id,
        "task_context": PHYSIONET_EEGBCI_RUN_CONTEXTS.get(_parse_run(run_id), "unknown"),
        "labels": mapped,
        "unknown_count": sum(1 for item in mapped if item["event_label"] == "UNKNOWN"),
    }


def _result(original: str, normalized: str, run_id: int | str | None) -> dict[str, Any]:
    parsed_run = _parse_run(run_id)
    return {
        "original_label": original,
        "event_label": str(normalized).strip().upper(),
        "run_id": parsed_run,
        "task_context": PHYSIONET_EEGBCI_RUN_CONTEXTS.get(parsed_run, "unknown"),
    }


def _parse_run(run_id: int | str | None) -> int | None:
    if run_id is None or run_id == "":
        return None
    try:
        return int(str(run_id).replace("R", "").replace("run", ""))
    except ValueError:
        return None


def _key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")
