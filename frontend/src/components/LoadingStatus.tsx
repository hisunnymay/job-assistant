import { useEffect, useId, useState } from 'react'
import { zhCN } from '../content/zh-CN'

interface LoadingStatusProps {
  title: string
  className?: string
}

export function LoadingStatus({ title, className = '' }: LoadingStatusProps) {
  const [elapsedSeconds, setElapsedSeconds] = useState(0)
  const durationDescriptionId = useId()

  useEffect(() => {
    const startedAt = Date.now()
    const timerId = window.setInterval(() => {
      setElapsedSeconds(Math.floor((Date.now() - startedAt) / 1000))
    }, 1000)

    return () => {
      window.clearInterval(timerId)
    }
  }, [])

  return (
    <article
      className={`status-message loading-message ${className}`.trim()}
      aria-label={`${zhCN.conversation.assistantName}：${title}`}
      aria-describedby={durationDescriptionId}
      role="status"
    >
      <span className="typing-indicator" aria-hidden="true">
        <i />
        <i />
        <i />
      </span>
      <div>
        <h2>{title}</h2>
        <p id={durationDescriptionId}>{zhCN.loading.typicalDuration}</p>
        <p className="elapsed-time" aria-hidden="true">
          {zhCN.loading.elapsed(elapsedSeconds)}
        </p>
        {elapsedSeconds > 60 ? (
          <p className="extended-wait-note">{zhCN.loading.extendedWait}</p>
        ) : null}
      </div>
    </article>
  )
}
