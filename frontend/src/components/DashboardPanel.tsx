import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react'
import { zhCN } from '../content/zh-CN'
import type {
  DashboardAggregate,
  DashboardClient,
  DashboardDateRange,
} from '../types/dashboard'

interface DashboardPanelProps {
  client: DashboardClient
}

type DashboardState = 'loading' | 'ready' | 'failure'

const defaultDashboardStartDate = '2026-09-01'
const dashboardTimezone = 'Asia/Shanghai'

const totalMetricKeys = [
  'pageVisits',
  'jobDescriptionSubmissions',
  'matchingReportsGenerated',
  'resumePreviews',
  'contactCtaClicks',
  'feedbackSubmissions',
] as const

function formatNumber(value: number) {
  return new Intl.NumberFormat('zh-CN').format(value)
}

function formatUpdatedAt(value: string, timezone: string) {
  return new Intl.DateTimeFormat('zh-CN', {
    dateStyle: 'medium',
    timeStyle: 'short',
    timeZone: timezone,
  }).format(new Date(value))
}

function currentDashboardDate() {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: dashboardTimezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date(Date.now()))
  const valueByType = Object.fromEntries(
    parts.map((part) => [part.type, part.value]),
  )
  return `${valueByType.year}-${valueByType.month}-${valueByType.day}`
}

function createDefaultDateRange(): DashboardDateRange {
  return {
    startDate: defaultDashboardStartDate,
    endDate: currentDashboardDate(),
  }
}

