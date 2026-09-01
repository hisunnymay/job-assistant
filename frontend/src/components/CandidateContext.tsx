import { useEffect, useId, useLayoutEffect, useRef, useState } from 'react'
import { zhCN } from '../content/zh-CN'
import { Icon } from './Icon'

export function CandidateContext() {
  const [isHintOpen, setIsHintOpen] = useState(false)
  const hintId = useId()
  const containerRef = useRef<HTMLElement>(null)
  const infoButtonRef = useRef<HTMLButtonElement>(null)

  useLayoutEffect(() => {
    if (!isHintOpen) {
      return
    }

    const container = containerRef.current
    if (!container) {
      return
    }

    const updateHintPosition = () => {
      const bounds = container.getBoundingClientRect()
      container.style.setProperty(
        '--candidate-hint-left',
        `${bounds.right + 12}px`,
      )
      container.style.setProperty(
        '--candidate-hint-top',
        `${Math.max(16, bounds.top)}px`,
      )
    }

    updateHintPosition()
    window.addEventListener('resize', updateHintPosition)
    return () => {
      window.removeEventListener('resize', updateHintPosition)
      container.style.removeProperty('--candidate-hint-left')
      container.style.removeProperty('--candidate-hint-top')
    }
  }, [isHintOpen])

  useEffect(() => {
    if (!isHintOpen) {
      return
    }

    const handlePointerDown = (event: PointerEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) {
        setIsHintOpen(false)
      }
    }
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsHintOpen(false)
        infoButtonRef.current?.focus()
      }
    }

    document.addEventListener('pointerdown', handlePointerDown)
    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('pointerdown', handlePointerDown)
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [isHintOpen])

  return (
    <section
      ref={containerRef}
      className="candidate-context"
      aria-label={zhCN.candidateContext.ariaLabel}
    >
      <span className="candidate-context-avatar" aria-hidden="true">
        <Icon name="candidate" size={22} />
      </span>
      <span className="candidate-context-label">
        {zhCN.candidateContext.label}
      </span>
      <div className="candidate-context-name-row">
        <strong className="candidate-context-name">
          {zhCN.candidateContext.name}
        </strong>
        <button
          ref={infoButtonRef}
          className="candidate-context-info"
          type="button"
          aria-label={zhCN.candidateContext.infoButton}
          aria-expanded={isHintOpen}
          aria-controls={hintId}
          onClick={() => setIsHintOpen((isOpen) => !isOpen)}
        >
          <Icon name="info" size={15} />
        </button>
      </div>
      {isHintOpen ? (
        <div
          id={hintId}
          className="candidate-context-hint"
          role="region"
          aria-label={zhCN.candidateContext.hintTitle}
        >
          <strong>{zhCN.candidateContext.hintTitle}</strong>
          <p>{zhCN.candidateContext.hintBody}</p>
        </div>
      ) : null}
    </section>
  )
}
