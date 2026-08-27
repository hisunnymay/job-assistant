from pathlib import Path

from app.ai.follow_up import FollowUpContextMessage
from app.ai.matching import AIServiceError

MOCK_MATCHING_ANALYSIS = """# 候选人与 AI 产品经理岗位的证据匹配报告

## 分析摘要

候选人的简历为 AI 产品设计、LLM 测试评估和复杂 B 端流程提供了明确证据；
技术协作能力有部分证据；量化业务结果仍缺少可核验信息。

## 职位要求与简历证据

### 1. AI 产品从需求分析到落地迭代

**证据状态：有明确证据**

**重要程度：核心要求**

简历提供了多段 AI 产品方案设计、验证与上线迭代经历。

**简历证据**

- 在 Lucy 大模型测试与评估平台中负责需求收集、可行性分析、PRD 编写及研发落地。
- 在国际化合同系统中完成 POA 授权管理流程设计、原型验证、PRD 与上线迭代。

### 2. LLM 应用、测试与评测反馈能力

**证据状态：有明确证据**

**重要程度：核心要求**

简历记录了模型接入、评测规则、测试数据和反馈迭代相关实践。

**简历证据**

- 设计模型测试数据提交、参数配置、批量调用和结果展示能力。
- 针对内容审核场景设计 Prompt 评测规则，并结合业务反馈持续调整评测逻辑。

### 3. 复杂 B 端业务流程与权限设计

**证据状态：有明确证据**

**重要程度：重要要求**

合同与授权系统经历能够支持复杂流程、权限边界和异常场景设计。

**简历证据**

- 梳理法务审核、代理签字人启停、POA 申请、审批、使用及管理流程。
- 推动国际化电子签署流程与内部合同系统整合。

### 4. 技术理解与开发协作能力

**证据状态：部分信息**

**重要程度：重要要求**

已有 API 调试、Python、TypeScript 与原型开发证据，但研发职责边界仍需确认。

**简历证据**

- 简历记录了使用 Python 处理数据、使用 TypeScript 开发模型功能页面及 API 调试。
- 使用 Cursor 构建交互原型并协同研发验证方案。

**仍需确认**

简历没有说明独立负责生产级软件工程交付的范围，不应据此推断为研发岗位经验。

### 5. 可量化的业务结果与商业影响

**证据状态：信息缺失**

**重要程度：补充要求**

现有简历描述了产品行为和交付结果，但缺少可核验的量化业务指标。

**仍需确认**

可进一步确认上线后的使用率、效率提升、成本变化或业务转化数据。

## 报告边界

- 此报告只使用静态简历中明确记录的信息，不补充未提供的经历。
- 报告用于帮助招聘者定位证据与信息缺口，不提供录用建议或候选人评分。
"""

MOCK_AGENT_EXPERIENCE_ANSWER = """## AI Agent 相关经验

当前可用候选人信息能够确认梅唱有 **AI 产品设计和 LLM 测试评估经验**：

- 在 Lucy 大模型测试与评估平台中负责需求收集、可行性分析、PRD 编写及研发落地；
- 设计过模型测试数据提交、参数配置、批量调用和结果展示能力；
- 针对内容审核场景设计 Prompt 评测规则，并根据业务反馈调整评测逻辑。

不过，现有信息没有明确写出她独立负责过以“AI Agent”为产品形态的上线项目。
因此可以确认相邻的 AI/LLM 产品经验，但具体 Agent 项目深度仍需向候选人核实。
"""

MOCK_TECHNICAL_COLLABORATION_ANSWER = """## 技术理解与研发协作

当前可用候选人信息记录了 API 调试、Python 数据处理、TypeScript 功能页面开发，
以及使用 Cursor 构建交互原型并协同研发验证方案的经历。

这些内容可以支持“具备技术理解和研发协作基础”的判断，但没有说明她独立承担生产级软件工程交付的范围，因此不应扩展为研发岗位经验。
"""

MOCK_PRODUCT_EXPERIENCE_ANSWER = """## 候选人相关经验

当前可用候选人信息显示，梅唱参与过 AI 产品方案设计、LLM 测试评估，
以及复杂 B 端合同和授权流程设计。相关工作包括需求收集、可行性分析、
PRD 编写、原型验证、研发协作和上线迭代。

这些内容可用于解释当前匹配报告中的产品与协作证据；没有写明的职责范围或结果仍应标记为待确认。
"""

MOCK_UNAVAILABLE_ANSWER = """## 当前信息不足

当前可用候选人信息没有提供这项内容，不能据此补充或推断。建议在联系候选人时直接确认，并记录可核验的项目背景、职责范围和结果。
"""

