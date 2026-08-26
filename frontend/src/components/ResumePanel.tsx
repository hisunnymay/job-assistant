import { zhCN } from '../content/zh-CN'
import { Icon } from './Icon'

interface ResumePanelProps {
  resumeUrl: string
}

export function ResumePanel({ resumeUrl }: ResumePanelProps) {
  const downloadUrl = `${resumeUrl}?download=true`

  return (
    <section className="resume-panel" id="resume" aria-labelledby="resume-title">
      <header className="page-header resume-header">
        <h1 id="resume-title">{zhCN.resume.title}</h1>
        <a className="download-button" href={downloadUrl} download>
          <Icon name="download" size={17} />
          {zhCN.resume.download}
        </a>
      </header>

      <iframe
        className="resume-frame"
        src={resumeUrl}
        title={zhCN.resume.previewTitle}
      />
    </section>
  )
}
