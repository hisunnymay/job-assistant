import { appConfig } from '../config/env'
import type { FollowUpClient, FollowUpResponse } from '../types/followUp'

interface ErrorResponse {
  code: string
  message: string
}

interface FollowUpClientOptions {
  apiBaseUrl?: string
  fetchImplementation?: typeof fetch
}

export class FollowUpClientError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly status: number,
  ) {
    super(message)
    this.name = 'FollowUpClientError'
  }
}

function isFollowUpResponse(value: unknown): value is FollowUpResponse {
  if (!value || typeof value !== 'object') {
    return false
  }

  const response = value as Record<string, unknown>
  return (
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

export function createFollowUpClient(
  options: FollowUpClientOptions = {},
): FollowUpClient {
  const apiBaseUrl = (options.apiBaseUrl ?? appConfig.apiBaseUrl).replace(
    /\/$/,
    '',
  )
  const fetchImplementation = options.fetchImplementation ?? fetch

  return {
    async ask(conversationId: string, question: string) {
      const response = await fetchImplementation(
        `${apiBaseUrl}/api/conversations/${encodeURIComponent(conversationId)}/messages`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question }),
        },
      )
      const responseBody = await readJson(response)

      if (!response.ok) {
        if (isErrorResponse(responseBody)) {
          throw new FollowUpClientError(
            responseBody.code,
            responseBody.message,
            response.status,
          )
        }

        throw new FollowUpClientError(
          'BACKEND_REQUEST_FAILED',
          'The follow-up request failed',
          response.status,
        )
      }

      if (!isFollowUpResponse(responseBody)) {
        throw new FollowUpClientError(
          'INVALID_RESPONSE',
          'The follow-up response was invalid',
          response.status,
        )
      }

      return responseBody
    },
  }
}
