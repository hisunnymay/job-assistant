import { useEffect, useRef, useState, type FormEvent } from 'react'
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
import {
  createFollowUpClient,
  FollowUpClientError,
} from './services/followUpClient'
import { createTrackingClient } from './services/trackingClient'
import type { FeedbackClient } from './types/feedback'
import type { FollowUpClient } from './types/followUp'
import type {
  AnalysisClient,
  ConversationMessage as ConversationMessageData,
} from './types/matching'
import type {
  TrackingClient,
  TrackingContext,
  TrackingEventName,
} from './types/tracking'
import './styles.css'

type JourneyState = 'ready' | 'loading' | 'success' | 'failure'
type FollowUpState = 'idle' | 'loading' | 'failure'
type WorkspaceView = 'home' | 'conversation' | 'resume' | 'contact'

interface FailedFollowUp {
  messageId: string
  question: string
}

const minimumJobDescriptionLength = 40
const maximumFollowUpLength = 1000
const defaultAnalysisClient = createAnalysisClient()
const defaultFeedbackClient = createFeedbackClient()
const defaultFollowUpClient = createFollowUpClient()
const defaultTrackingClient = createTrackingClient()
const resumeUrl = `${appConfig.apiBaseUrl.replace(/\/$/, '')}/api/resume`

interface AppProps {
  analysisClient?: AnalysisClient
  feedbackClient?: FeedbackClient
  followUpClient?: FollowUpClient
  trackingClient?: TrackingClient
}

