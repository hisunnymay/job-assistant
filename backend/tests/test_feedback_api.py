from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.controllers.feedback import get_feedback_service
from app.db.models import Feedback
from app.main import app
from app.services.feedback import FeedbackPersistenceError

VALID_JOB_DESCRIPTION = (
    "我们正在招聘一名 AI 产品经理，负责大模型产品需求分析、方案设计、研发落地和持续迭代，"
    "并能够清楚说明候选人经验与每项岗位要求之间的证据关系。"
)


def create_matching_report(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )
    assert response.status_code == 200
    return cast(dict[str, str], response.json())


@pytest.mark.parametrize("rating", [1, 5])
def test_feedback_is_persisted_against_the_matching_report(
    client: TestClient,
    db_session: Session,
    rating: int,
) -> None:
    report = create_matching_report(client)

    response = client.post(
        "/api/feedback",
        json={
            "conversationId": report["conversationId"],
            "messageId": report["messageId"],
            "rating": rating,
            "comment": "证据关系清楚，信息缺口也很明确。",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}
    feedback = db_session.scalar(select(Feedback))
    assert feedback is not None
    assert feedback.conversation_id == report["conversationId"]
    assert feedback.message_id == report["messageId"]
    assert feedback.rating == rating
    assert feedback.comment == "证据关系清楚，信息缺口也很明确。"


def test_feedback_retry_replays_success_without_duplicate_row(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)
    payload = {
        "conversationId": report["conversationId"],
        "messageId": report["messageId"],
        "rating": 5,
        "comment": "选择项：证据清晰可核验",
    }

    committed_response = client.post("/api/feedback", json=payload)
    retried_response = client.post("/api/feedback", json=payload)

    assert committed_response.status_code == 200
    assert retried_response.status_code == 200
    assert retried_response.json() == {"success": True}
    stored_feedback = list(db_session.scalars(select(Feedback)))
    assert len(stored_feedback) == 1
    assert stored_feedback[0].message_id == report["messageId"]
    assert stored_feedback[0].rating == 5
    assert stored_feedback[0].comment == "选择项：证据清晰可核验"


def test_feedback_rejects_invalid_format(client: TestClient) -> None:
    response = client.post(
        "/api/feedback",
        json={
            "conversationId": "conversation_001",
            "messageId": "message_002",
            "rating": 6,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_REQUEST",
        "message": "反馈格式无效，请检查评分和反馈内容。",
    }


def test_feedback_rejects_unknown_report_context(client: TestClient) -> None:
    response = client.post(
        "/api/feedback",
        json={
            "conversationId": "conversation_missing",
            "messageId": "message_missing",
            "rating": 4,
            "comment": "测试不存在的报告。",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "code": "REPORT_NOT_FOUND",
        "message": "未找到对应的匹配报告，请重新生成报告后提交反馈。",
    }


class FailingFeedbackService:
    def submit(self, **_kwargs: object) -> None:
        raise FeedbackPersistenceError


def test_feedback_storage_failure_is_safe(client: TestClient) -> None:
    def override_feedback_service() -> FailingFeedbackService:
        return FailingFeedbackService()

    app.dependency_overrides[get_feedback_service] = override_feedback_service

    response = client.post(
        "/api/feedback",
        json={
            "conversationId": "conversation_001",
            "messageId": "message_002",
            "rating": 4,
            "comment": "测试安全错误。",
        },
    )

    assert response.status_code == 500
    assert response.json() == {
        "code": "PERSISTENCE_ERROR",
        "message": "反馈暂时无法保存，请稍后重试。",
    }
