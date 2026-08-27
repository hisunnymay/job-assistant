import argparse
import json
from datetime import datetime

from app.db.session import get_session_factory
from app.repositories.tracking import TrackingRepository
from app.services.tracking import TrackingReportPeriodError, TrackingReportService


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise argparse.ArgumentTypeError("timestamp must include a timezone")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate privacy-safe MVP tracking events."
    )
    parser.add_argument("--start", required=True, type=parse_timestamp)
    parser.add_argument("--end", required=True, type=parse_timestamp)
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    with get_session_factory()() as session:
        service = TrackingReportService(TrackingRepository(session))
        try:
            report = service.generate(
                period_start=arguments.start,
                period_end=arguments.end,
            )
        except TrackingReportPeriodError as error:
            raise SystemExit(str(error)) from error
    print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
