from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.ai.schemas import ResumeSourceReference

WorkflowName = Literal["matching", "follow_up", "reliability"]
MatchingStatus = Literal["supported", "partial", "missing"]
Importance = Literal["required", "preferred", "unspecified"]
Answerability = Literal["answerable", "insufficient_evidence", "out_of_scope"]
ReliabilityScenario = Literal[
    "valid_first_response",
    "invalid_then_valid_retry",
    "exhausted_invalid_output",
    "transient_then_valid_retry",
    "non_retryable_provider_failure",
]
HardGuardrail = Literal[
    "no_invented_evidence",
    "no_invented_source_reference",
    "no_prohibited_behavior",
    "insufficient_evidence_gap_is_safe",
    "out_of_scope_declines_without_speculation",
    "schema_and_invariants_valid",
    "retry_behavior_is_bounded",
]


class EvalModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: "".join(
            [field_name.split("_")[0]]
            + [part.capitalize() for part in field_name.split("_")[1:]]
        ),
        extra="forbid",
        populate_by_name=True,
    )


class InputFixture(EvalModel):
    job_description: str | None = None
    base_job_description: str | None = None
    prior_matching_analysis: str | None = None
    question: str | None = None


class ExpectedMatchingRequirement(EvalModel):
    requirement_contains: list[str] = Field(min_length=1)
    status: MatchingStatus
    importance: Importance
    required_evidence_anchors: list[ResumeSourceReference] = Field(default_factory=list)
    allowed_evidence_anchors: list[ResumeSourceReference] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_evidence_anchors(self) -> Self:
        if not set(self.required_evidence_anchors).issubset(
            self.allowed_evidence_anchors
        ):
            raise ValueError("required evidence anchors must also be allowed")
        return self


class ExpectedOutcome(EvalModel):
    matching_requirements: list[ExpectedMatchingRequirement] = Field(default_factory=list)
    answerability: Answerability | None = None
    success: bool = True
    attempts: int = Field(default=1, ge=1, le=2)
    retry_reason: Literal[
        "invalid_structured_output", "transient_provider_error"
    ] | None = None


class RealAICase(EvalModel):
    case_id: str = Field(min_length=1)
    workflow: WorkflowName
    categories: list[str] = Field(min_length=1)
    input_fixture: InputFixture
    expected: ExpectedOutcome
    required_evidence_anchors: list[ResumeSourceReference] = Field(default_factory=list)
    allowed_evidence_anchors: list[ResumeSourceReference] = Field(default_factory=list)
    forbidden_claims: list[str] = Field(default_factory=list)
    hard_guardrail_checks: list[HardGuardrail] = Field(min_length=1)
    explanation_review_focus: str = Field(min_length=1)
    reliability_scenario: ReliabilityScenario | None = None

    @model_validator(mode="after")
    def validate_workflow_fixture(self) -> Self:
        fixture = self.input_fixture
        if self.workflow == "matching":
            if not fixture.job_description or not self.expected.matching_requirements:
                raise ValueError(
                    "matching cases require a job description and expected requirements"
                )
            if self.reliability_scenario is not None:
                raise ValueError("matching cases cannot define a reliability scenario")
        elif self.workflow == "follow_up":
            if not all(
                (
                    fixture.base_job_description,
                    fixture.prior_matching_analysis,
                    fixture.question,
                )
            ):
                raise ValueError("follow-up cases require base context and a question")
            if self.expected.answerability is None:
                raise ValueError("follow-up cases require expected answerability")
            if self.reliability_scenario is not None:
                raise ValueError("follow-up cases cannot define a reliability scenario")
        elif self.reliability_scenario is None or not fixture.job_description:
            raise ValueError("reliability cases require a scenario and job description")

        if self.required_evidence_anchors and not self.allowed_evidence_anchors:
            raise ValueError("required evidence anchors need an allowed-anchor set")
        if not set(self.required_evidence_anchors).issubset(
            self.allowed_evidence_anchors
        ):
            raise ValueError("required evidence anchors must also be allowed")
        return self


