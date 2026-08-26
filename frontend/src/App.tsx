import { useState, type FormEvent } from 'react'
import { ContactPanel } from './components/ContactPanel'
import { ConversationMessage } from './components/ConversationMessage'
import { FeedbackPanel } from './components/FeedbackPanel'
import { Icon } from './components/Icon'
import { JobDescriptionForm } from './components/JobDescriptionForm'
import { ResumePanel } from './components/ResumePanel'
import { appConfig } from './config/env'
import { zhCN } from './content/zh-CN'
import {
  AnalysisClientError,
  createAnalysisClient,
} from './services/analysisClient'
import { createFeedbackClient } from './services/feedbackClient'
import type { FeedbackClient } from './types/feedback'
import type {
  AnalysisClient,
  ConversationMessage as ConversationMessageData,
} from './types/matching'
import './styles.css'

type JourneyState = 'ready' | 'loading' | 'success' | 'failure'
type WorkspaceView = 'home' | 'conversation' | 'resume' | 'contact'

const minimumJobDescriptionLength = 40
const defaultAnalysisClient = createAnalysisClient()
const defaultFeedbackClient = createFeedbackClient()
const resumeUrl = `${appConfig.apiBaseUrl.replace(/\/$/, '')}/api/resume`

interface AppProps {
  analysisClient?: AnalysisClient
  feedbackClient?: FeedbackClient
}

function getInitialView(): WorkspaceView {
  if (window.location.hash === '#resume') {
    return 'resume'
  }

  if (window.location.hash === '#contact') {
    return 'contact'
  }

  return 'home'
}

