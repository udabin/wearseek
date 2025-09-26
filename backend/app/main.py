# backend/app/main.py

from fastapi import FastAPI
from app.api.routes_search import router as search_router
from app.api.routes_health import router as health_router

app = FastAPI(title="WearSeek API")

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(search_router, prefix="/api", tags=["search"])