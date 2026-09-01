from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session

from app.api.errors import raise_api_error
from app.db.session import get_db_session
from app.repositories.tracking import TrackingRepository
from app.services.tracking import (
    TestModeService,
    TrackingConversationNotFoundError,
    TrackingEventConflictError,
    TrackingEventName,
    TrackingInvalidEventNameError,
    TrackingPersistenceError,
    TrackingService,
)

router = APIRouter(prefix="/api", tags=["tracking"])


class TrackingEventRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    event_id: str = Field(alias="eventId", min_length=1, max_length=64)
    event_name: TrackingEventName = Field(alias="eventName")
    session_id: str = Field(alias="sessionId", min_length=1, max_length=64)
    occurred_at: datetime = Field(alias="occurredAt")
    conversation_id: str | None = Field(
        default=None,
        alias="conversationId",
        min_length=1,
        max_length=64,
    )

    @field_validator("occurred_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurredAt must include a timezone")
        return value


class TrackingEventResponse(BaseModel):
    success: Literal[True]


class TestModeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    session_id: str = Field(alias="sessionId", min_length=1, max_length=64)


class TestModeResponse(BaseModel):
    success: Literal[True]
    session_id: str = Field(alias="sessionId")
    test_mode: Literal[True] = Field(alias="testMode")


def get_tracking_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> TrackingService:
    return TrackingService(TrackingRepository(session))


def get_test_mode_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> TestModeService:
    return TestModeService(TrackingRepository(session))


@router.post("/tracking-events", response_model=TrackingEventResponse)
def submit_tracking_event(
    request: TrackingEventRequest,
    service: Annotated[TrackingService, Depends(get_tracking_service)],
) -> TrackingEventResponse:
    try:
        service.submit(
            event_id=request.event_id,
            event_name=request.event_name,
            session_id=request.session_id,
            occurred_at=request.occurred_at,
            conversation_id=request.conversation_id,
        )
    except TrackingConversationNotFoundError:
        raise_api_error(
            status_code=404,
            code="CONVERSATION_NOT_FOUND",
            message="未找到行为事件对应的会话。",
        )
    except TrackingEventConflictError:
        raise_api_error(
            status_code=409,
            code="TRACKING_EVENT_CONFLICT",
            message="行为事件标识符已被其他事件使用。",
        )
    except TrackingInvalidEventNameError:
        raise_api_error(
            status_code=400,
            code="INVALID_REQUEST",
            message="行为事件格式无效。",
        )
    except TrackingPersistenceError:
        raise_api_error(
            status_code=500,
            code="PERSISTENCE_ERROR",
            message="行为事件暂时无法保存。",
        )

    return TrackingEventResponse(success=True)


@router.post("/tracking-sessions/test-mode", response_model=TestModeResponse)
def designate_test_mode(
    request: TestModeRequest,
    service: Annotated[TestModeService, Depends(get_test_mode_service)],
) -> TestModeResponse:
    try:
        service.designate(session_id=request.session_id)
    except TrackingPersistenceError:
        raise_api_error(
            status_code=500,
            code="PERSISTENCE_ERROR",
            message="测试模式暂时无法启用。",
        )
    return TestModeResponse(
        success=True,
        sessionId=request.session_id,
        testMode=True,
    )
