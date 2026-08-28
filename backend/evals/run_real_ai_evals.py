import argparse
import hashlib
import json
import os
import sys
from collections.abc import Callable, Iterator, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from pydantic import BaseModel, SecretStr, ValidationError

from app.ai.ark import ArkAIService, ProviderClient, ProviderRequest
from app.ai.follow_up import FollowUpContextMessage
from app.ai.matching import AIServiceError
from app.ai.prompts import (
    FOLLOW_UP_SYSTEM_PROMPT,
    MATCHING_SYSTEM_PROMPT,
    STRUCTURED_OUTPUT_CORRECTION_PROMPT,
)
from app.ai.schemas import FollowUpResult, MatchingAnalysisResult
from app.ai.workflow import (
    ProviderPermanentError,
    ProviderTransientError,
    WorkflowExecution,
    WorkflowExecutionError,
)
from app.core.config import Settings
from app.resources.candidate_resume import get_candidate_resume_context_path
from evals.evaluator import (
    aggregate_metrics,
    evaluate_successful_live_case,
    failed_live_case,
)
from evals.models import (
    CaseMetrics,
    CaseRunResult,
    EvaluationArtifact,
    HumanReview,
    RealAICase,
    RealAISuite,
    RuleResult,
)

Reviewer = Callable[[RealAICase, BaseModel], HumanReview]
CLIENT_PATH = "LangChain ChatOpenAI Responses API"
APPROVED_GOAL_08_MODEL = "doubao-seed-2-1-pro-260628"
EVALUATOR_PATH = Path(__file__).with_name("evaluator.py")
PROHIBITED_ARTIFACT_KEYS = {
    "baseJobDescription",
    "generatedOutput",
    "jobDescription",
    "priorMatchingAnalysis",
    "providerPayload",
    "question",
    "rawResponse",
    "renderedOutput",
    "resumeContent",
}


class ScriptedProviderClient(ProviderClient):
    def __init__(self, responses: Sequence[object]) -> None:
        self._responses: Iterator[object] = iter(responses)
        self.requests: list[ProviderRequest] = []

    def complete(self, request: ProviderRequest) -> object:
        self.requests.append(request)
        response = next(self._responses)
        if isinstance(response, Exception):
            raise response
        return response


def load_suite(path: Path) -> tuple[RealAISuite, bytes]:
    raw = path.read_bytes()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("Evaluation case file must be valid UTF-8 JSON") from error
    return RealAISuite.model_validate(payload), raw


