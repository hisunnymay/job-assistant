import Markdown from 'react-markdown'
import { zhCN } from '../content/zh-CN'
import type { ConversationMessage as ConversationMessageData } from '../types/matching'

interface ConversationMessageProps {
  message: ConversationMessageData
  isMockAnalysis?: boolean
  onStartOver?(): void
}

const messageLabels = {
  initial_guidance: zhCN.conversation.initialMessageLabel,
  job_description: zhCN.conversation.jobDescriptionMessageLabel,
  matching_analysis: zhCN.conversation.matchingAnalysisMessageLabel,
} as const

export function ConversationMessage({
  message,
  isMockAnalysis = false,
  onStartOver,
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
        <div className="message-avatar" aria-hidden="true">
          {isAssistant
            ? zhCN.conversation.assistantAvatar
            : zhCN.conversation.userAvatar}
        </div>

        <div className="message-column">
          <div className="message-meta">
            <strong>{roleLabel}</strong>
            <span>{messageLabels[message.messageType]}</span>
          </div>

          <div className="message-bubble">
            {isMockAnalysis ? (
              <div className="mock-notice" role="note">
                <strong>{zhCN.report.mockNoticeTitle}</strong>
                <span>{zhCN.report.mockNoticeBody}</span>
              </div>
            ) : null}

            {isAssistant ? (
              <div className="markdown-content">
                <Markdown>{message.content}</Markdown>
              </div>
            ) : (
              <p className="user-message-content">{message.content}</p>
            )}

            {onStartOver ? (
              <div className="message-actions">
                <button
                  className="secondary-button"
                  type="button"
                  onClick={onStartOver}
                >
                  {zhCN.report.startOver}
                </button>
              </div>
            ) : null}
          </div>
        </div>
      </article>
    </li>
  )
}
