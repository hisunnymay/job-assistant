from datetime import datetime

from sqlalchemy import delete, distinct, exists, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, aliased

from app.db.models import Conversation, TrackingSession, UserBehaviorEvent


class TrackingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_event(self, event_id: str) -> UserBehaviorEvent | None:
        return self._session.get(UserBehaviorEvent, event_id)

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self._session.get(Conversation, conversation_id)

    def get_tracking_session(self, session_id: str) -> TrackingSession | None:
        return self._session.get(TrackingSession, session_id)

    def ensure_tracking_session(self, session_id: str) -> None:
        self._session.execute(
            insert(TrackingSession)
            .values(id=session_id, is_test=False)
            .on_conflict_do_nothing(index_elements=[TrackingSession.id])
        )

    def designate_test_session(self, session_id: str, activated_at: datetime) -> None:
        self.ensure_tracking_session(session_id)
        self._session.execute(
            update(TrackingSession)
            .where(TrackingSession.id == session_id)
            .values(
                is_test=True,
                test_mode_activated_at=func.coalesce(
                    TrackingSession.test_mode_activated_at,
                    activated_at,
                ),
            )
        )

    def add_event(self, event: UserBehaviorEvent) -> None:
        self._session.add(event)
        self._session.flush()

    def aggregate_events(
        self,
        *,
        period_start: datetime | None,
        period_end: datetime | None,
    ) -> list[tuple[str, int, int]]:
        statement = (
            select(
                UserBehaviorEvent.event_name,
                func.count(UserBehaviorEvent.id),
                func.count(distinct(UserBehaviorEvent.session_id)),
            )
            .join(TrackingSession)
            .where(TrackingSession.is_test.is_(False))
            .group_by(UserBehaviorEvent.event_name)
        )
        if period_start is not None and period_end is not None:
            statement = statement.where(
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
            )
        rows = self._session.execute(statement).all()
        return [
            (event_name, int(total_events), int(distinct_sessions))
            for event_name, total_events, distinct_sessions in rows
        ]

    def count_contact_sessions_with_report(
        self,
        *,
        period_start: datetime | None,
        period_end: datetime | None,
    ) -> int:
        report_sessions = (
            select(UserBehaviorEvent.session_id)
            .join(TrackingSession)
            .where(
                UserBehaviorEvent.event_name == "matching_report_generated",
                TrackingSession.is_test.is_(False),
            )
        )
        if period_start is not None and period_end is not None:
            report_sessions = report_sessions.where(
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
            )
        converted_statement = (
            select(func.count(distinct(UserBehaviorEvent.session_id)))
            .join(TrackingSession)
            .where(
                UserBehaviorEvent.event_name == "contact_cta_clicked",
                TrackingSession.is_test.is_(False),
                UserBehaviorEvent.session_id.in_(report_sessions),
            )
        )
        if period_start is not None and period_end is not None:
            converted_statement = converted_statement.where(
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
            )
        converted_sessions = self._session.scalar(converted_statement)
        return int(converted_sessions or 0)

    def latest_received_at(
        self,
        *,
        period_start: datetime | None,
        period_end: datetime | None,
    ) -> datetime | None:
        statement = (
            select(func.max(UserBehaviorEvent.received_at))
            .join(TrackingSession)
            .where(TrackingSession.is_test.is_(False))
        )
        if period_start is not None and period_end is not None:
            statement = statement.where(
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
            )
        return self._session.scalar(statement)

    def dashboard_aggregate(
        self,
        *,
        period_start: datetime | None,
        period_end: datetime | None,
    ) -> tuple[dict[str, int], int, int, datetime | None]:
        report_event = aliased(UserBehaviorEvent)
        report_session = aliased(TrackingSession)
        report_exists = (
            select(report_event.id)
            .join(report_session, report_session.id == report_event.session_id)
            .where(
                report_event.session_id == UserBehaviorEvent.session_id,
                report_event.event_name == "matching_report_generated",
                report_session.is_test.is_(False),
            )
        )
        if period_start is not None and period_end is not None:
            report_exists = report_exists.where(
                report_event.occurred_at >= period_start,
                report_event.occurred_at < period_end,
            )

        event_names = (
            "page_visit",
            "job_description_submitted",
            "matching_report_generated",
            "resume_previewed",
            "contact_cta_clicked",
            "feedback_submitted",
        )
        total_columns = [
            func.count(UserBehaviorEvent.id)
            .filter(UserBehaviorEvent.event_name == event_name)
            .label(f"{event_name}_total")
            for event_name in event_names
        ]
        report_sessions = func.count(
            distinct(UserBehaviorEvent.session_id)
        ).filter(UserBehaviorEvent.event_name == "matching_report_generated")
        converted_sessions = func.count(
            distinct(UserBehaviorEvent.session_id)
        ).filter(
            UserBehaviorEvent.event_name == "contact_cta_clicked",
            exists(report_exists),
        )
        statement = (
            select(
                *total_columns,
                report_sessions.label("report_sessions"),
                converted_sessions.label("converted_sessions"),
                func.max(UserBehaviorEvent.received_at).label("updated_at"),
            )
            .join(TrackingSession)
            .where(TrackingSession.is_test.is_(False))
        )
        if period_start is not None and period_end is not None:
            statement = statement.where(
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
            )

        row = self._session.execute(statement).one()
        totals = {
            event_name: int(getattr(row, f"{event_name}_total") or 0)
            for event_name in event_names
        }
        return (
            totals,
            int(row.converted_sessions or 0),
            int(row.report_sessions or 0),
            row.updated_at,
        )

    def delete_events_received_before(self, cutoff: datetime) -> int:
        event_ids = list(
            self._session.scalars(
                select(UserBehaviorEvent.id).where(
                    UserBehaviorEvent.received_at < cutoff
                )
            )
        )
        if event_ids:
            self._session.execute(
                delete(UserBehaviorEvent).where(UserBehaviorEvent.id.in_(event_ids))
            )
        return len(event_ids)

    def delete_inactive_empty_sessions(self, cutoff: datetime) -> int:
        session_ids = list(
            self._session.scalars(
                select(TrackingSession.id).where(
                    TrackingSession.created_at < cutoff,
                    TrackingSession.is_test.is_(False),
                    (
                        TrackingSession.test_mode_activated_at.is_(None)
                        | (TrackingSession.test_mode_activated_at < cutoff)
                    ),
                    ~exists().where(
                        UserBehaviorEvent.session_id == TrackingSession.id
                    ),
                )
            )
        )
        if session_ids:
            self._session.execute(
                delete(TrackingSession).where(TrackingSession.id.in_(session_ids))
            )
        return len(session_ids)

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
