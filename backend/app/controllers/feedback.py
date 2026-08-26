from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.api.errors import raise_api_error
from app.db.session import get_db_session
from app.repositories.conversations import ConversationRepository
from app.services.feedback import (
    FeedbackPersistenceError,
    FeedbackService,
    FeedbackTargetNotFoundError,
)

router = APIRouter(prefix="/api", tags=["feedback"])


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    conversation_id: str = Field(alias="conversationId", min_length=1, max_length=64)
    message_id: str = Field(alias="messageId", min_length=1, max_length=64)
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=2000)


class FeedbackResponse(BaseModel):
    success: Literal[True]


def get_feedback_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> FeedbackService:
    return FeedbackService(ConversationRepository(session))


@router.post("/feedback", response_model=FeedbackResponse)
def submit_feedback(
    request: FeedbackRequest,
    service: Annotated[FeedbackService, Depends(get_feedback_service)],
) -> FeedbackResponse:
    try:
        service.submit(
            conversation_id=request.conversation_id,
            message_id=request.message_id,
            rating=request.rating,
            comment=request.comment,
        )
    except FeedbackTargetNotFoundError:
        raise_api_error(
            status_code=404,
            code="REPORT_NOT_FOUND",
            message="未找到对应的匹配报告，请重新生成报告后提交反馈。",
        )
    except FeedbackPersistenceError:
        raise_api_error(
            status_code=500,
            code="PERSISTENCE_ERROR",
            message="反馈暂时无法保存，请稍后重试。",
        )

    return FeedbackResponse(success=True)
