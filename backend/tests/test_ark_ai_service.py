import json
import logging
from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import cast

import httpx
import pytest
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

import app.ai.ark as ark_module
from app.ai.ark import (
    ArkAIService,
    ChatOpenAIProviderClient,
    ProviderClient,
    ProviderRequest,
)
from app.ai.follow_up import FollowUpContextMessage
from app.ai.matching import AIServiceError
from app.ai.prompts import STRUCTURED_OUTPUT_CORRECTION_PROMPT
from app.ai.workflow import ProviderPermanentError, ProviderTransientError

MODEL = "doubao-seed-2-1-pro-260628"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
TIMEOUT_SECONDS = 60.0


def resume_context_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "app"
        / "resources"
        / "resume"
        / "mei_chang_resume.md"
    )


def valid_matching_result() -> dict[str, object]:
    return {
        "summary": "候选人具备相关 AI 产品经历。",
        "requirements": [
            {
                "requirement": "AI 产品经验",
                "importance": "required",
                "status": "supported",
                "evidence": [
                    {
                        "evidenceText": "负责大模型测试与评估平台",
                        "sourceReference": "工作经历",
                    }
                ],
                "explanation": "简历直接记录了相关职责。",
                "missingInformation": None,
            }
        ],
    }


def valid_follow_up_result() -> dict[str, object]:
    return {
        "answerability": "answerable",
        "answer": "简历记录了 AI 产品设计和评测经历。",
        "evidence": [
            {
                "evidenceText": "负责大模型测试与评估平台",
                "sourceReference": "工作经历",
            }
        ],
        "missingInformation": None,
    }


class FakeProviderClient(ProviderClient):
    def __init__(self, responses: list[object]) -> None:
        self._responses: Iterator[object] = iter(responses)
        self.requests: list[ProviderRequest] = []

    def complete(self, request: ProviderRequest) -> object:
        self.requests.append(request)
        response = next(self._responses)
        if isinstance(response, Exception):
            raise response
        return response


def create_service(provider: ProviderClient) -> ArkAIService:
    return ArkAIService(
        api_key=SecretStr("test-only-secret"),
        base_url=BASE_URL,
        model=MODEL,
        request_timeout_seconds=TIMEOUT_SECONDS,
        provider_client=provider,
    )


def get_user_text_blocks(request: ProviderRequest) -> list[Mapping[str, object]]:
    content = request.messages[1]["content"]
    assert isinstance(content, list)
    return [cast(Mapping[str, object], item) for item in content]


def test_matching_success_uses_exact_markdown_strict_schema_and_one_attempt(
    caplog: pytest.LogCaptureFixture,
) -> None:
    provider = FakeProviderClient([valid_matching_result()])
    service = create_service(provider)
    job_description = "sensitive job description that must not be logged"
    caplog.set_level(logging.INFO, logger="app.ai.workflow")

    rendered = service.generate_matching_analysis(
        resume_context_path=resume_context_path(),
        job_description=job_description,
    )

    assert "候选人具备相关 AI 产品经历" in rendered
    assert len(provider.requests) == 1
    request = provider.requests[0]
    assert set(request.headers) == {"X-Client-Request-Id"}
    assert request.headers["X-Client-Request-Id"].startswith("ai_")
    assert request.response_format["type"] == "json_schema"
    response_schema = cast(Mapping[str, object], request.response_format["json_schema"])
    assert response_schema["name"] == "matching_analysis"
    assert response_schema["strict"] is True
    schema = cast(Mapping[str, object], response_schema["schema"])
    assert schema["additionalProperties"] is False

    text_blocks = get_user_text_blocks(request)
    assert [block["type"] for block in text_blocks] == ["text", "text"]
    assert cast(str, text_blocks[0]["text"]).endswith(
        resume_context_path().read_text(encoding="utf-8")
    )
    assert cast(str, text_blocks[1]["text"]) == f"职位描述：\n{job_description}"

    assert job_description not in caplog.text
    assert "test-only-secret" not in caplog.text
    record = next(record for record in caplog.records if record.message == "ai_execution_completed")
    assert record.request_id == request.headers["X-Client-Request-Id"]  # type: ignore[attr-defined]
    assert record.workflow == "matching"  # type: ignore[attr-defined]
    assert record.model == MODEL  # type: ignore[attr-defined]
    assert record.attempt_count == 1  # type: ignore[attr-defined]
    assert record.retry_count == 0  # type: ignore[attr-defined]
    assert record.validation_status == "valid"  # type: ignore[attr-defined]


