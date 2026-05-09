from __future__ import annotations

import asyncio
import time
import uuid
from collections.abc import Callable, Coroutine
from typing import Any

from app.acquisition.simulator import BiosignalSimulator
from app.core.clock import SessionClock
from app.core.config import settings
from app.core.logging import logger
from app.core.runtime_status import runtime_status
from app.core.telemetry import telemetry
from app.features.eeg_features import extract_eeg_features
from app.features.gaze_features import extract_gaze_features
from app.features.multimodal_features import extract_multimodal_features
from app.features.physio_features import extract_physio_features
from app.inference.model_loader import get_active_model_status, load_active_estimator
from app.policy.adaptation_policy import AdaptationPolicy
from app.safety.safety_gate import SafetyGate
from app.schemas.adaptation import AdaptationActionPayload
from app.schemas.events import BaseEvent
from app.schemas.session import FeaturePayload
from app.sessions.recorder import SessionRecorder
from app.signal_quality.eeg_sqi import compute_eeg_sqi
from app.signal_quality.gaze_sqi import compute_gaze_sqi
from app.signal_quality.physio_sqi import compute_physio_sqi
from app.signal_quality.sqi import compute_multimodal_sqi

BroadcastFn = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]

_EEG_CHANNELS = {"Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"}
_PHYSIO_CHANNELS = {"HR", "HRV_RMSSD", "EDA_tonic", "EDA_phasic"}
_GAZE_CHANNELS = {"gaze_x", "gaze_y", "pupil_diameter", "blink"}


def _split_channels(
    data: list[list[float]], channel_names: list[str]
) -> tuple[
    list[list[float]],
    list[str],
    list[list[float]],
    list[str],
    list[list[float]],
    list[str],
]:
    eeg_data, eeg_names = [], []
    physio_data, physio_names = [], []
    gaze_data, gaze_names = [], []
    for i, name in enumerate(channel_names):
        if i >= len(data):
            break
        if name in _EEG_CHANNELS:
            eeg_data.append(data[i])
            eeg_names.append(name)
        elif name in _PHYSIO_CHANNELS:
            physio_data.append(data[i])
            physio_names.append(name)
        elif name in _GAZE_CHANNELS:
            gaze_data.append(data[i])
            gaze_names.append(name)
    return eeg_data, eeg_names, physio_data, physio_names, gaze_data, gaze_names


