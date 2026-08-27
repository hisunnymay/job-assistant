import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Literal, Protocol

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.db.models import Conversation, UserBehaviorEvent

TrackingEventName = Literal[
    "page_visit",
    "job_description_submitted",
    "matching_report_generated",
    "resume_previewed",
    "contact_cta_clicked",
    "feedback_submitted",
]

TRACKING_EVENT_NAMES: tuple[TrackingEventName, ...] = (
    "page_visit",
    "job_description_submitted",
    "matching_report_generated",
    "resume_previewed",
    "contact_cta_clicked",
    "feedback_submitted",
)
TRACKING_RETENTION_DAYS = 90


class TrackingConversationNotFoundError(Exception):
    """Raised when a supplied Conversation identifier does not exist."""


class TrackingEventConflictError(Exception):
    """Raised when an event identifier is reused with different data."""


class TrackingInvalidEventNameError(Exception):
    """Raised when an event is outside the approved S001 allowlist."""


class TrackingPersistenceError(Exception):
    """Raised when a valid tracking operation cannot be persisted."""


class TrackingReportPeriodError(ValueError):
    """Raised when an aggregate report period is empty or reversed."""


class TrackingRepositoryProtocol(Protocol):
    def get_event(self, event_id: str) -> UserBehaviorEvent | None: ...

    def get_conversation(self, conversation_id: str) -> Conversation | None: ...

    def add_event(self, event: UserBehaviorEvent) -> None: ...

    def aggregate_events(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
    ) -> list[tuple[str, int, int]]: ...

    def count_contact_sessions_with_report(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
    ) -> int: ...

    def delete_events_received_before(self, cutoff: datetime) -> int: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


@dataclass(frozen=True)
class EventMetric:
    total_events: int
    distinct_sessions: int


@dataclass(frozen=True)
class TrackingReport:
    period_start: datetime
    period_end: datetime
    events: dict[TrackingEventName, EventMetric]
    contact_conversion_rate: float | None

    def as_dict(self) -> dict[str, object]:
        return {
            "evaluationStart": self.period_start.isoformat(),
            "evaluationEnd": self.period_end.isoformat(),
            "events": {
                event_name: {
                    "totalEvents": metric.total_events,
                    "distinctSessions": metric.distinct_sessions,
                }
                for event_name, metric in self.events.items()
            },
            "contactConversionRate": self.contact_conversion_rate,
        }


def _same_event(
    event: UserBehaviorEvent,
    *,
    event_name: TrackingEventName,
    session_id: str,
    occurred_at: datetime,
    conversation_id: str | None,
) -> bool:
    expected_fingerprint = build_tracking_event_fingerprint(
        event_id=event.id,
        event_name=event_name,
        session_id=session_id,
        occurred_at=occurred_at,
        conversation_id=conversation_id,
    )
    if event.request_fingerprint:
        return event.request_fingerprint == expected_fingerprint

    return (
        event.event_name == event_name
        and event.session_id == session_id
        and event.occurred_at == occurred_at
        and event.conversation_id == conversation_id
    )


