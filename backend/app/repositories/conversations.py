from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Conversation, ConversationMessage, Feedback


class ConversationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_conversation(self, conversation: Conversation) -> None:
        self._session.add(conversation)
        self._session.flush()

    def add_message(self, message: ConversationMessage) -> None:
        self._session.add(message)
        self._session.flush()

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self._session.get(Conversation, conversation_id)

    def get_conversation_for_update(self, conversation_id: str) -> Conversation | None:
        return self._session.scalar(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .with_for_update()
        )

    def list_messages(self, conversation_id: str) -> list[ConversationMessage]:
        return list(
            self._session.scalars(
                select(ConversationMessage)
                .where(ConversationMessage.conversation_id == conversation_id)
                .order_by(ConversationMessage.created_at, ConversationMessage.id)
            )
        )

    def get_message(self, message_id: str) -> ConversationMessage | None:
        return self._session.get(ConversationMessage, message_id)

    def add_feedback(self, feedback: Feedback) -> None:
        self._session.add(feedback)
        self._session.flush()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
