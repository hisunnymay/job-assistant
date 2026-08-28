import json
from collections.abc import Iterable

from sqlalchemy import select

from app.ai.prompts import (
    FOLLOW_UP_SYSTEM_PROMPT,
    MATCHING_SYSTEM_PROMPT,
    STRUCTURED_OUTPUT_CORRECTION_PROMPT,
)
from app.core.config import get_settings
from app.db.models import ConversationMessage, Feedback
from app.db.session import get_session_factory

RAW_PROVIDER_MARKERS = (
    '"answerability":',
    '"requirements":',
    '"sourceReference":',
    '"summary":',
)


def count_prohibited_values(texts: Iterable[str], prohibited_values: Iterable[str]) -> int:
    markers = tuple(value for value in prohibited_values if value)
    return sum(any(marker in text for marker in markers) for text in texts)


def main() -> None:
    settings = get_settings()
    secret = (
        settings.ark_api_key.get_secret_value()
        if settings.ark_api_key is not None
        else ""
    )
    prohibited_values = (
        secret,
        MATCHING_SYSTEM_PROMPT,
        FOLLOW_UP_SYSTEM_PROMPT,
        STRUCTURED_OUTPUT_CORRECTION_PROMPT,
        *RAW_PROVIDER_MARKERS,
    )
    with get_session_factory()() as session:
        message_texts = list(session.scalars(select(ConversationMessage.content)))
        feedback_texts = list(
            session.scalars(select(Feedback.comment).where(Feedback.comment.is_not(None)))
        )
    detected = count_prohibited_values(
        (*message_texts, *(text for text in feedback_texts if text is not None)),
        prohibited_values,
    )
    result = {
        "status": "passed" if detected == 0 else "failed",
        "scannedConversationMessages": len(message_texts),
        "scannedFeedbackComments": len(feedback_texts),
        "prohibitedValuesDetected": detected,
    }
    print(json.dumps(result, ensure_ascii=False))
    if detected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
