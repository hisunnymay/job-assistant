export const zhCN = {
  appName: 'AI 职位匹配助手',
  navigationLabel: '招聘评估工作台',
  brandMark: '梅',
  demoChip: 'Mock MVP',
  hero: {
    eyebrow: '固定候选人 · 梅唱',
    title: '先看证据，再判断是否值得进一步沟通',
    introduction:
      '粘贴目标职位描述，快速查看职位要求与候选人简历证据之间的关系，以及仍需确认的信息。',
  },
  guidance: {
    label: '助手提示',
    title: '请提供完整的职位描述',
    body: '我会按职位要求整理已有证据、部分信息和缺失信息。当前阶段使用固定 mock 数据验证产品体验。',
    points: ['不生成候选人评分', '不作录用判断', '不补充简历中没有的信息'],
  },
  jobDescription: {
    kicker: '第一步',
    title: '输入职位描述',
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
    retry: '重新尝试',
  },
  report: {
    kicker: '匹配报告',
    startOver: '分析新的职位',
    mockNoticeTitle: '前端演示数据',
    mockNoticeBody: '此报告用于验证界面和交互，不代表针对当前输入职位的真实 AI 分析。',
    submittedJobDescription: '查看本次提交的职位描述',
    legendLabel: '证据状态说明',
    status: {
      supported: '有明确证据',
      partial: '部分信息',
      missing: '信息缺失',
    },
    importance: {
      core: '核心要求',
      important: '重要要求',
      additional: '补充要求',
    },
    evidenceTitle: '简历证据',
    gapTitle: '仍需确认',
    limitationsTitle: '报告边界',
  },
  sampleJobDescription:
    '我们正在招聘一名 AI 产品经理，负责大模型产品从需求分析、方案设计、PRD 到研发落地和持续迭代。候选人需要具备 LLM 应用、Prompt 与模型评测经验，能够设计复杂 B 端业务流程并与研发团队高效协作。具备数据分析能力、API 调试或基础编程经验者优先，同时希望候选人能够说明产品上线后的量化业务结果。',
} as const
