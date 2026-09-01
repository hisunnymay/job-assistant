import { useEffect, useId, useState } from 'react'
import { zhCN } from '../content/zh-CN'

interface LoadingStatusProps {
  title: string
  startedAt: number
  className?: string
  showTypicalDuration?: boolean
}

function getElapsedSeconds(startedAt: number, currentTime: number) {
  return Math.max(0, Math.floor((currentTime - startedAt) / 1000))
}

export function LoadingStatus({
  title,
  startedAt,
  className = '',
  showTypicalDuration = true,
}: LoadingStatusProps) {
  const [currentTime, setCurrentTime] = useState(Date.now)
  const elapsedSeconds = getElapsedSeconds(startedAt, currentTime)
  const durationDescriptionId = useId()

  useEffect(() => {
    const timerId = window.setInterval(() => {
      setCurrentTime(Date.now())
    }, 1000)

    return () => {
      window.clearInterval(timerId)
    }
  }, [startedAt])

  return (
    <article
      className={`status-message loading-message ${className}`.trim()}
      aria-label={`${zhCN.conversation.assistantName}：${title}`}
      aria-describedby={showTypicalDuration ? durationDescriptionId : undefined}
      role="status"
    >
      <span className="typing-indicator" aria-hidden="true">
        <i />
        <i />
        <i />
      </span>
      <div>
        <h2>{title}</h2>
        {showTypicalDuration ? (
          <p id={durationDescriptionId}>{zhCN.loading.typicalDuration}</p>
        ) : null}
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
