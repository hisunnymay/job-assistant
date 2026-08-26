export interface FeedbackSubmission {
  conversationId: string
  messageId: string
  rating: number
  comment?: string
}

export interface FeedbackClient {
  submit(feedback: FeedbackSubmission): Promise<void>
}
