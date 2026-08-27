from fastapi import APIRouter

from app.controllers import feedback, follow_up, health, matching_analysis, resume, tracking

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(matching_analysis.router)
api_router.include_router(resume.router)
api_router.include_router(feedback.router)
api_router.include_router(follow_up.router)
api_router.include_router(tracking.router)
