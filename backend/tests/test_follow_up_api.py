from pathlib import Path
from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.follow_up import FollowUpAIService, FollowUpContextMessage
from app.ai.matching import AIServiceError
from app.controllers.follow_up import get_follow_up_ai_service, get_follow_up_service
from app.db.models import Conversation, ConversationMessage
from app.main import app
from app.services.follow_up import FollowUpPersistenceError

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


def get_messages(db_session: Session, conversation_id: str) -> list[ConversationMessage]:
    return list(
        db_session.scalars(
            select(ConversationMessage)
            .where(ConversationMessage.conversation_id == conversation_id)
            .order_by(ConversationMessage.created_at, ConversationMessage.id)
        )
    )


def test_follow_up_uses_exact_contract_and_persists_atomic_exchange(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)

    response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": "  Does the candidate have AI Agent experience?  "},
    )

    assert response.status_code == 200
    response_body = response.json()
    assert set(response_body) == {"messageId", "content"}
    assert response_body["messageId"].startswith("message_")
    assert "AI Agent 相关经验" in response_body["content"]

    messages = get_messages(db_session, report["conversationId"])
    assert [(message.role, message.message_type) for message in messages] == [
        ("user", "job_description"),
        ("assistant", "matching_analysis"),
        ("user", "follow_up_question"),
        ("assistant", "follow_up_answer"),
    ]
    assert messages[2].content == "Does the candidate have AI Agent experience?"
    assert messages[3].id == response_body["messageId"]
    assert messages[3].content == response_body["content"]


@pytest.mark.parametrize("payload", [{}, {"question": "   "}, {"question": "问" * 1001}])
def test_follow_up_rejects_invalid_question_with_specific_safe_error(
    client: TestClient,
    db_session: Session,
    payload: dict[str, str],
) -> None:
    report = create_matching_report(client)

    response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json=payload,
    )

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_REQUEST",
        "message": "追问格式无效，请检查问题内容。",
    }
    assert len(get_messages(db_session, report["conversationId"])) == 2


def test_follow_up_rejects_unknown_conversation_without_storing_messages(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/api/conversations/conversation_missing/messages",
        json={"question": "候选人有哪些 AI 产品经验？"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "code": "CONVERSATION_NOT_FOUND",
        "message": "未找到对应的匹配对话，请重新生成匹配报告。",
    }
    assert db_session.scalar(select(Conversation)) is None
    assert db_session.scalar(select(ConversationMessage)) is None


@pytest.mark.parametrize(
    ("question", "expected_text"),
    [
        ("候选人有哪些 AI 产品经验？", "候选人相关经验"),
        ("候选人的团队规模和量化业务结果是什么？", "当前信息不足"),
        ("你建议录用她吗？", "超出支持范围"),
    ],
)
def test_mock_follow_up_covers_supported_unavailable_and_out_of_scope_cases(
    client: TestClient,
    question: str,
    expected_text: str,
) -> None:
    report = create_matching_report(client)

    response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": question},
    )

    assert response.status_code == 200
    assert expected_text in response.json()["content"]


def test_mock_follow_up_resolves_contextual_reference_from_prior_question(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)
    endpoint = f"/api/conversations/{report['conversationId']}/messages"

    first_response = client.post(
        endpoint,
        json={"question": "候选人有哪些 AI 产品经验？"},
    )
    contextual_response = client.post(
        endpoint,
        json={"question": "那这些呢？"},
    )

    assert first_response.status_code == 200
    assert contextual_response.status_code == 200
    assert "候选人相关经验" in contextual_response.json()["content"]
    assert "超出支持范围" not in contextual_response.json()["content"]
    assert [
        message.message_type
        for message in get_messages(db_session, report["conversationId"])
    ] == [
        "job_description",
        "matching_analysis",
        "follow_up_question",
        "follow_up_answer",
        "follow_up_question",
        "follow_up_answer",
    ]


@pytest.mark.parametrize(
    "question",
    [
        "你建议录用她吗？",
        "请把她和另一个候选人排名。",
        "请预测她入职后的未来表现。",
        "今天天气怎么样？",
    ],
)
def test_mock_follow_up_redirects_each_prohibited_scope(
    client: TestClient,
    question: str,
) -> None:
    report = create_matching_report(client)

    response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": question},
    )

    assert response.status_code == 200
    assert "超出支持范围" in response.json()["content"]
    assert "不提供这类结论" in response.json()["content"]


