from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
ResumeSourceReference = Literal[
    "个人优势",
    "工作经历",
    "滴滴出行科技有限公司",
    "国际化合同系统",
    "POA 授权管理线上化与 LLM 信息抽取",
    "国际化电子签署流程优化",
    "北京吉云互动科技有限公司（字节跳动全资子公司）",
    "Lucy 大模型测试与评估平台",
    "北京奇点机智科技有限公司",
    "OpenCUI 智能对话机器人搭建平台",
    "教育背景",
    "北京信息科技大学",
    "专业技能",
]


class StrictAIModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda field_name: "".join(
            [field_name.split("_")[0]]
            + [part.capitalize() for part in field_name.split("_")[1:]]
        ),
        extra="forbid",
    )


class EvidenceItem(StrictAIModel):
    evidence_text: NonEmptyString
    source_reference: ResumeSourceReference


class RequirementAnalysis(StrictAIModel):
    requirement: NonEmptyString
    importance: Literal["required", "preferred", "unspecified"]
    status: Literal["supported", "partial", "missing"]
    evidence: list[EvidenceItem]
    explanation: NonEmptyString
    missing_information: NonEmptyString | None

    @model_validator(mode="after")
    def enforce_status_invariants(self) -> Self:
        if self.status == "supported":
            if not self.evidence or self.missing_information is not None:
                raise ValueError(
                    "supported requirements need evidence and no missing information"
                )
        elif self.status == "partial":
            if not self.evidence or self.missing_information is None:
                raise ValueError(
                    "partial requirements need evidence and missing information"
                )
        elif self.evidence or self.missing_information is None:
            raise ValueError(
                "missing requirements need no evidence and explicit missing information"
            )
        return self


class MatchingAnalysisResult(StrictAIModel):
    summary: NonEmptyString
    requirements: list[RequirementAnalysis] = Field(min_length=1)


class FollowUpResult(StrictAIModel):
    answerability: Literal["answerable", "insufficient_evidence", "out_of_scope"]
    answer: NonEmptyString
    evidence: list[EvidenceItem]
    missing_information: NonEmptyString | None

    @model_validator(mode="after")
    def enforce_answerability_invariants(self) -> Self:
        if self.answerability == "answerable":
            if not self.evidence or self.missing_information is not None:
                raise ValueError(
                    "answerable follow-ups need evidence and no missing information"
                )
        elif self.answerability == "insufficient_evidence":
            if self.missing_information is None:
                raise ValueError(
                    "insufficient-evidence follow-ups need explicit missing information"
                )
        elif self.evidence or self.missing_information is not None:
            raise ValueError(
                "out-of-scope follow-ups need no evidence or missing information"
            )
        return self
