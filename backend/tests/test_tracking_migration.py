from datetime import UTC, datetime

from sqlalchemy import Engine, inspect, text

from app.db.init_db import ensure_tracking_sessions
from app.services.tracking import build_tracking_event_fingerprint


def test_tracking_session_migration_backfills_without_changing_existing_events(
    database_engine: Engine,
) -> None:
    occurred_at = datetime(2026, 8, 27, tzinfo=UTC)
    fingerprint = build_tracking_event_fingerprint(
        event_id="legacy_event",
        event_name="page_visit",
        session_id="legacy_session",
        occurred_at=occurred_at,
        conversation_id=None,
    )
    with database_engine.begin() as connection:
        connection.execute(
            text(
                "ALTER TABLE user_behavior_events DROP CONSTRAINT IF EXISTS "
                "fk_user_behavior_events_tracking_session"
            )
        )
        connection.execute(text("DROP TABLE IF EXISTS tracking_sessions CASCADE"))
        connection.execute(
            text(
                "INSERT INTO user_behavior_events "
                "(id, event_name, session_id, occurred_at, received_at, "
                "request_fingerprint, conversation_id) "
                "VALUES (:id, :event_name, :session_id, :occurred_at, :received_at, "
                ":fingerprint, NULL)"
            ),
            {
                "id": "legacy_event",
                "event_name": "page_visit",
                "session_id": "legacy_session",
                "occurred_at": occurred_at,
                "received_at": occurred_at,
                "fingerprint": fingerprint,
            },
        )
        connection.execute(
            text(
                "CREATE TABLE tracking_sessions ("
                "id VARCHAR(64) PRIMARY KEY, "
                "is_test BOOLEAN NOT NULL DEFAULT FALSE, "
                "created_at TIMESTAMP WITH TIME ZONE NOT NULL, "
                "test_mode_activated_at TIMESTAMP WITH TIME ZONE NULL)"
            )
        )
        ensure_tracking_sessions(connection)

        migrated_event = connection.execute(
            text(
                "SELECT id, session_id, request_fingerprint, conversation_id "
                "FROM user_behavior_events WHERE id = 'legacy_event'"
            )
        ).mappings().one()
        migrated_session = connection.execute(
            text(
                "SELECT id, is_test, created_at, test_mode_activated_at "
                "FROM tracking_sessions WHERE id = 'legacy_session'"
            )
        ).mappings().one()
        assert dict(migrated_event) == {
            "id": "legacy_event",
            "session_id": "legacy_session",
            "request_fingerprint": fingerprint,
            "conversation_id": None,
        }
        assert migrated_session["is_test"] is False
        assert migrated_session["created_at"] == occurred_at
        assert migrated_session["test_mode_activated_at"] is None

        connection.execute(
            text("DELETE FROM user_behavior_events WHERE id = 'legacy_event'")
        )
        connection.execute(
            text("DELETE FROM tracking_sessions WHERE id = 'legacy_session'")
        )

    foreign_keys = inspect(database_engine).get_foreign_keys("user_behavior_events")
    assert any(
        foreign_key["name"] == "fk_user_behavior_events_tracking_session"
        and foreign_key["referred_table"] == "tracking_sessions"
        for foreign_key in foreign_keys
    )