function trackSafely(
  trackingClient: TrackingClient,
  eventName: TrackingEventName,
  context?: TrackingContext,
) {
  try {
    trackingClient.track(eventName, context)
  } catch {
    // Tracking must never interrupt the recruiter journey.
  }
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
  followUpClient = defaultFollowUpClient,
  trackingClient = defaultTrackingClient,
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
  const [followUpQuestion, setFollowUpQuestion] = useState('')
  const [followUpState, setFollowUpState] = useState<FollowUpState>('idle')
  const [followUpError, setFollowUpError] = useState<string>()
  const [failedFollowUp, setFailedFollowUp] = useState<FailedFollowUp>()
  const conversationScrollRef = useRef<HTMLDivElement>(null)
  const activeConversationIdRef = useRef<string | undefined>(undefined)
  const followUpInFlightRef = useRef(false)
  const followUpSequenceRef = useRef(0)
  const pageVisitTrackedRef = useRef(false)

  const normalizedJobDescription = jobDescription.trim()
  const normalizedFollowUpQuestion = followUpQuestion.trim()
  const hasActiveConversation = Boolean(submittedJobDescription)
  const canSubmitJobDescription =
    normalizedJobDescription.length >= minimumJobDescriptionLength
  const canAskFollowUp = Boolean(conversationId) && journeyState === 'success'
  const canSubmitFollowUp =
    canAskFollowUp &&
    followUpState === 'idle' &&
    normalizedFollowUpQuestion.length >= 1 &&
    normalizedFollowUpQuestion.length <= maximumFollowUpLength

  useEffect(() => {
    const scrollContainer = conversationScrollRef.current
    if (activeView === 'conversation' && scrollContainer) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight
    }
  }, [activeView, followUpState, journeyState, messages.length])

  useEffect(() => {
    if (!pageVisitTrackedRef.current) {
      pageVisitTrackedRef.current = true
      trackSafely(trackingClient, 'page_visit')
    }
  }, [trackingClient])

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
      setConversationId(undefined)
      setMatchingMessageId(undefined)
      activeConversationIdRef.current = undefined
      setFollowUpQuestion('')
      setFollowUpState('idle')
      setFollowUpError(undefined)
      setFailedFollowUp(undefined)
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
      activeConversationIdRef.current = response.conversationId
      setMatchingMessageId(response.messageId)
      setMessages((currentMessages) => [...currentMessages, analysisMessage])
      setJourneyState('success')
      trackSafely(trackingClient, 'matching_report_generated', {
        conversationId: response.conversationId,
      })
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
          activeConversationIdRef.current = undefined
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
    trackSafely(trackingClient, 'job_description_submitted')
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

  function getFollowUpFailureDescription(error: unknown): string {
    if (!(error instanceof FollowUpClientError)) {
      return zhCN.followUp.failureDescription
    }

    if (error.code === 'INVALID_REQUEST') {
      return zhCN.followUp.invalidQuestion
    }
    if (error.code === 'CONVERSATION_NOT_FOUND') {
      return zhCN.followUp.conversationNotFound
    }
    if (error.code === 'AI_SERVICE_UNAVAILABLE') {
      return zhCN.followUp.aiUnavailable
    }
    if (error.code === 'PERSISTENCE_ERROR') {
      return zhCN.followUp.persistenceError
    }

    return zhCN.followUp.failureDescription
  }

  async function requestFollowUp(
    question: string,
    questionMessageId: string,
    appendQuestion: boolean,
  ) {
    const requestedConversationId = conversationId
    if (
      !requestedConversationId ||
      journeyState !== 'success' ||
      followUpInFlightRef.current
    ) {
      return
    }

    followUpInFlightRef.current = true
    if (appendQuestion) {
      const questionMessage: ConversationMessageData = {
        id: questionMessageId,
        role: 'user',
        messageType: 'follow_up_question',
        content: question,
      }
      setMessages((currentMessages) => [...currentMessages, questionMessage])
    }
    setFollowUpQuestion('')
    setFollowUpError(undefined)
    setFailedFollowUp(undefined)
    setFollowUpState('loading')

    try {
      const response = await followUpClient.ask(requestedConversationId, question)
      if (activeConversationIdRef.current !== requestedConversationId) {
        return
      }
      const answerMessage: ConversationMessageData = {
        id: response.messageId,
        role: 'assistant',
        messageType: 'follow_up_answer',
        content: response.content,
      }
      setMessages((currentMessages) => [...currentMessages, answerMessage])
      setFollowUpState('idle')
    } catch (error) {
      if (activeConversationIdRef.current === requestedConversationId) {
        setFollowUpError(getFollowUpFailureDescription(error))
        setFailedFollowUp({ messageId: questionMessageId, question })
        setFollowUpState('failure')
      }
    } finally {
      followUpInFlightRef.current = false
    }
  }

  function handleFollowUpSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!canSubmitFollowUp) {
      if (canAskFollowUp && followUpState !== 'loading') {
        setFollowUpError(zhCN.followUp.invalidQuestion)
      }
      return
    }

    followUpSequenceRef.current += 1
    const questionMessageId = `local-follow-up-${followUpSequenceRef.current}`
    void requestFollowUp(
      normalizedFollowUpQuestion,
      questionMessageId,
      true,
    )
  }

  function handleFollowUpChange(value: string) {
    setFollowUpQuestion(value)
    setFollowUpError(
      value.length > maximumFollowUpLength
        ? zhCN.followUp.invalidQuestion
        : undefined,
    )
  }

  function handleFollowUpRetry() {
    if (failedFollowUp) {
      void requestFollowUp(
        failedFollowUp.question,
        failedFollowUp.messageId,
        false,
      )
    }
  }

  function showJobMatching() {
    setActiveView(hasActiveConversation ? 'conversation' : 'home')
  }

  function showResume() {
    trackSafely(trackingClient, 'resume_previewed', { conversationId })
    setActiveView('resume')
  }

  function showContact() {
    trackSafely(trackingClient, 'contact_cta_clicked', { conversationId })
    setActiveView('contact')
  }

  function handleFeedbackSubmitted(rating: 1 | 5) {
    setSubmittedFeedbackRating(rating)
    trackSafely(trackingClient, 'feedback_submitted', { conversationId })
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
            isSubmitting={
              journeyState === 'loading' || followUpState === 'loading'
            }
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
            onClick={showResume}
          >
            <Icon name="file" />
            <span>{zhCN.navigation.resume}</span>
          </button>
          <button
            type="button"
            aria-label={zhCN.navigation.contact}
            aria-current={activeView === 'contact' ? 'page' : undefined}
            onClick={showContact}
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
            <div className="conversation-scroll" ref={conversationScrollRef}>
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
                            onClick={showResume}
                          >
                            <Icon name="file" />
                          </button>
                          <button
                            className="icon-action"
                            type="button"
                            data-tooltip={zhCN.report.contactCandidate}
                            aria-label={zhCN.report.contactCandidate}
                            onClick={showContact}
                          >
                            <Icon name="user" />
                          </button>
                          {conversationId && matchingMessageId ? (
                            <FeedbackPanel
                              conversationId={conversationId}
                              messageId={matchingMessageId}
                              feedbackClient={feedbackClient}
                              submittedRating={submittedFeedbackRating}
                              onSubmitted={handleFeedbackSubmitted}
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

                {followUpState === 'loading' ? (
                  <li className="message-row message-row-assistant">
                    <article
                      className="status-message loading-message follow-up-status-message"
                      aria-label={`${zhCN.conversation.assistantName}：${zhCN.followUp.loadingTitle}`}
                      role="status"
                    >
                      <span className="typing-indicator" aria-hidden="true">
                        <i />
                        <i />
                        <i />
                      </span>
                      <div>
                        <h2>{zhCN.followUp.loadingTitle}</h2>
                        <p>{zhCN.followUp.loadingDescription}</p>
                      </div>
                    </article>
                  </li>
                ) : null}

                {followUpState === 'failure' ? (
                  <li className="message-row message-row-assistant">
                    <article
                      className="status-message failure-message follow-up-status-message"
                      aria-label={`${zhCN.conversation.assistantName}：${zhCN.followUp.failureTitle}`}
                      role="alert"
                    >
                      <div>
                        <h2>{zhCN.followUp.failureTitle}</h2>
                        <p id="follow-up-error">
                          {followUpError ?? zhCN.followUp.failureDescription}
                        </p>
                      </div>
                      <button
                        className="secondary-button"
                        type="button"
                        onClick={handleFollowUpRetry}
                      >
                        {zhCN.followUp.retry}
                      </button>
                    </article>
                  </li>
                ) : null}
              </ol>
            </div>

            <form
              className="follow-up-composer"
              aria-describedby={
                followUpError
                  ? 'follow-up-error'
                  : canAskFollowUp
                    ? undefined
                    : 'follow-up-unavailable'
              }
              onSubmit={handleFollowUpSubmit}
              noValidate
            >
              <label className="sr-only" htmlFor="follow-up-question">
                {zhCN.followUp.label}
              </label>
              <input
                id="follow-up-question"
                type="text"
                value={followUpQuestion}
                placeholder={zhCN.followUp.placeholder}
                maxLength={maximumFollowUpLength}
                disabled={!canAskFollowUp || followUpState !== 'idle'}
                aria-invalid={Boolean(followUpError)}
                onChange={(event) => handleFollowUpChange(event.target.value)}
              />
              <button type="submit" disabled={!canSubmitFollowUp}>
                {followUpState === 'loading'
                  ? zhCN.followUp.sending
                  : zhCN.followUp.send}
              </button>
              {!canAskFollowUp ? (
                <span className="sr-only" id="follow-up-unavailable">
                  {zhCN.followUp.unavailable}
                </span>
              ) : null}
              {followUpError && followUpState !== 'failure' ? (
                <span
                  className="follow-up-field-error"
                  id="follow-up-error"
                  role="alert"
                >
                  {followUpError}
                </span>
              ) : null}
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
