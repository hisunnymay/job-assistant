from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError

from app.ai.matching import AIServiceError, MatchingAIService
from app.db.models import Conversation, ConversationMessage


class MatchingAnalysisUnavailableError(Exception):
    """Raised when matching analysis cannot be generated."""


class MatchingAnalysisPersistenceError(Exception):
    """Raised when the matching workflow cannot be stored."""


@dataclass(frozen=True)
class MatchingAnalysisResult:
    conversation_id: str
    message_id: str
    content: str


class MatchingAnalysisRepository(Protocol):
    def add_conversation(self, conversation: Conversation) -> None: ...

    def add_message(self, message: ConversationMessage) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class MatchingAnalysisService:
    def __init__(
        self,
        repository: MatchingAnalysisRepository,
        ai_service: MatchingAIService,
        resume_path: Path,
    ) -> None:
        self._repository = repository
        self._ai_service = ai_service
        self._resume_path = resume_path

    def generate(self, job_description: str) -> MatchingAnalysisResult:
        conversation_id = f"conversation_{uuid4().hex}"
        job_description_message = ConversationMessage(
            id=f"message_{uuid4().hex}",
            conversation_id=conversation_id,
            role="user",
            message_type="job_description",
            content=job_description,
        )

        try:
            self._repository.add_conversation(Conversation(id=conversation_id))
            self._repository.add_message(job_description_message)
            content = self._ai_service.generate_matching_analysis(
                resume_path=self._resume_path,
                job_description=job_description,
            )
            analysis_message = ConversationMessage(
                id=f"message_{uuid4().hex}",
                conversation_id=conversation_id,
                role="assistant",
                message_type="matching_analysis",
                content=content,
            )
            self._repository.add_message(analysis_message)
            self._repository.commit()
        except AIServiceError as error:
            self._repository.rollback()
            raise MatchingAnalysisUnavailableError from error
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise MatchingAnalysisPersistenceError from error

        return MatchingAnalysisResult(
            conversation_id=conversation_id,
            message_id=analysis_message.id,
            content=analysis_message.content,
        )
