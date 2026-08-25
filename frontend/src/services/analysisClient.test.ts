import { describe, expect, it, vi } from 'vitest'
import { AnalysisClientError, createAnalysisClient } from './analysisClient'

describe('matching-analysis API client', () => {
  it('submits the API request and returns the agreed response contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          conversationId: 'conversation_001',
          messageId: 'message_002',
          content: '# 后端 Mock 匹配报告',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    const client = createAnalysisClient({
      apiBaseUrl: 'http://api.example.test/',
      fetchImplementation,
    })

    await expect(client.analyze('一份长度足够的职位描述')).resolves.toEqual({
      conversationId: 'conversation_001',
      messageId: 'message_002',
      content: '# 后端 Mock 匹配报告',
    })
    expect(fetchImplementation).toHaveBeenCalledWith(
      'http://api.example.test/api/matching-analysis',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jobDescription: '一份长度足够的职位描述' }),
      },
    )
  })

  it('preserves the safe backend error contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          code: 'AI_SERVICE_UNAVAILABLE',
          message: '匹配分析暂时不可用，请稍后重试。',
        }),
        { status: 503, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    const client = createAnalysisClient({ fetchImplementation })

    await expect(client.analyze('一份长度足够的职位描述')).rejects.toEqual(
      new AnalysisClientError(
        'AI_SERVICE_UNAVAILABLE',
        '匹配分析暂时不可用，请稍后重试。',
        503,
      ),
    )
  })

  it('rejects a successful response that violates the contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify({ content: '# 缺少标识符' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    const client = createAnalysisClient({ fetchImplementation })

    await expect(client.analyze('一份长度足够的职位描述')).rejects.toMatchObject({
      code: 'INVALID_RESPONSE',
    })
  })
})
