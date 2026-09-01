from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

from sqlalchemy.exc import SQLAlchemyError

from app.services.tracking import (
    TRACKING_EVENT_NAMES,
    EventMetric,
    TrackingEventName,
    TrackingPersistenceError,
    TrackingRepositoryProtocol,
)

DASHBOARD_TIMEZONE = "Asia/Shanghai"


class DashboardPeriodError(ValueError):
    """Raised when the requested dashboard date pair is incomplete or reversed."""


@dataclass(frozen=True)
class DashboardReportingPeriod:
    mode: Literal["all_retained", "custom"]
    start_date: date | None
    end_date: date | None
    timezone: str = DASHBOARD_TIMEZONE


@dataclass(frozen=True)
class DashboardAggregate:
    reporting_period: DashboardReportingPeriod
    updated_at: datetime | None
    events: dict[TrackingEventName, EventMetric]
    contact_conversion_numerator: int
    contact_conversion_denominator: int
    contact_conversion_rate: float | None


class AnalyticsService:
    def __init__(self, repository: TrackingRepositoryProtocol) -> None:
        self._repository = repository

    def generate(
        self,
        *,
        start_date: date | None,
        end_date: date | None,
    ) -> DashboardAggregate:
        period_start, period_end, reporting_period = self._resolve_period(
            start_date=start_date,
            end_date=end_date,
        )
        try:
            totals, converted_sessions, denominator, updated_at = (
                self._repository.dashboard_aggregate(
                    period_start=period_start,
                    period_end=period_end,
                )
            )
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise TrackingPersistenceError from error

        metrics: dict[TrackingEventName, EventMetric] = {
            event_name: EventMetric(total_events=totals[event_name], distinct_sessions=0)
            for event_name in TRACKING_EVENT_NAMES
        }
        metrics["matching_report_generated"] = EventMetric(
            total_events=totals["matching_report_generated"],
            distinct_sessions=denominator,
        )
        return DashboardAggregate(
            reporting_period=reporting_period,
            updated_at=updated_at,
            events=metrics,
            contact_conversion_numerator=converted_sessions,
            contact_conversion_denominator=denominator,
            contact_conversion_rate=(
                None if denominator == 0 else converted_sessions / denominator
            ),
        )

    @staticmethod
    def _resolve_period(
        *,
        start_date: date | None,
        end_date: date | None,
    ) -> tuple[datetime | None, datetime | None, DashboardReportingPeriod]:
        if (start_date is None) != (end_date is None):
            raise DashboardPeriodError("both dashboard dates are required")
        if start_date is None or end_date is None:
            return (
                None,
                None,
                DashboardReportingPeriod(
                    mode="all_retained",
                    start_date=None,
                    end_date=None,
                ),
            )
        if start_date > end_date:
            raise DashboardPeriodError("dashboard start date must not exceed end date")
        if start_date == date.min or end_date == date.max:
            raise DashboardPeriodError("dashboard date is outside the supported range")

        timezone = ZoneInfo(DASHBOARD_TIMEZONE)
        period_start = datetime.combine(start_date, time.min, tzinfo=timezone).astimezone(
            UTC
        )
        period_end = datetime.combine(
            end_date + timedelta(days=1),
            time.min,
            tzinfo=timezone,
        ).astimezone(UTC)
        return (
            period_start,
            period_end,
            DashboardReportingPeriod(
                mode="custom",
                start_date=start_date,
                end_date=end_date,
            ),
        )