def test_follow_up_keeps_current_question_separate_from_ordered_history() -> None:
    provider = FakeProviderClient([valid_follow_up_result()])
    service = create_service(provider)
    history = (
        FollowUpContextMessage("user", "job_description", "完整职位描述"),
        FollowUpContextMessage("assistant", "matching_analysis", "# 匹配报告"),
        FollowUpContextMessage("user", "follow_up_question", "候选人有哪些 AI 产品经验？"),
    )

    rendered = service.answer_follow_up(
        resume_context_path=resume_context_path(),
        conversation_history=history,
    )

    assert "候选人信息回答" in rendered
    assert len(provider.requests) == 1
    request = provider.requests[0]
    content = request.messages[1]["content"]
    assert isinstance(content, list)
    assert [cast(Mapping[str, object], item)["type"] for item in content] == [
        "text",
        "text",
    ]
    resume_block = cast(Mapping[str, object], content[0])
    assert cast(str, resume_block["text"]).endswith(
        resume_context_path().read_text(encoding="utf-8")
    )
    text_block = cast(Mapping[str, object], content[1])
    request_text = cast(str, text_block["text"])
    assert "当前问题：\n候选人有哪些 AI 产品经验？" in request_text
    assert '"messageType":"job_description"' in request_text
    assert '"messageType":"matching_analysis"' in request_text
    assert '"messageType":"follow_up_question"' not in request_text
    response_schema = cast(Mapping[str, object], request.response_format["json_schema"])
    assert response_schema["name"] == "follow_up"
    assert response_schema["strict"] is True


def test_invalid_structured_output_adds_safe_correction_only_to_second_request(
    caplog: pytest.LogCaptureFixture,
) -> None:
    raw_response_marker = "raw-response-must-not-be-repeated"
    provider = FakeProviderClient(
        [{"summary": raw_response_marker}, valid_matching_result()]
    )
    caplog.set_level(logging.INFO, logger="app.ai.workflow")

    rendered = create_service(provider).generate_matching_analysis(
        resume_context_path=resume_context_path(),
        job_description="完整职位描述",
    )

    assert rendered
    assert len(provider.requests) == 2
    assert len({request.headers["X-Client-Request-Id"] for request in provider.requests}) == 1
    first_request, second_request = provider.requests
    assert len(first_request.messages) == 2
    assert len(second_request.messages) == 3
    assert second_request.messages[1] == {
        "role": "system",
        "content": STRUCTURED_OUTPUT_CORRECTION_PROMPT,
    }
    assert first_request.messages[-1] == second_request.messages[-1]
    assert first_request.response_format == second_request.response_format
    assert raw_response_marker not in repr(second_request.messages)
    record = next(
        record
        for record in caplog.records
        if record.message == "ai_execution_completed"
    )
    assert record.retry_reason == "invalid_structured_output"  # type: ignore[attr-defined]


def test_missing_provider_result_is_treated_as_invalid_structured_output() -> None:
    provider = FakeProviderClient([None, valid_matching_result()])

    rendered = create_service(provider).generate_matching_analysis(
        resume_context_path=resume_context_path(),
        job_description="完整职位描述",
    )

    assert rendered
    assert len(provider.requests) == 2
    assert provider.requests[1].messages[1]["content"] == (
        STRUCTURED_OUTPUT_CORRECTION_PROMPT
    )


def test_transient_failure_reuses_the_original_request_without_correction(
    caplog: pytest.LogCaptureFixture,
) -> None:
    provider = FakeProviderClient([ProviderTransientError(), valid_matching_result()])
    caplog.set_level(logging.INFO, logger="app.ai.workflow")

    rendered = create_service(provider).generate_matching_analysis(
        resume_context_path=resume_context_path(),
        job_description="完整职位描述",
    )

    assert rendered
    assert len(provider.requests) == 2
    assert provider.requests[0] == provider.requests[1]
    assert all(
        STRUCTURED_OUTPUT_CORRECTION_PROMPT not in repr(request.messages)
        for request in provider.requests
    )
    record = next(
        record
        for record in caplog.records
        if record.message == "ai_execution_completed"
    )
    assert record.retry_reason == "transient_provider_error"  # type: ignore[attr-defined]


