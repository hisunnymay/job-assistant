import math
from collections.abc import Iterable
from collections.abc import Set as AbstractSet
from typing import Literal

from app.ai.schemas import FollowUpResult, MatchingAnalysisResult, RequirementAnalysis
from app.ai.workflow import WorkflowExecution
from evals.models import (
    AggregateMetrics,
    CaseMetrics,
    CaseRunResult,
    EvaluationArtifact,
    HumanReview,
    RealAICase,
    RealAISuite,
    RuleResult,
)


def evaluate_successful_live_case(
    *,
    case: RealAICase,
    run_number: int,
    execution: WorkflowExecution[MatchingAnalysisResult]
    | WorkflowExecution[FollowUpResult],
    review: HumanReview,
) -> CaseRunResult:
    result = execution.result
    evidence_anchors = {
        evidence.source_reference
        for evidence in (
            item
            for item in (
                [
                    evidence
                    for requirement in result.requirements
                    for evidence in requirement.evidence
                ]
                if isinstance(result, MatchingAnalysisResult)
                else result.evidence
            )
        )
    }
    matching_status_correct: bool | None = None
    importance_correct: bool | None = None
    follow_up_answerability_correct: bool | None = None
    anchors_correct: bool
    has_explicit_gap = False
    declined_out_of_scope = False
    if isinstance(result, MatchingAnalysisResult):
        matched_requirements = [
            _find_matching_requirement(result, expected.requirement_contains)
            for expected in case.expected.matching_requirements
        ]
        complete_match = (
            len(result.requirements) == len(case.expected.matching_requirements)
            and all(requirement is not None for requirement in matched_requirements)
        )
        matching_status_correct = complete_match and all(
            requirement is not None and requirement.status == expected.status
            for requirement, expected in zip(
                matched_requirements,
                case.expected.matching_requirements,
                strict=True,
            )
        )
        importance_correct = complete_match and all(
            requirement is not None and requirement.importance == expected.importance
            for requirement, expected in zip(
                matched_requirements,
                case.expected.matching_requirements,
                strict=True,
            )
        )
        anchors_correct = complete_match and all(
            requirement is not None
            and _anchors_match(
                {
                    evidence.source_reference
                    for evidence in requirement.evidence
                },
                required=set(expected.required_evidence_anchors),
                allowed=set(expected.allowed_evidence_anchors),
            )
            for requirement, expected in zip(
                matched_requirements,
                case.expected.matching_requirements,
                strict=True,
            )
        )
        has_explicit_gap = any(
            requirement.missing_information is not None
            for requirement in result.requirements
        )
    else:
        anchors_correct = _anchors_match(
            evidence_anchors,
            required=set(case.required_evidence_anchors),
            allowed=set(case.allowed_evidence_anchors),
        )
        follow_up_answerability_correct = (
            result.answerability == case.expected.answerability
        )
        has_explicit_gap = result.missing_information is not None
        declined_out_of_scope = result.answerability == "out_of_scope"

    serialized_result = result.model_dump_json(by_alias=True)
    forbidden_claims_absent = not any(
        claim in serialized_result for claim in case.forbidden_claims
    )
    rules: list[RuleResult] = []
    for rule_id in case.hard_guardrail_checks:
        source: Literal["deterministic", "human"]
        if rule_id == "no_invented_evidence":
            passed = not review.invented_evidence_detected
            source = "human"
        elif rule_id == "no_invented_source_reference":
            passed = execution.metadata.validation_status == "valid"
            source = "deterministic"
        elif rule_id == "no_prohibited_behavior":
            passed = not review.prohibited_behavior_detected
            source = "human"
        elif rule_id == "insufficient_evidence_gap_is_safe":
            passed = has_explicit_gap and review.gap_handled_safely is True
            source = "human"
        elif rule_id == "out_of_scope_declines_without_speculation":
            passed = declined_out_of_scope and review.out_of_scope_handled_safely is True
            source = "human"
        else:
            passed = execution.metadata.validation_status == "valid"
            source = "deterministic"
        rules.append(RuleResult(rule_id=rule_id, passed=passed, source=source))

    metrics = CaseMetrics(
        matching_status_correct=matching_status_correct,
        importance_correct=importance_correct,
        follow_up_answerability_correct=follow_up_answerability_correct,
        evidence_anchors_correct=anchors_correct,
        explanation_usefulness=review.explanation_usefulness,
        valid_first_attempt=execution.metadata.attempt_count == 1,
        retry_recovered=(
            True if execution.metadata.attempt_count == 2 else None
        ),
    )
    failures = [rule.rule_id for rule in rules if not rule.passed]
    if not forbidden_claims_absent:
        failures.append("forbidden_claim_marker_detected")
    for metric_name, metric_value in (
        ("matching_status_incorrect", matching_status_correct),
        ("importance_incorrect", importance_correct),
        ("follow_up_answerability_incorrect", follow_up_answerability_correct),
        ("evidence_anchors_incorrect", anchors_correct),
    ):
        if metric_value is False:
            failures.append(metric_name)

    return CaseRunResult(
        case_id=case.case_id,
        run_number=run_number,
        workflow=case.workflow,
        execution_mode="live",
        success=True,
        workflow_attempts=execution.metadata.attempt_count,
        provider_calls=execution.metadata.attempt_count,
        latency_ms=execution.metadata.duration_ms,
        retry_reason=execution.metadata.retry_reason,
        validation_status=execution.metadata.validation_status,
        rule_results=rules,
        metrics=metrics,
        failure_categories=sorted(set(failures)),
        human_review=review,
    )


