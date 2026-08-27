from collections.abc import Mapping

import pytest
from pydantic import ValidationError

from app.ai.schemas import FollowUpResult, MatchingAnalysisResult


def matching_payload(
    *,
    status: str = "supported",
    evidence: list[dict[str, str]] | None = None,
    missing_information: str | None = None,
) -> dict[str, object]:
    if evidence is None:
        evidence = [
            {
                "evidenceText": "负责大模型产品需求分析与研发落地",
                "sourceReference": "工作经历",
            }
        ]
    return {
        "summary": "简历提供了相关产品经历证据。",
        "requirements": [
            {
                "requirement": "大模型产品经验",
                "importance": "required",
                "status": status,
                "evidence": evidence,
                "explanation": "现有经历能够支持该项判断。",
                "missingInformation": missing_information,
            }
        ],
    }


@pytest.mark.parametrize(
    "payload",
    [
        {**matching_payload(), "unexpected": "value"},
        {**matching_payload(), "summary": "   "},
        {**matching_payload(), "requirements": []},
        matching_payload(status="unknown"),
        {
            **matching_payload(),
            "requirements": [
                {
                    **matching_payload()["requirements"][0],  # type: ignore[index]
                    "importance": "critical",
                }
            ],
        },
        matching_payload(status="supported", evidence=[]),
        matching_payload(status="supported", missing_information="仍需确认"),
        matching_payload(status="partial", missing_information=None),
        matching_payload(status="missing", evidence=[]),
        matching_payload(status="missing", missing_information="   ", evidence=[]),
        {
            **matching_payload(),
            "requirements": [
                {
                    **matching_payload()["requirements"][0],  # type: ignore[index]
                    "evidence": [
                        {
                            "evidenceText": "",
                            "sourceReference": "工作经历",
                        }
                    ],
                }
            ],
        },
        {
            **matching_payload(),
            "requirements": [
                {
                    **matching_payload()["requirements"][0],  # type: ignore[index]
                    "evidence": [
                        {
                            "evidenceText": "负责大模型测试与评估平台",
                            "sourceReference": "第 1 页，工作经历",
                        }
                    ],
                }
            ],
        },
        {
            **matching_payload(),
            "requirements": [
                {
                    **matching_payload()["requirements"][0],  # type: ignore[index]
                    "evidence": [
                        {
                            "evidenceText": "负责大模型测试与评估平台",
                            "sourceReference": "项目经历",
                        }
                    ],
                }
            ],
        },
    ],
)
def test_matching_schema_rejects_invalid_structure_and_invariants(
    payload: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        MatchingAnalysisResult.model_validate(payload)


def test_matching_schema_accepts_all_approved_status_invariants() -> None:
    supported = MatchingAnalysisResult.model_validate(matching_payload())
    partial = MatchingAnalysisResult.model_validate(
        matching_payload(status="partial", missing_information="独立交付范围仍需确认")
    )
    missing = MatchingAnalysisResult.model_validate(
        matching_payload(
            status="missing",
            evidence=[],
            missing_information="简历未提供量化业务结果",
        )
    )

    assert [
        supported.requirements[0].status,
        partial.requirements[0].status,
        missing.requirements[0].status,
    ] == ["supported", "partial", "missing"]


def test_provider_output_rejects_snake_case_alias_bypass() -> None:
    payload = matching_payload()
    requirement = payload["requirements"]
    assert isinstance(requirement, list)
    requirement[0]["missing_information"] = requirement[0].pop("missingInformation")

    with pytest.raises(ValidationError):
        MatchingAnalysisResult.model_validate(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {
            "answerability": "unknown",
            "answer": "回答",
            "evidence": [],
            "missingInformation": None,
        },
        {
            "answerability": "answerable",
            "answer": " ",
            "evidence": [
                {
                    "evidenceText": "相关经历",
                    "sourceReference": "项目经历",
                }
            ],
            "missingInformation": None,
        },
        {
            "answerability": "answerable",
            "answer": "有相关经历",
            "evidence": [],
            "missingInformation": None,
        },
        {
            "answerability": "answerable",
            "answer": "有相关经历",
            "evidence": [
                {
                    "evidenceText": "相关经历",
                    "sourceReference": "项目经历",
                }
            ],
            "missingInformation": "仍需确认",
        },
        {
            "answerability": "insufficient_evidence",
            "answer": "当前信息不足",
            "evidence": [],
            "missingInformation": None,
        },
        {
            "answerability": "out_of_scope",
            "answer": "不提供录用建议",
            "evidence": [
                {
                    "evidenceText": "相关经历",
                    "sourceReference": "项目经历",
                }
            ],
            "missingInformation": None,
        },
        {
            "answerability": "out_of_scope",
            "answer": "不提供录用建议",
            "evidence": [],
            "missingInformation": "不适用",
        },
        {
            "answerability": "out_of_scope",
            "answer": "不提供录用建议",
            "evidence": [],
            "missingInformation": None,
            "unexpected": "value",
        },
    ],
)
def test_follow_up_schema_rejects_invalid_structure_and_invariants(
    payload: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        FollowUpResult.model_validate(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {
            "answerability": "answerable",
            "answer": "简历记录了相关经历。",
            "evidence": [
                {
                    "evidenceText": "负责大模型测试与评估平台",
                    "sourceReference": "工作经历",
                }
            ],
            "missingInformation": None,
        },
        {
            "answerability": "insufficient_evidence",
            "answer": "现有信息不能确认团队规模。",
            "evidence": [],
            "missingInformation": "简历未提供团队规模",
        },
        {
            "answerability": "out_of_scope",
            "answer": "本助手不提供录用建议。",
            "evidence": [],
            "missingInformation": None,
        },
    ],
)
def test_follow_up_schema_accepts_all_approved_answerability_states(
    payload: dict[str, object],
) -> None:
    assert FollowUpResult.model_validate(payload).answerability == payload["answerability"]


@pytest.mark.parametrize("model", [MatchingAnalysisResult, FollowUpResult])
def test_provider_json_schema_is_closed_and_requires_every_object_field(
    model: type[MatchingAnalysisResult] | type[FollowUpResult],
) -> None:
    schema = model.model_json_schema(by_alias=True, mode="validation")

    def assert_strict_objects(value: object) -> None:
        if isinstance(value, Mapping):
            if value.get("type") == "object":
                properties = value.get("properties")
                assert isinstance(properties, Mapping)
                assert value.get("additionalProperties") is False
                assert set(value.get("required", [])) == set(properties)
            for child in value.values():
                assert_strict_objects(child)
        elif isinstance(value, list):
            for child in value:
                assert_strict_objects(child)

    assert_strict_objects(schema)
