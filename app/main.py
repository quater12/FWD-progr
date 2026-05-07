"""
Точка входу FastAPI: роутери, CORS, Prometheus, кастомна метрика.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import settings
from app.routes_store import router as store_router
from app.db.session import AsyncSessionLocal
from app.metrics import refresh_orders_total_value


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with AsyncSessionLocal() as session:
        try:
            await refresh_orders_total_value(session)
        except Exception:
            pass
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI + PostgreSQL (async), JWT, Alembic, Prometheus/Grafana",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app, include_in_schema=False, endpoint="/metrics")
app.include_router(store_router)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": "FastAPI shop API",
        "version": "0.1.0",
        "store": "/store",
        "docs": "/docs",
        "metrics": "/metrics",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
