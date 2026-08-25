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

describe('conversation matching journey', () => {
  it('renders initial guidance as an assistant message above the JD composer', () => {
    renderJourney()

    expect(
      screen.getByRole('heading', { level: 1, name: zhCN.hero.title }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.initialMessageLabel}`,
      }),
    ).toHaveTextContent(zhCN.guidance.title)
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

  it('keeps the JD and loading state in one message timeline', () => {
    renderJourney()
    submitExampleJobDescription()

    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.jobDescriptionMessageLabel}`,
      }),
    ).toHaveTextContent(zhCN.sampleJobDescription)
    expect(
      screen.getByRole('status', {
        name: `${zhCN.conversation.assistantName}：${zhCN.loading.title}`,
      }),
    ).toHaveTextContent(zhCN.loading.description)
    expect(
      screen.queryByLabelText(zhCN.jobDescription.label),
    ).not.toBeInTheDocument()
  })

  it('renders Markdown analysis as an assistant message with all evidence states', async () => {
    renderJourney()
    submitExampleJobDescription()

    const analysisMessage = await screen.findByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    })

    expect(analysisMessage).toHaveTextContent('有明确证据')
    expect(analysisMessage).toHaveTextContent('部分信息')
    expect(analysisMessage).toHaveTextContent('信息缺失')
    expect(analysisMessage).toHaveTextContent('简历证据')
    expect(screen.getByText(zhCN.report.mockNoticeBody)).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: zhCN.report.startOver }),
    ).toBeEnabled()
  })

  it('keeps the submitted JD visible after failure and recovers in place', async () => {
    renderJourney({ failFirstRequest: true })
    submitExampleJobDescription()

    expect(
      await screen.findByRole('alert', {
        name: `${zhCN.conversation.assistantName}：${zhCN.failure.title}`,
      }),
    ).toHaveTextContent(zhCN.failure.description)
    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.jobDescriptionMessageLabel}`,
      }),
    ).toHaveTextContent(zhCN.sampleJobDescription)

    fireEvent.click(screen.getByRole('button', { name: zhCN.failure.retry }))

    expect(
      await screen.findByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('alert', {
        name: `${zhCN.conversation.assistantName}：${zhCN.failure.title}`,
      }),
    ).not.toBeInTheDocument()
  })

  it('starts a new conversation without retaining previous messages', async () => {
    window.scrollTo = vi.fn()
    renderJourney()
    submitExampleJobDescription()

    await screen.findByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    })
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.report.startOver }),
    )

    expect(screen.getByLabelText(zhCN.jobDescription.label)).toHaveValue('')
    expect(
      screen.queryByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.jobDescriptionMessageLabel}`,
      }),
    ).not.toBeInTheDocument()
    expect(
      screen.queryByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).not.toBeInTheDocument()
    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.initialMessageLabel}`,
      }),
    ).toBeInTheDocument()
  })
})
