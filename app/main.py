import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.routes import router
from app.config import get_settings
from app.models.database import init_db

settings = get_settings()
logging.basicConfig(level=settings.log_level)

FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FinAssistant MVP",
    description="AI Equity Research Agent — deterministic analytics + LLM narrative synthesis",
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/favicon.svg")
    async def favicon():
        path = FRONTEND_DIST / "favicon.svg"
        if path.exists():
            return FileResponse(path)
        raise HTTPException(status_code=404)

    @app.get("/")
    async def serve_frontend():
        return FileResponse(FRONTEND_DIST / "index.html")

else:

    @app.get("/")
    def root():
        return {
            "name": "FinAssistant MVP",
            "version": __version__,
            "docs": "/docs",
            "frontend": "Run 'cd frontend && npm install && npm run build' to enable UI",
            "endpoints": {
                "research": "POST /api/v1/research",
                "analytics": "GET /api/v1/analytics/{ticker}",
                "health": "GET /api/v1/health",
            },
        }
