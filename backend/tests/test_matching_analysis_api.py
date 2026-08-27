import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.matching import AIServiceError, MatchingAIService
from app.controllers.matching_analysis import (
    get_matching_ai_service,
    get_matching_analysis_service,
)
from app.db.models import Conversation, ConversationMessage
from app.main import app
from app.services.matching_analysis import MatchingAnalysisPersistenceError

VALID_JOB_DESCRIPTION = (
    "我们正在招聘一名 AI 产品经理，负责大模型产品需求分析、方案设计、研发落地和持续迭代，"
    "并能够清楚说明候选人经验与每项岗位要求之间的证据关系。"
)


def test_matching_analysis_persists_conversation_and_messages(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )

    assert response.status_code == 200
    response_body = response.json()
    assert set(response_body) == {"conversationId", "messageId", "content"}
    assert response_body["conversationId"].startswith("conversation_")
    assert response_body["messageId"].startswith("message_")
    assert "有明确证据" in response_body["content"]
    assert "信息缺失" in response_body["content"]

    conversation = db_session.scalar(
        select(Conversation).where(Conversation.id == response_body["conversationId"])
    )
    messages = list(
        db_session.scalars(
            select(ConversationMessage)
            .where(ConversationMessage.conversation_id == response_body["conversationId"])
            .order_by(ConversationMessage.created_at)
        )
    )

    assert conversation is not None
    assert [(message.role, message.message_type) for message in messages] == [
        ("user", "job_description"),
        ("assistant", "matching_analysis"),
    ]
    assert messages[0].content == VALID_JOB_DESCRIPTION
    assert messages[1].id == response_body["messageId"]
    assert messages[1].content == response_body["content"]


@pytest.mark.parametrize("payload", [{}, {"jobDescription": "内容过短"}])
def test_matching_analysis_rejects_invalid_request(
    client: TestClient,
    db_session: Session,
    payload: dict[str, str],
) -> None:
    response = client.post("/api/matching-analysis", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_REQUEST",
        "message": "请求格式无效，请检查职位描述。",
    }
    assert db_session.scalar(select(Conversation)) is None


class FailingAIService:
    def generate_matching_analysis(self, **_kwargs: object) -> str:
        raise AIServiceError("raw provider details must not reach the client")


def test_mock_ai_failure_is_safe_and_rolls_back(
    client: TestClient,
    db_session: Session,
) -> None:
    def override_ai_service() -> MatchingAIService:
        return FailingAIService()

    app.dependency_overrides[get_matching_ai_service] = override_ai_service

    response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )

    assert response.status_code == 503
    assert response.json() == {
        "code": "AI_SERVICE_UNAVAILABLE",
        "message": "匹配分析暂时不可用，请稍后重试。",
    }
    assert "raw provider details" not in response.text
    assert db_session.scalar(select(Conversation)) is None


class FailingPersistenceService:
    def generate(self, _job_description: str) -> None:
        raise MatchingAnalysisPersistenceError


def test_storage_failure_uses_safe_error_contract(client: TestClient) -> None:
    def override_matching_service() -> FailingPersistenceService:
        return FailingPersistenceService()

    app.dependency_overrides[get_matching_analysis_service] = override_matching_service

    response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )

    assert response.status_code == 500
    assert response.json() == {
        "code": "PERSISTENCE_ERROR",
        "message": "本次分析未能保存，请稍后重试。",
    }
