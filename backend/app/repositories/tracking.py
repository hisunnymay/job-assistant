from datetime import datetime

from sqlalchemy import delete, distinct, func, select
from sqlalchemy.orm import Session

from app.db.models import Conversation, UserBehaviorEvent


class TrackingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_event(self, event_id: str) -> UserBehaviorEvent | None:
        return self._session.get(UserBehaviorEvent, event_id)

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self._session.get(Conversation, conversation_id)

    def add_event(self, event: UserBehaviorEvent) -> None:
        self._session.add(event)
        self._session.flush()

    def aggregate_events(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
    ) -> list[tuple[str, int, int]]:
        rows = self._session.execute(
            select(
                UserBehaviorEvent.event_name,
                func.count(UserBehaviorEvent.id),
                func.count(distinct(UserBehaviorEvent.session_id)),
            )
            .where(
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
            )
            .group_by(UserBehaviorEvent.event_name)
        ).all()
        return [
            (event_name, int(total_events), int(distinct_sessions))
            for event_name, total_events, distinct_sessions in rows
        ]

    def count_contact_sessions_with_report(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
    ) -> int:
        report_sessions = select(UserBehaviorEvent.session_id).where(
            UserBehaviorEvent.event_name == "matching_report_generated",
            UserBehaviorEvent.occurred_at >= period_start,
            UserBehaviorEvent.occurred_at < period_end,
        )
        converted_sessions = self._session.scalar(
            select(func.count(distinct(UserBehaviorEvent.session_id))).where(
                UserBehaviorEvent.event_name == "contact_cta_clicked",
                UserBehaviorEvent.occurred_at >= period_start,
                UserBehaviorEvent.occurred_at < period_end,
                UserBehaviorEvent.session_id.in_(report_sessions),
            )
        )
        return int(converted_sessions or 0)

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

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