class HumanUsefulnessRubric(EvalModel):
    scale: dict[str, str]
    review_instruction: str = Field(min_length=1)


class RealAISuite(EvalModel):
    schema_version: Literal[2]
    suite_id: str = Field(min_length=1)
    client_path: str = Field(min_length=1)
    human_usefulness_rubric: HumanUsefulnessRubric
    cases: list[RealAICase] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_cases_and_required_matrix(self) -> Self:
        case_ids = [case.case_id for case in self.cases]
        if len(case_ids) != len(set(case_ids)):
            raise ValueError("case IDs must be unique")
        categories = {category for case in self.cases for category in case.categories}
        required_categories = {
            "supported_evidence",
            "partial_evidence",
            "missing_information",
            "importance_explicit",
            "importance_unspecified",
            "answerable_evidence_question",
            "insufficient_candidate_evidence",
            "contextual_reference",
            "out_of_scope_request",
            "invented_evidence_or_source",
            "hiring_recommendation",
            "candidate_comparison_or_ranking",
            "future_performance_prediction",
            "overall_match_score",
            "valid_first_response",
            "invalid_then_valid_retry",
            "exhausted_invalid_output",
            "transient_then_valid_retry",
            "non_retryable_provider_failure",
        }
        missing = required_categories - categories
        if missing:
            raise ValueError(f"required evaluation categories missing: {sorted(missing)}")
        return self


class HumanReview(EvalModel):
    invented_evidence_detected: bool
    prohibited_behavior_detected: bool
    gap_handled_safely: bool | None
    out_of_scope_handled_safely: bool | None
    explanation_usefulness: int = Field(ge=1, le=4)


class RuleResult(EvalModel):
    rule_id: str
    passed: bool
    source: Literal["deterministic", "human"]


class CaseMetrics(EvalModel):
    matching_status_correct: bool | None = None
    importance_correct: bool | None = None
    follow_up_answerability_correct: bool | None = None
    evidence_anchors_correct: bool | None = None
    explanation_usefulness: int | None = Field(default=None, ge=0, le=4)
    valid_first_attempt: bool | None = None
    retry_recovered: bool | None = None


class CaseRunResult(EvalModel):
    case_id: str
    run_number: int = Field(ge=1)
    workflow: WorkflowName
    execution_mode: Literal["live", "network_free"]
    success: bool
    workflow_attempts: int = Field(ge=1, le=2)
    provider_calls: int = Field(ge=0, le=2)
    latency_ms: int = Field(ge=0)
    retry_reason: str | None
    validation_status: str
    rule_results: list[RuleResult]
    metrics: CaseMetrics
    failure_categories: list[str]
    human_review: HumanReview | None = None


class AggregateMetrics(EvalModel):
    matching_status_accuracy: float | None
    importance_accuracy: float | None
    follow_up_answerability_accuracy: float | None
    evidence_anchor_correctness: float | None
    explanation_usefulness_mean: float | None
    valid_first_attempt_rate: float | None
    retry_recovery_rate: float | None
    latency_mean_ms: float | None
    latency_p95_ms: int | None


class PrivacyDeclaration(EvalModel):
    contains_resume: Literal[False] = False
    contains_job_description: Literal[False] = False
    contains_question: Literal[False] = False
    contains_prompt: Literal[False] = False
    contains_provider_payload_or_raw_response: Literal[False] = False
    contains_generated_output: Literal[False] = False


class EvaluationArtifact(EvalModel):
    schema_version: Literal[1] = 1
    goal: Literal["8"] = "8"
    suite_id: str
    executed_at: str
    model: str
    client_path: str
    runs_per_case: int = Field(ge=1)
    suite_hash: str
    evaluator_hash: str | None = None
    prompt_hashes: dict[str, str]
    schema_hashes: dict[str, str]
    provider_calls_used: int = Field(ge=0)
    hard_guardrails_passed: bool
    metrics: AggregateMetrics
    case_runs: list[CaseRunResult]
    privacy: PrivacyDeclaration = Field(default_factory=PrivacyDeclaration)
