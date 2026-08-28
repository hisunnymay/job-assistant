import hashlib
import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast

from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from app.ai.follow_up import FollowUpContextMessage
from app.ai.matching import AIServiceError
from app.ai.prompts import (
    FOLLOW_UP_SYSTEM_PROMPT,
    MATCHING_SYSTEM_PROMPT,
    STRUCTURED_OUTPUT_CORRECTION_PROMPT,
)
from app.ai.rendering import render_follow_up, render_matching_analysis
from app.ai.schemas import FollowUpResult, MatchingAnalysisResult
from app.ai.workflow import (
    ProviderPermanentError,
    ProviderTransientError,
    StructuredAIWorkflow,
    WorkflowExecution,
)
from app.resources.candidate_resume import (
    CANDIDATE_RESUME_CONTEXT_FILENAME,
    CANDIDATE_RESUME_CONTEXT_SHA256,
)

TRANSIENT_STATUS_CODES = {408, 409, 425, 429, 500, 502, 503, 504}
TRANSIENT_ERROR_NAMES = {
    "APIConnectionError",
    "APITimeoutError",
    "ConnectError",
    "ConnectTimeout",
    "InternalServerError",
    "NetworkError",
    "PoolTimeout",
    "RateLimitError",
    "ReadError",
    "ReadTimeout",
    "RemoteProtocolError",
    "TimeoutException",
    "WriteError",
    "WriteTimeout",
}


@dataclass(frozen=True)
class ProviderRequest:
    messages: tuple[dict[str, object], ...]
    response_format: dict[str, object]
    headers: dict[str, str]


class ProviderClient(Protocol):
    def complete(self, request: ProviderRequest) -> object: ...


class InvokableChatModel(Protocol):
    def invoke(self, input: object, **kwargs: object) -> object: ...


class ChatOpenAIProviderClient:
    def __init__(self, model: InvokableChatModel) -> None:
        self._model = model

    def complete(self, request: ProviderRequest) -> object:
        try:
            response = self._model.invoke(
                list(request.messages),
                response_format=request.response_format,
                extra_headers=request.headers,
            )
        except Exception as error:
            if _is_transient_provider_error(error):
                raise ProviderTransientError(type(error).__name__) from None
            raise ProviderPermanentError(type(error).__name__) from None

        additional_kwargs = getattr(response, "additional_kwargs", {})
        if isinstance(additional_kwargs, Mapping) and additional_kwargs.get("refusal"):
            raise ProviderPermanentError
        response_metadata = getattr(response, "response_metadata", {})
        if (
            isinstance(response_metadata, Mapping)
            and response_metadata.get("finish_reason") == "content_filter"
        ):
            raise ProviderPermanentError

        content = getattr(response, "content", None)
        if isinstance(content, str):
            return content
        if isinstance(content, Mapping):
            return cast(Mapping[str, object], content)
        if isinstance(content, list):
            if any(
                isinstance(item, Mapping)
                and (item.get("type") == "refusal" or item.get("refusal") is not None)
                for item in content
            ):
                raise ProviderPermanentError
            text_parts = [
                item.get("text")
                for item in content
                if isinstance(item, Mapping) and isinstance(item.get("text"), str)
            ]
            if text_parts:
                return "".join(cast(list[str], text_parts))
        return content


class ArkAIService:
    def __init__(
        self,
        *,
        api_key: SecretStr,
        base_url: str,
        model: str,
        request_timeout_seconds: float,
        provider_client: ProviderClient | None = None,
    ) -> None:
        self._model = model
        if provider_client is None:
            chat_model = ChatOpenAI(
                api_key=api_key,
                base_url=base_url,
                extra_body={"thinking": {"type": "disabled"}},
                max_retries=0,
                model=model,
                timeout=request_timeout_seconds,
                use_responses_api=True,
            )
            provider_client = ChatOpenAIProviderClient(cast(InvokableChatModel, chat_model))
        self._provider_client = provider_client

    def generate_matching_analysis(
        self,
        *,
        resume_context_path: Path,
        job_description: str,
    ) -> str:
        return self.execute_matching_analysis(
            resume_context_path=resume_context_path,
            job_description=job_description,
        ).rendered_output

    def execute_matching_analysis(
        self,
        *,
        resume_context_path: Path,
        job_description: str,
    ) -> WorkflowExecution[MatchingAnalysisResult]:
        if not job_description.strip():
            raise AIServiceError("AI processing failed")
        resume_context = _load_resume_context(resume_context_path)
        workflow = StructuredAIWorkflow(workflow_name="matching", model=self._model)
        return workflow.execute(
            generate=lambda request_id, use_correction: self._provider_client.complete(
                _matching_request(
                    request_id=request_id,
                    resume_context=resume_context,
                    job_description=job_description,
                    use_structured_output_correction=use_correction,
                )
            ),
            schema=MatchingAnalysisResult,
            renderer=render_matching_analysis,
        )

    def answer_follow_up(
        self,
        *,
        resume_context_path: Path,
        conversation_history: tuple[FollowUpContextMessage, ...],
    ) -> str:
        return self.execute_follow_up(
            resume_context_path=resume_context_path,
            conversation_history=conversation_history,
        ).rendered_output

    def execute_follow_up(
        self,
        *,
        resume_context_path: Path,
        conversation_history: tuple[FollowUpContextMessage, ...],
    ) -> WorkflowExecution[FollowUpResult]:
        if not conversation_history:
            raise AIServiceError("AI processing failed")
        current_question = conversation_history[-1]
        if current_question.message_type != "follow_up_question" or not current_question.content:
            raise AIServiceError("AI processing failed")
        has_job_description = any(
            item.message_type == "job_description" for item in conversation_history
        )
        has_matching_analysis = any(
            item.message_type == "matching_analysis" for item in conversation_history
        )
        if not has_job_description or not has_matching_analysis:
            raise AIServiceError("AI processing failed")

        resume_context = _load_resume_context(resume_context_path)
        workflow = StructuredAIWorkflow(workflow_name="follow_up", model=self._model)
        return workflow.execute(
            generate=lambda request_id, use_correction: self._provider_client.complete(
                _follow_up_request(
                    request_id=request_id,
                    resume_context=resume_context,
                    conversation_history=conversation_history[:-1],
                    current_question=current_question.content,
                    use_structured_output_correction=use_correction,
                )
            ),
            schema=FollowUpResult,
            renderer=render_follow_up,
        )


