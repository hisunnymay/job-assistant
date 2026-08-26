from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.ai.follow_up import FollowUpContextMessage
from app.db.models import Conversation, ConversationMessage
from app.repositories.conversations import ConversationRepository
from app.services.follow_up import FollowUpPersistenceError, FollowUpService


class StaticFollowUpAIService:
    def answer_follow_up(
        self,
        *,
        resume_path: Path,
        conversation_history: tuple[FollowUpContextMessage, ...],
    ) -> str:
        assert resume_path.is_file()
        assert conversation_history[-1].message_type == "follow_up_question"
        return "# 不应被持久化的回答"


class FailOnAnswerRepository(ConversationRepository):
    def add_message(self, message: ConversationMessage) -> None:
        if message.message_type == "follow_up_answer":
            raise SQLAlchemyError("simulated answer persistence failure")
        super().add_message(message)


def test_answer_persistence_failure_rolls_back_the_whole_exchange(
    db_session: Session,
) -> None:
    conversation_id = "conversation_persistence_failure"
    db_session.add(Conversation(id=conversation_id))
    db_session.add_all(
        [
            ConversationMessage(
                id="message_job_description",
                conversation_id=conversation_id,
                role="user",
                message_type="job_description",
                content="完整职位描述",
            ),
            ConversationMessage(
                id="message_matching_analysis",
                conversation_id=conversation_id,
                role="assistant",
                message_type="matching_analysis",
                content="# 匹配分析",
            ),
        ]
    )
    db_session.commit()
    resume_path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "resources"
        / "resume"
        / "mei_chang_resume.pdf"
    )
    service = FollowUpService(
        repository=FailOnAnswerRepository(db_session),
        ai_service=StaticFollowUpAIService(),
        resume_path=resume_path,
    )

    with pytest.raises(FollowUpPersistenceError):
        service.answer(
            conversation_id=conversation_id,
            question="候选人有哪些 AI 产品经验？",
        )

    stored_messages = list(
        db_session.scalars(
            select(ConversationMessage)
            .where(ConversationMessage.conversation_id == conversation_id)
            .order_by(ConversationMessage.created_at, ConversationMessage.id)
        )
    )
    assert [message.message_type for message in stored_messages] == [
        "job_description",
        "matching_analysis",
    ]
