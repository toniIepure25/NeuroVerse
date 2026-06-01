"""Read-only utility that extracts safety-relevant evidence from disk reports.

Aggregates evidence across the N most recent reports per type so that a
single failed report does not hide older valid evidence.

This module never enables closed-loop; it only reads artifacts and returns
structured evidence that the governance layer can reason over.

All booleans default to False (no evidence found → not validated).
Physical hardware is only flagged when a report explicitly records
physical_device_detected=True with a passing validation.
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent.parent.parent  # repo root

# SQI safety threshold — mirrors rules.py so we stay consistent
_SQI_THRESHOLD = 0.5

# Maximum number of recent files to inspect per report type
_DEFAULT_MAX_REPORTS = 10


# ---------------------------------------------------------------------------
#  Structured evidence summary
# ---------------------------------------------------------------------------


@dataclass
class ReportEvidenceSummary:
    """Safety-relevant evidence derived from recent disk reports.

    Fields ending in *_valid_* come from the best/latest passing report.
    Fields ending in *latest_* come from the most recently modified file
    regardless of whether it passed.

    This distinction matters when e.g. a failed LSL report is the newest
    file but an older passing BrainFlow report still contains valid evidence.
    """

    # ----- Signal quality -----
    signal_quality_ok: bool = False
    signal_quality_source: str = "unknown"  # hardware_validation | calibration | shadow
    signal_quality_note: str = ""
    latest_sqi_mean: float | None = None  # from latest hw validation (may be None if failed)
    latest_sqi_min: float | None = None
    best_sqi_mean: float | None = None  # best across all valid reports
    best_sqi_min: float | None = None

    # ----- Timing -----
    timing_ok: bool = False
    latest_jitter_p95_ms: float | None = None
    latest_drift_percent: float | None = None
    best_jitter_p95_ms: float | None = None  # lowest jitter seen in any valid report

    # ----- Hardware validation -----
    validation_report_present: bool = False
    validation_passed: bool = False
    latest_validation_report_path: str | None = None
    latest_valid_validation_report_path: str | None = None
    latest_failed_validation_report_path: str | None = None
    adapter: str | None = None

    # ----- Synthetic vs physical -----
    brainflow_synthetic_validated: bool = False
    lsl_synthetic_validated: bool = False
    lsl_replay_validated: bool = False
    physical_hardware_validated: bool = False

    # ----- Calibration -----
    calibration_complete: bool = False
    latest_calibration_report_path: str | None = None
    calibration_source: str | None = None
    calibration_sqi: float | None = None

    # ----- Shadow inference -----
    shadow_inference_passed: bool = False
    latest_shadow_report_path: str | None = None
    shadow_real_actions_emitted: int = 0
    shadow_prediction_count: int = 0

    # ----- Physical EEG trial -----
    latest_physical_trial_report_path: str | None = None
    trial_physical_device_detected: bool = False
    trial_synthetic_mode: bool = True

    # ----- LSL live validation -----
    lsl_live_validation_passed: bool = False
    lsl_validation_jitter_p95_ms: float | None = None

    # ----- Provenance / audit -----
    safety_audit_report_path: str | None = None
    evidence_sources: list[str] = field(default_factory=list)
    evidence_warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal_quality_ok": self.signal_quality_ok,
            "signal_quality_source": self.signal_quality_source,
            "signal_quality_note": self.signal_quality_note,
            "latest_sqi_mean": self.latest_sqi_mean,
            "latest_sqi_min": self.latest_sqi_min,
            "best_sqi_mean": self.best_sqi_mean,
            "best_sqi_min": self.best_sqi_min,
            "timing_ok": self.timing_ok,
            "latest_jitter_p95_ms": self.latest_jitter_p95_ms,
            "latest_drift_percent": self.latest_drift_percent,
            "best_jitter_p95_ms": self.best_jitter_p95_ms,
            "validation_report_present": self.validation_report_present,
            "validation_passed": self.validation_passed,
            "latest_validation_report_path": self.latest_validation_report_path,
            "latest_valid_validation_report_path": self.latest_valid_validation_report_path,
            "latest_failed_validation_report_path": self.latest_failed_validation_report_path,
            "adapter": self.adapter,
            "brainflow_synthetic_validated": self.brainflow_synthetic_validated,
            "lsl_synthetic_validated": self.lsl_synthetic_validated,
            "lsl_replay_validated": self.lsl_replay_validated,
            "physical_hardware_validated": self.physical_hardware_validated,
            "calibration_complete": self.calibration_complete,
            "latest_calibration_report_path": self.latest_calibration_report_path,
            "calibration_source": self.calibration_source,
            "calibration_sqi": self.calibration_sqi,
            "shadow_inference_passed": self.shadow_inference_passed,
            "latest_shadow_report_path": self.latest_shadow_report_path,
            "shadow_real_actions_emitted": self.shadow_real_actions_emitted,
            "shadow_prediction_count": self.shadow_prediction_count,
            "latest_physical_trial_report_path": self.latest_physical_trial_report_path,
            "trial_physical_device_detected": self.trial_physical_device_detected,
            "trial_synthetic_mode": self.trial_synthetic_mode,
            "lsl_live_validation_passed": self.lsl_live_validation_passed,
            "lsl_validation_jitter_p95_ms": self.lsl_validation_jitter_p95_ms,
            "safety_audit_report_path": self.safety_audit_report_path,
            "evidence_sources": self.evidence_sources,
            "evidence_warnings": self.evidence_warnings,
        }


# ---------------------------------------------------------------------------
#  File scanning helpers
# ---------------------------------------------------------------------------


def _sorted_files(
    directory: Path, pattern: str = "*.json", n: int = _DEFAULT_MAX_REPORTS
) -> list[Path]:
    """Return up to n most-recently-modified files matching pattern in directory."""
    try:
        if not directory.exists():
            return []
        files = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        return files[:n]
    except Exception:
        return []


def _sorted_nested_files(
    base: Path, glob_pattern: str, n: int = _DEFAULT_MAX_REPORTS
) -> list[Path]:
    """Return up to n most-recently-modified files matching a nested glob."""
    try:
        if not base.exists():
            return []
        files = sorted(base.glob(glob_pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        return files[:n]
    except Exception:
        return []


def _read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


# ---------------------------------------------------------------------------
#  Adapter classification
# ---------------------------------------------------------------------------


def _is_synthetic_adapter(adapter: str | None) -> bool:
    """Return True for adapters that use simulated/synthetic hardware."""
    if not adapter:
        return True
    a = str(adapter).lower()
    return (
        a
        in {
            "simulator",
            "brainflow_synthetic",
            "lsl_synthetic",
            "csv_replay",
            "eeg_lsl_replay",
            "dataset_replay",
        }
        or "synthetic" in a
    )


def _classify_hw_adapter(adapter: str | None, data: dict) -> str:
    """Return one of: brainflow_synthetic|brainflow_physical|lsl_synthetic|simulator|other."""
    if not adapter:
        return "other"
    a = adapter.lower()
    if "brainflow" in a:
        board = data.get("board")
        board_id = board.get("board_id") if isinstance(board, dict) else None
        if board_id == -1 or _is_synthetic_adapter(adapter):
            return "brainflow_synthetic"
        return "brainflow_physical"
    if a in {"lsl", "lsl_synthetic_eeg", "eeg_lsl_replay"}:
        return "lsl_synthetic"
    if a == "simulator":
        return "simulator"
    return "other"


# ---------------------------------------------------------------------------
#  Individual aggregating readers
# ---------------------------------------------------------------------------


def _update_best_sqi(
    ev: ReportEvidenceSummary, sqi_mean: float | None, sqi_min: float | None
) -> None:
    if sqi_mean is not None:
        if ev.best_sqi_mean is None or sqi_mean > ev.best_sqi_mean:
            ev.best_sqi_mean = sqi_mean
    if sqi_min is not None:
        if ev.best_sqi_min is None or sqi_min > ev.best_sqi_min:
            ev.best_sqi_min = sqi_min


def _update_best_jitter(ev: ReportEvidenceSummary, jitter: float | None) -> None:
    if jitter is not None:
        if ev.best_jitter_p95_ms is None or jitter < ev.best_jitter_p95_ms:
            ev.best_jitter_p95_ms = jitter


def _aggregate_hardware_validation(root: Path, ev: ReportEvidenceSummary, max_reports: int) -> None:
    hw_dir = root / "reports" / "hardware_validation"
    files = _sorted_files(hw_dir, "*.json", max_reports)
    if not files:
        return

    ev.validation_report_present = True

    # Always expose the latest file regardless of pass/fail
    latest_path = files[0]
    latest_data = _read_json(latest_path)
    if latest_data is not None:
        ev.latest_validation_report_path = str(latest_path)
        ev.adapter = latest_data.get("adapter")
        # Latest SQI (may be None if failed/no stream)
        sqi = latest_data.get("sqi_summary") or {}
        ev.latest_sqi_mean = sqi.get("mean")
        ev.latest_sqi_min = sqi.get("min")
        timing = latest_data.get("timing") or {}
        ev.latest_jitter_p95_ms = timing.get("jitter_ms_p95")
        ev.latest_drift_percent = timing.get("drift_percent")

    # Scan all N reports to aggregate best evidence
    for path in files:
        data = _read_json(path)
        if data is None:
            continue

        passed = bool(data.get("passed", False))
        adapter = data.get("adapter")
        kind = _classify_hw_adapter(adapter, data)

        # Track latest valid / latest failed
        if passed:
            if ev.latest_valid_validation_report_path is None:
                ev.latest_valid_validation_report_path = str(path)
                ev.validation_passed = True
        else:
            if ev.latest_failed_validation_report_path is None:
                ev.latest_failed_validation_report_path = str(path)

        # SQI and timing from passing reports
        if passed:
            sqi = data.get("sqi_summary") or {}
            _update_best_sqi(ev, sqi.get("mean"), sqi.get("min"))
            timing = data.get("timing") or {}
            if bool(timing.get("pass", False)):
                ev.timing_ok = True
                _update_best_jitter(ev, timing.get("jitter_ms_p95"))

            # Classify adapter
            if kind == "brainflow_synthetic":
                ev.brainflow_synthetic_validated = True
                ev.evidence_sources.append(f"brainflow_synthetic:{path.name}")
            elif kind == "brainflow_physical":
                ev.physical_hardware_validated = True
                ev.evidence_sources.append(f"brainflow_physical:{path.name}")
            elif kind == "lsl_synthetic":
                ev.lsl_synthetic_validated = True
                ev.evidence_sources.append(f"lsl_synthetic:{path.name}")
            elif kind == "simulator":
                ev.evidence_sources.append(f"simulator:{path.name}")

    # Signal quality from hw validation
    if ev.best_sqi_mean is not None and ev.best_sqi_mean >= _SQI_THRESHOLD:
        ev.signal_quality_ok = True
        ev.signal_quality_source = "hardware_validation"
        ev.signal_quality_note = f"Best SQI {ev.best_sqi_mean:.3f} from hw validation reports."

    # Warn if latest failed but valid evidence exists
    if (
        ev.latest_failed_validation_report_path is not None
        and ev.latest_valid_validation_report_path is not None
    ):
        latest_is_failed = (
            ev.latest_validation_report_path == ev.latest_failed_validation_report_path
        )
        if latest_is_failed:
            ev.evidence_warnings.append(
                "Latest hardware validation report failed; using older valid report for evidence. "
                f"Failed: {Path(ev.latest_failed_validation_report_path).name}"
            )


def _aggregate_calibration(root: Path, ev: ReportEvidenceSummary, max_reports: int) -> None:
    cal_dir = root / "reports" / "calibration"
    files = _sorted_files(cal_dir, "*.json", max_reports)
    if not files:
        return

    for path in files:
        data = _read_json(path)
        if data is None:
            continue

        baseline_sqi = data.get("baseline_sqi")
        if baseline_sqi is None:
            continue

        # Use first (most recent) valid calibration report
        if ev.latest_calibration_report_path is None:
            ev.latest_calibration_report_path = str(path)
            ev.calibration_source = data.get("source")
            ev.calibration_sqi = baseline_sqi
            ev.calibration_complete = True
            ev.evidence_sources.append(f"calibration:{path.name}")

        # Signal quality from calibration if hw validation didn't provide it
        if not ev.signal_quality_ok and baseline_sqi >= _SQI_THRESHOLD:
            ev.signal_quality_ok = True
            ev.signal_quality_source = "calibration"
            ev.signal_quality_note = (
                f"SQI {baseline_sqi:.3f} from calibration baseline (no hw validation SQI)."
            )

        # Always update best SQI if better
        _update_best_sqi(ev, baseline_sqi, None)

        # Only need the most recent valid one
        break


def _aggregate_shadow(root: Path, ev: ReportEvidenceSummary, max_reports: int) -> None:
    shadow_dir = root / "reports" / "shadow"
    files = _sorted_files(shadow_dir, "*.json", max_reports)
    if not files:
        return

    for path in files:
        data = _read_json(path)
        if data is None:
            continue

        emitted = data.get("real_adaptation_actions_emitted", 0)
        if emitted == 0:
            # First (most recent) shadow with zero real actions
            ev.latest_shadow_report_path = str(path)
            ev.shadow_inference_passed = True
            ev.shadow_real_actions_emitted = 0
            ev.shadow_prediction_count = len(
                data.get("predicted_states") or data.get("predictions") or []
            )
            ev.evidence_sources.append(f"shadow:{path.name}")
            break
    else:
        # All shadow reports had emitted actions — take the latest metadata
        if files:
            data = _read_json(files[0])
            if data is not None:
                ev.latest_shadow_report_path = str(files[0])
                ev.shadow_real_actions_emitted = int(data.get("real_adaptation_actions_emitted", 0))
                ev.evidence_warnings.append(
                    "All recent shadow reports emitted real adaptation actions (expected 0)."
                )


def _aggregate_physical_trial(root: Path, ev: ReportEvidenceSummary, max_reports: int) -> None:
    trial_dir = root / "reports" / "hardware_trials"
    files = _sorted_nested_files(trial_dir, "*/physical_eeg_trial_summary.json", max_reports)
    if not files:
        return

    # Latest trial for metadata
    latest_data = _read_json(files[0])
    if latest_data is not None:
        ev.latest_physical_trial_report_path = str(files[0])
        ev.trial_physical_device_detected = bool(latest_data.get("physical_device_detected", False))
        ev.trial_synthetic_mode = bool(latest_data.get("synthetic_mode", True))

    # Scan for any real-device trial that passed
    for path in files:
        data = _read_json(path)
        if data is None:
            continue
        physical = bool(data.get("physical_device_detected", False))
        synthetic = bool(data.get("synthetic_mode", True))
        if physical and not synthetic:
            validation = data.get("validation") or {}
            if bool(validation.get("passed", False)):
                ev.physical_hardware_validated = True
                ev.evidence_sources.append(f"physical_trial:{path.parent.name}")
                break


def _aggregate_lsl_live_validation(root: Path, ev: ReportEvidenceSummary, max_reports: int) -> None:
    lsl_dir = root / "reports" / "lsl_live_validation"
    files = _sorted_nested_files(lsl_dir, "*/live_validation_summary.json", max_reports)

    for path in files:
        data = _read_json(path)
        if data is None:
            continue

        validations = data.get("validations") or []
        if validations:
            if any(v.get("passed") for v in validations):
                ev.lsl_live_validation_passed = True
                ev.lsl_replay_validated = True
                ev.evidence_sources.append(f"lsl_live:{path.parent.name}")
                for v in validations:
                    timing = v.get("timing") or {}
                    _update_best_jitter(ev, timing.get("jitter_ms_p95"))
                    if ev.lsl_validation_jitter_p95_ms is None:
                        ev.lsl_validation_jitter_p95_ms = timing.get("jitter_ms_p95")
                break
        elif bool(data.get("passed", False)):
            ev.lsl_live_validation_passed = True
            ev.lsl_replay_validated = True
            ev.evidence_sources.append(f"lsl_live:{path.parent.name}")
            break


def _read_safety_audit(root: Path, ev: ReportEvidenceSummary) -> None:
    audit_dir = root / "reports" / "safety_audit"
    try:
        if not audit_dir.exists():
            return
        files = sorted(
            audit_dir.glob("*/safety_audit_summary.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if files:
            ev.safety_audit_report_path = str(files[0])
    except Exception:
        pass


# ---------------------------------------------------------------------------
#  Startup state inference helper
# ---------------------------------------------------------------------------


def infer_startup_safety_state(ev: ReportEvidenceSummary) -> str:
    """Map aggregated evidence to the most informative startup safety state.

    Never allows real EEG closed-loop. Only sets informative/audit state.
    """
    # Shadow + calibration: system has been through the validation pipeline
    if ev.shadow_inference_passed and ev.calibration_complete:
        if ev.physical_hardware_validated:
            return "SHADOW_READY"  # Physical device validated and shadow done
        return "SHADOW_READY"  # Synthetic path: SHADOW_READY but CL still locked

    # Calibration done but not shadow
    if ev.calibration_complete:
        return "CALIBRATION_REQUIRED"

    # Validation exists but no calibration
    if ev.validation_passed:
        return "VALIDATION_PASSED"

    # Hardware report present but failed
    if ev.validation_report_present and not ev.validation_passed:
        return "VALIDATION_FAILED"

    # Nothing at all
    return "CLOSED_LOOP_LOCKED"


# ---------------------------------------------------------------------------
#  Public API
# ---------------------------------------------------------------------------


def load_report_evidence(
    root: Path | None = None,
    max_reports_per_type: int = _DEFAULT_MAX_REPORTS,
    *,
    prefer_valid: bool = True,
) -> ReportEvidenceSummary:
    """Load and aggregate safety-relevant evidence from recent disk reports.

    Args:
        root: Repository root. Defaults to the repo root derived from this file.
        max_reports_per_type: Maximum number of recent files to inspect per type.
        prefer_valid: If True, older valid evidence survives a newer failed report.
                      Always True — argument kept for API compatibility.

    Returns:
        ReportEvidenceSummary with aggregated evidence across recent reports.
        All booleans default to False until positive evidence is found.
        Physical hardware is never flagged from synthetic-only reports.
    """
    if root is None:
        root = _ROOT
    ev = ReportEvidenceSummary()
    _aggregate_hardware_validation(root, ev, max_reports_per_type)
    _aggregate_calibration(root, ev, max_reports_per_type)
    _aggregate_shadow(root, ev, max_reports_per_type)
    _aggregate_physical_trial(root, ev, max_reports_per_type)
    _aggregate_lsl_live_validation(root, ev, max_reports_per_type)
    _read_safety_audit(root, ev)

    # Deduplicate sources and warnings
    ev.evidence_sources = list(dict.fromkeys(ev.evidence_sources))
    ev.evidence_warnings = list(dict.fromkeys(ev.evidence_warnings))

    return ev


# ---------------------------------------------------------------------------
#  In-process evidence cache
# ---------------------------------------------------------------------------

_CACHE_DEFAULT_TTL_SECONDS = 30


@dataclass
class _CacheEntry:
    evidence: ReportEvidenceSummary
    cached_at: float  # monotonic timestamp
    cached_at_iso: str  # UTC ISO string for display
    expires_at_iso: str  # UTC ISO string for display
    ttl_seconds: int
    refresh_count: int = 0
    invalidation_reason: str | None = None

    def is_expired(self) -> bool:
        return time.monotonic() > self.cached_at + self.ttl_seconds

    def to_meta(self, *, cache_hit: bool) -> dict[str, Any]:
        return {
            "cache_hit": cache_hit,
            "cached_at": self.cached_at_iso,
            "expires_at": self.expires_at_iso,
            "ttl_seconds": self.ttl_seconds,
            "refresh_count": self.refresh_count,
            "invalidation_reason": self.invalidation_reason,
        }


class _EvidenceCache:
    """Simple singleton in-process cache for ReportEvidenceSummary.

    Thread-safe for FastAPI's async context: lock is acquired only for
    short synchronous dict operations, never across an await boundary.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entry: _CacheEntry | None = None
        self._ttl: int = _CACHE_DEFAULT_TTL_SECONDS

    def get(
        self,
        root: Path | None = None,
        *,
        force_refresh: bool = False,
        max_reports_per_type: int = _DEFAULT_MAX_REPORTS,
    ) -> tuple[ReportEvidenceSummary, dict[str, Any]]:
        """Return (evidence, cache_meta). Loads from disk only when needed."""
        with self._lock:
            if not force_refresh and self._entry is not None and not self._entry.is_expired():
                meta = self._entry.to_meta(cache_hit=True)
                return self._entry.evidence, meta

        # Load outside lock — disk I/O should not hold the lock
        ev = load_report_evidence(root, max_reports_per_type)
        now_mono = time.monotonic()
        now_dt = datetime.now(timezone.utc)
        expires_dt = datetime.fromtimestamp(
            now_mono + self._ttl - now_mono + now_dt.timestamp(),
            tz=timezone.utc,
        )

        with self._lock:
            prev_count = self._entry.refresh_count if self._entry is not None else 0
            self._entry = _CacheEntry(
                evidence=ev,
                cached_at=now_mono,
                cached_at_iso=now_dt.isoformat(),
                expires_at_iso=expires_dt.isoformat(),
                ttl_seconds=self._ttl,
                refresh_count=prev_count + 1,
                invalidation_reason=None,
            )
            meta = self._entry.to_meta(cache_hit=False)
        return ev, meta

    def invalidate(self, reason: str = "manual invalidation") -> None:
        """Expire the cache so the next get() reloads from disk."""
        with self._lock:
            if self._entry is not None:
                # Force expiry by pushing cached_at far into the past
                self._entry.cached_at = 0.0
                self._entry.invalidation_reason = reason

    def is_populated(self) -> bool:
        with self._lock:
            return self._entry is not None and not self._entry.is_expired()

    def meta(self) -> dict[str, Any] | None:
        """Return current cache metadata without loading."""
        with self._lock:
            if self._entry is None:
                return None
            return self._entry.to_meta(cache_hit=not self._entry.is_expired())


# Module-level singleton
_cache = _EvidenceCache()


def get_cached_report_evidence(
    root: Path | None = None,
    *,
    force_refresh: bool = False,
    max_reports_per_type: int = _DEFAULT_MAX_REPORTS,
) -> tuple[ReportEvidenceSummary, dict[str, Any]]:
    """Return (evidence, cache_meta), using cached data when valid.

    Args:
        root: Repository root. None uses the default.
        force_refresh: If True, bypass the cache and reload from disk.
        max_reports_per_type: Passed through to load_report_evidence on miss.

    Returns:
        Tuple of (ReportEvidenceSummary, cache_metadata_dict).
        cache_metadata_dict contains: cache_hit, cached_at, expires_at,
        ttl_seconds, refresh_count, invalidation_reason.
    """
    return _cache.get(root, force_refresh=force_refresh, max_reports_per_type=max_reports_per_type)


def invalidate_report_evidence_cache(reason: str = "manual invalidation") -> None:
    """Expire the evidence cache so the next get_cached_report_evidence() reloads."""
    _cache.invalidate(reason)


def get_cache_meta() -> dict[str, Any] | None:
    """Return current cache metadata without loading evidence."""
    return _cache.meta()