class NeuroVerseEngine:
    """Orchestrates acquisition, features, state estimation, safety, and policy."""

    def __init__(self, broadcast: BroadcastFn | None = None) -> None:
        self._broadcast = broadcast
        self._task: asyncio.Task[None] | None = None
        self._session_id: str | None = None
        self._recorder: SessionRecorder | None = None
        self._clock = SessionClock()
        self._running = False

    @property
    def session_id(self) -> str | None:
        return self._session_id

    @property
    def is_running(self) -> bool:
        return self._running

    async def start_session(self) -> str:
        if self._running:
            await self.stop_session()
        sid = str(uuid.uuid4())[:12]
        self._session_id = sid
        self._recorder = SessionRecorder(sid)
        self._clock.reset()
        active = get_active_model_status()
        self._running = True
        runtime_status.start_session(
            sid,
            active.get("active_estimator", "heuristic"),
            active.get("model_id"),
            active.get("prediction_semantics"),
        )
        self._task = asyncio.create_task(self._run_loop(sid))
        logger.info("Session %s started", sid)
        await self._emit(sid, "neuroverse.session.started", {"session_id": sid})
        return sid

    async def stop_session(self) -> None:
        sid = self._session_id
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._recorder:
            self._recorder.close()
        if sid:
            await self._emit(sid, "neuroverse.session.stopped", {"session_id": sid})
        runtime_status.stop_session()
        logger.info("Session %s stopped", sid)
        self._session_id = None
        self._recorder = None
        self._task = None

    async def emergency_stop(self, reason: str = "manual emergency stop") -> dict[str, Any]:
        runtime_status.emergency_stop(reason)
        sid = self._session_id
        payload = {"status": "emergency_stopped", "reason": reason, "session_id": sid}
        if sid:
            await self._emit(sid, "neuroverse.runtime.emergency_stop", payload)
        return payload

    async def freeze_adaptation(self, reason: str = "manual freeze") -> dict[str, Any]:
        runtime_status.freeze(reason)
        sid = self._session_id
        payload = {"status": "frozen", "reason": reason, "session_id": sid}
        if sid:
            await self._emit(sid, "neuroverse.runtime.freeze", payload)
        return payload

    async def unfreeze_adaptation(self) -> dict[str, Any]:
        ok, reason = runtime_status.unfreeze()
        sid = self._session_id
        payload = {
            "status": "unfrozen" if ok else "blocked",
            "reason": reason,
            "session_id": sid,
        }
        if ok and sid:
            await self._emit(sid, "neuroverse.runtime.unfreeze", payload)
        return payload

    async def _run_loop(self, session_id: str) -> None:
        simulator = BiosignalSimulator(
            duration_s=settings.session_duration_s,
            tick_interval_ms=settings.tick_interval_ms,
        )
        await simulator.start()

        estimator = load_active_estimator()
        safety_gate = SafetyGate()
        policy = AdaptationPolicy(
            max_delta=settings.max_intensity_delta,
            cooldown_ms=settings.action_cooldown_ms,
            smoothing_window=settings.smoothing_window,
        )

        try:
            while self._running and simulator.is_running():
                t_start = time.monotonic()

                stage_start = time.perf_counter()
                window = await simulator.get_window()
                acquisition_ms = (time.perf_counter() - stage_start) * 1000.0
                ts = self._clock.elapsed()

                eeg_d, eeg_n, physio_d, physio_n, gaze_d, gaze_n = _split_channels(
                    window.data, window.channel_names
                )

                stage_start = time.perf_counter()
                eeg_feats = extract_eeg_features(eeg_d, eeg_n, window.sampling_rate)
                physio_feats = extract_physio_features(physio_d, physio_n)
                gaze_feats = extract_gaze_features(gaze_d, gaze_n)
                multi_feats = extract_multimodal_features(eeg_feats, physio_feats, gaze_feats)
                feature_ms = (time.perf_counter() - stage_start) * 1000.0

                stage_start = time.perf_counter()
                eeg_sqi = compute_eeg_sqi(eeg_d, eeg_n)
                physio_sqi = compute_physio_sqi(physio_d, physio_n)
                gaze_sqi = compute_gaze_sqi(gaze_d, gaze_n)
                multimodal_sqi = compute_multimodal_sqi(eeg_sqi, physio_sqi, gaze_sqi)
                sqi_ms = (time.perf_counter() - stage_start) * 1000.0

                sqi_scores = {
                    "eeg": round(eeg_sqi, 4),
                    "physio": round(physio_sqi, 4),
                    "gaze": round(gaze_sqi, 4),
                    "multimodal": round(multimodal_sqi, 4),
                }
                telemetry.record_sqi(sqi_scores)

                features = FeaturePayload(
                    eeg=eeg_feats,
                    physio=physio_feats,
                    gaze=gaze_feats,
                    multimodal=multi_feats,
                    sqi_scores=sqi_scores,
                )

                await self._emit(
                    session_id,
                    "neuroverse.features.extracted",
                    features.model_dump(),
                    ts,
                )

                stage_start = time.perf_counter()
                prediction = estimator.predict(features)
                inference_ms = (time.perf_counter() - stage_start) * 1000.0
                pred_dict = prediction.model_dump()
                await self._emit(session_id, "neuroverse.state.predicted", pred_dict, ts)

                stage_start = time.perf_counter()
                safety_decision = safety_gate.evaluate(
                    prediction, sqi_scores, policy.action_history
                )
                safety_ms = (time.perf_counter() - stage_start) * 1000.0
                safety_dict = safety_decision.model_dump()
                runtime_status.set_last_safety(safety_dict)
                await self._emit(session_id, "neuroverse.safety.decision", safety_dict, ts)

                stage_start = time.perf_counter()
                if runtime_status.is_adaptation_frozen():
                    action = AdaptationActionPayload(
                        action="FreezeAdaptation",
                        intensity=0.0,
                        duration_ms=settings.tick_interval_ms,
                        source_state="runtime_control",
                        reason="Adaptation frozen by runtime safety control",
                    )
                else:
                    action = policy.decide(prediction, safety_decision)
                policy_ms = (time.perf_counter() - stage_start) * 1000.0
                action_dict = action.model_dump()
                runtime_status.set_last_action(action_dict)
                await self._emit(session_id, "neuroverse.adaptation.action", action_dict, ts)
                telemetry.record_tick(
                    {
                        "acquisition": acquisition_ms,
                        "feature_extraction": feature_ms,
                        "signal_quality": sqi_ms,
                        "inference": inference_ms,
                        "safety": safety_ms,
                        "policy": policy_ms,
                    }
                )

                elapsed = time.monotonic() - t_start
                sleep_time = max(0, settings.tick_interval_s - elapsed)
                await asyncio.sleep(sleep_time)

                if self._clock.elapsed() >= settings.session_duration_s:
                    break

        except asyncio.CancelledError:
            pass
        except Exception:
            logger.exception("Engine error in session %s", session_id)
        finally:
            await simulator.stop()
            if self._running:
                self._running = False

    async def _emit(
        self, session_id: str, event_type: str, payload: dict, timestamp: float | None = None
    ) -> None:
        event = BaseEvent(
            session_id=session_id,
            event_type=event_type,  # type: ignore[arg-type]
            timestamp=timestamp if timestamp is not None else self._clock.elapsed(),
            source="engine",
            payload=payload,
        )
        if self._recorder:
            self._recorder.record(event)
        if self._broadcast:
            broadcast_start = time.perf_counter()
            await self._broadcast(event.model_dump())
            telemetry.record_latency(
                "websocket_broadcast",
                (time.perf_counter() - broadcast_start) * 1000.0,
            )
        telemetry.record_event(event_type, payload)
