import json
from pathlib import Path

import pytest
from pydantic import SecretStr

from app.ai.ark import ArkAIService
from evals.models import ExpectedMatchingRequirement, HumanReview, RealAICase
from evals.run_real_ai_evals import (
    ScriptedProviderClient,
    load_suite,
    main,
    run_suite,
    write_artifact,
)

BACKEND_ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = BACKEND_ROOT / "evals" / "goal_08_real_ai_cases.json"
MODEL = "doubao-seed-2-1-pro-260628"
PRIVATE_OUTPUT_MARKER = "generated-private-output-marker"


def test_goal_08_case_matrix_is_versioned_typed_and_complete() -> None:
    suite, raw = load_suite(CASES_PATH)

    assert suite.schema_version == 2
    assert suite.suite_id == "goal-08-real-ai-v2"
    assert raw == CASES_PATH.read_bytes()
    assert len(suite.cases) == 15
    assert {case.workflow for case in suite.cases} == {
        "matching",
        "follow_up",
        "reliability",
    }
    assert len({case.case_id for case in suite.cases}) == len(suite.cases)


def test_fake_adapter_runner_covers_metrics_reliability_and_privacy(
    tmp_path: Path,
) -> None:
    suite, raw = load_suite(CASES_PATH)
    live_cases = [case for case in suite.cases if case.workflow != "reliability"]
    provider = ScriptedProviderClient([_result_for_case(case) for case in live_cases])
    service = ArkAIService(
        api_key=SecretStr("fake-secret-must-not-be-stored"),
        base_url="https://example.invalid/api/v3",
        model=MODEL,
        request_timeout_seconds=1,
        provider_client=provider,
    )

    artifact = run_suite(
        suite=suite,
        suite_bytes=raw,
        service=service,
        model=MODEL,
        runs=1,
        max_provider_calls=20,
        reviewer=_passing_review,
        sensitive_values=("fake-secret-must-not-be-stored",),
    )
    output = tmp_path / "goal-08-test.json"
    write_artifact(output, artifact)
    serialized = output.read_text(encoding="utf-8")
    payload = json.loads(serialized)

    assert artifact.provider_calls_used == len(live_cases)
    assert len(provider.requests) == len(live_cases)
    assert artifact.hard_guardrails_passed is True
    assert artifact.metrics.matching_status_accuracy == 1.0
    assert artifact.metrics.importance_accuracy == 1.0
    assert artifact.metrics.follow_up_answerability_accuracy == 1.0
    assert artifact.metrics.evidence_anchor_correctness == 1.0
    assert artifact.metrics.explanation_usefulness_mean == 3.0
    team_size_run = next(
        case_run
        for case_run in artifact.case_runs
        if case_run.case_id == "follow_up_insufficient_team_size"
    )
    assert team_size_run.failure_categories == ["forbidden_claim_marker_detected"]
    assert next(
        rule
        for rule in team_size_run.rule_results
        if rule.rule_id == "no_prohibited_behavior"
    ).passed is True
    reliability_runs = [
        case_run
        for case_run in artifact.case_runs
        if case_run.execution_mode == "network_free"
    ]
    assert len(reliability_runs) == 5
    assert all(case_run.rule_results[0].passed for case_run in reliability_runs)
    assert {
        (case_run.case_id, case_run.success, case_run.workflow_attempts)
        for case_run in reliability_runs
    } == {
        ("reliability_valid_first_response", True, 1),
        ("reliability_invalid_then_valid", True, 2),
        ("reliability_exhausted_invalid", False, 2),
        ("reliability_transient_then_valid", True, 2),
        ("reliability_permanent_failure", False, 1),
    }
    assert PRIVATE_OUTPUT_MARKER not in serialized
    assert "fake-secret-must-not-be-stored" not in serialized
    assert "jobDescription" not in serialized
    assert "priorMatchingAnalysis" not in serialized
    assert "generatedOutput" not in serialized
    assert payload["privacy"] == {
        "containsResume": False,
        "containsJobDescription": False,
        "containsQuestion": False,
        "containsPrompt": False,
        "containsProviderPayloadOrRawResponse": False,
        "containsGeneratedOutput": False,
    }


def test_runner_records_live_schema_exhaustion_without_raw_output() -> None:
    suite, raw = load_suite(CASES_PATH)
    live_cases = [case for case in suite.cases if case.workflow != "reliability"]
    responses: list[object] = [
        {"summary": PRIVATE_OUTPUT_MARKER},
        {"summary": PRIVATE_OUTPUT_MARKER},
    ]
    responses.extend(_result_for_case(case) for case in live_cases[1:])
    provider = ScriptedProviderClient(responses)
    service = ArkAIService(
        api_key=SecretStr("fake-secret"),
        base_url="https://example.invalid/api/v3",
        model=MODEL,
        request_timeout_seconds=1,
        provider_client=provider,
    )

    artifact = run_suite(
        suite=suite,
        suite_bytes=raw,
        service=service,
        model=MODEL,
        runs=1,
        max_provider_calls=20,
        reviewer=_passing_review,
    )

    first = artifact.case_runs[0]
    assert first.case_id == "matching_supported_required"
    assert first.success is False
    assert first.workflow_attempts == 2
    assert first.retry_reason == "invalid_structured_output"
    assert first.failure_categories == ["invalid_structured_output"]
    assert first.metrics.matching_status_correct is False
    assert first.metrics.importance_correct is False
    assert first.metrics.evidence_anchors_correct is False
    assert first.metrics.explanation_usefulness == 0
    assert artifact.hard_guardrails_passed is False
    assert PRIVATE_OUTPUT_MARKER not in artifact.model_dump_json(by_alias=True)


