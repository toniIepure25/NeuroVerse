"""Authoritative closed-loop lock governance.

A single function determines whether closed-loop adaptation is allowed.
The default is LOCKED. This module does not enable closed-loop; it documents
why it is locked and what would be required to unlock it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.safety.reason_codes import SafetyReasonCode


@dataclass
class ClosedLoopGovernanceResult:
    """Result of the closed-loop governance check."""

    closed_loop_allowed: bool = False
    lock_reasons: list[str] = field(default_factory=list)
    lock_reason_codes: list[str] = field(default_factory=list)
    required_unlock_conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "closed_loop_allowed": self.closed_loop_allowed,
            "lock_reasons": self.lock_reasons,
            "lock_reason_codes": self.lock_reason_codes,
            "required_unlock_conditions": self.required_unlock_conditions,
        }


def evaluate_closed_loop_governance(
    *,
    environment_flag: bool = False,
    hardware_validated: bool = False,
    signal_quality_ok: bool = False,
    timing_validated: bool = False,
    calibration_complete: bool = False,
    shadow_inference_passed: bool = False,
    emergency_stop_active: bool = False,
    adaptation_frozen: bool = False,
    mode: str = "simulated",
    model_compatible: bool = True,
    operator_override: bool = False,
) -> ClosedLoopGovernanceResult:
    """Evaluate whether closed-loop adaptation is allowed.

    For this phase, the default is LOCKED. Physical hardware closed-loop
    remains locked. Only simulated/demo adaptation may proceed if already
    enabled by existing configuration.
    """
    result = ClosedLoopGovernanceResult()

    # Environment flag is the master switch
    if not environment_flag:
        result.lock_reasons.append("Real EEG closed-loop adaptation is disabled by default.")
        result.lock_reason_codes.append(SafetyReasonCode.CLOSED_LOOP_ENV_DISABLED.value)
        result.required_unlock_conditions.append(
            "Set NEUROVERSE_HARDWARE_CLOSED_LOOP_ENABLED=true in environment."
        )

    # Emergency stop overrides everything
    if emergency_stop_active:
        result.lock_reasons.append("Emergency stop is active.")
        result.lock_reason_codes.append(SafetyReasonCode.EMERGENCY_STOP_ACTIVE.value)
        result.required_unlock_conditions.append("Clear emergency stop and start a new session.")

    # Adaptation frozen
    if adaptation_frozen:
        result.lock_reasons.append("Adaptation is currently frozen.")
        result.lock_reason_codes.append(SafetyReasonCode.ADAPTATION_FROZEN.value)
        result.required_unlock_conditions.append("Unfreeze adaptation.")

    # Physical hardware must be validated
    if mode in {"physical_hardware", "brainflow_physical"} and not hardware_validated:
        result.lock_reasons.append("Physical hardware has not been validated.")
        result.lock_reason_codes.append(SafetyReasonCode.PHYSICAL_HARDWARE_UNVALIDATED.value)
        result.required_unlock_conditions.append(
            "Complete physical hardware validation with passing results."
        )

    # Real EEG modes always locked in this phase
    if mode in {"physical_hardware", "brainflow_physical", "lsl_live"}:
        result.lock_reasons.append("Real EEG closed-loop is disabled for safety in this phase.")
        result.lock_reason_codes.append(SafetyReasonCode.REAL_EEG_CLOSED_LOOP_DISABLED.value)
        result.required_unlock_conditions.append(
            "Future phase: safety review, operator confirmation, validated hardware."
        )

    # Signal quality
    if not signal_quality_ok:
        result.lock_reasons.append("Signal quality is insufficient.")
        result.lock_reason_codes.append(SafetyReasonCode.LOW_SQI.value)
        result.required_unlock_conditions.append(
            "Achieve sustained signal quality above safety thresholds."
        )

    # Calibration required
    if not calibration_complete:
        result.lock_reasons.append("Calibration has not been completed.")
        result.lock_reason_codes.append(SafetyReasonCode.MISSING_CALIBRATION.value)
        result.required_unlock_conditions.append("Complete calibration procedure.")

    # Shadow inference must pass
    if not shadow_inference_passed:
        result.lock_reasons.append("Shadow inference has not been completed.")
        result.lock_reason_codes.append(SafetyReasonCode.SHADOW_ONLY_MODE.value)
        result.required_unlock_conditions.append(
            "Complete shadow inference with acceptable results."
        )

    # Model compatibility
    if not model_compatible:
        result.lock_reasons.append("Active model is not compatible with closed-loop.")
        result.lock_reason_codes.append(SafetyReasonCode.MODEL_INCOMPATIBLE.value)
        result.required_unlock_conditions.append(
            "Activate a model validated for closed-loop operation."
        )

    # Timing validation
    if not timing_validated:
        result.lock_reasons.append("Timing validation has not been completed.")
        result.lock_reason_codes.append(SafetyReasonCode.HIGH_JITTER.value)
        result.required_unlock_conditions.append(
            "Complete timing validation with acceptable jitter and drift."
        )

    # Only allow if zero lock reasons
    result.closed_loop_allowed = len(result.lock_reasons) == 0

    return result
