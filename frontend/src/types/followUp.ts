export interface FollowUpResponse {
  messageId: string
  content: string
}

export interface FollowUpClient {
  ask(conversationId: string, question: string): Promise<FollowUpResponse>
}
