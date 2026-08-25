import { useState, type FormEvent } from 'react'
import { JobDescriptionForm } from './components/JobDescriptionForm'
import { MatchingReportView } from './components/MatchingReportView'
import { zhCN } from './content/zh-CN'
import { createMockAnalysisClient } from './services/mockAnalysisClient'
import type { AnalysisClient, MatchingReport } from './types/matching'
import './styles.css'

type JourneyState = 'initial' | 'loading' | 'success' | 'failure'

const minimumJobDescriptionLength = 40
const defaultAnalysisClient = createMockAnalysisClient()

interface AppProps {
  analysisClient?: AnalysisClient
}

export function App({ analysisClient = defaultAnalysisClient }: AppProps) {
  const [jobDescription, setJobDescription] = useState('')
  const [submittedJobDescription, setSubmittedJobDescription] = useState('')
  const [fieldError, setFieldError] = useState<string>()
  const [journeyState, setJourneyState] = useState<JourneyState>('initial')
  const [report, setReport] = useState<MatchingReport>()

  function validateJobDescription(value: string): string | undefined {
    if (!value) {
      return zhCN.jobDescription.emptyError
    }

    if (value.length < minimumJobDescriptionLength) {
      return zhCN.jobDescription.shortError
    }

    return undefined
  }

  async function runAnalysis() {
    const normalizedJobDescription = jobDescription.trim()
    const validationError = validateJobDescription(normalizedJobDescription)

    if (validationError) {
      setFieldError(validationError)
      return
    }

    setFieldError(undefined)
    setJourneyState('loading')
    setReport(undefined)
    setSubmittedJobDescription(normalizedJobDescription)

    try {
      const matchingReport = await analysisClient.analyze(
        normalizedJobDescription,
      )
      setReport(matchingReport)
      setJourneyState('success')
    } catch {
      setJourneyState('failure')
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    void runAnalysis()
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

  function handleStartOver() {
    setJobDescription('')
    setSubmittedJobDescription('')
    setReport(undefined)
    setJourneyState('initial')
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
        <section className="hero" aria-labelledby="hero-title">
          <div>
            <p className="hero-eyebrow">{zhCN.hero.eyebrow}</p>
            <h1 id="hero-title">{zhCN.hero.title}</h1>
            <p className="hero-introduction">{zhCN.hero.introduction}</p>
          </div>

          <aside className="guidance-card" aria-labelledby="guidance-title">
            <p className="assistant-label">{zhCN.guidance.label}</p>
            <h2 id="guidance-title">{zhCN.guidance.title}</h2>
            <p>{zhCN.guidance.body}</p>
            <ul>
              {zhCN.guidance.points.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
          </aside>
        </section>

        <section className="workspace" aria-label={zhCN.navigationLabel}>
          <JobDescriptionForm
            value={jobDescription}
            error={fieldError}
            isSubmitting={journeyState === 'loading'}
            onChange={handleChange}
            onUseExample={handleUseExample}
            onSubmit={handleSubmit}
          />

          <div className="journey-output" aria-live="polite">
            {journeyState === 'initial' ? (
              <div className="empty-state">
                <span className="empty-state-icon" aria-hidden="true">
                  ↗
                </span>
                <p>{zhCN.guidance.title}</p>
              </div>
            ) : null}

            {journeyState === 'loading' ? (
              <div className="loading-state" role="status">
                <span className="spinner" aria-hidden="true" />
                <div>
                  <h2>{zhCN.loading.title}</h2>
                  <p>{zhCN.loading.description}</p>
                </div>
              </div>
            ) : null}

            {journeyState === 'failure' ? (
              <div className="failure-state" role="alert">
                <div>
                  <h2>{zhCN.failure.title}</h2>
                  <p>{zhCN.failure.description}</p>
                </div>
                <button
                  className="secondary-button"
                  type="button"
                  onClick={() => void runAnalysis()}
                >
                  {zhCN.failure.retry}
                </button>
              </div>
            ) : null}

            {journeyState === 'success' && report ? (
              <MatchingReportView
                report={report}
                submittedJobDescription={submittedJobDescription}
                onStartOver={handleStartOver}
              />
            ) : null}
          </div>
        </section>
      </main>
    </div>
  )
}
