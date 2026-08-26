from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from app.api.errors import raise_api_error
from app.resources.candidate_resume import get_candidate_resume_path

router = APIRouter(prefix="/api", tags=["resume"])


@router.get("/resume", response_class=FileResponse)
def get_resume(
    download: Annotated[bool, Query()] = False,
) -> FileResponse:
    resume_path = get_candidate_resume_path()
    if not resume_path.is_file():
        raise_api_error(
            status_code=500,
            code="RESUME_UNAVAILABLE",
            message="简历暂时无法访问，请稍后重试。",
        )

    return FileResponse(
        resume_path,
        media_type="application/pdf",
        filename="mei_chang_resume.pdf",
        content_disposition_type="attachment" if download else "inline",
    )
