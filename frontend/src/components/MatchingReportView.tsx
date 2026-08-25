import { zhCN } from '../content/zh-CN'
import type {
  EvidenceStatus,
  MatchingReport,
  RequirementImportance,
} from '../types/matching'

const statusLabels: Record<EvidenceStatus, string> = {
  supported: zhCN.report.status.supported,
  partial: zhCN.report.status.partial,
  missing: zhCN.report.status.missing,
}

const importanceLabels: Record<RequirementImportance, string> = {
  core: zhCN.report.importance.core,
  important: zhCN.report.importance.important,
  additional: zhCN.report.importance.additional,
}

interface MatchingReportViewProps {
  report: MatchingReport
  submittedJobDescription: string
  onStartOver(): void
}

export function MatchingReportView({
  report,
  submittedJobDescription,
  onStartOver,
}: MatchingReportViewProps) {
  return (
    <section className="report" aria-labelledby="report-title">
      <header className="report-header">
        <div>
          <p className="section-kicker">{zhCN.report.kicker}</p>
          <h2 id="report-title">{report.title}</h2>
        </div>
        <button className="secondary-button" type="button" onClick={onStartOver}>
          {zhCN.report.startOver}
        </button>
      </header>

      <div className="mock-notice" role="note">
        <strong>{zhCN.report.mockNoticeTitle}</strong>
        <span>{zhCN.report.mockNoticeBody}</span>
      </div>

      <details className="submitted-jd">
        <summary>{zhCN.report.submittedJobDescription}</summary>
        <p>{submittedJobDescription}</p>
      </details>

      <div className="report-legend" aria-label={zhCN.report.legendLabel}>
        {(Object.keys(statusLabels) as EvidenceStatus[]).map((status) => (
          <span className={`legend-item status-${status}`} key={status}>
            <span className="legend-dot" aria-hidden="true" />
            {statusLabels[status]}
          </span>
        ))}
      </div>

      <div className="requirement-list">
        {report.requirements.map((item) => (
          <article
            className={`requirement-card status-${item.status}`}
            key={item.id}
          >
            <div className="requirement-heading">
              <div className="requirement-tags">
                <span className={`status-badge status-${item.status}`}>
                  {statusLabels[item.status]}
                </span>
                <span className="importance-badge">
                  {importanceLabels[item.importance]}
                </span>
              </div>
              <h3>{item.requirement}</h3>
            </div>

            <p className="finding">{item.finding}</p>

            {item.evidence.length > 0 ? (
              <div className="evidence-block">
                <h4>{zhCN.report.evidenceTitle}</h4>
                <ul>
                  {item.evidence.map((evidence) => (
                    <li key={evidence}>{evidence}</li>
                  ))}
                </ul>
              </div>
            ) : null}

            {item.informationGap ? (
              <div className="gap-block">
                <h4>{zhCN.report.gapTitle}</h4>
                <p>{item.informationGap}</p>
              </div>
            ) : null}
          </article>
        ))}
      </div>

      <aside className="limitations" aria-labelledby="limitations-title">
        <h3 id="limitations-title">{zhCN.report.limitationsTitle}</h3>
        <ul>
          {report.limitations.map((limitation) => (
            <li key={limitation}>{limitation}</li>
          ))}
        </ul>
      </aside>
    </section>
  )
}
