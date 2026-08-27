import { appConfig } from '../config/env'
import {
  trackingEventNames,
  type TrackingDeliveryClient,
  type TrackingEventPayload,
} from '../types/tracking'

const PENDING_EVENT_STORAGE_KEY = 'ai-job-fit-assistant.tracking-events.v1'
const SESSION_STORAGE_KEY = 'ai-job-fit-assistant.tracking-session.v1'
const MAX_PENDING_EVENTS = 100

interface StorageLike {
  getItem(key: string): string | null
  setItem(key: string, value: string): void
}

interface TrackingClientOptions {
  apiBaseUrl?: string
  fetchImplementation?: typeof fetch
  pendingStorage?: StorageLike
  sessionStorage?: StorageLike
  now?: () => Date
  createId?: () => string
}

function getBrowserStorage(kind: 'localStorage' | 'sessionStorage') {
  try {
    return window[kind]
  } catch {
    return undefined
  }
}

function createRandomId() {
  try {
    return crypto.randomUUID()
  } catch {
    return `${Date.now()}_${Math.random().toString(36).slice(2)}`
  }
}

function isBoundedIdentifier(value: unknown) {
  return typeof value === 'string' && value.length >= 1 && value.length <= 64
}

function parsePendingEvent(value: unknown): TrackingEventPayload | undefined {
  if (!value || typeof value !== 'object') {
    return undefined
  }

  const candidate = value as Record<string, unknown>
  if (
    !isBoundedIdentifier(candidate.eventId) ||
    typeof candidate.eventName !== 'string' ||
    !trackingEventNames.includes(
      candidate.eventName as (typeof trackingEventNames)[number],
    ) ||
    !isBoundedIdentifier(candidate.sessionId) ||
    typeof candidate.occurredAt !== 'string' ||
    Number.isNaN(Date.parse(candidate.occurredAt)) ||
    (candidate.conversationId !== undefined &&
      !isBoundedIdentifier(candidate.conversationId))
  ) {
    return undefined
  }

  return {
    eventId: candidate.eventId as string,
    eventName: candidate.eventName as (typeof trackingEventNames)[number],
    sessionId: candidate.sessionId as string,
    occurredAt: candidate.occurredAt,
    ...(candidate.conversationId
      ? { conversationId: candidate.conversationId as string }
      : {}),
  }
}

export function readPendingTrackingEvents(
  storage?: StorageLike,
): TrackingEventPayload[] {
  const pendingStorage = storage ?? getBrowserStorage('localStorage')
  if (!pendingStorage) {
    return []
  }

  try {
    const storedValue = pendingStorage.getItem(PENDING_EVENT_STORAGE_KEY)
    if (!storedValue) {
      return []
    }

    const parsedValue: unknown = JSON.parse(storedValue)
    if (!Array.isArray(parsedValue)) {
      return []
    }

    return parsedValue.flatMap((event) => {
      const safeEvent = parsePendingEvent(event)
      return safeEvent ? [safeEvent] : []
    })
  } catch {
    return []
  }
}

function writePendingTrackingEvents(
  storage: StorageLike | undefined,
  events: TrackingEventPayload[],
) {
  if (!storage) {
    return false
  }

  try {
    storage.setItem(
      PENDING_EVENT_STORAGE_KEY,
      JSON.stringify(events.slice(-MAX_PENDING_EVENTS)),
    )
    return true
  } catch {
    return false
  }
}

async function isAcknowledged(response: Response) {
  if (!response.ok) {
    return false
  }

  try {
    const responseBody: unknown = await response.json()
    return (
      Boolean(responseBody) &&
      typeof responseBody === 'object' &&
      (responseBody as Record<string, unknown>).success === true
    )
  } catch {
    return false
  }
}

function isNonRetryableClientError(response: Response) {
  return [400, 404, 409].includes(response.status)
}

export function createTrackingClient(
  options: TrackingClientOptions = {},
): TrackingDeliveryClient {
  const apiBaseUrl = (options.apiBaseUrl ?? appConfig.apiBaseUrl).replace(
    /\/$/,
    '',
  )
  const fetchImplementation = options.fetchImplementation ?? fetch
  const pendingStorage =
    options.pendingStorage ?? getBrowserStorage('localStorage')
  const trackingSessionStorage =
    options.sessionStorage ?? getBrowserStorage('sessionStorage')
  const now = options.now ?? (() => new Date())
  const createId = options.createId ?? createRandomId
  let sessionId: string | undefined
  let activeFlush: Promise<void> | undefined

  writePendingTrackingEvents(
    pendingStorage,
    readPendingTrackingEvents(pendingStorage),
  )

  function getSessionId() {
    if (sessionId) {
      return sessionId
    }

    try {
      const storedSessionId = trackingSessionStorage?.getItem(
        SESSION_STORAGE_KEY,
      )
      sessionId = isBoundedIdentifier(storedSessionId)
        ? (storedSessionId as string)
        : undefined
    } catch {
      sessionId = undefined
    }

    if (!sessionId) {
      sessionId = `session_${createId()}`.slice(0, 64)
      try {
        trackingSessionStorage?.setItem(SESSION_STORAGE_KEY, sessionId)
      } catch {
        // Tracking failure must not interrupt the recruiter journey.
      }
    }

    return sessionId
  }

  async function drainPendingEvents() {
    while (true) {
      const event = readPendingTrackingEvents(pendingStorage)[0]
      if (!event) {
        return true
      }

      let response: Response
      try {
        response = await fetchImplementation(
          `${apiBaseUrl}/api/tracking-events`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(event),
          },
        )
      } catch {
        return false
      }

      const acknowledged = await isAcknowledged(response)
      if (!acknowledged && !isNonRetryableClientError(response)) {
        return false
      }

      const remainingEvents = readPendingTrackingEvents(pendingStorage).filter(
        (pendingEvent) => pendingEvent.eventId !== event.eventId,
      )
      if (!writePendingTrackingEvents(pendingStorage, remainingEvents)) {
        return false
      }
    }
  }

  function flushPending() {
    if (activeFlush) {
      return activeFlush
    }

    if (readPendingTrackingEvents(pendingStorage).length === 0) {
      return Promise.resolve()
    }

    activeFlush = (async () => {
      let drained: boolean
      try {
        drained = await drainPendingEvents()
      } finally {
        activeFlush = undefined
      }

      if (drained && readPendingTrackingEvents(pendingStorage).length > 0) {
        await flushPending()
      }
    })()
    return activeFlush
  }

  const client: TrackingDeliveryClient = {
    track(eventName, context = {}) {
      try {
        const event: TrackingEventPayload = {
          eventId: `event_${createId()}`.slice(0, 64),
          eventName,
          sessionId: getSessionId(),
          occurredAt: now().toISOString(),
          ...(context.conversationId
            ? { conversationId: context.conversationId }
            : {}),
        }
        const queued = writePendingTrackingEvents(pendingStorage, [
          ...readPendingTrackingEvents(pendingStorage),
          event,
        ])
        if (queued) {
          void flushPending()
        }
      } catch {
        // Tracking failure must not interrupt the recruiter journey.
      }
    },
    flushPending,
  }

  void flushPending()
  return client
}
