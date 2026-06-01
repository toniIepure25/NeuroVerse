from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("NeuroVerse backend starting up")
    _run_startup_safety_inference()
    yield
    logger.info("NeuroVerse backend shutting down")


def _run_startup_safety_inference() -> None:
    """Load report evidence and infer initial safety state at startup."""
    try:
        from app.safety.report_status import get_cached_report_evidence  # noqa: PLC0415
        from app.safety.state_machine import safety_state_machine  # noqa: PLC0415

        ev, cache_meta = get_cached_report_evidence(force_refresh=True)
        state = safety_state_machine.infer_from_evidence(ev)
        logger.info(
            "Startup safety inference: state=%s sources=%d warnings=%d",
            state,
            len(ev.evidence_sources),
            len(ev.evidence_warnings),
        )
        for warning in ev.evidence_warnings:
            logger.warning("Safety evidence warning: %s", warning)
    except Exception:
        logger.exception("Startup safety inference failed; state machine remains at default")


def create_app() -> FastAPI:
    application = FastAPI(
        title="NeuroVerse",
        description="Multimodal Biosensing and Adaptive Neuroadaptive Interface Platform",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.routes_acquisition import router as acquisition_router
    from app.api.routes_calibration import router as calibration_router
    from app.api.routes_config import router as config_router
    from app.api.routes_data_sources import router as data_sources_router
    from app.api.routes_datasets import router as datasets_router
    from app.api.routes_evaluation import router as evaluation_router
    from app.api.routes_fusion import router as fusion_router
    from app.api.routes_hardware_trials import router as hardware_trials_router
    from app.api.routes_health import router as health_router
    from app.api.routes_imagina import router as imagina_router
    from app.api.routes_models import router as models_router
    from app.api.routes_protocols import router as protocols_router
    from app.api.routes_replay import router as replay_router
    from app.api.routes_runtime import router as runtime_router
    from app.api.routes_safety import router as safety_router
    from app.api.routes_sessions import router as sessions_router
    from app.api.routes_shadow import router as shadow_router
    from app.api.routes_stream import router as stream_router

    application.include_router(health_router)
    application.include_router(config_router)
    application.include_router(data_sources_router)
    application.include_router(sessions_router)
    application.include_router(stream_router)
    application.include_router(replay_router)
    application.include_router(datasets_router)
    application.include_router(models_router)
    application.include_router(evaluation_router)
    application.include_router(fusion_router)
    application.include_router(imagina_router)
    application.include_router(runtime_router)
    application.include_router(acquisition_router)
    application.include_router(hardware_trials_router)
    application.include_router(calibration_router)
    application.include_router(shadow_router)
    application.include_router(safety_router)
    application.include_router(protocols_router)

    return application


app = create_app()