MOCK_OUT_OF_SCOPE_ANSWER = """## 超出支持范围

这个问题需要招聘判断、候选人比较、未来表现预测、个人评价，或与当前候选人匹配分析无关的信息；本助手不提供这类结论。

你可以继续询问候选人的已有经历、匹配证据、信息缺口，或当前可用候选人信息中能够核验的背景。
"""

OUT_OF_SCOPE_TERMS = (
    "录用",
    "招聘建议",
    "是否推荐",
    "排名",
    "比较候选人",
    "另一个候选人",
    "未来表现",
    "性格",
    "人品",
    "评分",
    "打分",
    "天气",
    "hire",
    "recommend",
    "rank",
    "compare",
    "future performance",
    "personality",
    "score",
    "weather",
)
UNAVAILABLE_TERMS = (
    "团队规模",
    "下属人数",
    "薪资",
    "量化业务结果",
    "使用率",
    "效率提升",
    "成本变化",
    "转化率",
    "team size",
    "salary",
    "conversion rate",
    "quantified result",
)
AGENT_TERMS = ("agent", "智能体")
TECHNICAL_TERMS = ("api", "编程", "代码", "研发", "python", "typescript")
SUPPORTED_TERMS = (
    "候选人",
    "简历",
    "经验",
    "背景",
    "证据",
    "匹配",
    "信息缺口",
    "产品",
    "ai",
    "llm",
    "大模型",
    "prompt",
    "模型",
    "合同",
    "授权",
)
CONTEXT_REFERENCE_TERMS = (
    "这些",
    "那些",
    "这个",
    "那个",
    "上述",
    "前面",
    "刚才",
    "这方面",
    "它们",
    "those",
    "these",
    "that",
    "them",
    "previous",
    "above",
)


def _classify_follow_up(question: str) -> str | None:
    if any(term in question for term in OUT_OF_SCOPE_TERMS):
        return "out_of_scope"
    if any(term in question for term in UNAVAILABLE_TERMS):
        return "unavailable"
    if any(term in question for term in AGENT_TERMS):
        return "agent"
    if any(term in question for term in TECHNICAL_TERMS):
        return "technical"
    if any(term in question for term in SUPPORTED_TERMS):
        return "supported"
    return None


def _resolve_follow_up_category(
    question: str,
    conversation_history: tuple[FollowUpContextMessage, ...],
) -> str:
    category = _classify_follow_up(question)
    if category is not None:
        return category

    if any(term in question for term in CONTEXT_REFERENCE_TERMS):
        for message in reversed(conversation_history[:-1]):
            if message.message_type != "follow_up_question":
                continue
            category = _classify_follow_up(message.content.casefold())
            if category is not None:
                return category

    return "out_of_scope"


class MockAIService:
    def generate_matching_analysis(
        self,
        *,
        resume_context_path: Path,
        job_description: str,
    ) -> str:
        if (
            not resume_context_path.is_file()
            or resume_context_path.suffix.lower() != ".md"
        ):
            raise AIServiceError("The configured candidate resume is unavailable")
        if not job_description:
            raise AIServiceError("The job description is unavailable")

        return MOCK_MATCHING_ANALYSIS

    def answer_follow_up(
        self,
        *,
        resume_context_path: Path,
        conversation_history: tuple[FollowUpContextMessage, ...],
    ) -> str:
        if (
            not resume_context_path.is_file()
            or resume_context_path.suffix.lower() != ".md"
        ):
            raise AIServiceError("The configured candidate resume is unavailable")
        if not conversation_history:
            raise AIServiceError("The conversation history is unavailable")

        latest_message = conversation_history[-1]
        if latest_message.message_type != "follow_up_question" or not latest_message.content:
            raise AIServiceError("The follow-up question is unavailable")
        if not any(
            message.message_type == "job_description" for message in conversation_history
        ) or not any(
            message.message_type == "matching_analysis" for message in conversation_history
        ):
            raise AIServiceError("The matching context is incomplete")

        category = _resolve_follow_up_category(
            latest_message.content.casefold(),
            conversation_history,
        )
        if category == "out_of_scope":
            return MOCK_OUT_OF_SCOPE_ANSWER
        if category == "unavailable":
            return MOCK_UNAVAILABLE_ANSWER
        if category == "agent":
            return MOCK_AGENT_EXPERIENCE_ANSWER
        if category == "technical":
            return MOCK_TECHNICAL_COLLABORATION_ANSWER
        return MOCK_PRODUCT_EXPERIENCE_ANSWER
