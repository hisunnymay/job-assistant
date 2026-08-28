import json
import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from time import monotonic
from typing import Literal, TypeVar, cast
from uuid import uuid4

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ValidationError
from typing_extensions import TypedDict

from app.ai.matching import AIServiceError

logger = logging.getLogger(__name__)

ModelT = TypeVar("ModelT", bound=BaseModel)
Route = Literal["generate", "validate", "render", "error"]


@dataclass(frozen=True)
class WorkflowExecutionMetadata:
    attempt_count: int
    duration_ms: int
    validation_status: str
    error_type: str | None
    provider_error_type: str | None
    retry_reason: str | None


@dataclass(frozen=True)
class WorkflowExecution[ResultT: BaseModel]:
    result: ResultT
    rendered_output: str
    metadata: WorkflowExecutionMetadata


class WorkflowExecutionError(AIServiceError):
    """A safe workflow failure carrying only evaluation-safe execution metadata."""

    def __init__(self, metadata: WorkflowExecutionMetadata) -> None:
        super().__init__("AI processing failed")
        self.metadata = metadata


class ProviderTransientError(Exception):
    """A privacy-safe signal that the provider call may be retried."""

    def __init__(self, source_type: str = "unknown") -> None:
        super().__init__(source_type)
        self.source_type = source_type


class ProviderPermanentError(Exception):
    """A privacy-safe signal that the provider call must not be retried."""

    def __init__(self, source_type: str = "unknown") -> None:
        super().__init__(source_type)
        self.source_type = source_type


class WorkflowState(TypedDict, total=False):
    attempt_count: int
    provider_call_succeeded: bool
    raw_output: object | None
    parsed_output: BaseModel | None
    rendered_output: str | None
    retryable: bool
    validation_status: str
    error_type: str | None
    provider_error_type: str | None
    retry_reason: str | None


