import { useState } from 'react'
import { zhCN } from '../content/zh-CN'
import { Icon } from './Icon'

type CopyTarget = 'email' | 'phone' | 'greeting'
type CopyState = { target?: CopyTarget; result: 'idle' | 'success' | 'error' }

export function ContactPanel() {
  const [recruiterName, setRecruiterName] = useState('')
  const [copyState, setCopyState] = useState<CopyState>({ result: 'idle' })
  const greeting = zhCN.contact.greeting(
    recruiterName.trim() || zhCN.contact.recruiterNameFallback,
  )

  async function copy(value: string, target: CopyTarget) {
    try {
      await navigator.clipboard.writeText(value)
      setCopyState({ target, result: 'success' })
    } catch {
      setCopyState({ target, result: 'error' })
    }
  }

  function statusFor(target: CopyTarget) {
    if (copyState.target !== target) {
      return ''
    }

    return copyState.result === 'success'
      ? zhCN.contact.copySuccess
      : zhCN.contact.copyError
  }

  return (
    <section className="contact-panel" id="contact" aria-labelledby="contact-title">
      <header className="page-header">
        <h1 id="contact-title">{zhCN.contact.title}</h1>
      </header>

      <div className="contact-content">
        <h2>{zhCN.contact.methodsLabel}</h2>
        <div className="contact-methods">
          <article className="contact-method-card">
            <Icon name="mail" size={27} />
            <div>
              <span>{zhCN.contact.emailLabel}</span>
              <a href={`mailto:${zhCN.contact.email}`}>{zhCN.contact.email}</a>
            </div>
            <button
              className="copy-icon-button"
              type="button"
              aria-label={zhCN.contact.copyEmail}
              title={zhCN.contact.copyEmail}
              onClick={() => void copy(zhCN.contact.email, 'email')}
            >
              <Icon name="copy" size={18} />
            </button>
            <span className="sr-only" aria-live="polite">
              {statusFor('email')}
            </span>
          </article>

          <article className="contact-method-card">
            <Icon name="phone" size={27} />
            <div>
              <span>{zhCN.contact.phoneLabel}</span>
              <a href={`tel:${zhCN.contact.phone}`}>{zhCN.contact.phone}</a>
            </div>
            <button
              className="copy-icon-button"
              type="button"
              aria-label={zhCN.contact.copyPhone}
              title={zhCN.contact.copyPhone}
              onClick={() => void copy(zhCN.contact.phone, 'phone')}
            >
              <Icon name="copy" size={18} />
            </button>
            <span className="sr-only" aria-live="polite">
              {statusFor('phone')}
            </span>
          </article>
        </div>

        <label className="field-label" htmlFor="recruiter-name">
          {zhCN.contact.recruiterNameLabel}
        </label>
        <input
          id="recruiter-name"
          className="text-input"
          value={recruiterName}
          maxLength={80}
          placeholder={zhCN.contact.recruiterNamePlaceholder}
          onChange={(event) => {
            setRecruiterName(event.target.value)
            setCopyState({ result: 'idle' })
          }}
        />

        <h2 className="greeting-title">{zhCN.contact.greetingLabel}</h2>
        <div className="greeting-preview" aria-label={zhCN.contact.greetingLabel}>
          {greeting}
        </div>
        <button
          className="primary-button copy-greeting-button"
          type="button"
          onClick={() => void copy(greeting, 'greeting')}
        >
          {zhCN.contact.copyGreeting}
        </button>
        <span className="action-status" aria-live="polite">
          {statusFor('greeting')}
        </span>
        <p className="support-note">{zhCN.contact.noAutoSend}</p>
      </div>
    </section>
  )
}
