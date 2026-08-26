export type ConversationRole = 'user' | 'assistant'

export type ConversationMessageType =
  | 'initial_guidance'
  | 'job_description'
  | 'matching_analysis'
  | 'follow_up_question'
  | 'follow_up_answer'

export interface ConversationMessage {
  id: string
  role: ConversationRole
  messageType: ConversationMessageType
  content: string
}

export interface MatchingAnalysisResponse {
  conversationId: string
  messageId: string
  content: string
}

export interface AnalysisClient {
  analyze(jobDescription: string): Promise<MatchingAnalysisResponse>
}