def _matching_request(
    *,
    request_id: str,
    resume_context: str,
    job_description: str,
    use_structured_output_correction: bool = False,
) -> ProviderRequest:
    return ProviderRequest(
        messages=_provider_messages(
            system_prompt=MATCHING_SYSTEM_PROMPT,
            use_structured_output_correction=use_structured_output_correction,
            user_message={
                "role": "user",
                "content": [
                    _resume_context_block(resume_context),
                    {"type": "text", "text": f"职位描述：\n{job_description}"},
                ],
            },
        ),
        response_format=_strict_response_format(
            name="matching_analysis",
            schema=MatchingAnalysisResult,
        ),
        headers={"X-Client-Request-Id": request_id},
    )


def _follow_up_request(
    *,
    request_id: str,
    resume_context: str,
    conversation_history: tuple[FollowUpContextMessage, ...],
    current_question: str,
    use_structured_output_correction: bool = False,
) -> ProviderRequest:
    history = [
        {
            "role": item.role,
            "messageType": item.message_type,
            "content": item.content,
        }
        for item in conversation_history
    ]
    context = json.dumps(history, ensure_ascii=False, separators=(",", ":"))
    return ProviderRequest(
        messages=_provider_messages(
            system_prompt=FOLLOW_UP_SYSTEM_PROMPT,
            use_structured_output_correction=use_structured_output_correction,
            user_message={
                "role": "user",
                "content": [
                    _resume_context_block(resume_context),
                    {
                        "type": "text",
                        "text": f"当前问题：\n{current_question}\n\n此前对话：\n{context}",
                    },
                ],
            },
        ),
        response_format=_strict_response_format(
            name="follow_up",
            schema=FollowUpResult,
        ),
        headers={"X-Client-Request-Id": request_id},
    )


def _provider_messages(
    *,
    system_prompt: str,
    user_message: dict[str, object],
    use_structured_output_correction: bool,
) -> tuple[dict[str, object], ...]:
    messages: list[dict[str, object]] = [
        {"role": "system", "content": system_prompt},
    ]
    if use_structured_output_correction:
        messages.append(
            {"role": "system", "content": STRUCTURED_OUTPUT_CORRECTION_PROMPT}
        )
    messages.append(user_message)
    return tuple(messages)


def _resume_context_block(resume_context: str) -> dict[str, object]:
    return {
        "type": "text",
        "text": f"候选人简历（已核验固定文本）：\n{resume_context}",
    }


def _strict_response_format(*, name: str, schema: type[BaseModel]) -> dict[str, object]:
    return {
        "type": "json_schema",
        "json_schema": {
            "name": name,
            "strict": True,
            "schema": schema.model_json_schema(by_alias=True, mode="validation"),
        },
    }


def _load_resume_context(resume_context_path: Path) -> str:
    try:
        resume_bytes = resume_context_path.read_bytes()
        resume_context = resume_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        raise AIServiceError("AI processing failed") from None
    digest = hashlib.sha256(resume_bytes).hexdigest()
    if (
        resume_context_path.name != CANDIDATE_RESUME_CONTEXT_FILENAME
        or digest != CANDIDATE_RESUME_CONTEXT_SHA256
        or not resume_context.strip()
    ):
        raise AIServiceError("AI processing failed")
    return resume_context


def _is_transient_provider_error(error: Exception) -> bool:
    current: BaseException | None = error
    seen: set[int] = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        status_code = getattr(current, "status_code", None)
        if isinstance(status_code, int):
            return status_code in TRANSIENT_STATUS_CODES
        if isinstance(current, (ConnectionError, TimeoutError)):
            return True
        if type(current).__name__ in TRANSIENT_ERROR_NAMES:
            return True
        current = current.__cause__ or current.__context__
    return False
