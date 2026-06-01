"""Structured safety reason codes for auditable safety decisions."""

from __future__ import annotations

from enum import Enum


class SafetyReasonCode(str, Enum):
    """Machine-readable reason codes for every safety decision."""

    LOW_SQI = "low_sqi"
    HIGH_JITTER = "high_jitter"
    MISSING_CALIBRATION = "missing_calibration"
    NO_VALIDATION_REPORT = "no_validation_report"
    VALIDATION_FAILED = "validation_failed"
    PHYSICAL_HARDWARE_UNVALIDATED = "physical_hardware_unvalidated"
    MODEL_INCOMPATIBLE = "model_incompatible"
    CONFIDENCE_LOW = "confidence_low"
    HIGH_UNCERTAINTY = "high_uncertainty"
    MISSING_MODALITY = "missing_modality"
    SENSOR_DROPOUT = "sensor_dropout"
    STATE_OSCILLATION = "state_oscillation"
    HIGH_STRESS_PROXY = "high_stress_proxy"
    FATIGUE_HIGH = "fatigue_high"
    EMERGENCY_STOP_ACTIVE = "emergency_stop_active"
    ADAPTATION_FROZEN = "adaptation_frozen"
    SHADOW_ONLY_MODE = "shadow_only_mode"
    CLOSED_LOOP_ENV_DISABLED = "closed_loop_env_disabled"
    REAL_EEG_CLOSED_LOOP_DISABLED = "real_eeg_closed_loop_disabled"
    USER_MANUAL_OVERRIDE = "user_manual_override"
    REPEATED_FALSE_COMMAND = "repeated_false_command"
    UNSUPPORTED_MODE = "unsupported_mode"
    NO_DATA = "no_data"
    NORMAL_OPERATION = "normal_operation"
    UNKNOWN = "unknown"


class SafetySeverity(str, Enum):
    """Severity levels for safety states and decisions."""

    INFO = "info"
    WARNING = "warning"
    BLOCKED = "blocked"
    EMERGENCY = "emergency"


class SafetyDecisionType(str, Enum):
    """Safety decision outcomes."""

    ALLOW = "allow"
    SOFT_ALLOW = "soft_allow"
    WAIT = "wait"
    BLOCK = "block"
    FREEZE = "freeze"
    EMERGENCY_STOP = "emergency_stop"
