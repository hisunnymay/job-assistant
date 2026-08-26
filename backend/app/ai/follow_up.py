from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class FollowUpContextMessage:
    role: str
    message_type: str
    content: str


class FollowUpAIService(Protocol):
    def answer_follow_up(
        self,
        *,
        resume_path: Path,
        conversation_history: tuple[FollowUpContextMessage, ...],
    ) -> str: ...
