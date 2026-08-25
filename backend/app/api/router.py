from fastapi import APIRouter

from app.controllers import health, matching_analysis

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(matching_analysis.router)
