import { appConfig } from '../config/env'
import type {
  AnalysisClient,
  MatchingAnalysisResponse,
} from '../types/matching'

interface ErrorResponse {
  code: string
  message: string
}

interface AnalysisClientOptions {
  apiBaseUrl?: string
  fetchImplementation?: typeof fetch
}

export class AnalysisClientError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'AnalysisClientError'
  }
}

function isMatchingAnalysisResponse(
  value: unknown,
): value is MatchingAnalysisResponse {
  if (!value || typeof value !== 'object') {
    return false
  }

  const response = value as Record<string, unknown>
  return (
    typeof response.conversationId === 'string' &&
    typeof response.messageId === 'string' &&
    typeof response.content === 'string'
  )
}

function isErrorResponse(value: unknown): value is ErrorResponse {
  if (!value || typeof value !== 'object') {
    return false
  }

  const response = value as Record<string, unknown>
  return typeof response.code === 'string' && typeof response.message === 'string'
}

async function readJson(response: Response): Promise<unknown> {
  try {
    return await response.json()
  } catch {
    return undefined
  }
}

export function createAnalysisClient(
  options: AnalysisClientOptions = {},
): AnalysisClient {
  const apiBaseUrl = (options.apiBaseUrl ?? appConfig.apiBaseUrl).replace(
    /\/$/,
    '',
  )
  const fetchImplementation = options.fetchImplementation ?? fetch

  return {
    async analyze(jobDescription: string) {
      const response = await fetchImplementation(
        `${apiBaseUrl}/api/matching-analysis`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ jobDescription }),
        },
      )
      const responseBody = await readJson(response)

      if (!response.ok) {
        if (isErrorResponse(responseBody)) {
          throw new AnalysisClientError(
            responseBody.code,
            responseBody.message,
            response.status,
          )
        }

        throw new AnalysisClientError(
          'BACKEND_REQUEST_FAILED',
          'The matching-analysis request failed',
          response.status,
        )
      }

      if (!isMatchingAnalysisResponse(responseBody)) {
        throw new AnalysisClientError(
          'INVALID_RESPONSE',
          'The matching-analysis response was invalid',
          response.status,
        )
      }

      return responseBody
    },
  }
}
