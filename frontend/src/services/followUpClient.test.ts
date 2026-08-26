import { describe, expect, it, vi } from 'vitest'
import {
  createFollowUpClient,
  FollowUpClientError,
} from './followUpClient'

describe('follow-up API client', () => {
  it('posts the exact request and accepts the exact response contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          messageId: 'message_follow_up_001',
          content: '# 后端追问回答',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    const client = createFollowUpClient({
      apiBaseUrl: 'http://localhost:8000/',
      fetchImplementation,
    })

    await expect(
      client.ask('conversation_001', '候选人有哪些 AI 产品经验？'),
    ).resolves.toEqual({
      messageId: 'message_follow_up_001',
      content: '# 后端追问回答',
    })
    expect(fetchImplementation).toHaveBeenCalledWith(
      'http://localhost:8000/api/conversations/conversation_001/messages',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: '候选人有哪些 AI 产品经验？' }),
      },
    )
  })

  it('preserves safe backend errors', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          code: 'AI_SERVICE_UNAVAILABLE',
          message: '追问暂时无法回答，请稍后重试。',
        }),
        { status: 503, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    const client = createFollowUpClient({ fetchImplementation })

    await expect(client.ask('conversation_001', '问题')).rejects.toEqual(
      new FollowUpClientError(
        'AI_SERVICE_UNAVAILABLE',
        '追问暂时无法回答，请稍后重试。',
        503,
      ),
    )
  })

  it('rejects a malformed successful response', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify({ content: '# 缺少消息 ID' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    const client = createFollowUpClient({ fetchImplementation })

    await expect(client.ask('conversation_001', '问题')).rejects.toMatchObject({
      code: 'INVALID_RESPONSE',
    })
  })
})
