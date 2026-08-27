export const trackingEventNames = [
  'page_visit',
  'job_description_submitted',
  'matching_report_generated',
  'resume_previewed',
  'contact_cta_clicked',
  'feedback_submitted',
] as const

export type TrackingEventName = (typeof trackingEventNames)[number]

export interface TrackingContext {
  conversationId?: string
}

export interface TrackingClient {
  track(eventName: TrackingEventName, context?: TrackingContext): void
}

export interface TrackingEventPayload {
  eventId: string
  eventName: TrackingEventName
  sessionId: string
  occurredAt: string
  conversationId?: string
}

export interface TrackingDeliveryClient extends TrackingClient {
  flushPending(): Promise<void>
}
