import { appConfig } from '../config/env'
import type { FeedbackClient, FeedbackSubmission } from '../types/feedback'

interface ErrorResponse {
  code: string
  message: string
}

interface FeedbackClientOptions {
  apiBaseUrl?: string
  fetchImplementation?: typeof fetch
}

export class FeedbackClientError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'FeedbackClientError'
  }
}

function isErrorResponse(value: unknown): value is ErrorResponse {
  if (!value || typeof value !== 'object') {
    return false
  }

  const response = value as Record<string, unknown>
  return typeof response.code === 'string' && typeof response.message === 'string'
}

export function createFeedbackClient(
  options: FeedbackClientOptions = {},
): FeedbackClient {
  const apiBaseUrl = (options.apiBaseUrl ?? appConfig.apiBaseUrl).replace(
    /\/$/,
    '',
  )
  const fetchImplementation = options.fetchImplementation ?? fetch

  return {
    async submit(feedback: FeedbackSubmission) {
      const response = await fetchImplementation(`${apiBaseUrl}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedback),
      })

      let responseBody: unknown
      try {
        responseBody = await response.json()
      } catch {
        responseBody = undefined
      }

      if (!response.ok) {
        if (isErrorResponse(responseBody)) {
          throw new FeedbackClientError(
            responseBody.code,
            responseBody.message,
            response.status,
          )
        }

        throw new FeedbackClientError(
          'FEEDBACK_REQUEST_FAILED',
          'The feedback request failed',
          response.status,
        )
      }

      if (
        !responseBody ||
        typeof responseBody !== 'object' ||
        (responseBody as Record<string, unknown>).success !== true
      ) {
        throw new FeedbackClientError(
          'INVALID_RESPONSE',
          'The feedback response was invalid',
          response.status,
        )
      }
    },
  }
}
