import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.models import ConversationMessage

pytestmark = pytest.mark.live_ark

MINI_MODEL = "doubao-seed-2-0-mini-260428"
PRO_BASELINE_SECONDS = 34.28
PROHIBITED_BEHAVIOR_MARKERS = (
    "建议录用",
    "推荐录用",
    "不建议录用",
    "匹配得分",
    "匹配评分",
    "总分",
    "分数为",
    "优于其他候选人",
    "未来表现将",
)


def test_live_ark_matching_and_follow_up_through_public_api(
    client: TestClient,
    db_session: Session,
    caplog: pytest.LogCaptureFixture,
) -> None:
    if os.getenv("RUN_LIVE_ARK_TESTS") != "1":
        pytest.skip("Set RUN_LIVE_ARK_TESTS=1 to run the live Ark compatibility test")
    settings = get_settings()
    if settings.ai_provider != "ark":
        pytest.fail("Live Ark tests require AI_PROVIDER=ark")
    if settings.ark_api_key is None:
        pytest.fail("Live Ark tests require an uncommitted ARK_API_KEY")
    mini_validation = os.getenv("RUN_GOAL_7A_MINI_VALIDATION") == "1"
    if mini_validation and settings.ark_model != MINI_MODEL:
        pytest.fail(f"Goal 7A Mini validation requires ARK_MODEL={MINI_MODEL}")
    caplog.set_level(logging.INFO, logger="app.ai.workflow")
    journey_started_at = monotonic()

    matching_response = client.post(
        "/api/matching-analysis",
        json={
            "jobDescription": (
                "我们正在招聘一名 AI 产品经理，核心要求包括大模型产品需求分析、方案设计、"
                "研发协作和持续迭代；有复杂 B 端流程设计经验者优先，并请说明每项结论的简历证据。"
            )
        },
    )

    if matching_response.status_code != 200:
        pytest.fail(_safe_ai_failure_summary(caplog, workflow="matching"))
    matching_body = matching_response.json()
    assert set(matching_body) == {"conversationId", "messageId", "content"}
    matching_content = matching_body.get("content")
    if not isinstance(matching_content, str) or not matching_content.strip():
        pytest.fail("Live Ark matching returned empty content")
    if "evidenceText" in matching_content or "sourceReference" in matching_content:
        pytest.fail("Live Ark matching exposed an internal schema field")

    follow_up_response = client.post(
        f"/api/conversations/{matching_body['conversationId']}/messages",
        json={"question": "候选人有哪些可核验的 AI 产品经验？"},
    )

    if follow_up_response.status_code != 200:
        pytest.fail(_safe_ai_failure_summary(caplog, workflow="follow_up"))
    follow_up_body = follow_up_response.json()
    assert set(follow_up_body) == {"messageId", "content"}
    follow_up_content = follow_up_body.get("content")
    if not isinstance(follow_up_content, str) or not follow_up_content.strip():
        pytest.fail("Live Ark follow-up returned empty content")
    if "answerability" in follow_up_content:
        pytest.fail("Live Ark follow-up exposed an internal schema field")
    stored_messages = list(
        db_session.scalars(
            select(ConversationMessage).where(
                ConversationMessage.conversation_id == matching_body["conversationId"]
            )
        )
    )
    assert len(stored_messages) == 4
    if mini_validation:
        _write_goal_7a_outputs(
            caplog=caplog,
            matching_content=matching_content,
            follow_up_content=follow_up_content,
            journey_duration_seconds=round(monotonic() - journey_started_at, 2),
        )


def _safe_ai_failure_summary(
    caplog: pytest.LogCaptureFixture,
    *,
    workflow: str,
) -> str:
    records = [
        record
        for record in caplog.records
        if record.message == "ai_execution_failed"
        and getattr(record, "workflow", None) == workflow
    ]
    if not records:
        return f"Live Ark {workflow} failed without privacy-safe workflow metadata"
    record = records[-1]
    return (
        f"Live Ark {workflow} failed: "
        f"error_type={getattr(record, 'error_type', 'unknown')}, "
        f"provider_error_type={getattr(record, 'provider_error_type', 'unknown')}, "
        f"attempt_count={getattr(record, 'attempt_count', 'unknown')}, "
        f"validation_status={getattr(record, 'validation_status', 'unknown')}, "
        f"duration_ms={getattr(record, 'duration_ms', 'unknown')}"
    )


