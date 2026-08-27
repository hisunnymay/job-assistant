import json
from pathlib import Path
from typing import TypedDict, cast

import pytest

from app.ai.follow_up import FollowUpContextMessage
from app.ai.mock import MockAIService


class ExpectedTextCase(TypedDict):
    caseId: str
    requiredSubstrings: list[str]
    forbiddenSubstrings: list[str]


class MatchingReportCase(ExpectedTextCase):
    jobDescription: str


class FollowUpCase(ExpectedTextCase):
    question: str


class GuardrailFixtureSet(TypedDict):
    schemaVersion: int
    baseJobDescription: str
    matchingReportCases: list[MatchingReportCase]
    followUpCases: list[FollowUpCase]


BACKEND_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BACKEND_ROOT / "evals" / "goal_05_guardrail_cases.json"
RESUME_CONTEXT_PATH = (
    BACKEND_ROOT / "app" / "resources" / "resume" / "mei_chang_resume.md"
)
FIXTURES = cast(
    GuardrailFixtureSet,
    json.loads(FIXTURE_PATH.read_text(encoding="utf-8")),
)


def assert_text_expectations(content: str, case: ExpectedTextCase) -> None:
    for required_text in case["requiredSubstrings"]:
        assert required_text in content, case["caseId"]
    for forbidden_text in case["forbiddenSubstrings"]:
        assert forbidden_text not in content, case["caseId"]


def test_guardrail_fixture_schema_is_versioned_and_complete() -> None:
    assert FIXTURES["schemaVersion"] == 1
    assert {
        case["caseId"] for case in FIXTURES["matchingReportCases"]
    } == {
        "supported_candidate_evidence",
        "partial_engineering_information",
        "missing_quantified_results",
    }
    assert {
        case["caseId"] for case in FIXTURES["followUpCases"]
    } == {
        "supported_agent_evidence",
        "reject_invented_team_size",
        "reject_hiring_recommendation",
        "reject_candidate_ranking",
        "reject_future_performance_prediction",
        "reject_overall_scoring",
    }


@pytest.mark.parametrize(
    "case",
    FIXTURES["matchingReportCases"],
    ids=[case["caseId"] for case in FIXTURES["matchingReportCases"]],
)
def test_matching_report_guardrail_case(case: MatchingReportCase) -> None:
    content = MockAIService().generate_matching_analysis(
        resume_context_path=RESUME_CONTEXT_PATH,
        job_description=case["jobDescription"],
    )

    assert_text_expectations(content, case)


@pytest.mark.parametrize(
    "case",
    FIXTURES["followUpCases"],
    ids=[case["caseId"] for case in FIXTURES["followUpCases"]],
)
def test_follow_up_guardrail_case(case: FollowUpCase) -> None:
    ai_service = MockAIService()
    matching_report = ai_service.generate_matching_analysis(
        resume_context_path=RESUME_CONTEXT_PATH,
        job_description=FIXTURES["baseJobDescription"],
    )
    content = ai_service.answer_follow_up(
        resume_context_path=RESUME_CONTEXT_PATH,
        conversation_history=(
            FollowUpContextMessage(
                role="user",
                message_type="job_description",
                content=FIXTURES["baseJobDescription"],
            ),
            FollowUpContextMessage(
                role="assistant",
                message_type="matching_analysis",
                content=matching_report,
            ),
            FollowUpContextMessage(
                role="user",
                message_type="follow_up_question",
                content=case["question"],
            ),
        ),
    )

    assert_text_expectations(content, case)