def run_suite(
    *,
    suite: RealAISuite,
    suite_bytes: bytes,
    service: ArkAIService,
    model: str,
    runs: int,
    max_provider_calls: int,
    reviewer: Reviewer,
    case_ids: Sequence[str] | None = None,
    sensitive_values: Sequence[str] = (),
) -> EvaluationArtifact:
    if runs < 1:
        raise ValueError("runs must be at least 1")
    if model != APPROVED_GOAL_08_MODEL:
        raise ValueError(
            f"Goal 8 evaluations require the approved model {APPROVED_GOAL_08_MODEL}"
        )
    if max_provider_calls < 0:
        raise ValueError("max_provider_calls must not be negative")
    selected_case_ids = set(case_ids) if case_ids else None
    if selected_case_ids is not None:
        known_case_ids = {case.case_id for case in suite.cases}
        unknown_case_ids = selected_case_ids - known_case_ids
        if unknown_case_ids:
            unknown = ", ".join(sorted(unknown_case_ids))
            raise ValueError(f"Unknown Goal 8 case IDs: {unknown}")
    selected_cases = [
        case
        for case in suite.cases
        if selected_case_ids is None or case.case_id in selected_case_ids
    ]
    maximum_required_calls = (
        sum(case.workflow != "reliability" for case in selected_cases) * runs * 2
    )
    if maximum_required_calls > max_provider_calls:
        raise ValueError(
            "Provider call budget is below the selected run's worst-case requirement: "
            f"budget={max_provider_calls}, required={maximum_required_calls}"
        )
    case_runs: list[CaseRunResult] = []
    generated_outputs: list[str] = []
    for run_number in range(1, runs + 1):
        for case in selected_cases:
            if case.workflow == "reliability":
                case_runs.append(_run_reliability_case(case=case, run_number=run_number))
                continue
            try:
                execution = _execute_live_case(service=service, case=case)
            except WorkflowExecutionError as error:
                metadata = error.metadata
                case_runs.append(
                    failed_live_case(
                        case=case,
                        run_number=run_number,
                        attempts=metadata.attempt_count,
                        latency_ms=metadata.duration_ms,
                        retry_reason=metadata.retry_reason,
                        validation_status=metadata.validation_status,
                        failure_category=metadata.error_type or "ai_processing_failed",
                    )
                )
                continue
            except AIServiceError:
                case_runs.append(
                    failed_live_case(
                        case=case,
                        run_number=run_number,
                        attempts=1,
                        latency_ms=0,
                        retry_reason=None,
                        validation_status="not_validated",
                        failure_category="ai_processing_failed",
                    )
                )
                continue

            generated_outputs.extend(
                (
                    execution.rendered_output,
                    execution.result.model_dump_json(by_alias=True),
                )
            )
            review = reviewer(case, execution.result)
            case_runs.append(
                evaluate_successful_live_case(
                    case=case,
                    run_number=run_number,
                    execution=execution,
                    review=review,
                )
            )

    artifact = EvaluationArtifact(
        suite_id=suite.suite_id,
        executed_at=datetime.now(UTC).isoformat(),
        model=model,
        client_path=suite.client_path,
        runs_per_case=runs,
        suite_hash=_sha256_bytes(suite_bytes),
        evaluator_hash=_sha256_bytes(EVALUATOR_PATH.read_bytes()),
        prompt_hashes={
            "matching": _sha256_text(MATCHING_SYSTEM_PROMPT),
            "followUp": _sha256_text(FOLLOW_UP_SYSTEM_PROMPT),
            "structuredOutputCorrection": _sha256_text(
                STRUCTURED_OUTPUT_CORRECTION_PROMPT
            ),
        },
        schema_hashes={
            "matching": _schema_hash(MatchingAnalysisResult),
            "followUp": _schema_hash(FollowUpResult),
        },
        provider_calls_used=sum(case_run.provider_calls for case_run in case_runs),
        hard_guardrails_passed=(
            all(rule.passed for case_run in case_runs for rule in case_run.rule_results)
            and all(
                "forbidden_claim_marker_detected" not in case_run.failure_categories
                for case_run in case_runs
            )
        ),
        metrics=aggregate_metrics(case_runs),
        case_runs=case_runs,
    )
    _assert_artifact_privacy(
        artifact,
        suite=suite,
        generated_outputs=generated_outputs,
        sensitive_values=sensitive_values,
    )
    return artifact


def write_artifact(path: Path, artifact: EvaluationArtifact) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        artifact.model_dump_json(by_alias=True, indent=2) + "\n",
        encoding="utf-8",
    )


def _execute_live_case(
    *,
    service: ArkAIService,
    case: RealAICase,
) -> WorkflowExecution[MatchingAnalysisResult] | WorkflowExecution[FollowUpResult]:
    fixture = case.input_fixture
    if case.workflow == "matching":
        if fixture.job_description is None:
            raise ValueError("Validated matching fixture is incomplete")
        return service.execute_matching_analysis(
            resume_context_path=get_candidate_resume_context_path(),
            job_description=fixture.job_description,
        )
    if case.workflow != "follow_up" or any(
        value is None
        for value in (
            fixture.base_job_description,
            fixture.prior_matching_analysis,
            fixture.question,
        )
    ):
        raise ValueError("Validated follow-up fixture is incomplete")
    return service.execute_follow_up(
        resume_context_path=get_candidate_resume_context_path(),
        conversation_history=(
            FollowUpContextMessage(
                role="user",
                message_type="job_description",
                content=cast(str, fixture.base_job_description),
            ),
            FollowUpContextMessage(
                role="assistant",
                message_type="matching_analysis",
                content=cast(str, fixture.prior_matching_analysis),
            ),
            FollowUpContextMessage(
                role="user",
                message_type="follow_up_question",
                content=cast(str, fixture.question),
            ),
        ),
    )


