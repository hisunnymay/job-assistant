from pathlib import Path
from typing import Protocol


class AIServiceError(Exception):
    """Raised when the replaceable AI boundary cannot generate a response."""


class MatchingAIService(Protocol):
    def generate_matching_analysis(
        self,
        *,
        resume_context_path: Path,
        job_description: str,
    ) -> str: ...