class StructuredAIWorkflow:
    def __init__(self, *, workflow_name: str, model: str, max_attempts: int = 2) -> None:
        if max_attempts != 2:
            raise ValueError("The approved MVP workflow requires exactly two attempts")
        self._workflow_name = workflow_name
        self._model = model
        self._max_attempts = max_attempts

    def run(
        self,
        *,
        generate: Callable[[str, bool], object],
        schema: type[ModelT],
        renderer: Callable[[ModelT], str],
    ) -> str:
        return self.execute(generate=generate, schema=schema, renderer=renderer).rendered_output

    def execute(
        self,
        *,
        generate: Callable[[str, bool], object],
        schema: type[ModelT],
        renderer: Callable[[ModelT], str],
    ) -> WorkflowExecution[ModelT]:
        request_id = f"ai_{uuid4().hex}"
        started_at = monotonic()

        def generate_node(state: WorkflowState) -> WorkflowState:
            attempt_count = state.get("attempt_count", 0) + 1
            use_structured_output_correction = (
                state.get("error_type") == "invalid_structured_output"
            )
            try:
                raw_output = generate(request_id, use_structured_output_correction)
            except ProviderTransientError as error:
                return {
                    "attempt_count": attempt_count,
                    "provider_call_succeeded": False,
                    "raw_output": None,
                    "parsed_output": None,
                    "rendered_output": None,
                    "retryable": True,
                    "validation_status": "not_validated",
                    "error_type": "transient_provider_error",
                    "provider_error_type": error.source_type,
                    "retry_reason": state.get("retry_reason")
                    or "transient_provider_error",
                }
            except ProviderPermanentError as error:
                return {
                    "attempt_count": attempt_count,
                    "provider_call_succeeded": False,
                    "raw_output": None,
                    "parsed_output": None,
                    "rendered_output": None,
                    "retryable": False,
                    "validation_status": "not_validated",
                    "error_type": "permanent_provider_error",
                    "provider_error_type": error.source_type,
                    "retry_reason": state.get("retry_reason"),
                }
            return {
                "attempt_count": attempt_count,
                "provider_call_succeeded": True,
                "raw_output": raw_output,
                "parsed_output": None,
                "rendered_output": None,
                "retryable": False,
                "validation_status": "pending",
                "error_type": None,
                "provider_error_type": None,
                "retry_reason": state.get("retry_reason"),
            }

        def route_after_generate(state: WorkflowState) -> Route:
            if state.get("provider_call_succeeded"):
                return "validate"
            if state.get("retryable") and state.get("attempt_count", 0) < self._max_attempts:
                return "generate"
            return "error"

        def validate_node(state: WorkflowState) -> WorkflowState:
            try:
                candidate = _parse_json_object(state.get("raw_output"))
                parsed_output = schema.model_validate(candidate)
            except (TypeError, ValueError, json.JSONDecodeError, ValidationError):
                return {
                    "parsed_output": None,
                    "retryable": True,
                    "validation_status": "invalid",
                    "error_type": "invalid_structured_output",
                    "provider_error_type": None,
                    "retry_reason": state.get("retry_reason")
                    or "invalid_structured_output",
                }
            return {
                "parsed_output": parsed_output,
                "retryable": False,
                "validation_status": "valid",
                "error_type": None,
                "provider_error_type": None,
                "retry_reason": state.get("retry_reason"),
            }

        def route_after_validate(state: WorkflowState) -> Route:
            if state.get("parsed_output") is not None:
                return "render"
            if state.get("attempt_count", 0) < self._max_attempts:
                return "generate"
            return "error"

        def render_node(state: WorkflowState) -> WorkflowState:
            parsed_output = state.get("parsed_output")
            if parsed_output is None:
                return {
                    "rendered_output": None,
                    "error_type": "rendering_error",
                }
            rendered_output = renderer(cast(ModelT, parsed_output)).strip()
            if not rendered_output:
                return {
                    "rendered_output": None,
                    "error_type": "rendering_error",
                }
            return {"rendered_output": rendered_output}

        def route_after_render(state: WorkflowState) -> Literal["complete", "error"]:
            if state.get("rendered_output"):
                return "complete"
            return "error"

        def error_node(state: WorkflowState) -> WorkflowState:
            return state

        graph = StateGraph(WorkflowState)
        graph.add_node("generate", generate_node)
        graph.add_node("validate", validate_node)
        graph.add_node("render", render_node)
        graph.add_node("error", error_node)
        graph.add_edge(START, "generate")
        graph.add_conditional_edges(
            "generate",
            route_after_generate,
            {"generate": "generate", "validate": "validate", "error": "error"},
        )
        graph.add_conditional_edges(
            "validate",
            route_after_validate,
            {"generate": "generate", "render": "render", "error": "error"},
        )
        graph.add_conditional_edges(
            "render",
            route_after_render,
            {"complete": END, "error": "error"},
        )
        graph.add_edge("error", END)

        result = graph.compile().invoke(
            WorkflowState(
                attempt_count=0,
                provider_call_succeeded=False,
                raw_output=None,
                parsed_output=None,
                rendered_output=None,
                retryable=False,
                validation_status="not_validated",
                error_type=None,
                provider_error_type=None,
                retry_reason=None,
            )
        )
        duration_ms = round((monotonic() - started_at) * 1000)
        metadata = WorkflowExecutionMetadata(
            attempt_count=result.get("attempt_count", 0),
            duration_ms=duration_ms,
            validation_status=result.get("validation_status", "not_validated"),
            error_type=result.get("error_type"),
            provider_error_type=result.get("provider_error_type"),
            retry_reason=result.get("retry_reason"),
        )
        log_fields = {
            "request_id": request_id,
            "workflow": self._workflow_name,
            "model": self._model,
            "duration_ms": metadata.duration_ms,
            "attempt_count": metadata.attempt_count,
            "retry_count": max(metadata.attempt_count - 1, 0),
            "validation_status": metadata.validation_status,
            "error_type": metadata.error_type,
            "provider_error_type": metadata.provider_error_type,
            "retry_reason": metadata.retry_reason,
        }
        rendered_output = result.get("rendered_output")
        parsed_output = result.get("parsed_output")
        if rendered_output and parsed_output is not None:
            logger.info("ai_execution_completed", extra=log_fields)
            return WorkflowExecution(
                result=cast(ModelT, parsed_output),
                rendered_output=cast(str, rendered_output),
                metadata=metadata,
            )

        logger.warning("ai_execution_failed", extra=log_fields)
        raise WorkflowExecutionError(metadata)


def _parse_json_object(raw_output: object | None) -> Mapping[str, object]:
    candidate = json.loads(raw_output) if isinstance(raw_output, str) else raw_output
    if not isinstance(candidate, Mapping):
        raise TypeError("Structured output must be a JSON object")
    return cast(Mapping[str, object], candidate)
