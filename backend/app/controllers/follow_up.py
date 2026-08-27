from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.ai.dependencies import get_ai_service
from app.ai.follow_up import FollowUpAIService
from app.api.errors import raise_api_error
from app.db.session import get_db_session
from app.repositories.conversations import ConversationRepository
from app.resources.candidate_resume import get_candidate_resume_context_path
from app.services.follow_up import (
    FollowUpConversationNotFoundError,
    FollowUpPersistenceError,
    FollowUpService,
    FollowUpUnavailableError,
)

router = APIRouter(prefix="/api", tags=["follow-up"])
get_follow_up_ai_service = get_ai_service


class FollowUpRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=1, max_length=1000)


class FollowUpResponse(BaseModel):
    message_id: str = Field(serialization_alias="messageId")
    content: str


def get_follow_up_service(
    session: Annotated[Session, Depends(get_db_session)],
    ai_service: Annotated[FollowUpAIService, Depends(get_follow_up_ai_service)],
) -> FollowUpService:
    return FollowUpService(
        repository=ConversationRepository(session),
        ai_service=ai_service,
        resume_context_path=get_candidate_resume_context_path(),
    )


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=FollowUpResponse,
)
def answer_follow_up(
    conversation_id: str,
    request: FollowUpRequest,
    service: Annotated[FollowUpService, Depends(get_follow_up_service)],
) -> FollowUpResponse:
    try:
        result = service.answer(
            conversation_id=conversation_id,
            question=request.question,
        )
    except FollowUpConversationNotFoundError:
        raise_api_error(
            status_code=404,
            code="CONVERSATION_NOT_FOUND",
            message="未找到对应的匹配对话，请重新生成匹配报告。",
        )
    except FollowUpUnavailableError:
        raise_api_error(
            status_code=503,
            code="AI_SERVICE_UNAVAILABLE",
            message="追问暂时无法回答，请稍后重试。",
        )
    except FollowUpPersistenceError:
        raise_api_error(
            status_code=500,
            code="PERSISTENCE_ERROR",
            message="本次追问未能保存，请稍后重试。",
        )

    return FollowUpResponse(message_id=result.message_id, content=result.content)
