import { useState, type FormEvent } from 'react'
import { ConversationMessage } from './components/ConversationMessage'
import { JobDescriptionForm } from './components/JobDescriptionForm'
import { zhCN } from './content/zh-CN'
import { createMockAnalysisClient } from './services/mockAnalysisClient'
import type {
  AnalysisClient,
  ConversationMessage as ConversationMessageData,
} from './types/matching'
import './styles.css'

type JourneyState = 'ready' | 'loading' | 'success' | 'failure'

const minimumJobDescriptionLength = 40
const defaultAnalysisClient = createMockAnalysisClient()

const initialGuidanceMessage: ConversationMessageData = {
  id: 'initial-guidance',
  role: 'assistant',
  messageType: 'initial_guidance',
  content: zhCN.guidance.content,
}

interface AppProps {
  analysisClient?: AnalysisClient
}

export function App({ analysisClient = defaultAnalysisClient }: AppProps) {
  const [jobDescription, setJobDescription] = useState('')
  const [submittedJobDescription, setSubmittedJobDescription] = useState('')
  const [fieldError, setFieldError] = useState<string>()
  const [journeyState, setJourneyState] = useState<JourneyState>('ready')
  const [messages, setMessages] = useState<ConversationMessageData[]>([
    initialGuidanceMessage,
  ])
  const [conversationId, setConversationId] = useState<string>()

  function validateJobDescription(value: string): string | undefined {
    if (!value) {
      return zhCN.jobDescription.emptyError
    }

    if (value.length < minimumJobDescriptionLength) {
      return zhCN.jobDescription.shortError
    }

    return undefined
  }

  async function requestAnalysis(
    normalizedJobDescription: string,
    appendJobDescription: boolean,
  ) {
    if (appendJobDescription) {
      const jobDescriptionMessage: ConversationMessageData = {
        id: 'submitted-job-description',
        role: 'user',
        messageType: 'job_description',
        content: normalizedJobDescription,
      }

      setMessages((currentMessages) => [
        ...currentMessages,
        jobDescriptionMessage,
      ])
      setSubmittedJobDescription(normalizedJobDescription)
      setJobDescription('')
    }

    setJourneyState('loading')

    try {
      const response = await analysisClient.analyze(normalizedJobDescription)
      const analysisMessage: ConversationMessageData = {
        id: response.messageId,
        role: 'assistant',
        messageType: 'matching_analysis',
        content: response.content,
      }

      setConversationId(response.conversationId)
      setMessages((currentMessages) => [
        ...currentMessages,
        analysisMessage,
      ])
      setJourneyState('success')
    } catch {
      setJourneyState('failure')
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const normalizedJobDescription = jobDescription.trim()
    const validationError = validateJobDescription(normalizedJobDescription)

    if (validationError) {
      setFieldError(validationError)
      return
    }

    setFieldError(undefined)
    void requestAnalysis(normalizedJobDescription, true)
  }

  function handleChange(value: string) {
    setJobDescription(value)
    if (fieldError) {
      setFieldError(undefined)
    }
  }

  function handleUseExample() {
    setJobDescription(zhCN.sampleJobDescription)
    setFieldError(undefined)
  }

  function handleRetry() {
    void requestAnalysis(submittedJobDescription, false)
  }

  function handleStartOver() {
    setJobDescription('')
    setSubmittedJobDescription('')
    setFieldError(undefined)
    setJourneyState('ready')
    setMessages([initialGuidanceMessage])
    setConversationId(undefined)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#main-content" aria-label={zhCN.appName}>
          <span className="brand-mark" aria-hidden="true">
            {zhCN.brandMark}
          </span>
          <span>
            <strong>{zhCN.appName}</strong>
            <small>{zhCN.navigationLabel}</small>
          </span>
        </a>
        <span className="demo-chip">{zhCN.demoChip}</span>
      </header>

      <main id="main-content">
        <header className="workspace-intro">
          <p className="eyebrow">{zhCN.hero.eyebrow}</p>
          <h1>{zhCN.hero.title}</h1>
          <p>{zhCN.hero.introduction}</p>
        </header>

        <section
          className="conversation-shell"
          aria-labelledby="conversation-title"
          data-conversation-id={conversationId}
        >
          <header className="conversation-header">
            <div>
              <h2 id="conversation-title">{zhCN.conversation.title}</h2>
              <p>{zhCN.conversation.description}</p>
            </div>
            <span className="ready-status">
              <span aria-hidden="true" />
              {zhCN.conversation.ready}
            </span>
          </header>

          <ol className="message-list" aria-live="polite">
            {messages.map((message) => (
              <ConversationMessage
                key={message.id}
                message={message}
                isMockAnalysis={message.messageType === 'matching_analysis'}
                onStartOver={
                  message.messageType === 'matching_analysis'
                    ? handleStartOver
                    : undefined
                }
              />
            ))}

            {journeyState === 'loading' ? (
              <li className="message-row message-row-assistant">
                <article
                  className="message message-assistant status-message"
                  aria-label={`${zhCN.conversation.assistantName}：${zhCN.loading.title}`}
                  role="status"
                >
                  <div className="message-avatar" aria-hidden="true">
                    {zhCN.conversation.assistantAvatar}
                  </div>
                  <div className="message-column">
                    <div className="message-meta">
                      <strong>{zhCN.conversation.assistantName}</strong>
                    </div>
                    <div className="message-bubble loading-bubble">
                      <span className="typing-indicator" aria-hidden="true">
                        <i />
                        <i />
                        <i />
                      </span>
                      <div>
                        <h3>{zhCN.loading.title}</h3>
                        <p>{zhCN.loading.description}</p>
                      </div>
                    </div>
                  </div>
                </article>
              </li>
            ) : null}

            {journeyState === 'failure' ? (
              <li className="message-row message-row-assistant">
                <article
                  className="message message-assistant status-message"
                  aria-label={`${zhCN.conversation.assistantName}：${zhCN.failure.title}`}
                  role="alert"
                >
                  <div className="message-avatar" aria-hidden="true">
                    {zhCN.conversation.assistantAvatar}
                  </div>
                  <div className="message-column">
                    <div className="message-meta">
                      <strong>{zhCN.conversation.assistantName}</strong>
                    </div>
                    <div className="message-bubble failure-bubble">
                      <div>
                        <h3>{zhCN.failure.title}</h3>
                        <p>{zhCN.failure.description}</p>
                      </div>
                      <button
                        className="secondary-button"
                        type="button"
                        onClick={handleRetry}
                      >
                        {zhCN.failure.retry}
                      </button>
                    </div>
                  </div>
                </article>
              </li>
            ) : null}
          </ol>

          {journeyState === 'ready' ? (
            <JobDescriptionForm
              value={jobDescription}
              error={fieldError}
              isSubmitting={false}
              onChange={handleChange}
              onUseExample={handleUseExample}
              onSubmit={handleSubmit}
            />
          ) : null}
        </section>
      </main>
    </div>
  )
}