def _run_reliability_case(*, case: RealAICase, run_number: int) -> CaseRunResult:
    scenario = case.reliability_scenario
    valid = _valid_reliability_result()
    responses: dict[str, list[object]] = {
        "valid_first_response": [valid],
        "invalid_then_valid_retry": [{"summary": "invalid"}, valid],
        "exhausted_invalid_output": [
            {"summary": "invalid"},
            {"summary": "still invalid"},
        ],
        "transient_then_valid_retry": [ProviderTransientError("synthetic"), valid],
        "non_retryable_provider_failure": [ProviderPermanentError("synthetic")],
    }
    if scenario is None:
        raise ValueError("Validated reliability case is missing its scenario")
    provider = ScriptedProviderClient(responses[scenario])
    service = ArkAIService(
        api_key=SecretStr("network-free-evaluation-key"),
        base_url="https://example.invalid/api/v3",
        model="network-free-reliability-fixture",
        request_timeout_seconds=1,
        provider_client=provider,
    )
    success = False
    validation_status = "not_validated"
    retry_reason: str | None = None
    latency_ms = 0
    try:
        execution = service.execute_matching_analysis(
            resume_context_path=get_candidate_resume_context_path(),
            job_description=cast(str, case.input_fixture.job_description),
        )
    except WorkflowExecutionError as error:
        metadata = error.metadata
        attempts = metadata.attempt_count
        validation_status = metadata.validation_status
        retry_reason = metadata.retry_reason
        latency_ms = metadata.duration_ms
    else:
        success = True
        attempts = execution.metadata.attempt_count
        validation_status = execution.metadata.validation_status
        retry_reason = execution.metadata.retry_reason
        latency_ms = execution.metadata.duration_ms

    expected_passed = (
        success == case.expected.success
        and attempts == case.expected.attempts
        and retry_reason == case.expected.retry_reason
        and len(provider.requests) == attempts
        and attempts <= 2
    )
    return CaseRunResult(
        case_id=case.case_id,
        run_number=run_number,
        workflow="reliability",
        execution_mode="network_free",
        success=success,
        workflow_attempts=attempts,
        provider_calls=0,
        latency_ms=latency_ms,
        retry_reason=retry_reason,
        validation_status=validation_status,
        rule_results=[
            RuleResult(
                rule_id="retry_behavior_is_bounded",
                passed=expected_passed,
                source="deterministic",
            )
        ],
        metrics=CaseMetrics(
            valid_first_attempt=success and attempts == 1,
            retry_recovered=True if success and attempts == 2 else None,
        ),
        failure_categories=[] if expected_passed else ["reliability_behavior_mismatch"],
    )


def _valid_reliability_result() -> dict[str, object]:
    return {
        "summary": "现有简历提供了相关证据。",
        "requirements": [
            {
                "requirement": "AI 产品经验",
                "importance": "required",
                "status": "supported",
                "evidence": [
                    {
                        "evidenceText": "负责大模型测试与评估平台",
                        "sourceReference": "Lucy 大模型测试与评估平台",
                    }
                ],
                "explanation": "简历中的项目经历直接支持该要求。",
                "missingInformation": None,
            }
        ],
    }


