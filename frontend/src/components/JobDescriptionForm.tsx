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
    <form className="jd-form" onSubmit={onSubmit} noValidate>
      <div className="section-heading">
        <div>
          <p className="section-kicker">{zhCN.jobDescription.kicker}</p>
          <h2>{zhCN.jobDescription.title}</h2>
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

      <p className="section-description">{zhCN.jobDescription.description}</p>

      <label htmlFor="job-description">{zhCN.jobDescription.label}</label>
      <textarea
        id="job-description"
        name="jobDescription"
        value={value}
        placeholder={zhCN.jobDescription.placeholder}
        rows={10}
        maxLength={6000}
        disabled={isSubmitting}
        aria-invalid={Boolean(error)}
        aria-describedby={errorId}
        onChange={(event) => onChange(event.target.value)}
      />

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
    </form>
  )
}