def build_tracking_event_fingerprint(
    *,
    event_id: str,
    event_name: str,
    session_id: str,
    occurred_at: datetime,
    conversation_id: str | None,
) -> str:
    canonical_event = json.dumps(
        {
            "conversationId": conversation_id,
            "eventId": event_id,
            "eventName": event_name,
            "occurredAt": occurred_at.astimezone(UTC).isoformat(),
            "sessionId": session_id,
        },
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return sha256(canonical_event.encode("utf-8")).hexdigest()


class TrackingService:
    def __init__(self, repository: TrackingRepositoryProtocol) -> None:
        self._repository = repository

    def submit(
        self,
        *,
        event_id: str,
        event_name: TrackingEventName,
        session_id: str,
        occurred_at: datetime,
        conversation_id: str | None,
    ) -> None:
        try:
            if event_name not in TRACKING_EVENT_NAMES:
                raise TrackingInvalidEventNameError

            existing_event = self._repository.get_event(event_id)
            if existing_event is not None:
                self._finish_replay(
                    existing_event,
                    event_name=event_name,
                    session_id=session_id,
                    occurred_at=occurred_at,
                    conversation_id=conversation_id,
                )
                return

            if (
                conversation_id is not None
                and self._repository.get_conversation(conversation_id) is None
            ):
                raise TrackingConversationNotFoundError

            self._repository.add_event(
                UserBehaviorEvent(
                    id=event_id,
                    event_name=event_name,
                    session_id=session_id,
                    occurred_at=occurred_at,
                    request_fingerprint=build_tracking_event_fingerprint(
                        event_id=event_id,
                        event_name=event_name,
                        session_id=session_id,
                        occurred_at=occurred_at,
                        conversation_id=conversation_id,
                    ),
                    conversation_id=conversation_id,
                )
            )
            self._repository.commit()
        except (
            TrackingConversationNotFoundError,
            TrackingEventConflictError,
            TrackingInvalidEventNameError,
        ):
            self._repository.rollback()
            raise
        except IntegrityError as error:
            self._repository.rollback()
            self._resolve_concurrent_replay(
                error=error,
                event_id=event_id,
                event_name=event_name,
                session_id=session_id,
                occurred_at=occurred_at,
                conversation_id=conversation_id,
            )
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise TrackingPersistenceError from error

    def _finish_replay(
        self,
        existing_event: UserBehaviorEvent,
        *,
        event_name: TrackingEventName,
        session_id: str,
        occurred_at: datetime,
        conversation_id: str | None,
    ) -> None:
        if not _same_event(
            existing_event,
            event_name=event_name,
            session_id=session_id,
            occurred_at=occurred_at,
            conversation_id=conversation_id,
        ):
            raise TrackingEventConflictError
        self._repository.commit()

    def _resolve_concurrent_replay(
        self,
        *,
        error: IntegrityError,
        event_id: str,
        event_name: TrackingEventName,
        session_id: str,
        occurred_at: datetime,
        conversation_id: str | None,
    ) -> None:
        try:
            existing_event = self._repository.get_event(event_id)
            if existing_event is None:
                raise TrackingPersistenceError from error
            self._finish_replay(
                existing_event,
                event_name=event_name,
                session_id=session_id,
                occurred_at=occurred_at,
                conversation_id=conversation_id,
            )
        except TrackingEventConflictError:
            self._repository.rollback()
            raise
        except SQLAlchemyError as lookup_error:
            self._repository.rollback()
            raise TrackingPersistenceError from lookup_error


class TrackingReportService:
    def __init__(self, repository: TrackingRepositoryProtocol) -> None:
        self._repository = repository

    def generate(self, *, period_start: datetime, period_end: datetime) -> TrackingReport:
        if period_start >= period_end:
            raise TrackingReportPeriodError("evaluation start must be before end")

        try:
            aggregated_rows = self._repository.aggregate_events(
                period_start=period_start,
                period_end=period_end,
            )
            converted_sessions = self._repository.count_contact_sessions_with_report(
                period_start=period_start,
                period_end=period_end,
            )
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise TrackingPersistenceError from error

        row_metrics = {
            event_name: EventMetric(
                total_events=total_events,
                distinct_sessions=distinct_sessions,
            )
            for event_name, total_events, distinct_sessions in aggregated_rows
            if event_name in TRACKING_EVENT_NAMES
        }
        metrics: dict[TrackingEventName, EventMetric] = {
            event_name: row_metrics.get(event_name, EventMetric(0, 0))
            for event_name in TRACKING_EVENT_NAMES
        }
        report_sessions = metrics["matching_report_generated"].distinct_sessions

        return TrackingReport(
            period_start=period_start,
            period_end=period_end,
            events=metrics,
            contact_conversion_rate=(
                None if report_sessions == 0 else converted_sessions / report_sessions
            ),
        )


class TrackingRetentionService:
    def __init__(self, repository: TrackingRepositoryProtocol) -> None:
        self._repository = repository

    def delete_expired(self, *, now: datetime | None = None) -> tuple[int, datetime]:
        current_time = now or datetime.now(UTC)
        cutoff = current_time - timedelta(days=TRACKING_RETENTION_DAYS)
        try:
            deleted_events = self._repository.delete_events_received_before(cutoff)
            self._repository.commit()
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise TrackingPersistenceError from error
        return deleted_events, cutoff
