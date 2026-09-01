import { describe, expect, it, vi } from 'vitest'
import { createDashboardClient, DashboardClientError } from './dashboardClient'

const aggregate = {
  reportingPeriod: {
    mode: 'all_retained',
    startDate: null,
    endDate: null,
    timezone: 'Asia/Shanghai',
  },
  updatedAt: '2026-09-01T02:00:00.000Z',
  contactConversion: { rate: 0.5, numerator: 1, denominator: 2 },
  eventTotals: {
    pageVisits: 10,
    jobDescriptionSubmissions: 4,
    matchingReportsGenerated: 2,
    resumePreviews: 3,
    contactCtaClicks: 1,
    feedbackSubmissions: 1,
  },
}

describe('dashboard client', () => {
  it('requests all retained data and accepts the aggregate-only contract', async () => {
    const fetchImplementation = vi
      .fn<typeof fetch>()
      .mockResolvedValue(
        new Response(JSON.stringify(aggregate), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }),
      )
    const client = createDashboardClient({
      apiBaseUrl: 'http://api.example.test/',
      fetchImplementation,
    })

    await expect(client.getAggregate()).resolves.toEqual(aggregate)
    expect(fetchImplementation).toHaveBeenCalledWith(
      'http://api.example.test/api/dashboard',
    )
  })

  it('sends the approved date pair without adding browser-side aggregation', async () => {
    const fetchImplementation = vi
      .fn<typeof fetch>()
      .mockResolvedValue(new Response(JSON.stringify(aggregate), { status: 200 }))
    const client = createDashboardClient({ fetchImplementation })

    await client.getAggregate({
      startDate: '2026-08-01',
      endDate: '2026-09-01',
    })

    expect(String(fetchImplementation.mock.calls[0][0])).toContain(
      '/api/dashboard?startDate=2026-08-01&endDate=2026-09-01',
    )
  })

  it('rejects malformed success responses', async () => {
    const client = createDashboardClient({
      fetchImplementation: vi
        .fn<typeof fetch>()
        .mockResolvedValue(
          new Response(
            JSON.stringify({
              ...aggregate,
              eventTotals: { ...aggregate.eventTotals, pageVisits: '10' },
            }),
            { status: 200 },
          ),
        ),
    })

    await expect(client.getAggregate()).rejects.toMatchObject({
      code: 'INVALID_RESPONSE',
    })
  })

  it('surfaces safe backend errors without exposing them as aggregate data', async () => {
    const client = createDashboardClient({
      fetchImplementation: vi
        .fn<typeof fetch>()
        .mockResolvedValue(
          new Response(
            JSON.stringify({ code: 'PERSISTENCE_ERROR', message: 'safe message' }),
            { status: 500 },
          ),
        ),
    })

    await expect(client.getAggregate()).rejects.toEqual(
      expect.objectContaining<Partial<DashboardClientError>>({
        code: 'PERSISTENCE_ERROR',
        status: 500,
      }),
    )
  })
})
