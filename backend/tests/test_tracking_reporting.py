import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from typing import cast

import pytest
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session, sessionmaker

from app.commands import cleanup_tracking_events as cleanup_command
from app.commands import tracking_report as report_command
from app.commands.tracking_report import parse_timestamp
from app.db.models import UserBehaviorEvent
from app.repositories.tracking import TrackingRepository
from app.services.tracking import (
    TRACKING_EVENT_NAMES,
    TrackingEventName,
    TrackingInvalidEventNameError,
    TrackingReportPeriodError,
    TrackingReportService,
    TrackingRetentionService,
    TrackingService,
    build_tracking_event_fingerprint,
)


def add_event(
    db_session: Session,
    *,
    event_id: str,
    event_name: str,
    session_id: str,
    occurred_at: datetime,
    received_at: datetime | None = None,
) -> None:
    db_session.add(
        UserBehaviorEvent(
            id=event_id,
            event_name=event_name,
            session_id=session_id,
            occurred_at=occurred_at,
            received_at=received_at or occurred_at,
            request_fingerprint=build_tracking_event_fingerprint(
                event_id=event_id,
                event_name=event_name,
                session_id=session_id,
                occurred_at=occurred_at,
                conversation_id=None,
            ),
        )
    )
    db_session.commit()


def test_aggregate_report_counts_events_and_distinct_sessions(
    db_session: Session,
) -> None:
    period_start = datetime(2026, 8, 1, tzinfo=UTC)
    period_end = datetime(2026, 9, 1, tzinfo=UTC)
    add_event(
        db_session,
        event_id="event_report_1",
        event_name="matching_report_generated",
        session_id="session_1",
        occurred_at=period_start + timedelta(days=1),
    )
    add_event(
        db_session,
        event_id="event_report_2",
        event_name="matching_report_generated",
        session_id="session_2",
        occurred_at=period_start + timedelta(days=2),
    )
    add_event(
        db_session,
        event_id="event_contact_1",
        event_name="contact_cta_clicked",
        session_id="session_1",
        occurred_at=period_start + timedelta(days=3),
    )
    add_event(
        db_session,
        event_id="event_contact_2",
        event_name="contact_cta_clicked",
        session_id="session_1",
        occurred_at=period_start + timedelta(days=4),
    )
    add_event(
        db_session,
        event_id="event_contact_without_report",
        event_name="contact_cta_clicked",
        session_id="session_contact_only",
        occurred_at=period_start + timedelta(days=5),
    )
    add_event(
        db_session,
        event_id="event_outside",
        event_name="page_visit",
        session_id="session_outside",
        occurred_at=period_end,
    )

    report = TrackingReportService(TrackingRepository(db_session)).generate(
        period_start=period_start,
        period_end=period_end,
    )

    assert tuple(report.events) == TRACKING_EVENT_NAMES
    assert report.events["matching_report_generated"].total_events == 2
    assert report.events["matching_report_generated"].distinct_sessions == 2
    assert report.events["contact_cta_clicked"].total_events == 3
    assert report.events["contact_cta_clicked"].distinct_sessions == 2
    assert report.events["page_visit"].total_events == 0
    assert report.contact_conversion_rate == 0.5
    assert report.as_dict()["contactConversionRate"] == 0.5


def test_contact_conversion_rate_never_counts_contact_only_sessions(
    db_session: Session,
) -> None:
    period_start = datetime(2026, 8, 1, tzinfo=UTC)
    period_end = datetime(2026, 9, 1, tzinfo=UTC)
    add_event(
        db_session,
        event_id="event_report",
        event_name="matching_report_generated",
        session_id="session_report",
        occurred_at=period_start + timedelta(days=1),
    )
    add_event(
        db_session,
        event_id="event_contact_only_1",
        event_name="contact_cta_clicked",
        session_id="session_contact_only_1",
        occurred_at=period_start + timedelta(days=2),
    )
    add_event(
        db_session,
        event_id="event_contact_only_2",
        event_name="contact_cta_clicked",
        session_id="session_contact_only_2",
        occurred_at=period_start + timedelta(days=3),
    )

    report = TrackingReportService(TrackingRepository(db_session)).generate(
        period_start=period_start,
        period_end=period_end,
    )

    assert report.events["contact_cta_clicked"].distinct_sessions == 2
    assert report.contact_conversion_rate == 0.0


