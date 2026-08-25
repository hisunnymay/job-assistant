import type { AnalysisClient, MatchingReport } from '../types/matching'

const defaultDelayMs = 700

const mockReport: MatchingReport = {
  title: '候选人与 AI 产品经理岗位的证据匹配报告',
  requirements: [
    {
      id: 'ai-product-delivery',
      requirement: 'AI 产品从需求分析到落地迭代',
      importance: 'core',
      status: 'supported',
      finding: '简历提供了多段 AI 产品方案设计、验证与上线迭代经历。',
      evidence: [
        '在 Lucy 大模型测试与评估平台中负责需求收集、可行性分析、PRD 编写及研发落地。',
        '在国际化合同系统中完成 POA 授权管理流程设计、原型验证、PRD 与上线迭代。',
      ],
    },
    {
      id: 'llm-evaluation',
      requirement: 'LLM 应用、测试与评测反馈能力',
      importance: 'core',
      status: 'supported',
      finding: '简历记录了模型接入、评测规则、测试数据和反馈迭代相关实践。',
      evidence: [
        '设计模型测试数据提交、参数配置、批量调用和结果展示能力。',
        '针对内容审核场景设计 Prompt 评测规则，并结合业务反馈持续调整评测逻辑。',
      ],
    },
    {
      id: 'b2b-workflow',
      requirement: '复杂 B 端业务流程与权限设计',
      importance: 'important',
      status: 'supported',
      finding: '合同与授权系统经历能够支持复杂流程、权限边界和异常场景设计。',
      evidence: [
        '梳理法务审核、代理签字人启停、POA 申请、审批、使用及管理流程。',
        '推动国际化电子签署流程与内部合同系统整合。',
      ],
    },
    {
      id: 'technical-collaboration',
      requirement: '技术理解与开发协作能力',
      importance: 'important',
      status: 'partial',
      finding: '已有 API 调试、Python、TypeScript 与原型开发证据，但研发职责边界仍需确认。',
      evidence: [
        '简历记录了使用 Python 处理数据、使用 TypeScript 开发模型功能页面及 API 调试。',
        '使用 Cursor 构建交互原型并协同研发验证方案。',
      ],
      informationGap: '简历没有说明独立负责生产级软件工程交付的范围，不应据此推断为研发岗位经验。',
    },
    {
      id: 'measured-impact',
      requirement: '可量化的业务结果与商业影响',
      importance: 'additional',
      status: 'missing',
      finding: '现有简历描述了产品行为和交付结果，但缺少可核验的量化业务指标。',
      evidence: [],
      informationGap: '建议进一步确认上线后的使用率、效率提升、成本变化或业务转化数据。',
    },
  ],
  limitations: [
    '此报告只使用静态简历中明确记录的信息，不补充未提供的经历。',
    '报告用于帮助招聘者定位证据与信息缺口，不提供录用建议或候选人评分。',
  ],
}

export interface MockAnalysisOptions {
  delayMs?: number
  failFirstRequest?: boolean
}

function wait(delayMs: number): Promise<void> {
  return new Promise((resolve) => window.setTimeout(resolve, delayMs))
}

export function createMockAnalysisClient(
  options: MockAnalysisOptions = {},
): AnalysisClient {
  const delayMs = options.delayMs ?? defaultDelayMs
  let requestCount = 0

  return {
    async analyze() {
      requestCount += 1
      await wait(delayMs)

      if (options.failFirstRequest && requestCount === 1) {
        throw new Error('Simulated matching-analysis failure')
      }

      return structuredClone(mockReport)
    },
  }
}
