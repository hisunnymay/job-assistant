import { useState } from 'react'
import { zhCN } from '../content/zh-CN'
import { FeedbackClientError } from '../services/feedbackClient'
import type { FeedbackClient } from '../types/feedback'
import { Icon } from './Icon'

type SubmissionState = 'idle' | 'submitting' | 'success' | 'error'

const MAX_FEEDBACK_COMMENT_LENGTH = 2000

function serializeFeedbackComment(
  selectedOptions: string[],
  comment: string,
) {
  return [
    selectedOptions.length > 0
      ? `${zhCN.feedback.selectedReasonsPrefix}${selectedOptions.join('；')}`
      : '',
    comment.trim()
      ? `${zhCN.feedback.customFeedbackPrefix}${comment.trim()}`
      : '',
  ]
    .filter(Boolean)
    .join('\n')
}

function getCustomFeedbackMaxLength(selectedOptions: string[]) {
  const selectedReasons = serializeFeedbackComment(selectedOptions, '')
  const reservedLength =
    selectedReasons.length +
    (selectedReasons ? 1 : 0) +
    zhCN.feedback.customFeedbackPrefix.length

  return Math.max(0, MAX_FEEDBACK_COMMENT_LENGTH - reservedLength)
}

interface FeedbackPanelProps {
  conversationId: string
  messageId: string
  feedbackClient: FeedbackClient
  submittedRating?: 1 | 5
  onSubmitted(rating: 1 | 5): void
}

