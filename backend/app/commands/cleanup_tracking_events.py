import argparse
import json
from datetime import UTC, datetime

from app.commands.tracking_report import parse_timestamp
from app.db.session import get_session_factory
from app.repositories.tracking import TrackingRepository
from app.services.tracking import TrackingRetentionService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Delete user behavior events older than the 90-day retention period."
    )
    parser.add_argument("--now", type=parse_timestamp, default=datetime.now(UTC))
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    with get_session_factory()() as session:
        deleted_events, cutoff = TrackingRetentionService(
            TrackingRepository(session)
        ).delete_expired(now=arguments.now)
    print(
        json.dumps(
            {
                "deletedEvents": deleted_events,
                "cutoff": cutoff.isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
