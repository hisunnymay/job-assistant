import { describe, expect, it } from 'vitest'
import { createMockAnalysisClient } from './mockAnalysisClient'

describe('mock analysis contract fixture', () => {
  it('matches the authoritative matching-analysis response shape', async () => {
    const client = createMockAnalysisClient({ delayMs: 0 })

    const response = await client.analyze(
      '一份足够长的职位描述，用于验证前端与后端约定的响应字段。',
    )

    expect(response).toEqual({
      conversationId: expect.any(String),
      messageId: expect.any(String),
      content: expect.any(String),
    })
    expect(response.content).toContain(
      '# 候选人与 AI 产品经理岗位的证据匹配报告',
    )
    expect(response).not.toHaveProperty('requirements')
    expect(response).not.toHaveProperty('limitations')
  })
})
