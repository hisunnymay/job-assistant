import { describe, expect, it, vi } from 'vitest'
import {
  createTrackingClient,
  readPendingTrackingEvents,
} from './trackingClient'

class MemoryStorage {
  private readonly values = new Map<string, string>()

  getItem(key: string) {
    return this.values.get(key) ?? null
  }

  setItem(key: string, value: string) {
    this.values.set(key, value)
  }
}

function acknowledgedResponse() {
  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  })
}

function requestBody(call: unknown[]) {
  const options = call[1] as RequestInit
  return JSON.parse(options.body as string) as Record<string, unknown>
}

describe('centralized tracking delivery client', () => {
  it('delivers privacy-safe events and removes them after acknowledgement', async () => {
    const pendingStorage = new MemoryStorage()
    const trackingSessionStorage = new MemoryStorage()
    const identifiers = ['event-one', 'session-fixed', 'event-two']
    const fetchImplementation = vi
      .fn<typeof fetch>()
      .mockImplementation(async () => acknowledgedResponse())
    const client = createTrackingClient({
      apiBaseUrl: 'http://api.example.test/',
      fetchImplementation,
      pendingStorage,
      sessionStorage: trackingSessionStorage,
      now: () => new Date('2026-08-27T01:02:03.000Z'),
      createId: () => identifiers.shift() ?? 'unexpected',
    })

    client.track('page_visit')
    client.track('matching_report_generated', {
      conversationId: 'conversation_001',
    })
    await client.flushPending()

    expect(fetchImplementation).toHaveBeenCalledTimes(2)
    expect(fetchImplementation.mock.calls[0][0]).toBe(
      'http://api.example.test/api/tracking-events',
    )
    expect(requestBody(fetchImplementation.mock.calls[0])).toEqual({
      eventId: 'event_event-one',
      eventName: 'page_visit',
      sessionId: 'session_session-fixed',
      occurredAt: '2026-08-27T01:02:03.000Z',
    })
    expect(requestBody(fetchImplementation.mock.calls[1])).toEqual({
      eventId: 'event_event-two',
      eventName: 'matching_report_generated',
      sessionId: 'session_session-fixed',
      occurredAt: '2026-08-27T01:02:03.000Z',
      conversationId: 'conversation_001',
    })
    expect(readPendingTrackingEvents(pendingStorage)).toEqual([])
  })

  it('reuses the tracking session across client instances', async () => {
    const pendingStorage = new MemoryStorage()
    const trackingSessionStorage = new MemoryStorage()
    const fetchImplementation = vi
      .fn<typeof fetch>()
      .mockImplementation(async () => acknowledgedResponse())
    const firstClient = createTrackingClient({
      fetchImplementation,
      pendingStorage,
      sessionStorage: trackingSessionStorage,
      createId: () => 'first',
    })
    firstClient.track('page_visit')
    await firstClient.flushPending()

    const secondClient = createTrackingClient({
      fetchImplementation,
      pendingStorage,
      sessionStorage: trackingSessionStorage,
      createId: () => 'second',
    })
    secondClient.track('resume_previewed')
    await secondClient.flushPending()

    const firstEvent = requestBody(fetchImplementation.mock.calls[0])
    const secondEvent = requestBody(fetchImplementation.mock.calls[1])
    expect(secondEvent.sessionId).toBe(firstEvent.sessionId)
    expect(secondEvent.eventId).toBe('event_second')
  })

  it('retains a failed event and retries the stable payload on startup', async () => {
    const pendingStorage = new MemoryStorage()
    const trackingSessionStorage = new MemoryStorage()
    const failingFetch = vi
      .fn<typeof fetch>()
      .mockRejectedValue(new Error('network unavailable'))
    const firstClient = createTrackingClient({
      fetchImplementation: failingFetch,
      pendingStorage,
      sessionStorage: trackingSessionStorage,
      createId: () => 'stable',
      now: () => new Date('2026-08-27T01:02:03.000Z'),
    })

    firstClient.track('contact_cta_clicked')
    await firstClient.flushPending()
    const pendingEvent = readPendingTrackingEvents(pendingStorage)[0]
    expect(pendingEvent.eventId).toBe('event_stable')

    const successfulFetch = vi
      .fn<typeof fetch>()
      .mockResolvedValue(acknowledgedResponse())
    const secondClient = createTrackingClient({
      fetchImplementation: successfulFetch,
      pendingStorage,
      sessionStorage: trackingSessionStorage,
      createId: () => 'new-id-must-not-replace-pending',
    })
    await secondClient.flushPending()

    expect(requestBody(successfulFetch.mock.calls[0])).toEqual(pendingEvent)
    expect(readPendingTrackingEvents(pendingStorage)).toEqual([])
  })

  it('keeps an event pending when the backend does not acknowledge it', async () => {
    const pendingStorage = new MemoryStorage()
    const fetchImplementation = vi
      .fn<typeof fetch>()
      .mockResolvedValue(
        new Response(JSON.stringify({ success: false }), { status: 200 }),
      )
    const client = createTrackingClient({
      fetchImplementation,
      pendingStorage,
      sessionStorage: new MemoryStorage(),
      createId: () => 'not-acknowledged',
    })

    client.track('feedback_submitted')
    await client.flushPending()

    expect(readPendingTrackingEvents(pendingStorage)).toHaveLength(1)
  })

  it.each([400, 404, 409])(
    'discards permanent HTTP status %s and continues with later events',
    async (status) => {
      const pendingStorage = new MemoryStorage()
      const fetchImplementation = vi
        .fn<typeof fetch>()
        .mockResolvedValueOnce(
          new Response(
            JSON.stringify({ code: 'PERMANENT_REJECTION', message: 'rejected' }),
            { status },
          ),
        )
        .mockResolvedValueOnce(acknowledgedResponse())
      const identifiers = ['rejected', 'session-fixed', 'accepted']
      const client = createTrackingClient({
        fetchImplementation,
        pendingStorage,
        sessionStorage: new MemoryStorage(),
        createId: () => identifiers.shift() ?? 'unexpected',
      })

      client.track('contact_cta_clicked', {
        conversationId: 'conversation_deleted',
      })
      client.track('page_visit')
      await client.flushPending()

      expect(fetchImplementation).toHaveBeenCalledTimes(2)
      expect(requestBody(fetchImplementation.mock.calls[0]).eventId).toBe(
        'event_rejected',
      )
      expect(requestBody(fetchImplementation.mock.calls[1]).eventId).toBe(
        'event_accepted',
      )
      expect(readPendingTrackingEvents(pendingStorage)).toEqual([])
    },
  )

  it.each([408, 425, 429, 500])(
    'retains an event after retryable HTTP status %s',
    async (status) => {
      const pendingStorage = new MemoryStorage()
      const client = createTrackingClient({
        fetchImplementation: vi
          .fn<typeof fetch>()
          .mockResolvedValue(new Response(null, { status })),
        pendingStorage,
        sessionStorage: new MemoryStorage(),
        createId: () => `retry-${status}`,
      })

      client.track('page_visit')
      await client.flushPending()

      expect(readPendingTrackingEvents(pendingStorage)).toHaveLength(1)
    },
  )

  it('keeps only the newest 100 pending events', async () => {
    const pendingStorage = new MemoryStorage()
    let nextIdentifier = 0
    const fetchImplementation = vi
      .fn<typeof fetch>()
      .mockResolvedValue(new Response(null, { status: 503 }))
    const client = createTrackingClient({
      fetchImplementation,
      pendingStorage,
      sessionStorage: new MemoryStorage(),
      createId: () => String(++nextIdentifier),
    })

    for (let index = 0; index < 101; index += 1) {
      client.track('page_visit')
    }
    await client.flushPending()

    const pendingEvents = readPendingTrackingEvents(pendingStorage)
    expect(pendingEvents).toHaveLength(100)
    expect(pendingEvents[0].eventId).toBe('event_3')
    expect(pendingEvents[99].eventId).toBe('event_102')
  })

  it('normalizes a legacy browser log before startup delivery', async () => {
    const pendingStorage = new MemoryStorage()
    pendingStorage.setItem(
      'ai-job-fit-assistant.tracking-events.v1',
      JSON.stringify(
        Array.from({ length: 101 }, (_, index) => ({
          eventId: `legacy_${index}`,
          eventName: 'page_visit',
          sessionId: 'session_legacy',
          occurredAt: '2026-08-27T01:02:03.000Z',
          jobDescription: 'must be removed',
        })),
      ),
    )
    const client = createTrackingClient({
      fetchImplementation: vi
        .fn<typeof fetch>()
        .mockResolvedValue(new Response(null, { status: 503 })),
      pendingStorage,
      sessionStorage: new MemoryStorage(),
    })

    await client.flushPending()

    const storedValue = pendingStorage.getItem(
      'ai-job-fit-assistant.tracking-events.v1',
    )
    expect(storedValue).not.toContain('must be removed')
    const pendingEvents = readPendingTrackingEvents(pendingStorage)
    expect(pendingEvents).toHaveLength(100)
    expect(pendingEvents[0].eventId).toBe('legacy_1')
  })

  it('swallows unavailable storage without calling the backend', () => {
    const failingStorage = {
      getItem() {
        throw new Error('storage unavailable')
      },
      setItem() {
        throw new Error('storage unavailable')
      },
    }
    const fetchImplementation = vi.fn<typeof fetch>()
    const client = createTrackingClient({
      fetchImplementation,
      pendingStorage: failingStorage,
      sessionStorage: failingStorage,
      createId: () => 'fallback',
    })

    expect(() => client.track('contact_cta_clicked')).not.toThrow()
    expect(fetchImplementation).not.toHaveBeenCalled()
  })
})
