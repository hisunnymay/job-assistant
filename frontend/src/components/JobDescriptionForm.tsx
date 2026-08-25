import type { FormEvent } from 'react'
import { zhCN } from '../content/zh-CN'

interface JobDescriptionFormProps {
  value: string
  error?: string
  isSubmitting: boolean
  onChange(value: string): void
  onUseExample(): void
  onSubmit(event: FormEvent<HTMLFormElement>): void
}

export function JobDescriptionForm({
  value,
  error,
  isSubmitting,
  onChange,
  onUseExample,
  onSubmit,
}: JobDescriptionFormProps) {
  const errorId = error ? 'job-description-error' : undefined

  return (
    <form className="composer" onSubmit={onSubmit} noValidate>
      <div className="composer-heading">
        <div>
          <h2>{zhCN.jobDescription.title}</h2>
          <p>{zhCN.jobDescription.description}</p>
        </div>
        <button
          className="text-button"
          type="button"
          onClick={onUseExample}
          disabled={isSubmitting}
        >
          {zhCN.jobDescription.useExample}
        </button>
      </div>

      <label className="sr-only" htmlFor="job-description">
        {zhCN.jobDescription.label}
      </label>
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

      <div className="composer-footer">
        <div className="form-meta">
          <span>{zhCN.jobDescription.characterCount(value.length)}</span>
          {error ? (
            <span className="field-error" id={errorId} role="alert">
              {error}
            </span>
          ) : null}
        </div>

        <button className="primary-button" type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? zhCN.jobDescription.submitting
            : zhCN.jobDescription.submit}
        </button>
      </div>
    </form>
  )
}
