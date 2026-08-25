import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { App } from './App'
import { zhCN } from './content/zh-CN'
import { createMockAnalysisClient } from './services/mockAnalysisClient'

function renderJourney(options?: { failFirstRequest?: boolean }) {
  const analysisClient = createMockAnalysisClient({
    delayMs: 0,
    failFirstRequest: options?.failFirstRequest,
  })

  render(<App analysisClient={analysisClient} />)
}

function submitExampleJobDescription() {
  fireEvent.click(
    screen.getByRole('button', { name: zhCN.jobDescription.useExample }),
  )
  fireEvent.click(
    screen.getByRole('button', { name: zhCN.jobDescription.submit }),
  )
}

describe('matching journey', () => {
  it('renders initial guidance and an empty job-description form', () => {
    renderJourney()

    expect(
      screen.getByRole('heading', { level: 1, name: zhCN.hero.title }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: zhCN.guidance.title }),
    ).toBeInTheDocument()
    expect(screen.getByLabelText(zhCN.jobDescription.label)).toHaveValue('')
  })

  it('distinguishes empty and too-short job descriptions', () => {
    renderJourney()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.jobDescription.submit }),
    )
    expect(screen.getByRole('alert')).toHaveTextContent(
      zhCN.jobDescription.emptyError,
    )

    fireEvent.change(screen.getByLabelText(zhCN.jobDescription.label), {
      target: { value: '只写了很短的职位要求' },
    })
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.jobDescription.submit }),
    )
    expect(screen.getByRole('alert')).toHaveTextContent(
      zhCN.jobDescription.shortError,
    )
  })

  it('shows processing state and then renders all evidence states', async () => {
    renderJourney()
    submitExampleJobDescription()

    expect(screen.getByRole('status')).toHaveTextContent(zhCN.loading.title)

    expect(
      await screen.findByRole('heading', {
        name: '候选人与 AI 产品经理岗位的证据匹配报告',
      }),
    ).toBeInTheDocument()
    expect(
      screen.getAllByText(zhCN.report.status.supported).length,
    ).toBeGreaterThan(1)
    expect(
      screen.getAllByText(zhCN.report.status.partial).length,
    ).toBeGreaterThan(1)
    expect(
      screen.getAllByText(zhCN.report.status.missing).length,
    ).toBeGreaterThan(1)
    expect(screen.getByText(zhCN.report.mockNoticeBody)).toBeInTheDocument()
  })

  it('keeps the submitted input after failure and recovers on retry', async () => {
    renderJourney({ failFirstRequest: true })
    submitExampleJobDescription()

    expect(
      await screen.findByRole('heading', { name: zhCN.failure.title }),
    ).toBeInTheDocument()
    expect(screen.getByLabelText(zhCN.jobDescription.label)).toHaveValue(
      zhCN.sampleJobDescription,
    )

    fireEvent.click(screen.getByRole('button', { name: zhCN.failure.retry }))

    expect(
      await screen.findByRole('heading', {
        name: '候选人与 AI 产品经理岗位的证据匹配报告',
      }),
    ).toBeInTheDocument()
  })

  it('returns to the initial state for a new job description', async () => {
    window.scrollTo = vi.fn()
    renderJourney()
    submitExampleJobDescription()

    await screen.findByRole('heading', {
      name: '候选人与 AI 产品经理岗位的证据匹配报告',
    })
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.report.startOver }),
    )

    expect(screen.getByLabelText(zhCN.jobDescription.label)).toHaveValue('')
    expect(
      screen.getByRole('button', { name: zhCN.jobDescription.submit }),
    ).toBeEnabled()
    expect(
      screen.queryByRole('heading', {
        name: '候选人与 AI 产品经理岗位的证据匹配报告',
      }),
    ).not.toBeInTheDocument()
  })
})
