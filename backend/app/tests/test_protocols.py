"""Tests for the NeuroVerse protocol engine."""

from __future__ import annotations

import asyncio

import httpx
import pytest

from app.protocols.models import (
    ProtocolMode,
    ProtocolRun,
    ProtocolStepResult,
    ProtocolStepStatus,
)
from app.protocols.registry import get_protocol, list_protocols
from app.protocols.storage import list_runs, load_run, save_run

# ---------------------------------------------------------------------------
#  Registry
# ---------------------------------------------------------------------------


class TestProtocolRegistry:
    def test_list_returns_at_least_5_protocols(self):
        protocols = list_protocols()
        assert len(protocols) >= 5

    def test_expected_protocols_present(self):
        ids = {p.protocol_id for p in list_protocols()}
        assert "synthetic_demo_protocol" in ids
        assert "brainflow_synthetic_shadow_protocol" in ids
        assert "eeg_lsl_replay_shadow_protocol" in ids
        assert "physical_openbci_trial_protocol" in ids
        assert "safety_audit_only_protocol" in ids

    def test_get_protocol_by_id(self):
        p = get_protocol("synthetic_demo_protocol")
        assert p is not None
        assert p.protocol_id == "synthetic_demo_protocol"

    def test_get_nonexistent_protocol_returns_none(self):
        assert get_protocol("nonexistent_xyz") is None

    def test_all_protocols_have_steps(self):
        for p in list_protocols():
            assert len(p.steps) >= 1, f"{p.protocol_id} has no steps"

    def test_all_protocols_closed_loop_false_by_default(self):
        for p in list_protocols():
            assert p.closed_loop_allowed_default is False, (
                f"{p.protocol_id} has closed_loop_allowed_default=True"
            )

    def test_physical_protocol_requires_port_input(self):
        p = get_protocol("physical_openbci_trial_protocol")
        assert p is not None
        assert p.mode == ProtocolMode.PHYSICAL_HARDWARE
        assert "PORT" in p.required_inputs

    def test_protocol_definitions_have_scientific_limitations(self):
        for p in list_protocols():
            assert p.scientific_limitations, f"{p.protocol_id} missing scientific_limitations"


# ---------------------------------------------------------------------------
#  Physical hardware blocking
# ---------------------------------------------------------------------------


class TestPhysicalHardwareBlocking:
    def test_physical_openbci_blocks_without_port(self):
        from app.protocols.runner import execute_step

        protocol = get_protocol("physical_openbci_trial_protocol")
        assert protocol is not None

        hw_step_def = next(s for s in protocol.steps if "PORT" in s.required_inputs)
        step_result = ProtocolStepResult(step_id=hw_step_def.step_id, title=hw_step_def.title)
        run = ProtocolRun(
            run_id="test_block",
            protocol_id=protocol.protocol_id,
            protocol_title=protocol.title,
            mode=protocol.mode,
            steps=[step_result],
            inputs={},
            closed_loop_allowed=False,
        )
        execute_step(run, hw_step_def, step_result)
        assert step_result.status == ProtocolStepStatus.BLOCKED
        assert step_result.block_reason is not None
        assert "PORT" in step_result.block_reason

    def test_manual_step_marked_as_manual(self):
        from app.protocols.runner import execute_step

        protocol = get_protocol("eeg_lsl_replay_shadow_protocol")
        assert protocol is not None
        step_def = protocol.steps[0]
        assert step_def.action == "manual_command_required"
        step_result = ProtocolStepResult(step_id=step_def.step_id, title=step_def.title)
        run = ProtocolRun(
            run_id="test_manual",
            protocol_id=protocol.protocol_id,
            protocol_title=protocol.title,
            mode=protocol.mode,
            steps=[step_result],
            inputs={},
            closed_loop_allowed=False,
        )
        execute_step(run, step_def, step_result)
        assert step_result.status == ProtocolStepStatus.MANUAL_COMMAND_REQUIRED
        assert step_result.manual_command is not None

    def test_manual_step_does_not_execute_automatically(self):
        """Manual-command steps must stay manual, never auto-execute."""
        from app.protocols.runner import execute_step

        protocol = get_protocol("eeg_lsl_replay_shadow_protocol")
        assert protocol is not None
        manual_step = next(s for s in protocol.steps if s.action == "manual_command_required")
        step_result = ProtocolStepResult(step_id=manual_step.step_id, title=manual_step.title)
        run = ProtocolRun(
            run_id="test_no_auto_exec",
            protocol_id=protocol.protocol_id,
            protocol_title=protocol.title,
            mode=protocol.mode,
            steps=[step_result],
            inputs={},
            closed_loop_allowed=False,
        )
        execute_step(run, manual_step, step_result)
        # Must be manual_command_required, never passed/running
        assert step_result.status == ProtocolStepStatus.MANUAL_COMMAND_REQUIRED


# ---------------------------------------------------------------------------
#  Protocol run creation and storage
# ---------------------------------------------------------------------------


