from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ConversationMessage
from app.repositories.conversations import ConversationRepository
from app.services.matching_analysis import MatchingAnalysisService


class RecordingAIService:
    def __init__(self) -> None:
        self.resume_context_path: Path | None = None
        self.job_description: str | None = None

    def generate_matching_analysis(
        self,
        *,
        resume_context_path: Path,
        job_description: str,
    ) -> str:
        self.resume_context_path = resume_context_path
        self.job_description = job_description
        return "# 持久化的 Mock 分析"


def test_service_passes_static_markdown_to_ai_boundary_without_extraction(
    db_session: Session,
) -> None:
    resume_context_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "resources"
        / "resume"
        / "mei_chang_resume.md"
    )
    ai_service = RecordingAIService()
    service = MatchingAnalysisService(
        repository=ConversationRepository(db_session),
        ai_service=ai_service,
        resume_context_path=resume_context_path,
    )

    result = service.generate("用于验证静态 Markdown 交接与持久化的完整职位描述。" * 3)

    assert ai_service.resume_context_path == resume_context_path
    assert ai_service.resume_context_path.is_file()
    assert ai_service.job_description is not None
    stored_analysis = db_session.scalar(
        select(ConversationMessage).where(ConversationMessage.id == result.message_id)
    )
    assert stored_analysis is not None
    assert stored_analysis.content == "# 持久化的 Mock 分析"
