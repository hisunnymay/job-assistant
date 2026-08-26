from fastapi import APIRouter

from app.controllers import feedback, health, matching_analysis, resume

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(matching_analysis.router)
api_router.include_router(resume.router)
api_router.include_router(feedback.router)
