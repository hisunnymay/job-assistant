import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { App } from './App'
import { zhCN } from './content/zh-CN'
import {
  AnalysisClientError,
  createAnalysisClient,
} from './services/analysisClient'
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

  it('restores an editable composer when the backend rejects the request', async () => {
    const analyze = vi
      .fn()
      .mockRejectedValueOnce(
        new AnalysisClientError(
          'INVALID_REQUEST',
          '请求格式无效，请检查职位描述。',
          400,
        ),
      )
      .mockResolvedValueOnce({
        conversationId: 'conversation_corrected_001',
        messageId: 'message_corrected_002',
        content: '# 修改后生成的匹配分析',
      })
    render(<App analysisClient={{ analyze }} />)
    submitExampleJobDescription()

    expect(await screen.findByRole('alert')).toHaveTextContent(
      zhCN.failure.invalidRequest,
    )
    expect(screen.getByLabelText(zhCN.jobDescription.label)).toHaveValue(
      zhCN.sampleJobDescription,
    )
    expect(
      screen.queryByRole('button', { name: zhCN.failure.retry }),
    ).not.toBeInTheDocument()

    const correctedJobDescription = `${zhCN.sampleJobDescription} 补充岗位工作地点为北京。`
    fireEvent.change(screen.getByLabelText(zhCN.jobDescription.label), {
      target: { value: correctedJobDescription },
    })
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.jobDescription.submit }),
    )

    expect(
      await screen.findByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).toHaveTextContent('修改后生成的匹配分析')
    expect(analyze).toHaveBeenLastCalledWith(correctedJobDescription)
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

  it('renders the matching response returned through the backend API client', async () => {
    const fetchImplementation = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          conversationId: 'conversation_backend_001',
          messageId: 'message_backend_002',
          content: '# 后端返回的匹配分析\n\n**证据状态：部分信息**',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    const analysisClient = createAnalysisClient({ fetchImplementation })
    render(<App analysisClient={analysisClient} />)

    submitExampleJobDescription()

    expect(
      await screen.findByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).toHaveTextContent('后端返回的匹配分析')
    expect(fetchImplementation).toHaveBeenCalledOnce()
  })
})
