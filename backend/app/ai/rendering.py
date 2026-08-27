import re

from app.ai.schemas import FollowUpResult, MatchingAnalysisResult

MATCH_STATUS_LABELS = {
    "supported": "有明确证据",
    "partial": "部分信息",
    "missing": "信息缺失",
}
IMPORTANCE_LABELS = {
    "required": "核心要求",
    "preferred": "优先条件",
    "unspecified": "未注明",
}
FOLLOW_UP_TITLES = {
    "answerable": "候选人信息回答",
    "insufficient_evidence": "当前信息不足",
    "out_of_scope": "超出支持范围",
}
MARKDOWN_CONTROL_CHARACTERS = re.compile(r"([\\`*_[\]{}()#+\-.!|<>~>])")


def _escape_model_text(value: str) -> str:
    single_line_value = " ".join(value.replace("\r", " ").splitlines())
    return MARKDOWN_CONTROL_CHARACTERS.sub(r"\\\1", single_line_value)


def render_matching_analysis(result: MatchingAnalysisResult) -> str:
    sections = [
        "# 候选人与岗位要求的证据匹配报告",
        "## 分析摘要",
        _escape_model_text(result.summary),
        "## 职位要求与简历证据",
    ]

    for index, requirement in enumerate(result.requirements, start=1):
        sections.extend(
            [
                f"### {index}. {_escape_model_text(requirement.requirement)}",
                f"**证据状态：{MATCH_STATUS_LABELS[requirement.status]}**",
                f"**重要程度：{IMPORTANCE_LABELS[requirement.importance]}**",
                _escape_model_text(requirement.explanation),
            ]
        )
        if requirement.evidence:
            sections.append("**简历证据**")
            sections.extend(
                f"- {_escape_model_text(item.evidence_text)}"
                f"（{_escape_model_text(item.source_reference)}）"
                for item in requirement.evidence
            )
        if requirement.missing_information is not None:
            sections.extend(
                ["**仍需确认**", _escape_model_text(requirement.missing_information)]
            )

    sections.extend(
        [
            "## 报告边界",
            "- 此报告只使用固定候选人简历中可核验的信息，不补充未提供的经历。",
            "- 信息缺失表示现有材料无法证明，不代表候选人不具备相关能力。",
            "- 报告用于帮助招聘者定位证据与信息缺口，不提供录用建议或候选人评分。",
        ]
    )
    return "\n\n".join(sections).strip()


def render_follow_up(result: FollowUpResult) -> str:
    sections = [
        f"## {FOLLOW_UP_TITLES[result.answerability]}",
        _escape_model_text(result.answer),
    ]
    if result.evidence:
        sections.append("**简历证据**")
        sections.extend(
            f"- {_escape_model_text(item.evidence_text)}"
            f"（{_escape_model_text(item.source_reference)}）"
            for item in result.evidence
        )
    if result.missing_information is not None:
        sections.extend(["**仍需确认**", _escape_model_text(result.missing_information)])
    sections.append(
        "以上回答仅依据固定候选人简历和当前匹配对话，不补充未提供的候选人事实。"
    )
    return "\n\n".join(sections).strip()
