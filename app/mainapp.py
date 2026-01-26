import os
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import get_settings_singleton
# from app.core.logging import setup_logger
from app.db.db_async import async_engine
from app.api import rou

# setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with async_engine.begin() as conn: pass
        yield
    finally:
        await async_engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings_singleton()
    if os.environ.get("SERPERDEV_API_KEY") != settings.SERPERDEV_API_KEY:os.environ["SERPERDEV_API_KEY"] = settings.SERPERDEV_API_KEY
    if os.environ.get("OPENAI_API_KEY") != settings.OPENAI_API_KEY:      os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    if os.environ.get("FINNHUB_API_KEY") != settings.FINNHUB_API_KEY:              os.environ["FINNHUB_API_KEY"] = settings.FINNHUB_API_KEY
    if os.environ.get("TAVILY_API_KEY") != settings.TAVILY_API_KEY:              os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/swagger",
        redoc_url="/swagger_redoc",
        # lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.ALLOWED_ORIGINS,
        # allow_credentials=True,
        allow_origins=["*"],
        allow_credentials=False,  # MUST be False when origins="*"
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(rou)

    return app