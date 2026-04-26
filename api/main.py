from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from api.database import init_pool, close_pool
from api.routers import market


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_pool()
    yield
    close_pool()


app = FastAPI(
    title="efinmap API",
    description="Stock heatmap data API for efinmap.com",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — comma-separated origins from env. Defaults to production domain only.
# For local dev set: CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
_default_origins = "https://efinmap.com,https://www.efinmap.com"
allow_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", _default_origins).split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api/v1")

# Frontend is normally served by nginx in production. Set SERVE_STATIC=1 to also
# serve it from FastAPI (useful for local development without nginx).
if os.getenv("SERVE_STATIC") == "1":
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
    if os.path.isdir(frontend_path):
        app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
