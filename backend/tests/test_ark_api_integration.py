from collections.abc import Iterator
from pathlib import Path

from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.ark import ArkAIService, ProviderClient, ProviderRequest
from app.controllers.follow_up import get_follow_up_ai_service
from app.controllers.matching_analysis import get_matching_ai_service
from app.db.models import Conversation, ConversationMessage
from app.main import app

VALID_JOB_DESCRIPTION = (
    "我们正在招聘一名 AI 产品经理，负责大模型产品需求分析、方案设计、研发落地和持续迭代，"
    "并能够清楚说明候选人经验与每项岗位要求之间的证据关系。"
)


def valid_follow_up_result() -> dict[str, object]:
    return {
        "answerability": "answerable",
        "answer": "简历记录了相关 AI 产品经历。",
        "evidence": [
            {
                "evidenceText": "负责大模型测试与评估平台",
                "sourceReference": "工作经历",
            }
        ],
        "missingInformation": None,
    }


class FakeProvider(ProviderClient):
    def __init__(self, responses: list[object]) -> None:
        self._responses: Iterator[object] = iter(responses)
        self.requests: list[ProviderRequest] = []

    def complete(self, request: ProviderRequest) -> object:
        self.requests.append(request)
        return next(self._responses)


def ark_service(provider: ProviderClient) -> ArkAIService:
    return ArkAIService(
        api_key=SecretStr("test-only-secret"),
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        model="doubao-seed-2-1-pro-260628",
        request_timeout_seconds=60,
        provider_client=provider,
    )


def get_messages(db_session: Session, conversation_id: str) -> list[ConversationMessage]:
    return list(
        db_session.scalars(
            select(ConversationMessage)
            .where(ConversationMessage.conversation_id == conversation_id)
            .order_by(ConversationMessage.created_at, ConversationMessage.id)
        )
    )


def test_matching_validation_exhaustion_returns_exact_safe_error_and_rolls_back(
    client: TestClient,
    db_session: Session,
) -> None:
    provider = FakeProvider([{"invalid": "first"}, {"invalid": "second"}])
    service = ark_service(provider)

    def override_ai_service() -> ArkAIService:
        return service

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
    assert len(provider.requests) == 2
    assert db_session.scalar(select(Conversation)) is None
    assert db_session.scalar(select(ConversationMessage)) is None


def test_follow_up_validation_exhaustion_rolls_back_question_and_answer(
    client: TestClient,
    db_session: Session,
) -> None:
    report_response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )
    assert report_response.status_code == 200
    conversation_id = report_response.json()["conversationId"]
    provider = FakeProvider([{"invalid": "first"}, {"invalid": "second"}])
    service = ark_service(provider)

    def override_ai_service() -> ArkAIService:
        return service

    app.dependency_overrides[get_follow_up_ai_service] = override_ai_service

    response = client.post(
        f"/api/conversations/{conversation_id}/messages",
        json={"question": "候选人有哪些 AI 产品经验？"},
    )

    assert response.status_code == 503
    assert response.json() == {
        "code": "AI_SERVICE_UNAVAILABLE",
        "message": "追问暂时无法回答，请稍后重试。",
    }
    assert len(provider.requests) == 2
    assert [message.message_type for message in get_messages(db_session, conversation_id)] == [
        "job_description",
        "matching_analysis",
    ]


def test_completed_identical_follow_up_replays_without_another_provider_call(
    client: TestClient,
    db_session: Session,
) -> None:
    report_response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )
    assert report_response.status_code == 200
    conversation_id = report_response.json()["conversationId"]
    provider = FakeProvider([valid_follow_up_result()])
    service = ark_service(provider)

    def override_ai_service() -> ArkAIService:
        return service

    app.dependency_overrides[get_follow_up_ai_service] = override_ai_service
    endpoint = f"/api/conversations/{conversation_id}/messages"
    payload = {"question": "候选人有哪些 AI 产品经验？"}

    committed_response = client.post(endpoint, json=payload)
    replayed_response = client.post(endpoint, json=payload)

    assert committed_response.status_code == 200
    assert set(committed_response.json()) == {"messageId", "content"}
    assert replayed_response.json() == committed_response.json()
    assert len(provider.requests) == 1
    assert [message.message_type for message in get_messages(db_session, conversation_id)] == [
        "job_description",
        "matching_analysis",
        "follow_up_question",
        "follow_up_answer",
    ]


def test_fixed_repository_resume_pair_is_available() -> None:
    resume_directory = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "resources"
        / "resume"
    )

    assert (resume_directory / "mei_chang_resume.pdf").is_file()
    assert (resume_directory / "mei_chang_resume.md").is_file()
