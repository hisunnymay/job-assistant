export const zhCN = {
  appName: 'AI 职位匹配助手',
  navigationLabel: '招聘评估工作台',
  brandMark: '梅',
  demoChip: 'Mock MVP',
  hero: {
    eyebrow: '固定候选人 · 梅唱',
    title: '和 AI 助手一起核对职位匹配证据',
    introduction:
      '在同一段对话中提交职位描述、查看简历证据，并继续后续评估。',
  },
  conversation: {
    title: '职位匹配对话',
    description: '当前阶段使用确定性 Mock 响应验证完整交互。',
    ready: '助手已就绪',
    assistantName: 'AI 助手',
    userName: '招聘者',
    assistantAvatar: 'AI',
    userAvatar: '你',
    initialMessageLabel: '初始引导',
    jobDescriptionMessageLabel: '职位描述',
    matchingAnalysisMessageLabel: '匹配分析',
  },
  guidance: {
    title: '请提供完整的职位描述',
    content:
      '## 请提供完整的职位描述\n\n我会按职位要求整理候选人简历中的**明确证据**、**部分信息**和**缺失信息**。\n\n- 不生成候选人评分\n- 不作录用判断\n- 不补充简历中没有的信息',
  },
  jobDescription: {
    title: '向助手发送职位描述',
    description: '建议包含岗位职责、必要能力和加分项，以便后续真实分析覆盖关键要求。',
    label: '职位描述',
    placeholder: '请粘贴完整的职位描述，例如岗位职责、任职要求和优先条件……',
    useExample: '填入示例 JD',
    submit: '生成匹配报告',
    submitting: '正在整理证据…',
    characterCount: (count: number) => `${count} / 6000 字符`,
    emptyError: '请先输入职位描述。',
    shortError: '职位描述过短，请至少输入 40 个字符，以便识别有效的岗位要求。',
  },
  loading: {
    title: '正在生成匹配报告',
    description: '正在整理职位要求、候选人证据和需要进一步确认的信息。',
  },
  failure: {
    title: '暂时无法生成报告',
    description: '本次处理没有完成。你的职位描述仍然保留，可以重新尝试。',
    invalidRequest: '后端未接受这份职位描述。请检查内容后重新提交。',
    aiUnavailable: 'Mock AI 服务暂时不可用。你的职位描述仍然保留，可以重新尝试。',
    retry: '重新尝试',
  },
  report: {
    startOver: '分析新的职位',
    mockNoticeTitle: 'Mock AI 演示',
    mockNoticeBody: '此报告由后端确定性 Mock AI 服务生成，用于验证完整产品流程。',
  },
  sampleJobDescription:
    '我们正在招聘一名 AI 产品经理，负责大模型产品从需求分析、方案设计、PRD 到研发落地和持续迭代。候选人需要具备 LLM 应用、Prompt 与模型评测经验，能够设计复杂 B 端业务流程并与研发团队高效协作。具备数据分析能力、API 调试或基础编程经验者优先，同时希望候选人能够说明产品上线后的量化业务结果。',
} as const
