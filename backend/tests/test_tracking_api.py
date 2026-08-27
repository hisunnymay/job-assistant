import re
from datetime import UTC, datetime
from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.controllers.tracking import get_tracking_service
from app.db.models import Conversation, UserBehaviorEvent
from app.main import app
from app.services.tracking import TrackingPersistenceError

VALID_JOB_DESCRIPTION = (
    "我们正在招聘一名 AI 产品经理，负责大模型产品需求分析、方案设计、研发落地和持续迭代，"
    "并能够清楚说明候选人经验与每项岗位要求之间的证据关系。"
)


def tracking_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "eventId": "event_001",
        "eventName": "page_visit",
        "sessionId": "session_001",
        "occurredAt": "2026-08-27T01:02:03.000Z",
    }
    payload.update(overrides)
    return payload


def create_matching_report(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/matching-analysis",
        json={"jobDescription": VALID_JOB_DESCRIPTION},
    )
    assert response.status_code == 200
    return cast(dict[str, str], response.json())


def test_tracking_event_is_persisted_with_only_the_approved_schema(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post("/api/tracking-events", json=tracking_payload())

    assert response.status_code == 200
    assert response.json() == {"success": True}
    event = db_session.scalar(select(UserBehaviorEvent))
    assert event is not None
    assert event.id == "event_001"
    assert event.event_name == "page_visit"
    assert event.session_id == "session_001"
    assert event.occurred_at == datetime(2026, 8, 27, 1, 2, 3, tzinfo=UTC)
    assert event.received_at.tzinfo is not None
    assert re.fullmatch(r"[0-9a-f]{64}", event.request_fingerprint)
    assert event.conversation_id is None
    assert {column.name for column in inspect(UserBehaviorEvent).columns} == {
        "id",
        "event_name",
        "session_id",
        "occurred_at",
        "received_at",
        "request_fingerprint",
        "conversation_id",
    }


def test_tracking_event_can_reference_an_existing_conversation(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)

    response = client.post(
        "/api/tracking-events",
        json=tracking_payload(
            eventName="matching_report_generated",
            conversationId=report["conversationId"],
        ),
    )

    assert response.status_code == 200
    event = db_session.get(UserBehaviorEvent, "event_001")
    assert event is not None
    assert event.conversation_id == report["conversationId"]


def test_tracking_event_replay_is_idempotent(
    client: TestClient,
    db_session: Session,
) -> None:
    payload = tracking_payload()

    assert client.post("/api/tracking-events", json=payload).status_code == 200
    replay = client.post("/api/tracking-events", json=payload)

    assert replay.status_code == 200
    assert replay.json() == {"success": True}
    assert len(list(db_session.scalars(select(UserBehaviorEvent)))) == 1


def test_tracking_event_rejects_conflicting_identifier_reuse(
    client: TestClient,
    db_session: Session,
) -> None:
    assert client.post(
        "/api/tracking-events", json=tracking_payload()
    ).status_code == 200

    conflict = client.post(
        "/api/tracking-events",
        json=tracking_payload(eventName="resume_previewed"),
    )

    assert conflict.status_code == 409
    assert conflict.json() == {
        "code": "TRACKING_EVENT_CONFLICT",
        "message": "行为事件标识符已被其他事件使用。",
    }
    events = list(db_session.scalars(select(UserBehaviorEvent)))
    assert len(events) == 1
    assert events[0].event_name == "page_visit"


@pytest.mark.parametrize(
    "payload",
    [
        tracking_payload(eventName="unknown_event"),
        tracking_payload(occurredAt="2026-08-27T01:02:03"),
        tracking_payload(sessionId=""),
    ],
)
def test_tracking_event_rejects_invalid_payloads(
    client: TestClient,
    db_session: Session,
    payload: dict[str, object],
) -> None:
    response = client.post("/api/tracking-events", json=payload)

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_REQUEST",
        "message": "行为事件格式无效。",
    }
    assert db_session.scalar(select(UserBehaviorEvent)) is None


def test_tracking_event_rejects_content_fields_instead_of_persisting_them(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/api/tracking-events",
        json=tracking_payload(jobDescription="不得进入事件存储"),
        headers={"User-Agent": "must-not-be-persisted"},
    )

    assert response.status_code == 400
    assert "不得进入事件存储" not in response.text
    assert "must-not-be-persisted" not in response.text
    assert db_session.scalar(select(UserBehaviorEvent)) is None


def test_tracking_event_rejects_unknown_conversation(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/api/tracking-events",
        json=tracking_payload(conversationId="conversation_missing"),
    )

    assert response.status_code == 404
    assert response.json() == {
        "code": "CONVERSATION_NOT_FOUND",
        "message": "未找到行为事件对应的会话。",
    }
    assert db_session.scalar(select(UserBehaviorEvent)) is None


def test_deleting_conversation_preserves_event_and_clears_association(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)
    assert client.post(
        "/api/tracking-events",
        json=tracking_payload(conversationId=report["conversationId"]),
    ).status_code == 200

    conversation = db_session.get(Conversation, report["conversationId"])
    assert conversation is not None
    db_session.delete(conversation)
    db_session.commit()
    db_session.expire_all()

    event = db_session.get(UserBehaviorEvent, "event_001")
    assert event is not None
    assert event.conversation_id is None


def test_identical_replay_remains_idempotent_after_conversation_deletion(
    client: TestClient,
    db_session: Session,
) -> None:
    report = create_matching_report(client)
    payload = tracking_payload(conversationId=report["conversationId"])
    assert client.post("/api/tracking-events", json=payload).status_code == 200

    conversation = db_session.get(Conversation, report["conversationId"])
    assert conversation is not None
    db_session.delete(conversation)
    db_session.commit()
    db_session.expire_all()

    replay = client.post("/api/tracking-events", json=payload)
    conflict = client.post(
        "/api/tracking-events",
        json={**payload, "sessionId": "session_different"},
    )

    assert replay.status_code == 200
    assert replay.json() == {"success": True}
    assert conflict.status_code == 409
    assert len(list(db_session.scalars(select(UserBehaviorEvent)))) == 1


class FailingTrackingService:
    def submit(self, **_kwargs: object) -> None:
        raise TrackingPersistenceError


def test_tracking_storage_failure_uses_safe_error_contract(client: TestClient) -> None:
    def override_tracking_service() -> FailingTrackingService:
        return FailingTrackingService()

    app.dependency_overrides[get_tracking_service] = override_tracking_service

    response = client.post("/api/tracking-events", json=tracking_payload())

    assert response.status_code == 500
    assert response.json() == {
        "code": "PERSISTENCE_ERROR",
        "message": "行为事件暂时无法保存。",
    }