def test_aggregate_report_handles_zero_denominator(db_session: Session) -> None:
    period_start = datetime(2026, 8, 1, tzinfo=UTC)
    period_end = datetime(2026, 9, 1, tzinfo=UTC)

    report = TrackingReportService(TrackingRepository(db_session)).generate(
        period_start=period_start,
        period_end=period_end,
    )

    assert report.contact_conversion_rate is None
    assert all(metric.total_events == 0 for metric in report.events.values())


def test_aggregate_report_rejects_empty_period(db_session: Session) -> None:
    period_start = datetime(2026, 8, 1, tzinfo=UTC)

    with pytest.raises(TrackingReportPeriodError):
        TrackingReportService(TrackingRepository(db_session)).generate(
            period_start=period_start,
            period_end=period_start,
        )


def test_tracking_service_enforces_the_event_allowlist(db_session: Session) -> None:
    with pytest.raises(TrackingInvalidEventNameError):
        TrackingService(TrackingRepository(db_session)).submit(
            event_id="event_invalid",
            event_name=cast(TrackingEventName, "invalid_event"),
            session_id="session_1",
            occurred_at=datetime(2026, 8, 27, tzinfo=UTC),
            conversation_id=None,
        )


def test_retention_deletes_only_events_older_than_ninety_days(
    db_session: Session,
) -> None:
    now = datetime(2026, 8, 27, 12, tzinfo=UTC)
    cutoff = now - timedelta(days=90)
    add_event(
        db_session,
        event_id="event_expired",
        event_name="page_visit",
        session_id="session_1",
        occurred_at=cutoff - timedelta(days=1),
        received_at=cutoff - timedelta(microseconds=1),
    )
    add_event(
        db_session,
        event_id="event_boundary",
        event_name="page_visit",
        session_id="session_2",
        occurred_at=cutoff,
        received_at=cutoff,
    )
    add_event(
        db_session,
        event_id="event_recent",
        event_name="page_visit",
        session_id="session_3",
        occurred_at=now,
        received_at=now,
    )

    deleted_events, actual_cutoff = TrackingRetentionService(
        TrackingRepository(db_session)
    ).delete_expired(now=now)

    assert deleted_events == 1
    assert actual_cutoff == cutoff
    assert set(db_session.scalars(select(UserBehaviorEvent.id))) == {
        "event_boundary",
        "event_recent",
    }


def test_tracking_report_timestamp_parser_requires_timezone() -> None:
    assert parse_timestamp("2026-08-27T12:00:00Z") == datetime(
        2026, 8, 27, 12, tzinfo=UTC
    )
    with pytest.raises(argparse.ArgumentTypeError):
        parse_timestamp("2026-08-27T12:00:00")


def test_internal_report_command_outputs_aggregate_json(
    database_engine: Engine,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    add_event(
        db_session,
        event_id="event_report_command",
        event_name="matching_report_generated",
        session_id="session_1",
        occurred_at=datetime(2026, 8, 27, tzinfo=UTC),
    )
    factory = sessionmaker(bind=database_engine, expire_on_commit=False)
    monkeypatch.setattr(report_command, "get_session_factory", lambda: factory)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tracking_report",
            "--start",
            "2026-08-01T00:00:00Z",
            "--end",
            "2026-09-01T00:00:00Z",
        ],
    )

    report_command.main()

    output = cast(dict[str, object], json.loads(capsys.readouterr().out))
    event_metrics = cast(dict[str, dict[str, int]], output["events"])
    assert event_metrics["matching_report_generated"] == {
        "totalEvents": 1,
        "distinctSessions": 1,
    }
    assert output["contactConversionRate"] == 0.0


def test_retention_command_deletes_expired_events(
    database_engine: Engine,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    add_event(
        db_session,
        event_id="event_cleanup_command",
        event_name="page_visit",
        session_id="session_1",
        occurred_at=datetime(2026, 1, 1, tzinfo=UTC),
        received_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    factory = sessionmaker(bind=database_engine, expire_on_commit=False)
    monkeypatch.setattr(cleanup_command, "get_session_factory", lambda: factory)
    monkeypatch.setattr(
        sys,
        "argv",
        ["cleanup_tracking_events", "--now", "2026-08-27T00:00:00Z"],
    )

    cleanup_command.main()

    output = cast(dict[str, object], json.loads(capsys.readouterr().out))
    assert output["deletedEvents"] == 1
    assert db_session.get(UserBehaviorEvent, "event_cleanup_command") is None
