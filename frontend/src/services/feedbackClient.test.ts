import { describe, expect, it, vi } from 'vitest'
import { FeedbackClientError, createFeedbackClient } from './feedbackClient'

const submission = {
  conversationId: 'conversation_001',
  messageId: 'message_002',
  rating: 5,
  comment: '证据关系清楚。',
}

describe('feedback API client', () => {
  it('submits report-linked feedback using the agreed contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    const client = createFeedbackClient({
      apiBaseUrl: 'http://api.example.test/',
      fetchImplementation,
    })

    await expect(client.submit(submission)).resolves.toBeUndefined()
    expect(fetchImplementation).toHaveBeenCalledWith(
      'http://api.example.test/api/feedback',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submission),
      },
    )
  })

  it('preserves the safe backend error contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          code: 'REPORT_NOT_FOUND',
          message: '未找到对应的匹配报告。',
        }),
        { status: 404, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    const client = createFeedbackClient({ fetchImplementation })

    await expect(client.submit(submission)).rejects.toEqual(
      new FeedbackClientError(
        'REPORT_NOT_FOUND',
        '未找到对应的匹配报告。',
        404,
      ),
    )
  })

  it('rejects a successful response that violates the contract', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(JSON.stringify({ success: false }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    const client = createFeedbackClient({ fetchImplementation })

    await expect(client.submit(submission)).rejects.toMatchObject({
      code: 'INVALID_RESPONSE',
    })
  })
})
