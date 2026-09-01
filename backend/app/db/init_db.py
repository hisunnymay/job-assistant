from sqlalchemy import Connection, text

from app.db import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_engine
from app.services.tracking import build_tracking_event_fingerprint


def ensure_tracking_event_fingerprints(connection: Connection) -> None:
    connection.execute(
        text(
            "ALTER TABLE user_behavior_events "
            "ADD COLUMN IF NOT EXISTS request_fingerprint VARCHAR(64)"
        )
    )
    legacy_events = connection.execute(
        text(
            "SELECT id, event_name, session_id, occurred_at, conversation_id "
            "FROM user_behavior_events WHERE request_fingerprint IS NULL"
        )
    ).mappings()
    for event in legacy_events:
        fingerprint = build_tracking_event_fingerprint(
            event_id=event["id"],
            event_name=event["event_name"],
            session_id=event["session_id"],
            occurred_at=event["occurred_at"],
            conversation_id=event["conversation_id"],
        )
        connection.execute(
            text(
                "UPDATE user_behavior_events "
                "SET request_fingerprint = :fingerprint WHERE id = :event_id"
            ),
            {"fingerprint": fingerprint, "event_id": event["id"]},
        )
    connection.execute(
        text(
            "ALTER TABLE user_behavior_events "
            "ALTER COLUMN request_fingerprint SET NOT NULL"
        )
    )


def ensure_tracking_sessions(connection: Connection) -> None:
    connection.execute(
        text(
            "INSERT INTO tracking_sessions (id, is_test, created_at, "
            "test_mode_activated_at) "
            "SELECT session_id, FALSE, MIN(received_at), NULL "
            "FROM user_behavior_events GROUP BY session_id "
            "ON CONFLICT (id) DO NOTHING"
        )
    )
    connection.execute(
        text(
            "DO $$ BEGIN "
            "IF NOT EXISTS ("
            "SELECT 1 FROM pg_constraint "
            "WHERE conname = 'fk_user_behavior_events_tracking_session' "
            "AND conrelid = 'user_behavior_events'::regclass"
            ") THEN "
            "ALTER TABLE user_behavior_events "
            "ADD CONSTRAINT fk_user_behavior_events_tracking_session "
            "FOREIGN KEY (session_id) REFERENCES tracking_sessions(id) "
            "ON DELETE RESTRICT; "
            "END IF; END $$"
        )
    )


def initialize_database() -> None:
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        ensure_tracking_event_fingerprints(connection)
        ensure_tracking_sessions(connection)
        connection.execute(text("SELECT 1"))


def main() -> None:
    initialize_database()
    print("Database initialization succeeded.")


if __name__ == "__main__":
    main()