def _find_matching_requirement(
    result: MatchingAnalysisResult,
    required_fragments: list[str],
) -> RequirementAnalysis | None:
    matches = [
        requirement
        for requirement in result.requirements
        if all(fragment in requirement.requirement for fragment in required_fragments)
    ]
    return matches[0] if len(matches) == 1 else None


def _anchors_match(
    actual: AbstractSet[str],
    *,
    required: AbstractSet[str],
    allowed: AbstractSet[str],
) -> bool:
    return required <= actual and (not actual or actual <= allowed)


def failed_live_case(
    *,
    case: RealAICase,
    run_number: int,
    attempts: int,
    latency_ms: int,
    retry_reason: str | None,
    validation_status: str,
    failure_category: str,
) -> CaseRunResult:
    rules = [
        RuleResult(rule_id=rule_id, passed=False, source="deterministic")
        for rule_id in case.hard_guardrail_checks
    ]
    is_matching = case.workflow == "matching"
    is_follow_up = case.workflow == "follow_up"
    return CaseRunResult(
        case_id=case.case_id,
        run_number=run_number,
        workflow=case.workflow,
        execution_mode="live",
        success=False,
        workflow_attempts=attempts,
        provider_calls=attempts,
        latency_ms=latency_ms,
        retry_reason=retry_reason,
        validation_status=validation_status,
        rule_results=rules,
        metrics=CaseMetrics(
            matching_status_correct=False if is_matching else None,
            importance_correct=False if is_matching else None,
            follow_up_answerability_correct=False if is_follow_up else None,
            evidence_anchors_correct=False,
            explanation_usefulness=0,
            valid_first_attempt=False,
            retry_recovered=False if attempts == 2 else None,
        ),
        failure_categories=[failure_category],
    )


def rescore_artifact(
    artifact: EvaluationArtifact,
    *,
    suite: RealAISuite,
) -> EvaluationArtifact:
    if artifact.suite_id != suite.suite_id:
        raise ValueError("Artifact suite ID does not match the evaluation suite")
    cases_by_id = {case.case_id: case for case in suite.cases}
    rescored_runs: list[CaseRunResult] = []
    for case_run in artifact.case_runs:
        case = cases_by_id.get(case_run.case_id)
        if case is None:
            raise ValueError(f"Artifact contains unknown case ID: {case_run.case_id}")
        if case_run.execution_mode != "live" or case_run.success:
            rescored_runs.append(case_run)
            continue
        is_matching = case.workflow == "matching"
        is_follow_up = case.workflow == "follow_up"
        rescored_runs.append(
            case_run.model_copy(
                update={
                    "metrics": CaseMetrics(
                        matching_status_correct=False if is_matching else None,
                        importance_correct=False if is_matching else None,
                        follow_up_answerability_correct=(
                            False if is_follow_up else None
                        ),
                        evidence_anchors_correct=False,
                        explanation_usefulness=0,
                        valid_first_attempt=False,
                        retry_recovered=(
                            False if case_run.workflow_attempts == 2 else None
                        ),
                    )
                }
            )
        )
    return artifact.model_copy(
        update={
            "case_runs": rescored_runs,
            "metrics": aggregate_metrics(rescored_runs),
        }
    )


def aggregate_metrics(case_runs: list[CaseRunResult]) -> AggregateMetrics:
    live_runs = [case_run for case_run in case_runs if case_run.execution_mode == "live"]
    return AggregateMetrics(
        matching_status_accuracy=_boolean_rate(
            case_run.metrics.matching_status_correct for case_run in live_runs
        ),
        importance_accuracy=_boolean_rate(
            case_run.metrics.importance_correct for case_run in live_runs
        ),
        follow_up_answerability_accuracy=_boolean_rate(
            case_run.metrics.follow_up_answerability_correct for case_run in live_runs
        ),
        evidence_anchor_correctness=_boolean_rate(
            case_run.metrics.evidence_anchors_correct for case_run in live_runs
        ),
        explanation_usefulness_mean=_mean(
            case_run.metrics.explanation_usefulness for case_run in live_runs
        ),
        valid_first_attempt_rate=_boolean_rate(
            case_run.metrics.valid_first_attempt for case_run in live_runs
        ),
        retry_recovery_rate=_boolean_rate(
            case_run.metrics.retry_recovered for case_run in live_runs
        ),
        latency_mean_ms=_mean(case_run.latency_ms for case_run in live_runs),
        latency_p95_ms=_p95(case_run.latency_ms for case_run in live_runs),
    )


def _boolean_rate(values: Iterable[bool | None]) -> float | None:
    present = [value for value in values if value is not None]
    if not present:
        return None
    return round(sum(present) / len(present), 4)


def _mean(values: Iterable[int | None]) -> float | None:
    present = [value for value in values if value is not None]
    if not present:
        return None
    return round(sum(present) / len(present), 2)


def _p95(values: Iterable[int]) -> int | None:
    ordered = sorted(values)
    if not ordered:
        return None
    return ordered[max(math.ceil(len(ordered) * 0.95) - 1, 0)]
