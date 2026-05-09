from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

EstimatorType = Literal["heuristic", "learned"]
DataSource = Literal["live_synthetic", "recorded_replay", "dataset_replay", "idle"]


class RuntimeStatus:
    """In-memory runtime status for the current backend process."""

    def __init__(self) -> None:
        self._status: dict[str, Any] = {
            "current_session_id": None,
            "active_estimator": "heuristic",
            "active_model_id": None,
            "prediction_semantics": None,
            "current_data_source": "idle",
            "current_dataset_id": None,
            "current_replay_status": None,
            "last_safety_decision": None,
            "last_adaptation_action": None,
            "emergency_stop_active": False,
            "adaptation_frozen": False,
            "freeze_reason": None,
            "hardware_closed_loop_enabled": False,
            "hardware_validation_state": "UNKNOWN",
            "latest_hardware_validation_report_id": None,
        }

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self._status)

    def set_active_model(
        self,
        estimator: EstimatorType,
        model_id: str | None = None,
        prediction_semantics: str | None = None,
    ) -> None:
        self._status["active_estimator"] = estimator
        self._status["active_model_id"] = model_id
        self._status["prediction_semantics"] = prediction_semantics

    def start_session(
        self,
        session_id: str,
        estimator: EstimatorType,
        model_id: str | None,
        prediction_semantics: str | None,
        data_source: DataSource = "live_synthetic",
    ) -> None:
        self._status.update(
            {
                "current_session_id": session_id,
                "active_estimator": estimator,
                "active_model_id": model_id,
                "prediction_semantics": prediction_semantics,
                "current_data_source": data_source,
                "current_dataset_id": None,
                "current_replay_status": None,
                "last_safety_decision": None,
                "last_adaptation_action": None,
                "emergency_stop_active": False,
                "adaptation_frozen": False,
                "freeze_reason": None,
            }
        )

    def stop_session(self) -> None:
        self._status.update(
            {
                "current_session_id": None,
                "current_data_source": "idle",
                "current_replay_status": None,
                "emergency_stop_active": False,
                "adaptation_frozen": False,
                "freeze_reason": None,
            }
        )

    def start_dataset_replay(
        self,
        session_id: str,
        dataset_id: str,
        model_id: str | None,
    ) -> None:
        self._status.update(
            {
                "current_session_id": session_id,
                "current_data_source": "dataset_replay",
                "current_dataset_id": dataset_id,
                "current_replay_status": "running",
                "active_model_id": model_id,
                "active_estimator": "learned" if model_id else "heuristic",
            }
        )

    def complete_replay(self) -> None:
        self._status["current_replay_status"] = "completed"

    def set_last_safety(self, safety: dict[str, Any]) -> None:
        self._status["last_safety_decision"] = safety

    def set_last_action(self, action: dict[str, Any]) -> None:
        self._status["last_adaptation_action"] = action

    def emergency_stop(self, reason: str = "manual emergency stop") -> None:
        self._status["emergency_stop_active"] = True
        self._status["adaptation_frozen"] = True
        self._status["freeze_reason"] = reason

    def freeze(self, reason: str = "manual freeze") -> None:
        self._status["adaptation_frozen"] = True
        self._status["freeze_reason"] = reason

    def unfreeze(self) -> tuple[bool, str | None]:
        if self._status.get("emergency_stop_active"):
            return False, "Emergency stop is active; start a new session to clear it."
        last_safety = self._status.get("last_safety_decision") or {}
        decision = str(last_safety.get("decision", "")).lower()
        if decision in {"block", "blocked"}:
            return False, "Last safety decision blocks adaptation."
        self._status["adaptation_frozen"] = False
        self._status["freeze_reason"] = None
        return True, None

    def is_adaptation_frozen(self) -> bool:
        return bool(self._status.get("adaptation_frozen"))

    def set_hardware_validation_state(
        self,
        state: str,
        report_id: str | None = None,
    ) -> None:
        self._status["hardware_validation_state"] = state
        if report_id is not None:
            self._status["latest_hardware_validation_report_id"] = report_id


runtime_status = RuntimeStatus()
