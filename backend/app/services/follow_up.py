from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError

from app.ai.follow_up import FollowUpAIService, FollowUpContextMessage
from app.ai.matching import AIServiceError
from app.db.models import Conversation, ConversationMessage


class FollowUpConversationNotFoundError(Exception):
    """Raised when a follow-up does not reference a persisted conversation."""


class FollowUpUnavailableError(Exception):
    """Raised when the AI boundary cannot answer a follow-up."""


class FollowUpPersistenceError(Exception):
    """Raised when the follow-up exchange cannot be stored atomically."""


@dataclass(frozen=True)
class FollowUpResult:
    message_id: str
    content: str


class FollowUpRepository(Protocol):
    def get_conversation_for_update(
        self, conversation_id: str
    ) -> Conversation | None: ...

    def add_message(self, message: ConversationMessage) -> None: ...

    def list_messages(self, conversation_id: str) -> list[ConversationMessage]: ...

    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class FollowUpService:
    def __init__(
        self,
        repository: FollowUpRepository,
        ai_service: FollowUpAIService,
        resume_path: Path,
    ) -> None:
        self._repository = repository
        self._ai_service = ai_service
        self._resume_path = resume_path

    def answer(self, *, conversation_id: str, question: str) -> FollowUpResult:
        try:
            if self._repository.get_conversation_for_update(conversation_id) is None:
                raise FollowUpConversationNotFoundError

            persisted_messages = self._repository.list_messages(conversation_id)
            if len(persisted_messages) >= 2:
                previous_question = persisted_messages[-2]
                previous_answer = persisted_messages[-1]
                if (
                    previous_question.role == "user"
                    and previous_question.message_type == "follow_up_question"
                    and previous_question.content == question
                    and previous_answer.role == "assistant"
                    and previous_answer.message_type == "follow_up_answer"
                ):
                    self._repository.commit()
                    return FollowUpResult(
                        message_id=previous_answer.id,
                        content=previous_answer.content,
                    )

            question_message = ConversationMessage(
                id=f"message_{uuid4().hex}",
                conversation_id=conversation_id,
                role="user",
                message_type="follow_up_question",
                content=question,
            )
            self._repository.add_message(question_message)
            persisted_messages = self._repository.list_messages(conversation_id)
            conversation_history = tuple(
                FollowUpContextMessage(
                    role=message.role,
                    message_type=message.message_type,
                    content=message.content,
                )
                for message in persisted_messages
            )
            content = self._ai_service.answer_follow_up(
                resume_path=self._resume_path,
                conversation_history=conversation_history,
            )
            answer_message = ConversationMessage(
                id=f"message_{uuid4().hex}",
                conversation_id=conversation_id,
                role="assistant",
                message_type="follow_up_answer",
                content=content,
            )
            self._repository.add_message(answer_message)
            self._repository.commit()
        except FollowUpConversationNotFoundError:
            self._repository.rollback()
            raise
        except AIServiceError as error:
            self._repository.rollback()
            raise FollowUpUnavailableError from error
        except SQLAlchemyError as error:
            self._repository.rollback()
            raise FollowUpPersistenceError from error
        except Exception:
            self._repository.rollback()
            raise

        return FollowUpResult(
            message_id=answer_message.id,
            content=answer_message.content,
        )