export function App({
  analysisClient = defaultAnalysisClient,
  feedbackClient = defaultFeedbackClient,
}: AppProps) {
  const [jobDescription, setJobDescription] = useState('')
  const [submittedJobDescription, setSubmittedJobDescription] = useState('')
  const [fieldError, setFieldError] = useState<string>()
  const [journeyState, setJourneyState] = useState<JourneyState>('ready')
  const [activeView, setActiveView] = useState<WorkspaceView>(getInitialView)
  const [failureDescription, setFailureDescription] = useState<string>(
    zhCN.failure.description,
  )
  const [canRetryFailure, setCanRetryFailure] = useState(true)
  const [messages, setMessages] = useState<ConversationMessageData[]>([])
  const [conversationId, setConversationId] = useState<string>()
  const [matchingMessageId, setMatchingMessageId] = useState<string>()
  const [submittedFeedbackRating, setSubmittedFeedbackRating] = useState<1 | 5>()

  const normalizedJobDescription = jobDescription.trim()
  const hasActiveConversation = Boolean(submittedJobDescription)
  const canSubmitJobDescription =
    normalizedJobDescription.length >= minimumJobDescriptionLength

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
    description: string,
    appendJobDescription: boolean,
  ) {
    if (appendJobDescription) {
      const jobDescriptionMessage: ConversationMessageData = {
        id: 'submitted-job-description',
        role: 'user',
        messageType: 'job_description',
        content: description,
      }

      setMessages([jobDescriptionMessage])
      setSubmittedJobDescription(description)
      setJobDescription('')
      setSubmittedFeedbackRating(undefined)
    }

    setJourneyState('loading')
    setFailureDescription(zhCN.failure.description)
    setCanRetryFailure(true)

    try {
      const response = await analysisClient.analyze(description)
      const analysisMessage: ConversationMessageData = {
        id: response.messageId,
        role: 'assistant',
        messageType: 'matching_analysis',
        content: response.content,
      }

      setConversationId(response.conversationId)
      setMatchingMessageId(response.messageId)
      setMessages((currentMessages) => [...currentMessages, analysisMessage])
      setJourneyState('success')
    } catch (error) {
      if (error instanceof AnalysisClientError) {
        if (error.code === 'INVALID_REQUEST') {
          setFailureDescription(zhCN.failure.invalidRequest)
          setJobDescription(description)
          setFieldError(zhCN.failure.invalidRequest)
          setCanRetryFailure(false)
          setSubmittedJobDescription('')
          setMessages([])
          setConversationId(undefined)
          setMatchingMessageId(undefined)
          setActiveView('home')
        } else if (error.code === 'AI_SERVICE_UNAVAILABLE') {
          setFailureDescription(zhCN.failure.aiUnavailable)
        }
      }
      setJourneyState('failure')
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const validationError = validateJobDescription(normalizedJobDescription)

    if (validationError) {
      setFieldError(validationError)
      return
    }

    setFieldError(undefined)
    setFailureDescription(zhCN.failure.description)
    setCanRetryFailure(true)
    setActiveView('conversation')
    void requestAnalysis(normalizedJobDescription, true)
  }

  function handleChange(value: string) {
    setJobDescription(value)
    const normalizedValue = value.trim()
    setFieldError(
      normalizedValue && normalizedValue.length < minimumJobDescriptionLength
        ? zhCN.jobDescription.shortError
        : undefined,
    )
  }

  function handleUseExample() {
    setJobDescription(zhCN.sampleJobDescription)
    setFieldError(undefined)
  }

  function handleRetry() {
    void requestAnalysis(submittedJobDescription, false)
  }

  function showJobMatching() {
    setActiveView(hasActiveConversation ? 'conversation' : 'home')
  }

  if (activeView === 'home') {
    return (
      <main className="entrance-page" id="main-content">
        <section className="entrance-view" aria-labelledby="entrance-title">
          <header className="entrance-intro">
            <h1 id="entrance-title">{zhCN.hero.title}</h1>
            <p>{zhCN.hero.introduction}</p>
          </header>

          {hasActiveConversation ? (
            <button
              className="return-conversation-button"
              type="button"
              onClick={() => setActiveView('conversation')}
            >
              {zhCN.navigation.returnToConversation}
            </button>
          ) : null}

          <JobDescriptionForm
            value={jobDescription}
            error={fieldError}
            isSubmitting={journeyState === 'loading'}
            canSubmit={canSubmitJobDescription}
            onChange={handleChange}
            onUseExample={handleUseExample}
            onSubmit={handleSubmit}
          />
        </section>
      </main>
    )
  }

  return (
    <div className="workspace-shell">
      <aside className="sidebar">
        <button
          className="brand"
          type="button"
          aria-label={zhCN.navigation.home}
          onClick={() => setActiveView('home')}
        >
          {zhCN.appName}
        </button>
        <nav className="sidebar-nav" aria-label={zhCN.navigation.ariaLabel}>
          <button
            type="button"
            aria-label={zhCN.navigation.assistant}
            aria-current={activeView === 'conversation' ? 'page' : undefined}
            onClick={showJobMatching}
          >
            <Icon name="briefcase" />
            <span>{zhCN.navigation.assistant}</span>
          </button>
          <button
            type="button"
            aria-label={zhCN.navigation.resume}
            aria-current={activeView === 'resume' ? 'page' : undefined}
            onClick={() => setActiveView('resume')}
          >
            <Icon name="file" />
            <span>{zhCN.navigation.resume}</span>
          </button>
          <button
            type="button"
            aria-label={zhCN.navigation.contact}
            aria-current={activeView === 'contact' ? 'page' : undefined}
            onClick={() => setActiveView('contact')}
          >
            <Icon name="user" />
            <span>{zhCN.navigation.contact}</span>
          </button>
        </nav>
      </aside>

      <main className="workspace-main" id="main-content">
        {activeView === 'conversation' ? (
          <section
            className="conversation-view"
            aria-label={zhCN.conversation.title}
            data-conversation-id={conversationId}
          >
            <div className="conversation-scroll">
              <ol className="message-list" aria-live="polite">
                {messages.map((message) => (
                  <ConversationMessage
                    key={message.id}
                    message={message}
                    actions={
                      message.messageType === 'matching_analysis' ? (
                        <div className="report-actions">
                          <button
                            className="icon-action"
                            type="button"
                            data-tooltip={zhCN.report.viewResume}
                            aria-label={zhCN.report.viewResume}
                            onClick={() => setActiveView('resume')}
                          >
                            <Icon name="file" />
                          </button>
                          <button
                            className="icon-action"
                            type="button"
                            data-tooltip={zhCN.report.contactCandidate}
                            aria-label={zhCN.report.contactCandidate}
                            onClick={() => setActiveView('contact')}
                          >
                            <Icon name="user" />
                          </button>
                          {conversationId && matchingMessageId ? (
                            <FeedbackPanel
                              conversationId={conversationId}
                              messageId={matchingMessageId}
                              feedbackClient={feedbackClient}
                              submittedRating={submittedFeedbackRating}
                              onSubmitted={setSubmittedFeedbackRating}
                            />
                          ) : null}
                        </div>
                      ) : undefined
                    }
                  />
                ))}

                {journeyState === 'loading' ? (
                  <li className="message-row message-row-assistant">
                    <article
                      className="status-message loading-message"
                      aria-label={`${zhCN.conversation.assistantName}：${zhCN.loading.title}`}
                      role="status"
                    >
                      <span className="typing-indicator" aria-hidden="true">
                        <i />
                        <i />
                        <i />
                      </span>
                      <div>
                        <h2>{zhCN.loading.title}</h2>
                        <p>{zhCN.loading.description}</p>
                      </div>
                    </article>
                  </li>
                ) : null}

                {journeyState === 'failure' ? (
                  <li className="message-row message-row-assistant">
                    <article
                      className="status-message failure-message"
                      aria-label={`${zhCN.conversation.assistantName}：${zhCN.failure.title}`}
                      role="alert"
                    >
                      <div>
                        <h2>{zhCN.failure.title}</h2>
                        <p>{failureDescription}</p>
                      </div>
                      {canRetryFailure ? (
                        <button
                          className="secondary-button"
                          type="button"
                          onClick={handleRetry}
                        >
                          {zhCN.failure.retry}
                        </button>
                      ) : null}
                    </article>
                  </li>
                ) : null}
              </ol>
            </div>

            <form
              className="follow-up-composer"
              aria-describedby="follow-up-unavailable"
              onSubmit={(event) => event.preventDefault()}
            >
              <label className="sr-only" htmlFor="follow-up-question">
                {zhCN.followUp.label}
              </label>
              <input
                id="follow-up-question"
                type="text"
                placeholder={zhCN.followUp.placeholder}
                disabled
              />
              <button type="submit" disabled>
                {zhCN.followUp.send}
              </button>
              <span className="sr-only" id="follow-up-unavailable">
                {zhCN.followUp.unavailable}
              </span>
            </form>
          </section>
        ) : null}

        {activeView === 'resume' ? (
          <section className="workspace-view resume-view" aria-label={zhCN.resume.title}>
            <ResumePanel resumeUrl={resumeUrl} />
          </section>
        ) : null}

        {activeView === 'contact' ? (
          <section className="workspace-view contact-view" aria-label={zhCN.contact.title}>
            <ContactPanel />
          </section>
        ) : null}
      </main>
    </div>
  )
}
