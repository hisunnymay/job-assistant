from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.controllers.dashboard import get_analytics_service
from app.db.models import TrackingSession, UserBehaviorEvent
from app.main import app
from app.repositories.tracking import TrackingRepository
from app.services.analytics import AnalyticsService
from app.services.tracking import TrackingPersistenceError


def submit_event(
    client: TestClient,
    *,
    event_id: str,
    event_name: str,
    session_id: str,
    occurred_at: str,
) -> None:
    response = client.post(
        "/api/tracking-events",
        json={
            "eventId": event_id,
            "eventName": event_name,
            "sessionId": session_id,
            "occurredAt": occurred_at,
        },
    )
    assert response.status_code == 200


def test_dashboard_returns_six_totals_distinct_conversion_and_no_identifiers(
    client: TestClient,
) -> None:
    submit_event(
        client,
        event_id="report_1a",
        event_name="matching_report_generated",
        session_id="normal_1",
        occurred_at="2026-09-01T01:00:00Z",
    )
    submit_event(
        client,
        event_id="report_1b",
        event_name="matching_report_generated",
        session_id="normal_1",
        occurred_at="2026-09-01T02:00:00Z",
    )
    submit_event(
        client,
        event_id="contact_1",
        event_name="contact_cta_clicked",
        session_id="normal_1",
        occurred_at="2026-09-01T03:00:00Z",
    )
    submit_event(
        client,
        event_id="report_2",
        event_name="matching_report_generated",
        session_id="normal_2",
        occurred_at="2026-09-01T04:00:00Z",
    )
    submit_event(
        client,
        event_id="contact_only",
        event_name="contact_cta_clicked",
        session_id="contact_only_session",
        occurred_at="2026-09-01T05:00:00Z",
    )

    response = client.get("/api/dashboard")
    body = response.json()

    assert response.status_code == 200
    assert body["reportingPeriod"] == {
        "mode": "all_retained",
        "startDate": None,
        "endDate": None,
        "timezone": "Asia/Shanghai",
    }
    assert body["contactConversion"] == {
        "rate": 0.5,
        "numerator": 1,
        "denominator": 2,
    }
    assert body["eventTotals"] == {
        "pageVisits": 0,
        "jobDescriptionSubmissions": 0,
        "matchingReportsGenerated": 3,
        "resumePreviews": 0,
        "contactCtaClicks": 2,
        "feedbackSubmissions": 0,
    }
    assert body["updatedAt"] is not None
    serialized = response.text
    assert "normal_1" not in serialized
    assert "sessionId" not in serialized
    assert "eventId" not in serialized


def test_dashboard_uses_inclusive_asia_shanghai_dates_and_excludes_test_sessions(
    client: TestClient,
) -> None:
    cases = [
        ("before", "2026-08-01T15:59:59Z"),
        ("start", "2026-08-01T16:00:00Z"),
        ("end", "2026-08-02T15:59:59Z"),
        ("after", "2026-08-02T16:00:00Z"),
    ]
    for event_id, occurred_at in cases:
        submit_event(
            client,
            event_id=event_id,
            event_name="page_visit",
            session_id=f"session_{event_id}",
            occurred_at=occurred_at,
        )
    submit_event(
        client,
        event_id="test_report",
        event_name="matching_report_generated",
        session_id="session_test",
        occurred_at="2026-08-02T00:00:00Z",
    )
    assert client.post(
        "/api/tracking-sessions/test-mode",
        json={"sessionId": "session_test"},
    ).status_code == 200
    submit_event(
        client,
        event_id="test_late",
        event_name="page_visit",
        session_id="session_test",
        occurred_at="2026-08-02T01:00:00Z",
    )

    response = client.get(
        "/api/dashboard?startDate=2026-08-02&endDate=2026-08-02"
    )

    assert response.status_code == 200
    assert response.json()["reportingPeriod"] == {
        "mode": "custom",
        "startDate": "2026-08-02",
        "endDate": "2026-08-02",
        "timezone": "Asia/Shanghai",
    }
    assert response.json()["eventTotals"]["pageVisits"] == 2
    assert response.json()["eventTotals"]["matchingReportsGenerated"] == 0
    assert response.json()["contactConversion"] == {
        "rate": None,
        "numerator": 0,
        "denominator": 0,
    }


@pytest.mark.parametrize(
    "query",
    [
        "?startDate=2026-09-01",
        "?endDate=2026-09-01",
        "?startDate=2026-09-02&endDate=2026-09-01",
        "?startDate=not-a-date&endDate=2026-09-01",
        "?startDate=0001-01-01&endDate=0001-01-01",
        "?startDate=9999-12-31&endDate=9999-12-31",
    ],
)
def test_dashboard_rejects_invalid_date_ranges(
    client: TestClient,
    query: str,
) -> None:
    response = client.get(f"/api/dashboard{query}")

    assert response.status_code == 400
    assert response.json() == {
        "code": "INVALID_REQUEST",
        "message": "数据看板日期范围无效。",
    }


def test_dashboard_empty_result_has_null_update_and_rate(client: TestClient) -> None:
    response = client.get("/api/dashboard")

    assert response.status_code == 200
    assert response.json()["updatedAt"] is None
    assert response.json()["contactConversion"] == {
        "rate": None,
        "numerator": 0,
        "denominator": 0,
    }
    assert set(response.json()["eventTotals"].values()) == {0}


def test_dashboard_reads_one_consistent_repository_snapshot(
    client: TestClient,
    db_session: Session,
) -> None:
    repository = TrackingRepository(db_session)
    calls = 0
    original = repository.dashboard_aggregate

    def dashboard_aggregate(**kwargs: object) -> object:
        nonlocal calls
        calls += 1
        return original(**kwargs)  # type: ignore[arg-type]

    repository.dashboard_aggregate = dashboard_aggregate  # type: ignore[assignment,method-assign]
    app.dependency_overrides[get_analytics_service] = lambda: AnalyticsService(repository)

    response = client.get("/api/dashboard")

    assert response.status_code == 200
    assert calls == 1


class FailingAnalyticsService:
    def generate(self, **_kwargs: object) -> None:
        raise TrackingPersistenceError


def test_dashboard_failure_uses_safe_error_contract(client: TestClient) -> None:
    app.dependency_overrides[get_analytics_service] = FailingAnalyticsService

    response = client.get("/api/dashboard")

    assert response.status_code == 500
    assert response.json() == {
        "code": "PERSISTENCE_ERROR",
        "message": "数据看板暂时无法加载。",
    }


def test_designating_session_retroactively_excludes_existing_rows(
    client: TestClient,
    db_session: Session,
) -> None:
    submit_event(
        client,
        event_id="retroactive",
        event_name="page_visit",
        session_id="retroactive_session",
        occurred_at="2026-09-01T00:00:00Z",
    )
    assert client.get("/api/dashboard").json()["eventTotals"]["pageVisits"] == 1

    client.post(
        "/api/tracking-sessions/test-mode",
        json={"sessionId": "retroactive_session"},
    )

    assert client.get("/api/dashboard").json()["eventTotals"]["pageVisits"] == 0
    assert db_session.scalar(
        select(TrackingSession.is_test).where(
            TrackingSession.id == "retroactive_session"
        )
    ) is True
    event = db_session.get(UserBehaviorEvent, "retroactive")
    assert event is not None
    assert event.occurred_at == datetime(2026, 9, 1, tzinfo=UTC)
