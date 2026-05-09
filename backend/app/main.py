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
    yield
    logger.info("NeuroVerse backend shutting down")


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
    from app.api.routes_datasets import router as datasets_router
    from app.api.routes_evaluation import router as evaluation_router
    from app.api.routes_hardware_trials import router as hardware_trials_router
    from app.api.routes_health import router as health_router
    from app.api.routes_models import router as models_router
    from app.api.routes_replay import router as replay_router
    from app.api.routes_runtime import router as runtime_router
    from app.api.routes_sessions import router as sessions_router
    from app.api.routes_shadow import router as shadow_router
    from app.api.routes_stream import router as stream_router

    application.include_router(health_router)
    application.include_router(config_router)
    application.include_router(sessions_router)
    application.include_router(stream_router)
    application.include_router(replay_router)
    application.include_router(datasets_router)
    application.include_router(models_router)
    application.include_router(evaluation_router)
    application.include_router(runtime_router)
    application.include_router(acquisition_router)
    application.include_router(hardware_trials_router)
    application.include_router(calibration_router)
    application.include_router(shadow_router)

    return application


app = create_app()
