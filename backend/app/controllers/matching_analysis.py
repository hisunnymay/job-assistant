from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.ai.matching import MatchingAIService
from app.ai.mock import MockAIService
from app.api.errors import raise_api_error
from app.db.session import get_db_session
from app.repositories.conversations import ConversationRepository
from app.resources.candidate_resume import get_candidate_resume_path
from app.services.matching_analysis import (
    MatchingAnalysisPersistenceError,
    MatchingAnalysisService,
    MatchingAnalysisUnavailableError,
)

router = APIRouter(prefix="/api", tags=["matching-analysis"])


class MatchingAnalysisRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    job_description: str = Field(alias="jobDescription", min_length=40, max_length=6000)


class MatchingAnalysisResponse(BaseModel):
    conversation_id: str = Field(serialization_alias="conversationId")
    message_id: str = Field(serialization_alias="messageId")
    content: str


def get_ai_service() -> MatchingAIService:
    return MockAIService()


def get_matching_analysis_service(
    session: Annotated[Session, Depends(get_db_session)],
    ai_service: Annotated[MatchingAIService, Depends(get_ai_service)],
) -> MatchingAnalysisService:
    return MatchingAnalysisService(
        repository=ConversationRepository(session),
        ai_service=ai_service,
        resume_path=get_candidate_resume_path(),
    )


@router.post("/matching-analysis", response_model=MatchingAnalysisResponse)
def generate_matching_analysis(
    request: MatchingAnalysisRequest,
    service: Annotated[MatchingAnalysisService, Depends(get_matching_analysis_service)],
) -> MatchingAnalysisResponse:
    try:
        result = service.generate(request.job_description)
    except MatchingAnalysisUnavailableError:
        raise_api_error(
            status_code=503,
            code="AI_SERVICE_UNAVAILABLE",
            message="匹配分析暂时不可用，请稍后重试。",
        )
    except MatchingAnalysisPersistenceError:
        raise_api_error(
            status_code=500,
            code="PERSISTENCE_ERROR",
            message="本次分析未能保存，请稍后重试。",
        )

    return MatchingAnalysisResponse(
        conversation_id=result.conversation_id,
        message_id=result.message_id,
        content=result.content,
    )