def test_follow_up_invalid_output_uses_the_same_safe_correction_path() -> None:
    provider = FakeProviderClient([{"answer": "invalid"}, valid_follow_up_result()])
    history = (
        FollowUpContextMessage("user", "job_description", "完整职位描述"),
        FollowUpContextMessage("assistant", "matching_analysis", "# 匹配报告"),
        FollowUpContextMessage("user", "follow_up_question", "候选人有哪些 AI 产品经验？"),
    )

    rendered = create_service(provider).answer_follow_up(
        resume_context_path=resume_context_path(),
        conversation_history=history,
    )

    assert rendered
    assert len(provider.requests) == 2
    assert provider.requests[1].messages[1]["content"] == (
        STRUCTURED_OUTPUT_CORRECTION_PROMPT
    )
    assert provider.requests[0].messages[-1] == provider.requests[1].messages[-1]


@pytest.mark.parametrize(
    ("responses", "expected_attempts", "expected_error_type"),
    [
        ([ProviderPermanentError()], 1, "permanent_provider_error"),
        ([{"summary": "invalid"}, {"summary": "still invalid"}], 2, "invalid_structured_output"),
        ([ProviderTransientError(), ProviderTransientError()], 2, "transient_provider_error"),
    ],
)
def test_permanent_or_exhausted_failure_is_safe_and_bounded(
    responses: list[object],
    expected_attempts: int,
    expected_error_type: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    provider = FakeProviderClient(responses)
    caplog.set_level(logging.INFO, logger="app.ai.workflow")

    with pytest.raises(AIServiceError, match="AI processing failed"):
        create_service(provider).generate_matching_analysis(
            resume_context_path=resume_context_path(),
            job_description="raw job description must stay private",
        )

    assert len(provider.requests) == expected_attempts
    assert "raw job description" not in caplog.text
    assert "test-only-secret" not in caplog.text
    record = next(record for record in caplog.records if record.message == "ai_execution_failed")
    assert record.error_type == expected_error_type  # type: ignore[attr-defined]
    assert record.attempt_count == expected_attempts  # type: ignore[attr-defined]


class StatusError(Exception):
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class RaisingChatModel:
    def __init__(self, error: Exception) -> None:
        self._error = error

    def invoke(self, input: object, **kwargs: object) -> object:
        del input, kwargs
        raise self._error


class ReturningChatModel:
    def __init__(self, response: object) -> None:
        self._response = response

    def invoke(self, input: object, **kwargs: object) -> object:
        del input, kwargs
        return self._response


class ResponsesRefusal:
    additional_kwargs: dict[str, object] = {}
    response_metadata: dict[str, object] = {"status": "completed"}
    content: list[dict[str, str]] = [
        {"type": "refusal", "refusal": "provider safety refusal"}
    ]


@pytest.mark.parametrize(
    ("error", "expected_error"),
    [
        (StatusError(429), ProviderTransientError),
        (StatusError(503), ProviderTransientError),
        (httpx.ReadTimeout("timed out"), ProviderTransientError),
        (httpx.ConnectError("connection failed"), ProviderTransientError),
        (StatusError(401), ProviderPermanentError),
        (StatusError(400), ProviderPermanentError),
        (RuntimeError("unsupported capability"), ProviderPermanentError),
    ],
)
def test_chat_client_classifies_retryable_and_permanent_failures(
    error: Exception,
    expected_error: type[Exception],
) -> None:
    client = ChatOpenAIProviderClient(RaisingChatModel(error))
    request = ProviderRequest(messages=(), response_format={}, headers={})

    with pytest.raises(expected_error):
        client.complete(request)


def test_chat_client_classifies_nested_timeout_as_transient() -> None:
    timeout = httpx.ReadTimeout("timed out")
    wrapper = RuntimeError("provider wrapper")
    wrapper.__cause__ = timeout
    client = ChatOpenAIProviderClient(RaisingChatModel(wrapper))

    with pytest.raises(ProviderTransientError) as captured:
        client.complete(ProviderRequest(messages=(), response_format={}, headers={}))

    assert captured.value.source_type == "RuntimeError"


def test_responses_safety_refusal_is_non_retryable() -> None:
    client = ChatOpenAIProviderClient(ReturningChatModel(ResponsesRefusal()))

    with pytest.raises(ProviderPermanentError):
        client.complete(ProviderRequest(messages=(), response_format={}, headers={}))


def test_chat_openai_configuration_uses_base_url_timeout_and_disables_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    class NoCallModel:
        def invoke(self, input: object, **kwargs: object) -> object:
            del input, kwargs
            raise AssertionError("No provider call is expected during construction")

    def fake_chat_openai(**kwargs: object) -> NoCallModel:
        captured.update(kwargs)
        return NoCallModel()

    monkeypatch.setattr(ark_module, "ChatOpenAI", fake_chat_openai)

    ArkAIService(
        api_key=SecretStr("test-only-secret"),
        base_url=BASE_URL,
        model=MODEL,
        request_timeout_seconds=TIMEOUT_SECONDS,
    )

    assert captured["base_url"] == BASE_URL
    assert captured["extra_body"] == {"thinking": {"type": "disabled"}}
    assert captured["model"] == MODEL
    assert captured["timeout"] == TIMEOUT_SECONDS
    assert captured["max_retries"] == 0
    assert captured["use_responses_api"] is True
    assert cast(SecretStr, captured["api_key"]).get_secret_value() == "test-only-secret"


def test_chatopenai_preserves_text_schema_and_correlation_header_without_network() -> None:
    captured_body: dict[str, object] = {}
    captured_header: str | None = None
    captured_path: str | None = None

    def handle_request(request: httpx.Request) -> httpx.Response:
        nonlocal captured_body, captured_header, captured_path
        captured_body = cast(dict[str, object], json.loads(request.content))
        captured_header = request.headers.get("X-Client-Request-Id")
        captured_path = request.url.path
        return httpx.Response(
            200,
            json={
                "id": "resp-test",
                "object": "response",
                "created_at": 1,
                "model": MODEL,
                "output": [
                    {
                        "id": "msg-test",
                        "type": "message",
                        "role": "assistant",
                        "status": "completed",
                        "content": [
                            {
                                "type": "output_text",
                                "annotations": [],
                                "text": json.dumps(
                                    valid_matching_result(), ensure_ascii=False
                                ),
                            }
                        ],
                    }
                ],
                "parallel_tool_calls": True,
                "tool_choice": "auto",
                "tools": [],
            },
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handle_request))
    chat_model = ChatOpenAI(
        api_key=SecretStr("test-only-secret"),
        base_url=BASE_URL,
        extra_body={"thinking": {"type": "disabled"}},
        http_client=http_client,
        max_retries=0,
        model=MODEL,
        timeout=TIMEOUT_SECONDS,
        use_responses_api=True,
    )
    client = ChatOpenAIProviderClient(cast(ark_module.InvokableChatModel, chat_model))
    provider = FakeProviderClient([valid_matching_result()])
    service = create_service(provider)
    service.generate_matching_analysis(
        resume_context_path=resume_context_path(),
        job_description="完整职位描述",
    )
    request = provider.requests[0]

    returned = client.complete(request)

    assert isinstance(returned, str)
    assert json.loads(returned) == valid_matching_result()
    assert captured_path == "/api/v3/responses"
    assert captured_header == request.headers["X-Client-Request-Id"]
    assert captured_body["model"] == MODEL
    assert captured_body["thinking"] == {"type": "disabled"}
    assert captured_body["stream"] is False
    input_items = cast(list[dict[str, object]], captured_body["input"])
    user_item = next(item for item in input_items if item.get("role") == "user")
    content = cast(list[dict[str, object]], user_item["content"])
    assert [item.get("type") for item in content] == ["input_text", "input_text"]
    assert cast(str, content[0]["text"]).endswith(
        resume_context_path().read_text(encoding="utf-8")
    )
    assert content[1]["text"] == "职位描述：\n完整职位描述"
    text_config = cast(dict[str, object], captured_body["text"])
    response_format = cast(dict[str, object], text_config["format"])
    assert response_format["type"] == "json_schema"
    assert response_format["name"] == "matching_analysis"
    assert response_format["strict"] is True


def test_modified_resume_context_is_rejected_before_provider_call(tmp_path: Path) -> None:
    provider = FakeProviderClient([valid_matching_result()])
    wrong_resume = tmp_path / "mei_chang_resume.md"
    wrong_resume.write_text("not the approved resume", encoding="utf-8")

    with pytest.raises(AIServiceError, match="AI processing failed"):
        create_service(provider).generate_matching_analysis(
            resume_context_path=wrong_resume,
            job_description="完整职位描述",
        )

    assert provider.requests == []


def test_renamed_resume_context_is_rejected_before_provider_call(tmp_path: Path) -> None:
    provider = FakeProviderClient([valid_matching_result()])
    renamed_resume = tmp_path / "resume.md"
    renamed_resume.write_bytes(resume_context_path().read_bytes())

    with pytest.raises(AIServiceError, match="AI processing failed"):
        create_service(provider).generate_matching_analysis(
            resume_context_path=renamed_resume,
            job_description="完整职位描述",
        )

    assert provider.requests == []
