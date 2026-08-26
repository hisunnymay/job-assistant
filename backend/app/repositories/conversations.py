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

    def get_message(self, message_id: str) -> ConversationMessage | None:
        return self._session.get(ConversationMessage, message_id)

    def add_feedback(self, feedback: Feedback) -> None:
        self._session.add(feedback)
        self._session.flush()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