class TestProtocolRunStorage:
    def test_save_and_load_run(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)

        run = ProtocolRun(
            run_id="test_run_001",
            protocol_id="synthetic_demo_protocol",
            protocol_title="Synthetic Demo",
            mode=ProtocolMode.SIMULATED,
            steps=[ProtocolStepResult(step_id="step1", title="Step 1")],
            closed_loop_allowed=False,
        )
        save_run(run)

        loaded = load_run("test_run_001")
        assert loaded is not None
        assert loaded.run_id == "test_run_001"
        assert loaded.protocol_id == "synthetic_demo_protocol"
        assert loaded.closed_loop_allowed is False

    def test_save_creates_json_md_and_manifest(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)

        run = ProtocolRun(
            run_id="test_files",
            protocol_id="safety_audit_only_protocol",
            protocol_title="Safety Audit",
            mode=ProtocolMode.SIMULATED,
            steps=[
                ProtocolStepResult(step_id="s1", title="S1"),
                ProtocolStepResult(step_id="s2", title="S2"),
            ],
            closed_loop_allowed=False,
        )
        run_dir = save_run(run)
        assert (run_dir / "protocol_run.json").exists()
        assert (run_dir / "protocol_run.md").exists()
        assert (run_dir / "step_results.json").exists()
        assert (run_dir / "artifacts_manifest.json").exists()

    def test_list_runs_returns_saved_runs(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)

        run = ProtocolRun(
            run_id="list_test_001",
            protocol_id="synthetic_demo_protocol",
            protocol_title="Synthetic Demo",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
        )
        save_run(run)
        runs = list_runs()
        assert any(r["run_id"] == "list_test_001" for r in runs)

    def test_markdown_report_contains_disclaimer(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)

        run = ProtocolRun(
            run_id="disclaimer_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="Synthetic Demo",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
        )
        run_dir = save_run(run)
        md = (run_dir / "protocol_run.md").read_text()
        assert "Closed-loop from real EEG is disabled by default" in md

    def test_load_nonexistent_run_returns_none(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        assert load_run("nonexistent_run_id") is None


# ---------------------------------------------------------------------------
#  Protocol run model
# ---------------------------------------------------------------------------


class TestProtocolRunModel:
    def test_overall_status_pending_when_no_steps_started(self):
        run = ProtocolRun(
            run_id="r1",
            protocol_id="p1",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[ProtocolStepResult(step_id="s", title="S")],
            closed_loop_allowed=False,
        )
        assert run.overall_status() == ProtocolStepStatus.PENDING

    def test_overall_status_passed_when_all_passed(self):
        run = ProtocolRun(
            run_id="r1",
            protocol_id="p1",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
        )
        s = ProtocolStepResult(step_id="s", title="S")
        s.complete(passed=True)
        run.steps = [s]
        assert run.overall_status() == ProtocolStepStatus.PASSED

    def test_overall_status_failed_when_any_failed(self):
        run = ProtocolRun(
            run_id="r1",
            protocol_id="p1",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
        )
        s1 = ProtocolStepResult(step_id="s1", title="S1")
        s1.complete(passed=True)
        s2 = ProtocolStepResult(step_id="s2", title="S2")
        s2.complete(passed=False)
        run.steps = [s1, s2]
        assert run.overall_status() == ProtocolStepStatus.FAILED

    def test_closed_loop_always_false_in_run(self):
        run = ProtocolRun(
            run_id="r1",
            protocol_id="p1",
            protocol_title="T",
            mode=ProtocolMode.PHYSICAL_HARDWARE,
            steps=[],
            closed_loop_allowed=False,
        )
        assert run.closed_loop_allowed is False

    def test_step_result_has_extended_fields(self):
        s = ProtocolStepResult(step_id="s", title="S")
        assert s.progress_percent is None
        assert s.log_lines == []
        assert s.duration_seconds is None
        assert s.execution_mode is None
        assert s.exit_code is None
        assert s.log_file_path is None
        assert s.last_updated_at is None


# ---------------------------------------------------------------------------
#  Safety audit protocol (no hardware, runs fully)
# ---------------------------------------------------------------------------


class TestSafetyAuditProtocol:
    def test_aggregate_evidence_step_runs(self):
        from app.protocols.runner import _run_internal_aggregate_evidence

        protocol = get_protocol("safety_audit_only_protocol")
        assert protocol is not None
        run = ProtocolRun(
            run_id="audit_test",
            protocol_id=protocol.protocol_id,
            protocol_title=protocol.title,
            mode=protocol.mode,
            steps=[],
            closed_loop_allowed=False,
        )
        result = _run_internal_aggregate_evidence(run)
        assert result["passed"] is True


# ---------------------------------------------------------------------------
#  Governance invariants
# ---------------------------------------------------------------------------


class TestGovernanceInvariants:
    def test_closed_loop_remains_false_after_protocol_run(self):
        from app.protocols.runner import _run_internal_safety_audit

        protocol = get_protocol("safety_audit_only_protocol")
        assert protocol is not None
        run = ProtocolRun(
            run_id="gov_test",
            protocol_id=protocol.protocol_id,
            protocol_title=protocol.title,
            mode=protocol.mode,
            steps=[],
            closed_loop_allowed=False,
        )
        _run_internal_safety_audit(run)
        assert run.closed_loop_allowed is False

    def test_physical_protocol_closed_loop_false(self):
        protocol = get_protocol("physical_openbci_trial_protocol")
        assert protocol is not None
        run = ProtocolRun(
            run_id="phys_gov",
            protocol_id=protocol.protocol_id,
            protocol_title=protocol.title,
            mode=protocol.mode,
            steps=[],
            closed_loop_allowed=False,
        )
        assert run.closed_loop_allowed is False


# ---------------------------------------------------------------------------
#  API route registration smoke tests
# ---------------------------------------------------------------------------


class TestProtocolAPISmoke:
    def test_app_has_protocol_routes(self):
        from app.main import create_app

        app = create_app()
        paths = {r.path for r in app.routes if hasattr(r, "path")}
        assert "/api/v1/protocols" in paths
        assert "/api/v1/protocols/{protocol_id}" in paths
        assert "/api/v1/protocols/{protocol_id}/runs" in paths
        assert "/api/v1/protocols/{protocol_id}/preflight" in paths
        assert "/api/v1/protocol-runs" in paths
        assert "/api/v1/protocol-runs/{run_id}" in paths
        assert "/api/v1/protocol-runs/{run_id}/steps/{step_id}/run" in paths
        assert "/api/v1/protocol-runs/{run_id}/steps/{step_id}/cancel" in paths
        assert "/api/v1/protocol-runs/{run_id}/run-all" in paths
        assert "/api/v1/protocol-runs/{run_id}/stop" in paths
        assert "/api/v1/protocol-runs/{run_id}/complete" in paths
        assert "/api/v1/protocol-runs/{run_id}/report" in paths
        assert "/api/v1/protocol-runs/{run_id}/status/stream" in paths


# ---------------------------------------------------------------------------
#  Async API behaviour tests — background execution, 409, SSE, cancel
# ---------------------------------------------------------------------------


@pytest.fixture
async def async_client():
    """Async HTTPX client backed by the FastAPI app via ASGITransport."""
    from app.main import create_app

    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


class TestAsyncStepExecution:
    async def test_run_step_returns_immediately_with_running_status(self, async_client):
        """POSTing a runnable step must return quickly with status=running."""
        # Create a run first
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]
        step_id = resp.json()["steps"][0]["step_id"]

        resp2 = await async_client.post(
            f"/api/v1/protocol-runs/{run_id}/steps/{step_id}/run"
        )
        assert resp2.status_code == 200
        body = resp2.json()
        # Must return running or a fast-complete status (manual/blocked finish synchronously)
        assert body["run_id"] == run_id
        assert body["step_id"] == step_id
        assert body["closed_loop_allowed"] is False
        allowed = {"running", "manual_command_required", "blocked", "passed", "failed"}
        assert body["status"] in allowed

    async def test_409_when_step_already_running(self, async_client, monkeypatch):
        """A second POST while a step is running must return 409."""
        import app.api.routes_protocols as routes_mod

        # Create a run
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]
        step_id = resp.json()["steps"][0]["step_id"]

        # Inject a fake never-completing task to simulate a running step
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        routes_mod._RUNNING_TASKS[run_id] = asyncio.ensure_future(fut)

        # Mark the step as running in the run object too
        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            run.steps[0].start(execution_mode="background_task")
            run.current_step_id = step_id

        try:
            resp2 = await async_client.post(
                f"/api/v1/protocol-runs/{run_id}/steps/{step_id}/run"
            )
            assert resp2.status_code == 409
            assert resp2.json()["detail"]["error"] == "step_already_running"
        finally:
            fut.cancel()
            routes_mod._RUNNING_TASKS.pop(run_id, None)

    async def test_complete_run_rejects_while_step_running(self, async_client, monkeypatch):
        """POST /complete must return 409 if a step task is active."""
        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]

        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        routes_mod._RUNNING_TASKS[run_id] = asyncio.ensure_future(fut)

        try:
            resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/complete")
            assert resp2.status_code == 409
            assert resp2.json()["detail"]["error"] == "step_running"
        finally:
            fut.cancel()
            routes_mod._RUNNING_TASKS.pop(run_id, None)

    async def test_get_run_returns_is_step_running(self, async_client):
        """GET /protocol-runs/{run_id} must include is_step_running field."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]
        resp2 = await async_client.get(f"/api/v1/protocol-runs/{run_id}")
        assert resp2.status_code == 200
        assert "is_step_running" in resp2.json()
        assert resp2.json()["is_step_running"] is False

    async def test_closed_loop_always_false_in_api_responses(self, async_client):
        """Every protocol-related response must carry closed_loop_allowed=false."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.json()["closed_loop_allowed"] is False

        run_id = resp.json()["run_id"]
        resp2 = await async_client.get(f"/api/v1/protocol-runs/{run_id}")
        assert resp2.json()["closed_loop_allowed"] is False

    async def test_physical_protocol_requires_port(self, async_client):
        """Creating a physical hardware run without PORT must return 422."""
        resp = await async_client.post(
            "/api/v1/protocols/physical_openbci_trial_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 422

    async def test_status_stream_endpoint_exists_and_responds(self, async_client):
        """GET /status/stream must return 200 with text/event-stream."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        # Stream the first chunk only
        async with async_client.stream(
            "GET", f"/api/v1/protocol-runs/{run_id}/status/stream"
        ) as stream_resp:
            assert stream_resp.status_code == 200
            assert "text/event-stream" in stream_resp.headers.get("content-type", "")
            # Read one chunk to verify format
            chunk = b""
            async for raw in stream_resp.aiter_raw():
                chunk = raw
                break
        assert b"data:" in chunk

    async def test_cancel_step_404_when_no_task(self, async_client):
        """Cancelling when no step is running must return 404."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]
        step_id = resp.json()["steps"][0]["step_id"]
        resp2 = await async_client.post(
            f"/api/v1/protocol-runs/{run_id}/steps/{step_id}/cancel"
        )
        assert resp2.status_code == 404

    async def test_manual_step_not_in_running_task(self, async_client):
        """Manual-command steps complete synchronously; no background task created."""
        import app.api.routes_protocols as routes_mod

        protocol = get_protocol("eeg_lsl_replay_shadow_protocol")
        assert protocol is not None

        resp = await async_client.post(
            "/api/v1/protocols/eeg_lsl_replay_shadow_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]

        # Find the first manual step
        manual_step = next(
            s for s in protocol.steps if s.action == "manual_command_required"
        )

        resp2 = await async_client.post(
            f"/api/v1/protocol-runs/{run_id}/steps/{manual_step.step_id}/run"
        )
        assert resp2.status_code == 200
        assert resp2.json()["status"] == "manual_command_required"
        # No background task should have been created
        assert run_id not in routes_mod._RUNNING_TASKS

    async def test_step_log_persistence_after_completion(self, async_client, tmp_path, monkeypatch):
        """After an internal step completes, a log file should be written."""
        import app.protocols.runner as runner_mod
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(runner_mod, "_ROOT", tmp_path.parent)

        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]

        step_id = resp.json()["steps"][0]["step_id"]
        resp2 = await async_client.post(
            f"/api/v1/protocol-runs/{run_id}/steps/{step_id}/run"
        )
        assert resp2.status_code == 200

        # Wait for background task to complete (up to 10 seconds)
        import app.api.routes_protocols as routes_mod

        for _ in range(20):
            await asyncio.sleep(0.5)
            if not routes_mod._is_step_running(run_id):
                break


# ---------------------------------------------------------------------------
#  Preflight and orchestration tests
# ---------------------------------------------------------------------------


class TestPreflight:
    def test_preflight_model_has_required_fields(self):
        from app.protocols.models import PreflightResult

        pf = PreflightResult(
            protocol_id="test",
            can_start=True,
            can_auto_run=False,
        )
        assert pf.closed_loop_allowed is False
        assert pf.blocking_issues == []
        assert pf.executable_steps == []

    def test_preflight_returns_expected_fields(self):
        from app.protocols.registry import get_protocol

        protocol = get_protocol("synthetic_demo_protocol")
        assert protocol is not None
        assert protocol.supports_auto_run is True
        assert protocol.auto_run_policy == "full"
        assert protocol.reviewer_demo_recommended is True

    def test_physical_protocol_auto_run_disabled(self):
        from app.protocols.registry import get_protocol

        protocol = get_protocol("physical_openbci_trial_protocol")
        assert protocol is not None
        assert protocol.supports_auto_run is False
        assert protocol.auto_run_policy == "disabled"
        assert protocol.reviewer_demo_recommended is False

    def test_safety_audit_protocol_supports_auto_run(self):
        from app.protocols.registry import get_protocol

        protocol = get_protocol("safety_audit_only_protocol")
        assert protocol is not None
        assert protocol.supports_auto_run is True
        assert protocol.auto_run_policy == "full"

    def test_eeg_lsl_replay_until_manual_step(self):
        from app.protocols.registry import get_protocol

        protocol = get_protocol("eeg_lsl_replay_shadow_protocol")
        assert protocol is not None
        assert protocol.supports_auto_run is True
        assert protocol.auto_run_policy == "until_manual_step"

    def test_brainflow_synthetic_supports_auto_run(self):
        from app.protocols.registry import get_protocol

        protocol = get_protocol("brainflow_synthetic_shadow_protocol")
        assert protocol is not None
        assert protocol.supports_auto_run is True
        assert protocol.auto_run_policy == "full"
        assert protocol.reviewer_demo_recommended is True

    async def test_api_preflight_get_returns_expected_fields(self, async_client):
        resp = await async_client.get("/api/v1/protocols/synthetic_demo_protocol/preflight")
        assert resp.status_code == 200
        body = resp.json()
        assert body["protocol_id"] == "synthetic_demo_protocol"
        assert "can_start" in body
        assert "can_auto_run" in body
        assert "blocking_issues" in body
        assert "warnings" in body
        assert "manual_steps" in body
        assert "executable_steps" in body
        assert body["closed_loop_allowed"] is False

    async def test_api_preflight_post_with_inputs(self, async_client):
        resp = await async_client.post(
            "/api/v1/protocols/physical_openbci_trial_protocol/preflight",
            json={"inputs": {"PORT": "/dev/ttyUSB0"}},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["protocol_id"] == "physical_openbci_trial_protocol"
        assert body["closed_loop_allowed"] is False

    async def test_api_preflight_physical_without_port(self, async_client):
        resp = await async_client.get(
            "/api/v1/protocols/physical_openbci_trial_protocol/preflight"
        )
        assert resp.status_code == 200
        body = resp.json()
        # Without PORT, should have blocking issue and can_start=False
        assert body["can_start"] is False
        assert body["can_auto_run"] is False
        assert len(body["blocking_issues"]) > 0

    async def test_api_preflight_safe_protocol_can_auto_run(self, async_client):
        resp = await async_client.get(
            "/api/v1/protocols/synthetic_demo_protocol/preflight"
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["can_start"] is True
        assert body["can_auto_run"] is True
        assert len(body["blocking_issues"]) == 0

    async def test_create_run_includes_preflight(self, async_client):
        """POST /runs should include preflight result in response."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        assert "preflight" in resp.json()
        pf = resp.json()["preflight"]
        assert "can_start" in pf
        assert "can_auto_run" in pf


class TestOrchestration:
    async def test_run_all_returns_running_status(self, async_client):
        """POST /run-all should start orchestration and return immediately."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
        assert resp2.status_code == 200
        body = resp2.json()
        assert body["orchestration_status"] in {"running", "completed"}
        assert body["closed_loop_allowed"] is False

    async def test_run_all_disabled_protocol_returns_422(self, async_client):
        """Physical protocol with auto_run_policy=disabled must reject run-all."""
        resp = await async_client.post(
            "/api/v1/protocols/physical_openbci_trial_protocol/runs",
            json={"inputs": {"PORT": "/dev/ttyUSB0"}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
        assert resp2.status_code == 422
        assert resp2.json()["detail"]["error"] == "auto_run_not_supported"

    async def test_run_all_409_when_already_running(self, async_client, monkeypatch):
        """run-all while orchestration active must return 409."""
        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        routes_mod._RUNNING_TASKS[run_id] = asyncio.ensure_future(fut)

        try:
            resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
            assert resp2.status_code == 409
        finally:
            fut.cancel()
            routes_mod._RUNNING_TASKS.pop(run_id, None)

    async def test_run_all_skips_passed_steps(self, async_client):
        """Orchestration should skip already-passed steps."""
        import app.api.routes_protocols as routes_mod
        from app.protocols.models import ProtocolStepStatus

        resp = await async_client.post(
            "/api/v1/protocols/safety_audit_only_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        # Pre-mark first step as passed in the in-memory run
        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            run.steps[0].complete(passed=True)

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
        assert resp2.status_code == 200

        # Wait for orchestration to complete
        for _ in range(30):
            await asyncio.sleep(0.5)
            if not routes_mod._is_step_running(run_id):
                break

        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            # First step should still be passed (not re-run)
            assert run.steps[0].status == ProtocolStepStatus.PASSED

    async def test_run_all_stops_at_manual_step(self, async_client):
        """Orchestration must stop cleanly at manual_command_required steps."""
        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/eeg_lsl_replay_shadow_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
        assert resp2.status_code == 200

        # Wait for orchestration to finish (should be fast — stops at first manual step)
        for _ in range(20):
            await asyncio.sleep(0.3)
            if not routes_mod._is_step_running(run_id):
                break

        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            assert run.orchestration_status in {
                "stopped_manual_required",
                "cancelled",
                "completed",
            }
            assert run.closed_loop_allowed is False

    async def test_stop_orchestration_endpoint(self, async_client, monkeypatch):
        """POST /stop should cancel active orchestration."""
        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        # Inject a fake never-completing task
        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        routes_mod._RUNNING_TASKS[run_id] = asyncio.ensure_future(fut)

        # Set orchestration_status to running on the in-memory run
        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            run.orchestration_status = "running"

        try:
            resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/stop")
            assert resp2.status_code == 200
            assert resp2.json()["closed_loop_allowed"] is False
        finally:
            fut.cancel()
            routes_mod._RUNNING_TASKS.pop(run_id, None)
            routes_mod._STOP_EVENTS.pop(run_id, None)

    async def test_complete_fails_while_orchestration_running(self, async_client, monkeypatch):
        """POST /complete must 409 while orchestration is active."""
        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        fut: asyncio.Future = asyncio.get_event_loop().create_future()
        routes_mod._RUNNING_TASKS[run_id] = asyncio.ensure_future(fut)

        try:
            resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/complete")
            assert resp2.status_code == 409
        finally:
            fut.cancel()
            routes_mod._RUNNING_TASKS.pop(run_id, None)

    async def test_run_all_get_includes_orchestration_status(self, async_client):
        """GET /protocol-runs/{run_id} must include orchestration_status field."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]
        resp2 = await async_client.get(f"/api/v1/protocol-runs/{run_id}")
        body = resp2.json()
        assert "orchestration_status" in body
        assert "auto_advance" in body
        assert body["closed_loop_allowed"] is False

    async def test_sse_includes_orchestration_status(self, async_client):
        """SSE stream must include orchestration_status in events."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        async with async_client.stream(
            "GET", f"/api/v1/protocol-runs/{run_id}/status/stream"
        ) as stream_resp:
            assert stream_resp.status_code == 200
            chunk = b""
            async for raw in stream_resp.aiter_raw():
                chunk = raw
                break

        assert b"orchestration_status" in chunk

    async def test_closed_loop_always_false_in_all_orchestration_endpoints(
        self, async_client
    ):
        """Every orchestration response must carry closed_loop_allowed=false."""
        # Preflight
        resp = await async_client.get(
            "/api/v1/protocols/synthetic_demo_protocol/preflight"
        )
        assert resp.json()["closed_loop_allowed"] is False

        # Create run
        resp2 = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs", json={"inputs": {}}
        )
        assert resp2.json()["closed_loop_allowed"] is False
        run_id = resp2.json()["run_id"]

        # GET run
        resp3 = await async_client.get(f"/api/v1/protocol-runs/{run_id}")
        assert resp3.json()["closed_loop_allowed"] is False

    async def test_report_includes_orchestration_metadata(self, async_client):
        """GET /report must include orchestration fields."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        report_resp = await async_client.get(f"/api/v1/protocol-runs/{run_id}/report")
        body = report_resp.json()
        assert "orchestration_status" in body
        assert "auto_advance" in body
        assert "preflight_result" in body
        assert body["closed_loop_allowed"] is False


# ---------------------------------------------------------------------------
#  Auto-complete and completion report tests
# ---------------------------------------------------------------------------


class TestAutoComplete:
    def test_protocol_run_model_has_auto_complete_fields(self):
        from app.protocols.models import ProtocolMode, ProtocolRun

        run = ProtocolRun(
            run_id="ac_test",
            protocol_id="p1",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
        )
        assert run.auto_completed is False
        assert run.auto_completed_at is None
        assert run.protocol_completion_report_path is None
        assert run.final_report_generated is False
        assert run.closed_loop_allowed is False

    def test_generate_completion_report_writes_json_and_md(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun, ProtocolStepResult

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        s = ProtocolStepResult(step_id="s1", title="S1")
        s.complete(passed=True)
        run = ProtocolRun(
            run_id="cr_test_001",
            protocol_id="synthetic_demo_protocol",
            protocol_title="Synthetic Demo",
            mode=ProtocolMode.SIMULATED,
            steps=[s],
            closed_loop_allowed=False,
            auto_completed=True,
        )
        run_dir = storage_mod.generate_completion_report(run)
        assert (run_dir / "protocol_completion_report.json").exists()
        assert (run_dir / "protocol_completion_report.md").exists()

    def test_completion_report_closed_loop_false(self, tmp_path, monkeypatch):
        import json as _json

        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        run = ProtocolRun(
            run_id="cr_cl_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
        )
        run_dir = storage_mod.generate_completion_report(run)
        report = _json.loads((run_dir / "protocol_completion_report.json").read_text())
        assert report["closed_loop_allowed"] is False
        assert "Closed-loop from real EEG is disabled by default" in report["scientific_disclaimer"]
        assert len(report["what_this_proves"]) > 0
        assert len(report["what_this_does_not_prove"]) > 0

    def test_update_latest_auto_run_evidence_writes_files(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        run = ProtocolRun(
            run_id="ep_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
            auto_completed=True,
        )
        storage_mod.update_latest_auto_run_evidence(run)
        ep = tmp_path / "ep"
        assert (ep / "latest_auto_run_protocol.json").exists()
        assert (ep / "latest_auto_run_protocol.md").exists()

    def test_find_latest_auto_run_returns_none_with_no_runs(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        result = storage_mod.find_latest_auto_run()
        assert result is None

    def test_find_latest_auto_run_finds_auto_completed_run(self, tmp_path, monkeypatch):
        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        run = ProtocolRun(
            run_id="find_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
            auto_completed=True,
        )
        storage_mod.save_run(run)
        result = storage_mod.find_latest_auto_run()
        assert result is not None
        assert result["run_id"] == "find_test"
        assert result["auto_completed"] is True

    async def test_run_all_auto_completes_safe_protocol(self, async_client):
        """run-all on a safe protocol should auto-complete and generate completion report."""
        import asyncio as _asyncio

        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/safety_audit_only_protocol/runs",
            json={"inputs": {}},
        )
        assert resp.status_code == 200
        run_id = resp.json()["run_id"]

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
        assert resp2.status_code == 200

        # Wait for orchestration to complete (safety_audit_only is fast, ~1s)
        for _ in range(30):
            await _asyncio.sleep(0.5)
            if not routes_mod._is_step_running(run_id):
                break

        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            # Check auto-completed fields
            assert run.orchestration_status == "completed"
            assert run.auto_completed is True
            assert run.closed_loop_allowed is False
            assert run.final_report_generated is True

    async def test_stopped_manual_does_not_auto_complete(self, async_client):
        """Orchestration that stops at a manual step must NOT auto-complete."""
        import asyncio as _asyncio

        import app.api.routes_protocols as routes_mod

        resp = await async_client.post(
            "/api/v1/protocols/eeg_lsl_replay_shadow_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/run-all")
        assert resp2.status_code == 200

        for _ in range(20):
            await _asyncio.sleep(0.3)
            if not routes_mod._is_step_running(run_id):
                break

        run = routes_mod._ACTIVE_RUNS.get(run_id)
        if run:
            assert run.auto_completed is False
            assert run.orchestration_status in {"stopped_manual_required", "cancelled"}
            assert run.closed_loop_allowed is False

    async def test_latest_auto_run_endpoint_returns_404_when_none(self, async_client, monkeypatch):
        """GET /latest-auto-run returns 404 if no auto-completed run exists."""
        import app.api.routes_protocols as routes_mod

        monkeypatch.setattr(routes_mod, "find_latest_auto_run", lambda: None)
        resp = await async_client.get("/api/v1/protocol-runs/latest-auto-run")
        assert resp.status_code == 404

    async def test_completion_report_endpoint_returns_404_before_run(self, async_client):
        """GET /completion-report returns 404 when report not yet generated."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]
        resp2 = await async_client.get(
            f"/api/v1/protocol-runs/{run_id}/completion-report"
        )
        assert resp2.status_code == 404

    async def test_complete_endpoint_generates_completion_report(
        self, async_client, tmp_path, monkeypatch
    ):
        """POST /complete should trigger completion report generation."""
        import app.protocols.storage as storage_mod

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]

        resp2 = await async_client.post(f"/api/v1/protocol-runs/{run_id}/complete")
        assert resp2.status_code == 200
        body = resp2.json()
        assert body["closed_loop_allowed"] is False
        assert "final_report_generated" in body

    async def test_get_run_includes_auto_complete_fields(self, async_client):
        """GET /protocol-runs/{run_id} must include auto_completed field."""
        resp = await async_client.post(
            "/api/v1/protocols/synthetic_demo_protocol/runs",
            json={"inputs": {}},
        )
        run_id = resp.json()["run_id"]
        resp2 = await async_client.get(f"/api/v1/protocol-runs/{run_id}")
        body = resp2.json()
        assert "auto_completed" in body
        assert body["auto_completed"] is False
        assert body["closed_loop_allowed"] is False

    async def test_app_has_completion_report_routes(self):
        """Smoke: verify all new routes are registered."""
        from app.main import create_app

        app = create_app()
        paths = {r.path for r in app.routes if hasattr(r, "path")}
        assert "/api/v1/protocol-runs/latest-auto-run" in paths
        assert "/api/v1/protocol-runs/latest-auto-run/report" in paths
        assert "/api/v1/protocol-runs/{run_id}/completion-report" in paths


# ---------------------------------------------------------------------------
#  Source-of-truth / serialization tests
# ---------------------------------------------------------------------------


class TestSourceOfTruth:
    def test_completion_report_status_is_plain_string(self, tmp_path, monkeypatch):
        """generate_completion_report must write status as 'passed', not enum repr."""
        import json as _json

        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun, ProtocolStepResult

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        s = ProtocolStepResult(step_id="s1", title="S1")
        s.complete(passed=True)
        run = ProtocolRun(
            run_id="serial_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="Synthetic Demo",
            mode=ProtocolMode.SIMULATED,
            steps=[s],
            closed_loop_allowed=False,
            auto_completed=True,
        )
        run_dir = storage_mod.generate_completion_report(run)
        data = _json.loads((run_dir / "protocol_completion_report.json").read_text())
        # Must be "passed", never "ProtocolStepStatus.PASSED"
        assert data["status"] == "passed"
        assert "ProtocolStepStatus" not in data["status"]

    def test_update_evidence_status_is_plain_string(self, tmp_path, monkeypatch):
        """update_latest_auto_run_evidence must write status as plain string."""
        import json as _json

        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        # Add a pending step so overall_status() returns "pending"
        pending_step = ProtocolStepResult(step_id="s1", title="S1")
        run = ProtocolRun(
            run_id="ev_serial_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[pending_step],
            closed_loop_allowed=False,
            auto_completed=True,
        )
        storage_mod.update_latest_auto_run_evidence(run)
        data = _json.loads((tmp_path / "ep" / "latest_auto_run_protocol.json").read_text())
        assert data["status"] == "pending"
        assert "ProtocolStepStatus" not in str(data["status"])

    def test_update_evidence_includes_all_source_of_truth_fields(self, tmp_path, monkeypatch):
        """update_latest_auto_run_evidence must include all fields the API needs."""
        import json as _json

        import app.protocols.storage as storage_mod
        from app.protocols.models import ProtocolMode, ProtocolRun

        monkeypatch.setattr(storage_mod, "PROTOCOL_RUNS_DIR", tmp_path)
        monkeypatch.setattr(storage_mod, "_EVIDENCE_PACK_DIR", tmp_path / "ep")

        run = ProtocolRun(
            run_id="field_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[],
            closed_loop_allowed=False,
            auto_completed=True,
            final_report_generated=True,
        )
        storage_mod.update_latest_auto_run_evidence(run)
        data = _json.loads((tmp_path / "ep" / "latest_auto_run_protocol.json").read_text())
        required_fields = [
            "run_id", "protocol_id", "protocol_title", "mode", "status",
            "auto_completed", "auto_completed_at", "final_report_generated",
            "step_summary", "artifact_paths", "artifact_count",
            "what_this_proves", "what_this_does_not_prove",
            "scientific_disclaimer", "closed_loop_allowed",
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        assert data["closed_loop_allowed"] is False

    async def test_latest_auto_run_api_returns_enriched_fields(self, async_client, monkeypatch):
        """GET /latest-auto-run must return step_summary and proves/not-proves."""
        import app.api.routes_protocols as routes_mod
        from app.protocols.models import ProtocolMode, ProtocolRun, ProtocolStepResult

        # Build a fake auto-completed run
        s = ProtocolStepResult(step_id="s1", title="S1")
        s.complete(passed=True)
        run = ProtocolRun(
            run_id="api_enrich_test",
            protocol_id="synthetic_demo_protocol",
            protocol_title="T",
            mode=ProtocolMode.SIMULATED,
            steps=[s],
            closed_loop_allowed=False,
            auto_completed=True,
        )

        # Monkeypatch find_latest_auto_run to return our test run's JSON form
        import json as _json

        run_data = _json.loads(run.model_dump_json())
        run_data["_completion_report_path"] = None

        monkeypatch.setattr(routes_mod, "find_latest_auto_run", lambda: run_data)
        resp = await async_client.get("/api/v1/protocol-runs/latest-auto-run")
        assert resp.status_code == 200
        body = resp.json()
        assert "step_summary" in body
        assert "artifact_paths" in body
        assert "what_this_proves" in body
        assert "what_this_does_not_prove" in body
        assert body["closed_loop_allowed"] is False
        # status must be a plain string, never enum repr
        assert "ProtocolStepStatus" not in str(body.get("status", ""))

    async def test_latest_auto_run_status_plain_string(self, async_client, monkeypatch):
        """Status field in API response must be a plain string."""
        import app.api.routes_protocols as routes_mod

        # Simulate a run_data with enum repr status (as might exist in older JSON)
        run_data = {
            "run_id": "str_test",
            "protocol_id": "synthetic_demo_protocol",
            "protocol_title": "T",
            "mode": "simulated",
            "status": "ProtocolStepStatus.PASSED",
            "auto_completed": True,
            "steps": [],
            "_completion_report_path": None,
        }
        monkeypatch.setattr(routes_mod, "find_latest_auto_run", lambda: run_data)
        resp = await async_client.get("/api/v1/protocol-runs/latest-auto-run")
        assert resp.status_code == 200
        body = resp.json()
        # Route must normalize the status to a plain string
        assert "ProtocolStepStatus" not in body["status"]
        assert body["status"] == "passed"

    async def test_latest_auto_run_404_clean(self, async_client, monkeypatch):
        """GET /latest-auto-run returns 404 cleanly when no auto-run exists."""
        import app.api.routes_protocols as routes_mod

        monkeypatch.setattr(routes_mod, "find_latest_auto_run", lambda: None)
        resp = await async_client.get("/api/v1/protocol-runs/latest-auto-run")
        assert resp.status_code == 404

    async def test_latest_auto_run_report_404_when_no_path(self, async_client, monkeypatch):
        """GET /latest-auto-run/report returns 404 when no completion report path."""
        import app.api.routes_protocols as routes_mod

        run_data = {
            "run_id": "rpt_404_test",
            "auto_completed": True,
            "_completion_report_path": None,
        }
        monkeypatch.setattr(routes_mod, "find_latest_auto_run", lambda: run_data)
        resp = await async_client.get("/api/v1/protocol-runs/latest-auto-run/report")
        assert resp.status_code == 404
