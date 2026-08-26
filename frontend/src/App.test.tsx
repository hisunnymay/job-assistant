import { fireEvent, render, screen, within } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { App } from './App'
import { zhCN } from './content/zh-CN'
import {
  AnalysisClientError,
  createAnalysisClient,
} from './services/analysisClient'
import { FeedbackClientError } from './services/feedbackClient'
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

async function openCompletedAnalysis() {
  submitExampleJobDescription()
  return screen.findByRole('article', {
    name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
  })
}

describe('Goal 4 recruiter workspace', () => {
  beforeEach(() => {
    window.history.replaceState({}, '', '/')
  })

  it('starts on a standalone entrance with the approved JD composer behavior', () => {
    renderJourney()

    expect(
      screen.getByRole('heading', { level: 1, name: zhCN.hero.title }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('navigation', { name: zhCN.navigation.ariaLabel }),
    ).not.toBeInTheDocument()

    const input = screen.getByLabelText(zhCN.jobDescription.label)
    const submit = screen.getByRole('button', {
      name: zhCN.jobDescription.submit,
    })
    expect(input).toHaveAttribute('maxlength', '6000')
    expect(input).toHaveValue('')
    expect(submit).toBeDisabled()
    expect(screen.getByText('0 / 6000 字符')).toBeInTheDocument()

    fireEvent.change(input, { target: { value: '只写了很短的职位要求' } })
    expect(screen.getByRole('alert')).toHaveTextContent(
      zhCN.jobDescription.shortError,
    )
    expect(submit).toBeDisabled()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.jobDescription.useExample }),
    )
    expect(input).toHaveValue(zhCN.sampleJobDescription)
    expect(submit).toBeEnabled()
  })

  it('supports direct résumé entry and workspace replacement navigation', () => {
    window.history.replaceState({}, '', '/#resume')
    renderJourney()

    expect(
      screen.getByRole('heading', { name: zhCN.resume.title }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: zhCN.navigation.resume }),
    ).toHaveAttribute('aria-current', 'page')

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.contact }),
    )
    expect(
      screen.getByRole('heading', { name: zhCN.contact.title }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('heading', { name: zhCN.resume.title }),
    ).not.toBeInTheDocument()
  })

  it('moves a valid JD into the three-item workspace and keeps loading in context', () => {
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
      screen.getByRole('navigation', { name: zhCN.navigation.ariaLabel }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: zhCN.navigation.assistant }),
    ).toHaveAttribute('aria-current', 'page')
    expect(
      screen.queryByRole('button', { name: zhCN.navigation.home }),
    ).toBeInTheDocument()
  })

  it('renders backend Markdown without a frontend-owned analysis schema', async () => {
    renderJourney()
    const analysisMessage = await openCompletedAnalysis()

    expect(analysisMessage).toHaveTextContent('有明确证据')
    expect(analysisMessage).toHaveTextContent('部分信息')
    expect(analysisMessage).toHaveTextContent('信息缺失')
    expect(analysisMessage).toHaveTextContent('简历证据')
    expect(
      within(analysisMessage).getByRole('button', {
        name: zhCN.report.viewResume,
      }),
    ).toHaveAttribute('data-tooltip', zhCN.report.viewResume)
    expect(
      within(analysisMessage).getByRole('button', {
        name: zhCN.report.contactCandidate,
      }),
    ).toHaveAttribute('data-tooltip', zhCN.report.contactCandidate)
    expect(
      within(analysisMessage).getByRole('button', {
        name: zhCN.feedback.helpful,
      }),
    ).toHaveAttribute('data-tooltip', zhCN.feedback.helpful)
    expect(
      within(analysisMessage).getByRole('button', {
        name: zhCN.feedback.notHelpful,
      }),
    ).toHaveAttribute('data-tooltip', zhCN.feedback.notHelpful)
    expect(screen.getByLabelText(zhCN.followUp.label)).toBeDisabled()
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
  })

  it('restores the standalone editable entrance when the API rejects the JD', async () => {
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
    expect(
      screen.queryByRole('navigation', { name: zhCN.navigation.ariaLabel }),
    ).not.toBeInTheDocument()
    expect(
      screen.queryByRole('button', {
        name: zhCN.navigation.returnToConversation,
      }),
    ).not.toBeInTheDocument()
    expect(screen.getByLabelText(zhCN.jobDescription.label)).toHaveValue(
      zhCN.sampleJobDescription,
    )
  })

  it('renders the matching response returned through the real API client boundary', async () => {
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

  it('preserves the active analysis across Home, résumé, and contact views', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText },
    })
    renderJourney()
    const analysisMessage = await openCompletedAnalysis()

    fireEvent.click(
      within(analysisMessage).getByRole('button', {
        name: zhCN.report.viewResume,
      }),
    )
    expect(screen.getByTitle(zhCN.resume.previewTitle)).toHaveAttribute(
      'src',
      'http://localhost:8000/api/resume',
    )
    expect(
      screen.getByRole('link', { name: zhCN.resume.download }),
    ).toHaveAttribute('href', 'http://localhost:8000/api/resume?download=true')

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.contact }),
    )
    fireEvent.click(screen.getByRole('button', { name: zhCN.contact.copyEmail }))
    expect(writeText).toHaveBeenCalledWith(zhCN.contact.email)

    fireEvent.change(screen.getByLabelText(zhCN.contact.recruiterNameLabel), {
      target: { value: '张经理' },
    })
    expect(screen.getByLabelText(zhCN.contact.greetingLabel)).toHaveTextContent(
      '您好梅唱，我是张经理。',
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.contact.copyGreeting }),
    )
    expect(writeText).toHaveBeenLastCalledWith(
      expect.stringContaining('您好梅唱，我是张经理。'),
    )
    expect(screen.getByText(zhCN.contact.noAutoSend)).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: zhCN.navigation.home }))
    expect(
      screen.queryByRole('navigation', { name: zhCN.navigation.ariaLabel }),
    ).not.toBeInTheDocument()
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.returnToConversation }),
    )
    expect(
      await screen.findByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).toBeInTheDocument()
  })

  it('maps Helpful to rating 5 and locks duplicate feedback', async () => {
    const submit = vi.fn().mockResolvedValue(undefined)
    const analysisClient = createMockAnalysisClient({ delayMs: 0 })
    render(<App analysisClient={analysisClient} feedbackClient={{ submit }} />)
    await openCompletedAnalysis()

    expect(
      screen.queryByRole('dialog', {
        name: zhCN.feedback.dialogTitle(5),
      }),
    ).not.toBeInTheDocument()
    const helpful = screen.getByRole('button', { name: zhCN.feedback.helpful })
    fireEvent.click(helpful)
    expect(
      screen.getByRole('dialog', {
        name: zhCN.feedback.dialogTitle(5),
      }),
    ).toBeInTheDocument()
    const submitFeedback = screen.getByRole('button', {
      name: zhCN.feedback.submit,
    })
    expect(submitFeedback).toBeDisabled()
    expect(
      screen.getByText(zhCN.feedback.contributionRequired),
    ).toBeInTheDocument()
    const helpfulOption = screen.getByRole('button', {
      name: `+ ${zhCN.feedback.predefinedOptions(5)[0]}`,
    })
    fireEvent.click(helpfulOption)
    expect(helpfulOption).toHaveAttribute('aria-pressed', 'true')
    fireEvent.click(
      screen.getByRole('button', { name: '+ 信息缺口标注清楚' }),
    )
    expect(submitFeedback).toBeEnabled()
    fireEvent.change(screen.getByLabelText(zhCN.feedback.commentLabel), {
      target: { value: '证据结构清楚。' },
    })
    fireEvent.click(submitFeedback)

    expect(
      await screen.findByText(zhCN.feedback.successDescription),
    ).toBeInTheDocument()
    expect(submit).toHaveBeenCalledOnce()
    expect(submit).toHaveBeenCalledWith({
      conversationId: 'conversation_mock_001',
      messageId: 'message_mock_002',
      rating: 5,
      comment:
        '选择项：证据清晰可核验；信息缺口标注清楚\n补充：证据结构清楚。',
    })
    expect(helpful).toHaveAttribute('aria-pressed', 'true')
    expect(helpful).toBeDisabled()
    expect(
      screen.getByRole('button', { name: zhCN.feedback.notHelpful }),
    ).toBeDisabled()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.resume }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.assistant }),
    )
    expect(
      screen.getByRole('button', { name: zhCN.feedback.helpful }),
    ).toBeDisabled()
    expect(submit).toHaveBeenCalledOnce()
  })

  it('maps Not Helpful to rating 1', async () => {
    const submit = vi.fn().mockResolvedValue(undefined)
    const analysisClient = createMockAnalysisClient({ delayMs: 0 })
    render(<App analysisClient={analysisClient} feedbackClient={{ submit }} />)
    await openCompletedAnalysis()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.feedback.notHelpful }),
    )
    expect(
      screen.getByRole('dialog', {
        name: zhCN.feedback.dialogTitle(1),
      }),
    ).toBeInTheDocument()
    const submitFeedback = screen.getByRole('button', {
      name: zhCN.feedback.submit,
    })
    expect(submitFeedback).toBeDisabled()
    fireEvent.click(
      screen.getByRole('button', { name: '+ 遗漏关键岗位要求' }),
    )
    expect(submitFeedback).toBeEnabled()
    fireEvent.click(submitFeedback)

    await screen.findByText(zhCN.feedback.successDescription)
    expect(submit).toHaveBeenCalledWith({
      conversationId: 'conversation_mock_001',
      messageId: 'message_mock_002',
      rating: 1,
      comment: '选择项：遗漏关键岗位要求',
    })
  })

  it('accepts custom feedback but rejects whitespace-only input', async () => {
    const submit = vi.fn().mockResolvedValue(undefined)
    const analysisClient = createMockAnalysisClient({ delayMs: 0 })
    render(<App analysisClient={analysisClient} feedbackClient={{ submit }} />)
    await openCompletedAnalysis()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.feedback.notHelpful }),
    )
    const submitFeedback = screen.getByRole('button', {
      name: zhCN.feedback.submit,
    })
    const comment = screen.getByLabelText(zhCN.feedback.commentLabel)

    fireEvent.change(comment, { target: { value: '   ' } })
    expect(submitFeedback).toBeDisabled()

    fireEvent.change(comment, { target: { value: '需要更明确地对应岗位要求。' } })
    expect(submitFeedback).toBeEnabled()
    fireEvent.click(submitFeedback)

    await screen.findByText(zhCN.feedback.successDescription)
    expect(submit).toHaveBeenCalledWith({
      conversationId: 'conversation_mock_001',
      messageId: 'message_mock_002',
      rating: 1,
      comment: '补充：需要更明确地对应岗位要求。',
    })
  })

  it('shows a recoverable inline error when feedback cannot be stored', async () => {
    const submit = vi.fn().mockRejectedValue(
      new FeedbackClientError(
        'PERSISTENCE_ERROR',
        '反馈暂时无法保存，请稍后重试。',
        500,
      ),
    )
    const analysisClient = createMockAnalysisClient({ delayMs: 0 })
    render(<App analysisClient={analysisClient} feedbackClient={{ submit }} />)
    await openCompletedAnalysis()

    const helpful = screen.getByRole('button', { name: zhCN.feedback.helpful })
    fireEvent.click(helpful)
    fireEvent.click(
      screen.getByRole('button', { name: '+ 证据清晰可核验' }),
    )
    fireEvent.click(screen.getByRole('button', { name: zhCN.feedback.submit }))

    expect(await screen.findByText(zhCN.feedback.submitError)).toBeInTheDocument()
    expect(helpful).toBeEnabled()
  })
})