export function FeedbackPanel({
  conversationId,
  messageId,
  feedbackClient,
  submittedRating,
  onSubmitted,
}: FeedbackPanelProps) {
  const [pendingRating, setPendingRating] = useState<1 | 5>()
  const [submissionState, setSubmissionState] =
    useState<SubmissionState>('idle')
  const [errorMessage, setErrorMessage] = useState('')
  const [comment, setComment] = useState('')
  const [selectedOptions, setSelectedOptions] = useState<string[]>([])

  const effectiveRating = submittedRating ?? pendingRating
  const feedbackLocked =
    submittedRating !== undefined ||
    submissionState === 'submitting' ||
    submissionState === 'success'
  const hasFeedbackContribution =
    selectedOptions.length > 0 || comment.trim().length > 0
  const customFeedbackMaxLength =
    getCustomFeedbackMaxLength(selectedOptions)

  function openFeedbackDialog(rating: 1 | 5) {
    if (feedbackLocked) {
      return
    }

    setPendingRating(rating)
    setComment('')
    setSelectedOptions([])
    setSubmissionState('idle')
    setErrorMessage('')
  }

  function closeFeedbackDialog() {
    if (submissionState === 'submitting') {
      return
    }

    setPendingRating(undefined)
    setComment('')
    setSelectedOptions([])
    setSubmissionState('idle')
    setErrorMessage('')
  }

  async function submitFeedback() {
    if (
      feedbackLocked ||
      pendingRating === undefined ||
      !hasFeedbackContribution
    ) {
      return
    }

    const rating = pendingRating
    const serializedComment = serializeFeedbackComment(selectedOptions, comment)
    setSubmissionState('submitting')
    setErrorMessage('')

    try {
      await feedbackClient.submit({
        conversationId,
        messageId,
        rating,
        comment: serializedComment,
      })
      setSubmissionState('success')
      onSubmitted(rating)
      setPendingRating(undefined)
      setComment('')
      setSelectedOptions([])
    } catch (error) {
      setSubmissionState('error')
      setErrorMessage(
        error instanceof FeedbackClientError && error.code === 'REPORT_NOT_FOUND'
          ? zhCN.feedback.reportNotFound
          : zhCN.feedback.submitError,
      )
    }
  }

  return (
    <div className="feedback-actions" aria-label={zhCN.feedback.actionsLabel}>
      <button
        className="icon-action"
        type="button"
        data-tooltip={zhCN.feedback.helpful}
        aria-label={zhCN.feedback.helpful}
        aria-pressed={effectiveRating === 5}
        disabled={feedbackLocked}
        onClick={() => openFeedbackDialog(5)}
      >
        <Icon name="thumbs-up" />
      </button>
      <button
        className="icon-action"
        type="button"
        data-tooltip={zhCN.feedback.notHelpful}
        aria-label={zhCN.feedback.notHelpful}
        aria-pressed={effectiveRating === 1}
        disabled={feedbackLocked}
        onClick={() => openFeedbackDialog(1)}
      >
        <Icon name="thumbs-down" />
      </button>
      <span
        className={`feedback-status feedback-status-${submissionState}`}
        aria-live="polite"
      >
        {submissionState === 'submitting' ? zhCN.feedback.submitting : null}
        {submissionState === 'success' || submittedRating !== undefined
          ? zhCN.feedback.successDescription
          : null}
        {submissionState === 'error' && pendingRating === undefined
          ? errorMessage
          : null}
      </span>
      {pendingRating !== undefined ? (
        <div
          className="feedback-dialog-backdrop"
          role="presentation"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              closeFeedbackDialog()
            }
          }}
        >
          <section
            className="feedback-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="feedback-dialog-title"
            aria-describedby="feedback-dialog-description"
            onKeyDown={(event) => {
              if (event.key === 'Escape') {
                closeFeedbackDialog()
              }
            }}
          >
            <h2 id="feedback-dialog-title">
              {zhCN.feedback.dialogTitle(pendingRating)}
            </h2>
            <p id="feedback-dialog-description">
              {zhCN.feedback.dialogDescription}
            </p>
            <fieldset className="feedback-options">
              <legend>{zhCN.feedback.optionsLabel}</legend>
              <div className="feedback-option-list">
                {zhCN.feedback.predefinedOptions(pendingRating).map((option) => {
                  const isSelected = selectedOptions.includes(option)
                  return (
                    <button
                      key={option}
                      className="feedback-option"
                      type="button"
                      aria-pressed={isSelected}
                      disabled={submissionState === 'submitting'}
                      onClick={() => {
                        const nextOptions = isSelected
                          ? selectedOptions.filter(
                              (currentOption) => currentOption !== option,
                            )
                          : [...selectedOptions, option]
                        setSelectedOptions(nextOptions)
                        setComment((currentComment) =>
                          currentComment.slice(
                            0,
                            getCustomFeedbackMaxLength(nextOptions),
                          ),
                        )
                      }}
                    >
                      {isSelected ? '✓' : '+'} {option}
                    </button>
                  )
                })}
              </div>
            </fieldset>
            <label htmlFor="feedback-comment">
              {zhCN.feedback.commentLabel}
            </label>
            <textarea
              id="feedback-comment"
              value={comment}
              maxLength={customFeedbackMaxLength}
              autoFocus
              disabled={submissionState === 'submitting'}
              placeholder={zhCN.feedback.commentPlaceholder}
              onChange={(event) =>
                setComment(
                  event.target.value.slice(0, customFeedbackMaxLength),
                )
              }
            />
            {!hasFeedbackContribution ? (
              <p className="feedback-contribution-required">
                {zhCN.feedback.contributionRequired}
              </p>
            ) : null}
            {submissionState === 'error' ? (
              <p className="feedback-dialog-error" role="alert">
                {errorMessage}
              </p>
            ) : null}
            <div className="feedback-dialog-actions">
              <button
                className="secondary-button"
                type="button"
                disabled={submissionState === 'submitting'}
                onClick={closeFeedbackDialog}
              >
                {zhCN.feedback.cancel}
              </button>
              <button
                className="primary-button"
                type="button"
                disabled={
                  submissionState === 'submitting' || !hasFeedbackContribution
                }
                onClick={() => void submitFeedback()}
              >
                {submissionState === 'submitting'
                  ? zhCN.feedback.submitting
                  : zhCN.feedback.submit}
              </button>
            </div>
          </section>
        </div>
      ) : null}
    </div>
  )
}
