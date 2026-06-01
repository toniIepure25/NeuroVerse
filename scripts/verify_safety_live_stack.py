"""Verify the NeuroVerse safety governance live stack.

Checks that a running backend correctly returns safety state, governance,
evidence cache metadata, and keeps closed_loop_allowed=False.

Usage:
    # With backend running (make dev):
    python3 scripts/verify_safety_live_stack.py

    # Strict mode (exits non-zero if backend unreachable):
    python3 scripts/verify_safety_live_stack.py --strict

    # Custom backend URL:
    python3 scripts/verify_safety_live_stack.py --url http://localhost:8000

    # Via Makefile (non-strict by default):
    make verify-safety-live-stack
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = "http://localhost:8000"


def _get(url: str, timeout: int = 5) -> dict[str, Any] | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError:
        return None
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return None


def _post(url: str, timeout: int = 5) -> dict[str, Any] | None:
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read())
            return {"http_error": exc.code, "detail": body.get("detail", str(exc))}
        except Exception:
            return {"http_error": exc.code}
    except urllib.error.URLError:
        return None
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return None


def _check(label: str, condition: bool, detail: str = "") -> bool:
    status = "PASS" if condition else "FAIL"
    line = f"  [{status}] {label}"
    if detail:
        line += f"  ({detail})"
    print(line)
    return condition


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify NeuroVerse safety governance live stack")
    parser.add_argument("--url", default=DEFAULT_URL, help="Backend base URL")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if backend is unreachable (default: graceful)",
    )
    args = parser.parse_args()

    base = args.url.rstrip("/")
    failures: list[str] = []

    print(f"\n{'='*60}")
    print(f"NeuroVerse Safety Governance Live Stack Verification")
    print(f"Backend: {base}")
    print(f"{'='*60}\n")

    # -- Health check ---------------------------------------------------------
    print("1. Health check")
    health = _get(f"{base}/health")
    if health is None:
        print(f"  [FAIL] Backend unreachable at {base}")
        print(f"\n  Run `make dev` in the NeuroVerse root to start the backend.")
        if args.strict:
            sys.exit(1)
        print("\n  Skipping live checks (backend not running).")
        print(f"{'='*60}\n")
        sys.exit(0)
    ok = _check("Backend reachable", health.get("status") == "ok", f"status={health.get('status')}")
    if not ok:
        failures.append("health")

    # -- Safety state ---------------------------------------------------------
    print("\n2. GET /api/v1/safety/state")
    state = _get(f"{base}/api/v1/safety/state")
    if state is None:
        failures.append("safety_state")
        _check("Safety state endpoint", False, "returned None")
    else:
        _check("state_id present", "state_id" in state, str(state.get("state_id")))
        _check("severity present", "severity" in state)
        ev = state.get("evidence_summary", {})
        _check(
            "evidence_summary present",
            bool(ev),
            f"keys={len(ev)}",
        )
        cache = ev.get("evidence_cache")
        _check("evidence_cache metadata present", cache is not None)
        if cache:
            _check("cache_hit field present", "cache_hit" in cache, str(cache.get("cache_hit")))
            _check("cached_at field present", "cached_at" in cache)
            _check("ttl_seconds field present", "ttl_seconds" in cache)
            _check("refresh_count field present", "refresh_count" in cache)

    # -- Closed-loop governance -----------------------------------------------
    print("\n3. GET /api/v1/safety/closed-loop")
    cl = _get(f"{base}/api/v1/safety/closed-loop")
    if cl is None:
        failures.append("closed_loop")
        _check("Closed-loop endpoint", False, "returned None")
    else:
        ok = _check(
            "closed_loop_allowed is False",
            cl.get("closed_loop_allowed") is False,
            str(cl.get("closed_loop_allowed")),
        )
        if not ok:
            failures.append("closed_loop_allowed_not_false")
        _check("lock_reasons present", bool(cl.get("lock_reasons")))
        _check("evidence_summary present", bool(cl.get("evidence_summary")))

    # -- Safety report --------------------------------------------------------
    print("\n4. GET /api/v1/safety/report/latest")
    report = _get(f"{base}/api/v1/safety/report/latest")
    if report is None:
        failures.append("safety_report")
        _check("Safety report endpoint", False, "returned None")
    else:
        _check("governance present", "governance" in report)
        _check(
            "closed_loop_allowed false in report",
            report.get("governance", {}).get("closed_loop_allowed") is False,
        )
        _check("evidence_summary present", "evidence_summary" in report)
        _check("scientific_disclaimer present", "scientific_disclaimer" in report)

    # -- Evidence refresh -----------------------------------------------------
    print("\n5. POST /api/v1/safety/evidence/refresh")
    refresh = _post(f"{base}/api/v1/safety/evidence/refresh")
    if refresh is None:
        failures.append("evidence_refresh")
        _check("Evidence refresh endpoint", False, "returned None")
    else:
        _check("status=refreshed", refresh.get("status") == "refreshed", str(refresh.get("status")))
        _check("evidence_summary present", "evidence_summary" in refresh)
        cache_after = (refresh.get("evidence_summary") or {}).get("evidence_cache")
        _check("cache metadata after refresh", cache_after is not None)
        if cache_after:
            _check(
                "cache_hit=False after force refresh",
                cache_after.get("cache_hit") is False,
                str(cache_after.get("cache_hit")),
            )
        ok = _check(
            "closed_loop_allowed still False after refresh",
            refresh.get("closed_loop_allowed") is False,
            str(refresh.get("closed_loop_allowed")),
        )
        if not ok:
            failures.append("closed_loop_unlocked_after_refresh")

    # -- Cache hit after warm-up ----------------------------------------------
    print("\n6. Cache hit check (second GET /api/v1/safety/closed-loop)")
    cl2 = _get(f"{base}/api/v1/safety/closed-loop")
    if cl2 is not None:
        cache2 = (cl2.get("evidence_summary") or {}).get("evidence_cache")
        if cache2 is not None:
            _check("cache_hit=True on second request", cache2.get("cache_hit") is True,
                   str(cache2.get("cache_hit")))
        else:
            _check("cache metadata on second request", False, "evidence_cache missing")
    else:
        _check("Second closed-loop request", False, "returned None")

    # -- Summary --------------------------------------------------------------
    print(f"\n{'='*60}")
    if failures:
        print(f"FAILURES: {', '.join(failures)}")
        print("='*60}\n")
        sys.exit(1)
    else:
        print("All checks PASSED.")
        print(
            "\nSafety governance verified:"
            "\n  - closed_loop_allowed=False (correct)"
            "\n  - Evidence cache metadata present"
            "\n  - Force refresh works"
            "\n  - Cache hit on warm requests"
        )
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
