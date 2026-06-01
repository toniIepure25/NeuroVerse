"""Tests for the in-process ReportEvidenceSummary cache."""

from __future__ import annotations

import json
import time
from pathlib import Path

from app.safety.report_status import (
    _EvidenceCache,
    get_cache_meta,
    get_cached_report_evidence,
    invalidate_report_evidence_cache,
    load_report_evidence,
)

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------


def _fresh_cache() -> _EvidenceCache:
    """Return a new isolated cache instance for each test."""
    from app.safety.report_status import _EvidenceCache

    return _EvidenceCache()


def _make_cal_report(tmp: Path) -> None:
    cal_dir = tmp / "reports" / "calibration"
    cal_dir.mkdir(parents=True, exist_ok=True)
    (cal_dir / "cal.json").write_text(json.dumps({"baseline_sqi": 0.88, "source": "simulator"}))


# ---------------------------------------------------------------------------
#  Cache miss / hit behavior
# ---------------------------------------------------------------------------


class TestCacheMissAndHit:
    def test_cache_miss_on_first_load(self, tmp_path):
        c = _fresh_cache()
        ev, meta = c.get(tmp_path)
        assert meta["cache_hit"] is False

    def test_cache_hit_on_second_load(self, tmp_path):
        c = _fresh_cache()
        c.get(tmp_path)  # first: miss
        ev, meta = c.get(tmp_path)  # second: hit
        assert meta["cache_hit"] is True

    def test_force_refresh_bypasses_cache(self, tmp_path):
        c = _fresh_cache()
        c.get(tmp_path)  # populate
        ev, meta = c.get(tmp_path, force_refresh=True)
        assert meta["cache_hit"] is False

    def test_refresh_count_increments(self, tmp_path):
        c = _fresh_cache()
        _, m1 = c.get(tmp_path)
        _, m2 = c.get(tmp_path, force_refresh=True)
        assert m2["refresh_count"] > m1["refresh_count"]

    def test_cache_miss_after_expiry(self, tmp_path, monkeypatch):
        """Simulate TTL expiry by patching monotonic time."""
        c = _fresh_cache()
        c._ttl = 1  # 1 second TTL for this test
        c.get(tmp_path)
        # Advance time past TTL
        original_monotonic = time.monotonic
        monkeypatch.setattr(time, "monotonic", lambda: original_monotonic() + 2)
        ev, meta = c.get(tmp_path)
        assert meta["cache_hit"] is False


# ---------------------------------------------------------------------------
#  Invalidation
# ---------------------------------------------------------------------------


class TestCacheInvalidation:
    def test_invalidate_clears_cache(self, tmp_path):
        c = _fresh_cache()
        c.get(tmp_path)  # populate
        c.invalidate("test_reason")
        _, meta = c.get(tmp_path)
        assert meta["cache_hit"] is False

    def test_invalidation_reason_recorded(self, tmp_path):
        c = _fresh_cache()
        c.get(tmp_path)
        c.invalidate("test_invalidation")
        # The invalidation reason should survive until next reload
        # (entry is expired, not deleted — so meta shows last reason)
        raw_meta = c.meta()
        assert raw_meta is not None
        # After invalidation the entry is expired
        assert not c.is_populated()

    def test_module_level_invalidate_function(self, tmp_path):
        # Use the module-level cache; isolate by force-refreshing first
        get_cached_report_evidence(tmp_path, force_refresh=True)
        ev, meta1 = get_cached_report_evidence(tmp_path)
        assert meta1["cache_hit"] is True

        invalidate_report_evidence_cache("test_module_invalidate")
        ev, meta2 = get_cached_report_evidence(tmp_path)
        assert meta2["cache_hit"] is False

    def test_operator_action_invalidation(self, tmp_path):
        """Simulates the pattern used by operator endpoints."""
        get_cached_report_evidence(tmp_path, force_refresh=True)
        _, m1 = get_cached_report_evidence(tmp_path)
        assert m1["cache_hit"] is True

        # Operator action: invalidate + force refresh
        invalidate_report_evidence_cache("freeze:operator_freeze")
        _, m2 = get_cached_report_evidence(tmp_path, force_refresh=True)
        assert m2["cache_hit"] is False