def _schema_hash(schema: type[BaseModel]) -> str:
    canonical = json.dumps(
        schema.model_json_schema(by_alias=True, mode="validation"),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return _sha256_text(canonical)


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _assert_artifact_privacy(
    artifact: EvaluationArtifact,
    *,
    suite: RealAISuite,
    generated_outputs: Sequence[str],
    sensitive_values: Sequence[str],
) -> None:
    payload = artifact.model_dump(by_alias=True)
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    _assert_no_prohibited_keys(payload)
    fixture_values = [
        value
        for case in suite.cases
        for value in case.input_fixture.model_dump().values()
        if isinstance(value, str) and value
    ]
    protected_values = [
        MATCHING_SYSTEM_PROMPT,
        FOLLOW_UP_SYSTEM_PROMPT,
        STRUCTURED_OUTPUT_CORRECTION_PROMPT,
        get_candidate_resume_context_path().read_text(encoding="utf-8"),
        *fixture_values,
        *generated_outputs,
        *sensitive_values,
    ]
    leaked = [value for value in protected_values if value and value in serialized]
    if leaked:
        raise ValueError("Privacy-safe artifact validation detected protected content")


def _assert_no_prohibited_keys(value: object) -> None:
    if isinstance(value, Mapping):
        prohibited = PROHIBITED_ARTIFACT_KEYS.intersection(value)
        if prohibited:
            raise ValueError(f"Privacy-safe artifact contains prohibited keys: {prohibited}")
        for nested in value.values():
            _assert_no_prohibited_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_no_prohibited_keys(nested)


def _interactive_reviewer(rubric: Mapping[str, str]) -> Reviewer:
    def review(case: RealAICase, result: BaseModel) -> HumanReview:
        print(f"\nReview case: {case.case_id}")
        print(f"Focus: {case.explanation_review_focus}")
        print(json.dumps(result.model_dump(by_alias=True), ensure_ascii=False, indent=2))
        print("Usefulness rubric:")
        for score, description in sorted(rubric.items()):
            print(f"  {score}: {description}")
        prompt = (
            "Enter compact JSON with inventedEvidenceDetected, "
            "prohibitedBehaviorDetected, gapHandledSafely (true/false/null), "
            "outOfScopeHandledSafely (true/false/null), and "
            "explanationUsefulness (1-4): "
        )
        while True:
            try:
                return HumanReview.model_validate(json.loads(input(prompt)))
            except (json.JSONDecodeError, ValidationError) as error:
                print(f"Invalid privacy-safe review decision: {error}")

    return review


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Goal 8 real-AI evaluations")
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--runs", required=True, type=int)
    parser.add_argument("--max-provider-calls", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--case-id",
        action="append",
        help="Run only the named case; repeat the option to select multiple cases",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if os.getenv("RUN_LIVE_ARK_EVALS") != "1":
        raise SystemExit("Set RUN_LIVE_ARK_EVALS=1 to authorize the live-eval runner")
    settings = Settings()
    if settings.ai_provider != "ark" or settings.ark_api_key is None:
        raise SystemExit("Live Goal 8 evaluations require AI_PROVIDER=ark and ARK_API_KEY")
    if settings.ark_model != APPROVED_GOAL_08_MODEL:
        raise SystemExit(
            f"Goal 8 evaluations require ARK_MODEL={APPROVED_GOAL_08_MODEL}"
        )
    if not sys.stdin.isatty():
        raise SystemExit("Goal 8 live evaluations require an interactive human reviewer")
    suite, suite_bytes = load_suite(args.cases)
    service = ArkAIService(
        api_key=settings.ark_api_key,
        base_url=settings.ark_base_url,
        model=settings.ark_model,
        request_timeout_seconds=settings.ark_request_timeout_seconds,
    )
    artifact = run_suite(
        suite=suite,
        suite_bytes=suite_bytes,
        service=service,
        model=settings.ark_model,
        runs=args.runs,
        max_provider_calls=args.max_provider_calls,
        reviewer=_interactive_reviewer(suite.human_usefulness_rubric.scale),
        case_ids=args.case_id,
        sensitive_values=(settings.ark_api_key.get_secret_value(),),
    )
    write_artifact(args.output, artifact)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "providerCallsUsed": artifact.provider_calls_used,
                "hardGuardrailsPassed": artifact.hard_guardrails_passed,
                "metrics": artifact.metrics.model_dump(by_alias=True),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
