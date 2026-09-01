import { appConfig } from '../config/env'
import type {
  DashboardAggregate,
  DashboardClient,
  DashboardDateRange,
} from '../types/dashboard'

export class DashboardClientError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status: number,
  ) {
    super(message)
    this.name = 'DashboardClientError'
  }
}

function isNonNegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0
}

function parseAggregate(value: unknown): DashboardAggregate | undefined {
  if (!value || typeof value !== 'object') {
    return undefined
  }
  const aggregate = value as Record<string, unknown>
  const period = aggregate.reportingPeriod as Record<string, unknown> | undefined
  const conversion = aggregate.contactConversion as
    | Record<string, unknown>
    | undefined
  const totals = aggregate.eventTotals as Record<string, unknown> | undefined
  if (
    !period ||
    !conversion ||
    !totals ||
    !['all_retained', 'custom'].includes(String(period.mode)) ||
    period.timezone !== 'Asia/Shanghai' ||
    !isNonNegativeInteger(conversion.numerator) ||
    !isNonNegativeInteger(conversion.denominator) ||
    (conversion.rate !== null &&
      (typeof conversion.rate !== 'number' ||
        conversion.rate < 0 ||
        conversion.rate > 1)) ||
    !isNonNegativeInteger(totals.pageVisits) ||
    !isNonNegativeInteger(totals.jobDescriptionSubmissions) ||
    !isNonNegativeInteger(totals.matchingReportsGenerated) ||
    !isNonNegativeInteger(totals.resumePreviews) ||
    !isNonNegativeInteger(totals.contactCtaClicks) ||
    !isNonNegativeInteger(totals.feedbackSubmissions) ||
    (aggregate.updatedAt !== null &&
      (typeof aggregate.updatedAt !== 'string' ||
        Number.isNaN(Date.parse(aggregate.updatedAt))))
  ) {
    return undefined
  }
  const startDate = period.startDate
  const endDate = period.endDate
  if (
    (startDate !== null && typeof startDate !== 'string') ||
    (endDate !== null && typeof endDate !== 'string') ||
    (period.mode === 'custom' && (!startDate || !endDate)) ||
    (period.mode === 'all_retained' && (startDate !== null || endDate !== null))
  ) {
    return undefined
  }

  return value as DashboardAggregate
}

export function createDashboardClient(
  options: {
    apiBaseUrl?: string
    fetchImplementation?: typeof fetch
  } = {},
): DashboardClient {
  const apiBaseUrl = (options.apiBaseUrl ?? appConfig.apiBaseUrl).replace(
    /\/$/,
    '',
  )
  const fetchImplementation = options.fetchImplementation ?? fetch

  return {
    async getAggregate(dateRange?: DashboardDateRange) {
      const query = dateRange
        ? `?${new URLSearchParams({
            startDate: dateRange.startDate,
            endDate: dateRange.endDate,
          }).toString()}`
        : ''
      const response = await fetchImplementation(
        `${apiBaseUrl}/api/dashboard${query}`,
      )
      let responseBody: unknown
      try {
        responseBody = await response.json()
      } catch {
        throw new DashboardClientError(
          'INVALID_RESPONSE',
          'Dashboard response was not valid JSON.',
          response.status,
        )
      }
      if (!response.ok) {
        const error = responseBody as Record<string, unknown>
        throw new DashboardClientError(
          typeof error.code === 'string' ? error.code : 'REQUEST_FAILED',
          typeof error.message === 'string'
            ? error.message
            : 'Dashboard request failed.',
          response.status,
        )
      }
      const aggregate = parseAggregate(responseBody)
      if (!aggregate) {
        throw new DashboardClientError(
          'INVALID_RESPONSE',
          'Dashboard response did not match the approved contract.',
          response.status,
        )
      }
      return aggregate
    },
  }
}