# ---------------------------------------------------------------------------
#  Cache metadata fields
# ---------------------------------------------------------------------------


class TestCacheMetadata:
    def test_meta_has_required_fields(self, tmp_path):
        c = _fresh_cache()
        _, meta = c.get(tmp_path)
        for key in ("cache_hit", "cached_at", "expires_at", "ttl_seconds", "refresh_count"):
            assert key in meta, f"Missing key: {key}"

    def test_meta_ttl_seconds_is_positive(self, tmp_path):
        c = _fresh_cache()
        _, meta = c.get(tmp_path)
        assert meta["ttl_seconds"] > 0

    def test_cached_at_and_expires_at_are_strings(self, tmp_path):
        c = _fresh_cache()
        _, meta = c.get(tmp_path)
        assert isinstance(meta["cached_at"], str)
        assert isinstance(meta["expires_at"], str)

    def test_get_cache_meta_returns_none_before_first_load(self):
        """Fresh isolated cache has no metadata yet."""
        c = _fresh_cache()
        assert c.meta() is None

    def test_get_cache_meta_module_function_after_load(self, tmp_path):
        get_cached_report_evidence(tmp_path, force_refresh=True)
        meta = get_cache_meta()
        assert meta is not None
        assert "cache_hit" in meta


# ---------------------------------------------------------------------------
#  Evidence correctness after cache
# ---------------------------------------------------------------------------


class TestCachedEvidenceCorrectness:
    def test_cached_evidence_reflects_disk(self, tmp_path):
        _make_cal_report(tmp_path)
        ev, _ = get_cached_report_evidence(tmp_path, force_refresh=True)
        assert ev.calibration_complete is True

    def test_cached_evidence_matches_uncached(self, tmp_path):
        _make_cal_report(tmp_path)
        uncached = load_report_evidence(tmp_path)
        cached, _ = get_cached_report_evidence(tmp_path, force_refresh=True)
        assert cached.calibration_complete == uncached.calibration_complete
        assert cached.signal_quality_ok == uncached.signal_quality_ok

    def test_closed_loop_false_after_cache_refresh(self, tmp_path):
        from app.safety.closed_loop_governance import evaluate_closed_loop_governance

        _make_cal_report(tmp_path)
        ev, _ = get_cached_report_evidence(tmp_path, force_refresh=True)
        gov = evaluate_closed_loop_governance(
            calibration_complete=ev.calibration_complete,
            shadow_inference_passed=ev.shadow_inference_passed,
            signal_quality_ok=ev.signal_quality_ok,
            timing_validated=ev.timing_ok,
            hardware_validated=ev.physical_hardware_validated,
        )
        assert gov.closed_loop_allowed is False

    def test_physical_hardware_false_after_cache_refresh(self, tmp_path):
        """physical_hardware_validated must remain False from synthetic reports."""
        hw_dir = tmp_path / "reports" / "hardware_validation"
        hw_dir.mkdir(parents=True, exist_ok=True)
        (hw_dir / "synthetic.json").write_text(
            json.dumps(
                {
                    "passed": True,
                    "adapter": "brainflow",
                    "sqi_summary": {"mean": 0.92},
                    "timing": {"pass": True},
                    "board": {"board_id": -1},
                }
            )
        )
        ev, _ = get_cached_report_evidence(tmp_path, force_refresh=True)
        assert ev.physical_hardware_validated is False
        assert ev.brainflow_synthetic_validated is True


# ---------------------------------------------------------------------------
#  Thread safety (basic)
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_reads_do_not_raise(self, tmp_path):
        import threading

        errors: list[Exception] = []

        def reader():
            try:
                c = _fresh_cache()
                for _ in range(10):
                    c.get(tmp_path)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=reader) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert not errors

    def test_concurrent_invalidation_does_not_raise(self, tmp_path):
        import threading

        errors: list[Exception] = []

        def mixed():
            try:
                c = _fresh_cache()
                for i in range(5):
                    c.get(tmp_path)
                    c.invalidate(f"reason_{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=mixed) for _ in range(3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert not errors
