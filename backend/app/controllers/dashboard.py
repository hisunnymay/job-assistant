from datetime import date, datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app.api.errors import raise_api_error
from app.db.session import get_db_session
from app.repositories.tracking import TrackingRepository
from app.services.analytics import AnalyticsService, DashboardPeriodError
from app.services.tracking import TrackingPersistenceError

router = APIRouter(prefix="/api", tags=["dashboard"])


class ReportingPeriodResponse(BaseModel):
    model_config = ConfigDict(alias_generator=lambda value: value, populate_by_name=True)

    mode: Literal["all_retained", "custom"]
    startDate: date | None
    endDate: date | None
    timezone: Literal["Asia/Shanghai"]


class ContactConversionResponse(BaseModel):
    rate: float | None
    numerator: int
    denominator: int


class EventTotalsResponse(BaseModel):
    pageVisits: int
    jobDescriptionSubmissions: int
    matchingReportsGenerated: int
    resumePreviews: int
    contactCtaClicks: int
    feedbackSubmissions: int


class DashboardResponse(BaseModel):
    reportingPeriod: ReportingPeriodResponse
    updatedAt: datetime | None
    contactConversion: ContactConversionResponse
    eventTotals: EventTotalsResponse


def get_analytics_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> AnalyticsService:
    return AnalyticsService(TrackingRepository(session))


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    service: Annotated[AnalyticsService, Depends(get_analytics_service)],
    start_date: Annotated[date | None, Query(alias="startDate")] = None,
    end_date: Annotated[date | None, Query(alias="endDate")] = None,
) -> DashboardResponse:
    try:
        aggregate = service.generate(start_date=start_date, end_date=end_date)
    except DashboardPeriodError:
        raise_api_error(
            status_code=400,
            code="INVALID_REQUEST",
            message="数据看板日期范围无效。",
        )
    except TrackingPersistenceError:
        raise_api_error(
            status_code=500,
            code="PERSISTENCE_ERROR",
            message="数据看板暂时无法加载。",
        )

    events = aggregate.events
    period = aggregate.reporting_period
    return DashboardResponse(
        reportingPeriod=ReportingPeriodResponse(
            mode=period.mode,
            startDate=period.start_date,
            endDate=period.end_date,
            timezone="Asia/Shanghai",
        ),
        updatedAt=aggregate.updated_at,
        contactConversion=ContactConversionResponse(
            rate=aggregate.contact_conversion_rate,
            numerator=aggregate.contact_conversion_numerator,
            denominator=aggregate.contact_conversion_denominator,
        ),
        eventTotals=EventTotalsResponse(
            pageVisits=events["page_visit"].total_events,
            jobDescriptionSubmissions=events["job_description_submitted"].total_events,
            matchingReportsGenerated=events["matching_report_generated"].total_events,
            resumePreviews=events["resume_previewed"].total_events,
            contactCtaClicks=events["contact_cta_clicked"].total_events,
            feedbackSubmissions=events["feedback_submitted"].total_events,
        ),
    )
