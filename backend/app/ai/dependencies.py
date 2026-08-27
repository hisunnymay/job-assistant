from typing import Annotated, Protocol

from fastapi import Depends

from app.ai.ark import ArkAIService
from app.ai.follow_up import FollowUpAIService
from app.ai.matching import MatchingAIService
from app.ai.mock import MockAIService
from app.core.config import Settings, get_settings


class AIService(MatchingAIService, FollowUpAIService, Protocol):
    """The single replaceable AI boundary used by both MVP workflows."""


def create_ai_service(settings: Settings) -> AIService:
    if settings.ai_provider == "mock":
        return MockAIService()
    api_key = settings.ark_api_key
    if api_key is None:
        raise RuntimeError("Validated Ark configuration is missing its API key")
    return ArkAIService(
        api_key=api_key,
        base_url=settings.ark_base_url,
        model=settings.ark_model,
        request_timeout_seconds=settings.ark_request_timeout_seconds,
    )


def get_ai_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> AIService:
    return create_ai_service(settings)
