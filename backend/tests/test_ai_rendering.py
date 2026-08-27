import pytest

from app.ai.rendering import render_follow_up, render_matching_analysis
from app.ai.schemas import FollowUpResult, MatchingAnalysisResult


def test_matching_renderer_golden_output_covers_all_statuses() -> None:
    result = MatchingAnalysisResult.model_validate(
        {
            "summary": "一项明确支持，一项部分支持，一项缺少信息。",
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
                    "explanation": "简历直接记录了相关经历。",
                    "missingInformation": None,
                },
                {
                    "requirement": "生产级开发",
                    "importance": "preferred",
                    "status": "partial",
                    "evidence": [
                        {
                            "evidenceText": "使用 TypeScript 开发功能页面",
                            "sourceReference": "OpenCUI 智能对话机器人搭建平台",
                        }
                    ],
                    "explanation": "有相邻技术实践，但交付范围不明确。",
                    "missingInformation": "独立承担生产交付的范围仍需确认。",
                },
                {
                    "requirement": "量化业务结果",
                    "importance": "unspecified",
                    "status": "missing",
                    "evidence": [],
                    "explanation": "简历没有给出可核验指标。",
                    "missingInformation": "使用率、效率或转化结果仍需确认。",
                },
            ],
        }
    )

    rendered = render_matching_analysis(result)

    assert rendered == """# 候选人与岗位要求的证据匹配报告

## 分析摘要

一项明确支持，一项部分支持，一项缺少信息。

## 职位要求与简历证据

### 1. AI 产品经验

**证据状态：有明确证据**

**重要程度：核心要求**

简历直接记录了相关经历。

**简历证据**

- 负责大模型测试与评估平台（工作经历）

### 2. 生产级开发

**证据状态：部分信息**

**重要程度：优先条件**

有相邻技术实践，但交付范围不明确。

**简历证据**

- 使用 TypeScript 开发功能页面（OpenCUI 智能对话机器人搭建平台）

**仍需确认**

独立承担生产交付的范围仍需确认。

### 3. 量化业务结果

**证据状态：信息缺失**

**重要程度：未注明**

简历没有给出可核验指标。

**仍需确认**

使用率、效率或转化结果仍需确认。

## 报告边界

- 此报告只使用固定候选人简历中可核验的信息，不补充未提供的经历。

- 信息缺失表示现有材料无法证明，不代表候选人不具备相关能力。

- 报告用于帮助招聘者定位证据与信息缺口，不提供录用建议或候选人评分。"""
    for internal_name in (
        "evidenceText",
        "sourceReference",
        "missingInformation",
        "provider",
        "request_id",
    ):
        assert internal_name not in rendered


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        (
            {
                "answerability": "answerable",
                "answer": "简历记录了 AI 产品经验。",
                "evidence": [
                    {
                        "evidenceText": "负责大模型测试与评估平台",
                        "sourceReference": "工作经历",
                    }
                ],
                "missingInformation": None,
            },
            """## 候选人信息回答

简历记录了 AI 产品经验。

**简历证据**

- 负责大模型测试与评估平台（工作经历）

以上回答仅依据固定候选人简历和当前匹配对话，不补充未提供的候选人事实。""",
        ),
        (
            {
                "answerability": "insufficient_evidence",
                "answer": "现有信息不能确认团队规模。",
                "evidence": [],
                "missingInformation": "简历未提供团队规模。",
            },
            """## 当前信息不足

现有信息不能确认团队规模。

**仍需确认**

简历未提供团队规模。

以上回答仅依据固定候选人简历和当前匹配对话，不补充未提供的候选人事实。""",
        ),
        (
            {
                "answerability": "out_of_scope",
                "answer": "本助手不提供录用建议，请询问候选人背景或证据缺口。",
                "evidence": [],
                "missingInformation": None,
            },
            """## 超出支持范围

本助手不提供录用建议，请询问候选人背景或证据缺口。

以上回答仅依据固定候选人简历和当前匹配对话，不补充未提供的候选人事实。""",
        ),
    ],
)
def test_follow_up_renderer_golden_outputs(
    payload: dict[str, object],
    expected: str,
) -> None:
    rendered = render_follow_up(FollowUpResult.model_validate(payload))

    assert rendered == expected
    assert "answerability" not in rendered
    assert "missingInformation" not in rendered


def test_renderer_escapes_provider_controlled_markdown_and_external_images() -> None:
    malicious_text = "![外部图片](https://example.invalid/pixel)\n# 伪造标题"
    matching = MatchingAnalysisResult.model_validate(
        {
            "summary": malicious_text,
            "requirements": [
                {
                    "requirement": malicious_text,
                    "importance": "preferred",
                    "status": "partial",
                    "evidence": [
                        {
                            "evidenceText": malicious_text,
                            "sourceReference": "工作经历",
                        }
                    ],
                    "explanation": malicious_text,
                    "missingInformation": malicious_text,
                }
            ],
        }
    )
    follow_up = FollowUpResult.model_validate(
        {
            "answerability": "answerable",
            "answer": malicious_text,
            "evidence": [
                {
                    "evidenceText": malicious_text,
                    "sourceReference": "工作经历",
                }
            ],
            "missingInformation": None,
        }
    )

    for rendered in (
        render_matching_analysis(matching),
        render_follow_up(follow_up),
    ):
        assert "![外部图片](https://example.invalid/pixel)" not in rendered
        assert "\n# 伪造标题" not in rendered
        assert "\\!\\[外部图片\\]\\(https://example\\.invalid/pixel\\)" in rendered
