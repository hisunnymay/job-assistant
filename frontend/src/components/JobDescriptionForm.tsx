import type { FormEvent } from 'react'
import { zhCN } from '../content/zh-CN'

interface JobDescriptionFormProps {
  value: string
  error?: string
  isSubmitting: boolean
  canSubmit: boolean
  onChange(value: string): void
  onUseExample(): void
  onViewExampleReport(): void
  onSubmit(event: FormEvent<HTMLFormElement>): void
}

export function JobDescriptionForm({
  value,
  error,
  isSubmitting,
  canSubmit,
  onChange,
  onUseExample,
  onViewExampleReport,
  onSubmit,
}: JobDescriptionFormProps) {
  const errorId = error ? 'job-description-error' : undefined

  return (
    <form className="composer" onSubmit={onSubmit} noValidate>
      <label className="sr-only" htmlFor="job-description">
        {zhCN.jobDescription.label}
      </label>
      <div className="composer-input-area">
        <textarea
          id="job-description"
          name="jobDescription"
          value={value}
          placeholder={zhCN.jobDescription.placeholder}
          rows={6}
          maxLength={6000}
          disabled={isSubmitting}
          aria-invalid={Boolean(error)}
          aria-describedby={errorId}
          onChange={(event) => onChange(event.target.value)}
        />
        <button
          className="text-button example-button"
          type="button"
          onClick={onUseExample}
          disabled={isSubmitting}
        >
          {zhCN.jobDescription.useExample}
        </button>
      </div>

      <div className="composer-footer">
        <button
          className="secondary-button example-report-button"
          type="button"
          onClick={onViewExampleReport}
          disabled={isSubmitting}
        >
          {zhCN.jobDescription.viewExampleReport}
        </button>
        <div className="form-meta">
          <span>{zhCN.jobDescription.characterCount(value.length)}</span>
          {error ? (
            <span className="field-error" id={errorId} role="alert">
              {error}
            </span>
          ) : null}
        </div>

        <button
          className="primary-button"
          type="submit"
          disabled={isSubmitting || !canSubmit}
        >
          {isSubmitting
            ? zhCN.jobDescription.submitting
            : zhCN.jobDescription.submit}
        </button>
      </div>
    </form>
  )
}