def test_cli_requires_explicit_live_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("RUN_LIVE_ARK_EVALS", raising=False)
    monkeypatch.setattr(
        "sys.argv",
        [
            "run_real_ai_evals",
            "--cases",
            str(CASES_PATH),
            "--runs",
            "1",
            "--max-provider-calls",
            "20",
            "--output",
            "unused.json",
        ],
    )

    with pytest.raises(SystemExit, match="RUN_LIVE_ARK_EVALS"):
        main()


def test_runner_rejects_unapproved_model_before_provider_access() -> None:
    suite, raw = load_suite(CASES_PATH)
    provider = ScriptedProviderClient([])
    service = ArkAIService(
        api_key=SecretStr("fake-secret"),
        base_url="https://example.invalid/api/v3",
        model="doubao-seed-2-0-mini-260428",
        request_timeout_seconds=1,
        provider_client=provider,
    )

    with pytest.raises(ValueError, match="approved model"):
        run_suite(
            suite=suite,
            suite_bytes=raw,
            service=service,
            model="doubao-seed-2-0-mini-260428",
            runs=1,
            max_provider_calls=20,
            reviewer=_passing_review,
        )

    assert provider.requests == []


def test_runner_can_select_focused_cases_and_rejects_unknown_ids() -> None:
    suite, raw = load_suite(CASES_PATH)
    selected = next(
        case
        for case in suite.cases
        if case.case_id == "follow_up_contextual_gap_reference"
    )
    provider = ScriptedProviderClient([_result_for_case(selected)])
    service = ArkAIService(
        api_key=SecretStr("fake-secret"),
        base_url="https://example.invalid/api/v3",
        model=MODEL,
        request_timeout_seconds=1,
        provider_client=provider,
    )

    artifact = run_suite(
        suite=suite,
        suite_bytes=raw,
        service=service,
        model=MODEL,
        runs=1,
        max_provider_calls=2,
        reviewer=_passing_review,
        case_ids=[selected.case_id],
    )

    assert [case_run.case_id for case_run in artifact.case_runs] == [selected.case_id]
    assert artifact.provider_calls_used == 1
    assert len(provider.requests) == 1

    with pytest.raises(ValueError, match="Unknown Goal 8 case IDs"):
        run_suite(
            suite=suite,
            suite_bytes=raw,
            service=service,
            model=MODEL,
            runs=1,
            max_provider_calls=2,
            reviewer=_passing_review,
            case_ids=["not-a-real-case"],
        )

    assert len(provider.requests) == 1


def test_runner_rejects_undersized_provider_budget_before_provider_access() -> None:
    suite, raw = load_suite(CASES_PATH)
    selected_case_id = "follow_up_contextual_gap_reference"
    provider = ScriptedProviderClient([])
    service = ArkAIService(
        api_key=SecretStr("fake-secret"),
        base_url="https://example.invalid/api/v3",
        model=MODEL,
        request_timeout_seconds=1,
        provider_client=provider,
    )

    with pytest.raises(ValueError, match=r"budget=1, required=2"):
        run_suite(
            suite=suite,
            suite_bytes=raw,
            service=service,
            model=MODEL,
            runs=1,
            max_provider_calls=1,
            reviewer=_passing_review,
            case_ids=[selected_case_id],
        )

    assert provider.requests == []


def _passing_review(case: RealAICase, _result: object) -> HumanReview:
    return HumanReview(
        invented_evidence_detected=False,
        prohibited_behavior_detected=False,
        gap_handled_safely=(
            True
            if "insufficient_evidence_gap_is_safe" in case.hard_guardrail_checks
            else None
        ),
        out_of_scope_handled_safely=(
            True
            if "out_of_scope_declines_without_speculation"
            in case.hard_guardrail_checks
            else None
        ),
        explanation_usefulness=3,
    )


def _result_for_case(case: RealAICase) -> dict[str, object]:
    if case.workflow == "matching":
        return {
            "summary": f"{PRIVATE_OUTPUT_MARKER}：匹配结果。",
            "requirements": [
                _matching_requirement_result(expected)
                for expected in case.expected.matching_requirements
            ],
        }

    answerability = case.expected.answerability
    assert answerability is not None
    evidence = []
    if answerability == "answerable":
        evidence = [
            {
                "evidenceText": f"{PRIVATE_OUTPUT_MARKER}：可核验项目事实",
                "sourceReference": case.required_evidence_anchors[0],
            }
        ]
    answer = f"{PRIVATE_OUTPUT_MARKER}：边界清楚的回答。"
    if case.case_id == "follow_up_insufficient_team_size":
        answer = (
            f"{PRIVATE_OUTPUT_MARKER}：简历第 2 页显示这一说法无法核验，"
            "固定简历未提供团队规模。"
        )
    return {
        "answerability": answerability,
        "answer": answer,
        "evidence": evidence,
        "missingInformation": (
            "简历未提供待核实信息。"
            if answerability == "insufficient_evidence"
            else None
        ),
    }


def _matching_requirement_result(
    expected: ExpectedMatchingRequirement,
) -> dict[str, object]:
    evidence = []
    if expected.status != "missing":
        anchor = (
            expected.required_evidence_anchors or expected.allowed_evidence_anchors
        )[0]
        evidence = [
            {
                "evidenceText": f"{PRIVATE_OUTPUT_MARKER}：可核验项目事实",
                "sourceReference": anchor,
            }
        ]
    return {
        "requirement": " / ".join(expected.requirement_contains),
        "importance": expected.importance,
        "status": expected.status,
        "evidence": evidence,
        "explanation": "证据与结论关系清楚。",
        "missingInformation": (
            None if expected.status == "supported" else "仍需核实未证明的部分。"
        ),
    }