export function DashboardPanel({ client }: DashboardPanelProps) {
  const [defaultDateRange] = useState(createDefaultDateRange)
  const [aggregate, setAggregate] = useState<DashboardAggregate>()
  const [state, setState] = useState<DashboardState>('loading')
  const [startDate, setStartDate] = useState(defaultDateRange.startDate)
  const [endDate, setEndDate] = useState(defaultDateRange.endDate)
  const [retryRange, setRetryRange] = useState<
    DashboardDateRange | undefined
  >(defaultDateRange)
  const [validationError, setValidationError] = useState<string>()
  const [retrievalError, setRetrievalError] = useState<string>()
  const requestSequence = useRef(0)

  const loadAggregate = useCallback(
    async (dateRange?: DashboardDateRange) => {
      requestSequence.current += 1
      const requestId = requestSequence.current
      setState('loading')
      setRetrievalError(undefined)
      setRetryRange(dateRange)
      try {
        const nextAggregate = await client.getAggregate(dateRange)
        if (requestSequence.current !== requestId) {
          return
        }
        setAggregate(nextAggregate)
        setState('ready')
      } catch {
        if (requestSequence.current !== requestId) {
          return
        }
        setRetrievalError(zhCN.dashboard.retrievalError)
        setState('failure')
      }
    },
    [client],
  )

  useEffect(() => {
    requestSequence.current += 1
    const requestId = requestSequence.current
    void client
      .getAggregate(defaultDateRange)
      .then((nextAggregate) => {
        if (requestSequence.current === requestId) {
          setAggregate(nextAggregate)
          setState('ready')
        }
      })
      .catch(() => {
        if (requestSequence.current === requestId) {
          setRetrievalError(zhCN.dashboard.retrievalError)
          setState('failure')
        }
      })
    return () => {
      requestSequence.current += 1
    }
  }, [client, defaultDateRange])

  function handleApply(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!startDate || !endDate) {
      setValidationError(zhCN.dashboard.incompleteRangeError)
      return
    }
    if (startDate > endDate) {
      setValidationError(zhCN.dashboard.invalidRangeError)
      return
    }
    setValidationError(undefined)
    void loadAggregate({ startDate, endDate })
  }

  function handleReset() {
    setStartDate('')
    setEndDate('')
    setValidationError(undefined)
    void loadAggregate()
  }

  const period = aggregate?.reportingPeriod
  const periodLabel =
    period?.mode === 'custom'
      ? zhCN.dashboard.customPeriod(period.startDate ?? '', period.endDate ?? '')
      : zhCN.dashboard.allRetainedPeriod
  const isEmpty = aggregate?.updatedAt === null

  return (
    <section
      className="dashboard-panel"
      aria-labelledby="dashboard-title"
      aria-busy={state === 'loading'}
    >
      <header className="dashboard-header">
        <div>
          <h1 id="dashboard-title">{zhCN.dashboard.title}</h1>
          <p>{zhCN.dashboard.description}</p>
        </div>
      </header>

      <form className="dashboard-filter" onSubmit={handleApply} noValidate>
        <div className="date-field">
          <label htmlFor="dashboard-start-date">{zhCN.dashboard.startDate}</label>
          <input
            id="dashboard-start-date"
            type="date"
            value={startDate}
            aria-invalid={Boolean(validationError)}
            onChange={(event) => {
              setStartDate(event.target.value)
              setValidationError(undefined)
            }}
          />
        </div>
        <div className="date-field">
          <label htmlFor="dashboard-end-date">{zhCN.dashboard.endDate}</label>
          <input
            id="dashboard-end-date"
            type="date"
            value={endDate}
            aria-invalid={Boolean(validationError)}
            onChange={(event) => {
              setEndDate(event.target.value)
              setValidationError(undefined)
            }}
          />
        </div>
        <div className="dashboard-filter-actions">
          <button
            className="primary-button"
            type="submit"
            disabled={state === 'loading'}
          >
            {zhCN.dashboard.apply}
          </button>
          <button
            className="secondary-button"
            type="button"
            disabled={state === 'loading' && !aggregate}
            onClick={handleReset}
          >
            {zhCN.dashboard.reset}
          </button>
        </div>
        {validationError ? (
          <p className="dashboard-filter-error" role="alert">
            {validationError}
          </p>
        ) : null}
      </form>

      {state === 'loading' ? (
        <p className="dashboard-status" role="status">
          {aggregate
            ? zhCN.dashboard.refreshing
            : zhCN.dashboard.initialLoading}
        </p>
      ) : null}
      {retrievalError ? (
        <div className="dashboard-error" role="alert">
          <p>
            {aggregate
              ? retrievalError
              : zhCN.dashboard.initialRetrievalError}
          </p>
          <button
            className="secondary-button"
            type="button"
            onClick={() => void loadAggregate(retryRange)}
          >
            {zhCN.dashboard.retry}
          </button>
        </div>
      ) : null}

      {aggregate ? (
        <div className="dashboard-results">
          {isEmpty ? (
            <p className="dashboard-empty" role="status">
              {zhCN.dashboard.noData}
            </p>
          ) : null}
          <article className="conversion-card">
            <div className="metric-heading-row">
              <h2>{zhCN.dashboard.conversion.title}</h2>
              <span>{zhCN.dashboard.primaryMetric}</span>
            </div>
            <p className="conversion-value">
              {aggregate.contactConversion.rate === null
                ? zhCN.dashboard.unavailableRate
                : new Intl.NumberFormat('zh-CN', {
                    style: 'percent',
                    maximumFractionDigits: 1,
                  }).format(aggregate.contactConversion.rate)}
            </p>
            <p className="conversion-ratio">
              {formatNumber(aggregate.contactConversion.numerator)} /{' '}
              {formatNumber(aggregate.contactConversion.denominator)}
            </p>
            <p className="metric-definition">
              {zhCN.dashboard.conversion.definition}
            </p>
          </article>

          <div className="metric-grid">
            {totalMetricKeys.map((metricKey, index) => {
              const metric = zhCN.dashboard.metrics[metricKey]
              return (
                <article className={`metric-card metric-card-${index + 1}`} key={metricKey}>
                  <span className="metric-icon" aria-hidden="true">
                    {metric.icon}
                  </span>
                  <div>
                    <h2>{metric.title}</h2>
                    <p className="metric-value">
                      {formatNumber(aggregate.eventTotals[metricKey])}
                    </p>
                    <p className="metric-definition">{metric.definition}</p>
                  </div>
                </article>
              )
            })}
          </div>

          <footer className="dashboard-metadata">
            <p>
              <strong>{zhCN.dashboard.reportingPeriod}：</strong>
              {periodLabel}
            </p>
            <p>
              <strong>{zhCN.dashboard.timezone}：</strong>
              {period?.timezone}
            </p>
            <p>
              <strong>{zhCN.dashboard.updatedAt}：</strong>
              {aggregate.updatedAt
                ? formatUpdatedAt(
                    aggregate.updatedAt,
                    aggregate.reportingPeriod.timezone,
                  )
                : zhCN.dashboard.noUpdate}
            </p>
          </footer>
        </div>
      ) : null}
    </section>
  )
}