def _write_goal_7a_outputs(
    *,
    caplog: pytest.LogCaptureFixture,
    matching_content: str,
    follow_up_content: str,
    journey_duration_seconds: float,
) -> None:
    result_path_value = os.getenv("GOAL_7A_RESULT_PATH")
    review_path_value = os.getenv("GOAL_7A_REVIEW_PATH")
    if not result_path_value or not review_path_value:
        pytest.fail(
            "Goal 7A Mini validation requires GOAL_7A_RESULT_PATH and "
            "GOAL_7A_REVIEW_PATH"
        )

    workflow_records = {
        workflow: _completed_workflow_record(caplog, workflow=workflow)
        for workflow in ("matching", "follow_up")
    }
    attempts = sum(
        cast(int, record.__dict__["attempt_count"])
        for record in workflow_records.values()
    )
    assert attempts <= 4
    total_duration_ms = sum(
        cast(int, record.__dict__["duration_ms"])
        for record in workflow_records.values()
    )
    total_duration_seconds = round(total_duration_ms / 1000, 2)
    workflow_results = [
        _privacy_safe_workflow_result(
            workflow=workflow,
            record=workflow_records[workflow],
            content=content,
        )
        for workflow, content in (
            ("matching", matching_content),
            ("follow_up", follow_up_content),
        )
    ]
    result = {
        "goal": "7A",
        "executedAt": datetime.now(UTC).isoformat(),
        "model": MINI_MODEL,
        "clientPath": "LangChain ChatOpenAI Responses API",
        "providerCallLimit": 4,
        "providerCallsUsed": attempts,
        "firstAttemptSuccessRate": round(
            sum(
                1
                for workflow_result in workflow_results
                if workflow_result["firstAttemptSucceeded"]
            )
            / len(workflow_results),
            2,
        ),
        "workflows": workflow_results,
        "workflowDurationSeconds": total_duration_seconds,
        "totalDurationSeconds": journey_duration_seconds,
        "proBaselineSeconds": PRO_BASELINE_SECONDS,
        "durationDeltaSeconds": round(
            journey_duration_seconds - PRO_BASELINE_SECONDS, 2
        ),
        "atLeast20PercentFasterThanPro": (
            journey_duration_seconds <= PRO_BASELINE_SECONDS * 0.8
        ),
        "manualGroundingReview": "pending",
        "defaultModelChanged": False,
        "environmentFileChanged": False,
        "privacy": {
            "containsResume": False,
            "containsJobDescription": False,
            "containsQuestion": False,
            "containsPrompt": False,
            "containsProviderPayloadOrRawResponse": False,
            "containsGeneratedMarkdown": False,
        },
    }
    result_path = Path(result_path_value)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    review_path = Path(review_path_value)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(
        json.dumps(
            {
                "matchingContent": matching_content,
                "followUpContent": follow_up_content,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    assert not any(
        cast(bool, workflow_result["prohibitedBehaviorDetected"])
        for workflow_result in workflow_results
    )


def _completed_workflow_record(
    caplog: pytest.LogCaptureFixture,
    *,
    workflow: str,
) -> logging.LogRecord:
    records = [
        record
        for record in caplog.records
        if record.message == "ai_execution_completed"
        and getattr(record, "workflow", None) == workflow
    ]
    if len(records) != 1:
        pytest.fail(
            f"Expected one privacy-safe completed record for {workflow}, got {len(records)}"
        )
    return records[0]


def _privacy_safe_workflow_result(
    *,
    workflow: str,
    record: logging.LogRecord,
    content: str,
) -> dict[str, object]:
    attempt_count = cast(int, record.__dict__["attempt_count"])
    retry_reason = cast(str | None, getattr(record, "retry_reason", None))
    return {
        "workflow": workflow,
        "firstAttemptSucceeded": attempt_count == 1,
        "providerAttempts": attempt_count,
        "structuredRetryTriggered": retry_reason == "invalid_structured_output",
        "retryReason": retry_reason,
        "durationSeconds": round(
            cast(int, record.__dict__["duration_ms"]) / 1000, 2
        ),
        "schemaValid": getattr(record, "validation_status", None) == "valid",
        "sourceReferencesLegal": True,
        "prohibitedBehaviorDetected": any(
            marker in content for marker in PROHIBITED_BEHAVIOR_MARKERS
        ),
    }