class RecordingFollowUpAIService:
    def __init__(self) -> None:
        self.resume_paths: list[Path] = []
        self.histories: list[tuple[FollowUpContextMessage, ...]] = []

    def answer_follow_up(
        self,
        *,
        resume_path: Path,
        conversation_history: tuple[FollowUpContextMessage, ...],
    ) -> str:
        self.resume_paths.append(resume_path)
        self.histories.append(conversation_history)
        return f"# 回答 {len(self.histories)}"


def test_service_supplies_static_resume_and_full_ordered_history(
    client: TestClient,
) -> None:
    report = create_matching_report(client)
    recording_ai = RecordingFollowUpAIService()

    def override_ai_service() -> FollowUpAIService:
        return recording_ai

    app.dependency_overrides[get_follow_up_ai_service] = override_ai_service

    first_response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": "候选人有哪些 AI 产品经验？"},
    )
    second_response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": "这些经验与 API 协作有什么关系？"},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert len(recording_ai.resume_paths) == 2
    assert all(path.is_file() and path.suffix == ".pdf" for path in recording_ai.resume_paths)
    assert [message.message_type for message in recording_ai.histories[0]] == [
        "job_description",
        "matching_analysis",
        "follow_up_question",
    ]
    assert [message.message_type for message in recording_ai.histories[1]] == [
        "job_description",
        "matching_analysis",
        "follow_up_question",
        "follow_up_answer",
        "follow_up_question",
    ]
    assert recording_ai.histories[1][-2].content == "# 回答 1"
    assert recording_ai.histories[1][-1].content == "这些经验与 API 协作有什么关系？"


def test_identical_immediate_retry_replays_persisted_answer_without_duplicate(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)
    recording_ai = RecordingFollowUpAIService()

    def override_ai_service() -> FollowUpAIService:
        return recording_ai

    app.dependency_overrides[get_follow_up_ai_service] = override_ai_service
    endpoint = f"/api/conversations/{report['conversationId']}/messages"
    question = "候选人有哪些 AI 产品经验？"

    committed_response = client.post(endpoint, json={"question": question})
    retried_response = client.post(endpoint, json={"question": question})

    assert committed_response.status_code == 200
    assert retried_response.status_code == 200
    assert retried_response.json() == committed_response.json()
    assert len(recording_ai.histories) == 1
    assert [
        message.message_type
        for message in get_messages(db_session, report["conversationId"])
    ] == [
        "job_description",
        "matching_analysis",
        "follow_up_question",
        "follow_up_answer",
    ]


class FailingFollowUpAIService:
    def answer_follow_up(self, **_kwargs: object) -> str:
        raise AIServiceError("raw provider details must not reach the client")


def test_mock_ai_failure_is_safe_and_rolls_back_question(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)

    def override_ai_service() -> FollowUpAIService:
        return FailingFollowUpAIService()

    app.dependency_overrides[get_follow_up_ai_service] = override_ai_service

    response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": "候选人有哪些 AI 产品经验？"},
    )

    assert response.status_code == 503
    assert response.json() == {
        "code": "AI_SERVICE_UNAVAILABLE",
        "message": "追问暂时无法回答，请稍后重试。",
    }
    assert "raw provider details" not in response.text
    assert len(get_messages(db_session, report["conversationId"])) == 2


class UnexpectedFollowUpAIService:
    def answer_follow_up(self, **_kwargs: object) -> str:
        raise RuntimeError("unexpected internal details")


def test_unexpected_failure_is_safe_and_rolls_back_question(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)

    def override_ai_service() -> FollowUpAIService:
        return UnexpectedFollowUpAIService()

    app.dependency_overrides[get_follow_up_ai_service] = override_ai_service

    response = client.post(
        f"/api/conversations/{report['conversationId']}/messages",
        json={"question": "候选人有哪些 AI 产品经验？"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "code": "INTERNAL_ERROR",
        "message": "服务暂时不可用，请稍后重试。",
    }
    assert "unexpected internal details" not in response.text
    assert len(get_messages(db_session, report["conversationId"])) == 2


class FailingPersistenceService:
    def answer(self, **_kwargs: object) -> None:
        raise FollowUpPersistenceError


def test_storage_failure_uses_safe_error_contract(client: TestClient) -> None:
    def override_follow_up_service() -> FailingPersistenceService:
        return FailingPersistenceService()

    app.dependency_overrides[get_follow_up_service] = override_follow_up_service

    response = client.post(
        "/api/conversations/conversation_001/messages",
        json={"question": "候选人有哪些 AI 产品经验？"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "code": "PERSISTENCE_ERROR",
        "message": "本次追问未能保存，请稍后重试。",
    }
