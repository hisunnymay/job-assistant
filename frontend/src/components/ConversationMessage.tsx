import Markdown from 'react-markdown'
import type { ReactNode } from 'react'
import { zhCN } from '../content/zh-CN'
import type { ConversationMessage as ConversationMessageData } from '../types/matching'

interface ConversationMessageProps {
  message: ConversationMessageData
  actions?: ReactNode
}

const messageLabels = {
  initial_guidance: zhCN.conversation.initialMessageLabel,
  job_description: zhCN.conversation.jobDescriptionMessageLabel,
  matching_analysis: zhCN.conversation.matchingAnalysisMessageLabel,
  follow_up_question: zhCN.conversation.followUpQuestionMessageLabel,
  follow_up_answer: zhCN.conversation.followUpAnswerMessageLabel,
} as const

export function ConversationMessage({
  message,
  actions,
}: ConversationMessageProps) {
  const isAssistant = message.role === 'assistant'
  const roleLabel = isAssistant
    ? zhCN.conversation.assistantName
    : zhCN.conversation.userName

  return (
    <li className={`message-row message-row-${message.role}`}>
      <article
        className={`message message-${message.role}`}
        aria-label={`${roleLabel}：${messageLabels[message.messageType]}`}
        data-message-type={message.messageType}
      >
        {isAssistant ? (
          <div className="assistant-message-content">
            <div className="markdown-content">
              <Markdown>{message.content}</Markdown>
            </div>
            {actions ? <div className="message-actions">{actions}</div> : null}
          </div>
        ) : (
          <p className="user-message-content">{message.content}</p>
        )}
      </article>
    </li>
  )
}
