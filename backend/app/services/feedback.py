from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError

from app.db.models import ConversationMessage, Feedback


class FeedbackTargetNotFoundError(Exception):
    """Raised when feedback does not reference a persisted matching report."""


class FeedbackPersistenceError(Exception):
    """Raised when valid feedback cannot be stored."""


class FeedbackRepository(Protocol):
    def get_message_for_update(
        self, message_id: str
    ) -> ConversationMessage | None: ...

    def get_feedback_for_message(self, message_id: str) -> Feedback | None: ...

    def add_feedback(self, feedback: Feedback) -> None: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


@dataclass(frozen=True)
class FeedbackResult:
    feedback_id: str


class FeedbackService:
    def __init__(self, repository: FeedbackRepository) -> None:
        self._repository = repository

    def submit(
        self,
        *,
        conversation_id: str,
        message_id: str,
        rating: int,
        comment: str | None,
    ) -> FeedbackResult:
        try:
            message = self._repository.get_message_for_update(message_id)
            if (
                message is None
                or message.conversation_id != conversation_id
                or message.message_type != "matching_analysis"
            ):
                raise FeedbackTargetNotFoundError

            existing_feedback = self._repository.get_feedback_for_message(message_id)
            if existing_feedback is not None:
                self._repository.commit()
                return FeedbackResult(feedback_id=existing_feedback.id)

            feedback = Feedback(
                id=f"feedback_{uuid4().hex}",
                conversation_id=conversation_id,
                message_id=message_id,
                rating=rating,
                comment=comment or None,
            )
            self._repository.add_feedback(feedback)
            self._repository.commit()
        except FeedbackTargetNotFoundError:
            self._repository.rollback()
            raise
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise FeedbackPersistenceError from error

        return FeedbackResult(feedback_id=feedback.id)
