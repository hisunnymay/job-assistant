import { act, fireEvent, render, screen, within } from '@testing-library/react'
import { StrictMode } from 'react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { App } from './App'
import { zhCN } from './content/zh-CN'
import {
  AnalysisClientError,
  createAnalysisClient,
} from './services/analysisClient'
import { FeedbackClientError } from './services/feedbackClient'
import { FollowUpClientError } from './services/followUpClient'
import { createMockAnalysisClient } from './services/mockAnalysisClient'
import type { FollowUpClient } from './types/followUp'
import type { DashboardClient } from './types/dashboard'
import type { AnalysisClient } from './types/matching'
import type { TrackingClient } from './types/tracking'

function renderJourney(options?: {
  failFirstRequest?: boolean
  followUpClient?: FollowUpClient
  trackingClient?: TrackingClient
  dashboardClient?: DashboardClient
}) {
  const analysisClient = createMockAnalysisClient({
    delayMs: 0,
    failFirstRequest: options?.failFirstRequest,
  })

  render(
    <App
      analysisClient={analysisClient}
      followUpClient={options?.followUpClient}
      trackingClient={options?.trackingClient}
      dashboardClient={options?.dashboardClient}
    />,
  )
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

  afterEach(() => {
    vi.useRealTimers()
  })

  it('starts on a standalone entrance with the approved JD composer behavior', () => {
    renderJourney()

    expect(
      screen.getByRole('heading', { level: 1, name: zhCN.hero.title }),
    ).toBeInTheDocument()
    expect(screen.getByText(zhCN.developerCredit)).toBeInTheDocument()
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
    expect(
      screen.getByRole('button', {
        name: zhCN.jobDescription.viewExampleReport,
      }),
    ).toBeEnabled()

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

  it('opens the checked example instantly without provider, persistence, feedback, follow-up, or generated-report tracking', () => {
    const analyze = vi.fn<AnalysisClient['analyze']>()
    const ask = vi.fn<FollowUpClient['ask']>()
    const track = vi.fn()
    render(
      <App
        analysisClient={{ analyze }}
        followUpClient={{ ask }}
        trackingClient={{ track }}
      />,
    )

    fireEvent.click(
      screen.getByRole('button', {
        name: zhCN.jobDescription.viewExampleReport,
      }),
    )

    const report = screen.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    })
    expect(report).toHaveTextContent(zhCN.report.exampleModeLabel)
    expect(report).toHaveTextContent('产品上线后的量化业务结果')
    expect(
      screen.getByRole('region', { name: zhCN.conversation.title }),
    ).toHaveAttribute('data-conversation-mode', 'example')
    expect(
      screen.getByRole('region', { name: zhCN.conversation.title }),
    ).not.toHaveAttribute('data-conversation-id')
    expect(screen.queryByLabelText(zhCN.followUp.label)).not.toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: zhCN.report.exampleFollowUpTitle }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('button', { name: zhCN.feedback.helpful }),
    ).not.toBeInTheDocument()
    expect(analyze).not.toHaveBeenCalled()
    expect(ask).not.toHaveBeenCalled()
    expect(track.mock.calls).toEqual([['page_visit', undefined]])

    fireEvent.click(
      screen.getByRole('button', {
        name: zhCN.report.submitOwnJobDescription,
      }),
    )
    expect(
      screen.getByRole('heading', { level: 1, name: zhCN.hero.title }),
    ).toBeInTheDocument()
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
    expect(screen.getByText(zhCN.developerCredit)).toBeInTheDocument()
    const candidateContext = screen.getByRole('region', {
      name: zhCN.candidateContext.ariaLabel,
    })
    expect(candidateContext).toHaveTextContent(
      `${zhCN.candidateContext.label}${zhCN.candidateContext.name}`,
    )
    expect(candidateContext).not.toHaveTextContent('固定简历')

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.contact }),
    )
    expect(
      screen.getByRole('heading', { name: zhCN.contact.title }),
    ).toBeInTheDocument()
    expect(
      screen.queryByRole('heading', { name: zhCN.navigation.contact }),
    ).not.toBeInTheDocument()
    expect(
      screen.queryByRole('heading', { name: zhCN.resume.title }),
    ).not.toBeInTheDocument()
  })

  it('opens the dashboard without clearing an active conversation', async () => {
    const getAggregate = vi.fn().mockResolvedValue({
      reportingPeriod: {
        mode: 'all_retained',
        startDate: null,
        endDate: null,
        timezone: 'Asia/Shanghai',
      },
      updatedAt: null,
      contactConversion: { rate: null, numerator: 0, denominator: 0 },
      eventTotals: {
        pageVisits: 0,
        jobDescriptionSubmissions: 0,
        matchingReportsGenerated: 0,
        resumePreviews: 0,
        contactCtaClicks: 0,
        feedbackSubmissions: 0,
      },
    })
    renderJourney({ dashboardClient: { getAggregate } })
    await openCompletedAnalysis()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.dashboard }),
    )
    expect(
      await screen.findByRole('heading', { name: zhCN.dashboard.title }),
    ).toBeInTheDocument()
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.assistant }),
    )

    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).toBeInTheDocument()
  })

  it('activates test mode only after acknowledgement and exits with a normal page visit', async () => {
    let resolveActivation: (() => void) | undefined
    const activateTestMode = vi.fn(
      () =>
        new Promise<void>((resolve) => {
          resolveActivation = resolve
        }),
    )
    const exitTestMode = vi.fn()
    const track = vi.fn()
    renderJourney({
      trackingClient: {
        track,
        isTestModeActive: () => false,
        activateTestMode,
        exitTestMode,
      },
    })

    const trigger = screen.getByRole('button', {
      name: zhCN.testMode.triggerLabel,
    })
    fireEvent.click(trigger)
    fireEvent.click(trigger)
    fireEvent.click(trigger)
    expect(activateTestMode).toHaveBeenCalledOnce()
    expect(screen.queryByText(zhCN.testMode.activeLabel)).not.toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent(
      zhCN.testMode.activating,
    )

    resolveActivation?.()
    expect(await screen.findByText(zhCN.testMode.activeLabel)).toBeInTheDocument()
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.testMode.exit }),
    )

    expect(exitTestMode).toHaveBeenCalledOnce()
    expect(screen.queryByText(zhCN.testMode.activeLabel)).not.toBeInTheDocument()
    expect(track.mock.calls).toEqual([
      ['page_visit', undefined],
      ['page_visit', undefined],
    ])
  })

  it('keeps the test label hidden when designation fails', async () => {
    renderJourney({
      trackingClient: {
        track: vi.fn(),
        isTestModeActive: () => false,
        activateTestMode: vi.fn().mockRejectedValue(new Error('failed')),
      },
    })
    const trigger = screen.getByRole('button', {
      name: zhCN.testMode.triggerLabel,
    })

    fireEvent.click(trigger)
    fireEvent.click(trigger)
    fireEvent.click(trigger)

    expect(await screen.findByRole('alert')).toHaveTextContent(
      zhCN.testMode.activationError,
    )
    expect(screen.queryByText(zhCN.testMode.activeLabel)).not.toBeInTheDocument()
  })

  it('resets the hidden activation sequence after two seconds', async () => {
    vi.useFakeTimers()
    const activateTestMode = vi.fn().mockResolvedValue(undefined)
    renderJourney({
      trackingClient: {
        track: vi.fn(),
        isTestModeActive: () => false,
        activateTestMode,
      },
    })
    const trigger = screen.getByRole('button', {
      name: zhCN.testMode.triggerLabel,
    })

    fireEvent.click(trigger)
    fireEvent.click(trigger)
    act(() => vi.advanceTimersByTime(2001))
    fireEvent.click(trigger)
    fireEvent.click(trigger)
    expect(activateTestMode).not.toHaveBeenCalled()

    fireEvent.click(trigger)
    await act(async () => Promise.resolve())
    expect(activateTestMode).toHaveBeenCalledOnce()
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
    ).toHaveTextContent(zhCN.loading.typicalDuration)
    expect(screen.getByText(zhCN.loading.elapsed(0))).toBeInTheDocument()
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
    expect(screen.getByLabelText(zhCN.followUp.label)).toBeEnabled()
    expect(
      screen.getByRole('button', { name: zhCN.followUp.send }),
    ).toBeDisabled()
  })

  it('enables follow-up only after analysis and appends backend Markdown in context', async () => {
    let resolveFollowUp:
      | ((value: { messageId: string; content: string }) => void)
      | undefined
    const ask = vi.fn().mockImplementation(
      () =>
        new Promise<{ messageId: string; content: string }>((resolve) => {
          resolveFollowUp = resolve
        }),
    )
    renderJourney({ followUpClient: { ask } })
    submitExampleJobDescription()

    const followUpInput = screen.getByLabelText(zhCN.followUp.label)
    expect(followUpInput).toBeDisabled()
    expect(followUpInput).toHaveAttribute('maxlength', '1000')

    await screen.findByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    })
    expect(followUpInput).toBeEnabled()
    const send = screen.getByRole('button', { name: zhCN.followUp.send })
    expect(send).toBeDisabled()

    fireEvent.change(followUpInput, { target: { value: '   ' } })
    expect(send).toBeDisabled()
    expect(ask).not.toHaveBeenCalled()

    fireEvent.change(followUpInput, {
      target: { value: '  候选人有哪些 AI 产品经验？  ' },
    })
    expect(send).toBeEnabled()
    fireEvent.click(send)

    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.followUpQuestionMessageLabel}`,
      }),
    ).toHaveTextContent('候选人有哪些 AI 产品经验？')
    expect(
      screen.getByRole('status', {
        name: `${zhCN.conversation.assistantName}：${zhCN.followUp.loadingTitle}`,
      }),
    ).not.toHaveTextContent(zhCN.loading.typicalDuration)
    expect(screen.getByText(zhCN.loading.elapsed(0))).toBeInTheDocument()
    expect(followUpInput).toBeDisabled()
    expect(ask).toHaveBeenCalledOnce()
    expect(ask).toHaveBeenCalledWith(
      'conversation_mock_001',
      '候选人有哪些 AI 产品经验？',
    )

    resolveFollowUp?.({
      messageId: 'message_follow_up_001',
      content: '# 后端边界回答\n\n**只渲染后端内容**',
    })

    expect(
      await screen.findByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.followUpAnswerMessageLabel}`,
      }),
    ).toHaveTextContent('只渲染后端内容')
    expect(followUpInput).toBeEnabled()
  })

  it('keeps a failed question visible and retries without duplicating it', async () => {
    const ask = vi
      .fn()
      .mockRejectedValueOnce(
        new FollowUpClientError(
          'AI_SERVICE_UNAVAILABLE',
          'raw backend detail',
          503,
        ),
      )
      .mockResolvedValueOnce({
        messageId: 'message_follow_up_retry',
        content: '# 重试后的回答',
      })
    renderJourney({ followUpClient: { ask } })
    await openCompletedAnalysis()

    fireEvent.change(screen.getByLabelText(zhCN.followUp.label), {
      target: { value: '候选人的 API 协作经验是什么？' },
    })
    fireEvent.click(screen.getByRole('button', { name: zhCN.followUp.send }))

    const failure = await screen.findByRole('alert', {
      name: `${zhCN.conversation.assistantName}：${zhCN.followUp.failureTitle}`,
    })
    expect(failure).toHaveTextContent(zhCN.followUp.aiUnavailable)
    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
      }),
    ).toBeInTheDocument()
    expect(
      screen.getAllByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.followUpQuestionMessageLabel}`,
      }),
    ).toHaveLength(1)

    fireEvent.click(
      within(failure).getByRole('button', { name: zhCN.followUp.retry }),
    )

    expect(
      await screen.findByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.followUpAnswerMessageLabel}`,
      }),
    ).toHaveTextContent('重试后的回答')
    expect(
      screen.getAllByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.followUpQuestionMessageLabel}`,
      }),
    ).toHaveLength(1)
    expect(ask).toHaveBeenCalledTimes(2)
    expect(ask.mock.calls[0]).toEqual(ask.mock.calls[1])
  })

  it('preserves matching elapsed time when leaving and returning to an active request', async () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-08-27T00:00:00Z'))
    let resolveAnalysis:
      | ((value: {
          conversationId: string
          messageId: string
          content: string
        }) => void)
      | undefined
    const analyze = vi.fn(
      () =>
        new Promise<{
          conversationId: string
          messageId: string
          content: string
        }>((resolve) => {
          resolveAnalysis = resolve
        }),
    )
    render(<App analysisClient={{ analyze }} trackingClient={{ track: vi.fn() }} />)
    submitExampleJobDescription()

    act(() => {
      vi.advanceTimersByTime(5_000)
    })
    expect(screen.getByText(zhCN.loading.elapsed(5))).toBeInTheDocument()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.resume }),
    )
    expect(screen.queryByText(zhCN.loading.elapsed(5))).not.toBeInTheDocument()
    expect(vi.getTimerCount()).toBe(0)

    act(() => {
      vi.advanceTimersByTime(4_000)
    })

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.assistant }),
    )
    expect(screen.getByText(zhCN.loading.elapsed(9))).toBeInTheDocument()

    await act(async () => {
      resolveAnalysis?.({
        conversationId: 'conversation_timer',
        messageId: 'message_timer',
        content: '# 完成',
      })
    })
    expect(screen.queryByRole('status')).not.toBeInTheDocument()
    expect(vi.getTimerCount()).toBe(0)
    vi.useRealTimers()
  })

  it('prevents concurrent follow-ups and preserves multiple turns in order', async () => {
    let resolveFirst:
      | ((value: { messageId: string; content: string }) => void)
      | undefined
    const ask = vi
      .fn()
      .mockImplementationOnce(
        () =>
          new Promise<{ messageId: string; content: string }>((resolve) => {
            resolveFirst = resolve
          }),
      )
      .mockResolvedValueOnce({
        messageId: 'message_answer_002',
        content: '# 第二个回答',
      })
    renderJourney({ followUpClient: { ask } })
    await openCompletedAnalysis()

    const input = screen.getByLabelText(zhCN.followUp.label)
    fireEvent.change(input, { target: { value: '第一个候选人经验问题' } })
    fireEvent.click(screen.getByRole('button', { name: zhCN.followUp.send }))
    expect(input).toBeDisabled()
    fireEvent.submit(input.closest('form') as HTMLFormElement)
    expect(ask).toHaveBeenCalledOnce()

    resolveFirst?.({
      messageId: 'message_answer_001',
      content: '# 第一个回答',
    })
    await screen.findByText('第一个回答')

    fireEvent.change(input, { target: { value: '第二个候选人经验问题' } })
    fireEvent.click(screen.getByRole('button', { name: zhCN.followUp.send }))
    await screen.findByText('第二个回答')

    expect(ask).toHaveBeenCalledTimes(2)
    const timeline = screen
      .getAllByRole('article')
      .map((article) => article.getAttribute('data-message-type'))
      .filter(Boolean)
    expect(timeline).toEqual([
      'job_description',
      'matching_analysis',
      'follow_up_question',
      'follow_up_answer',
      'follow_up_question',
      'follow_up_answer',
    ])
  })

  it('preserves follow-up messages across workspace and Home navigation', async () => {
    const ask = vi.fn().mockResolvedValue({
      messageId: 'message_follow_up_preserved',
      content: '# 保留的追问回答',
    })
    renderJourney({ followUpClient: { ask } })
    await openCompletedAnalysis()

    fireEvent.change(screen.getByLabelText(zhCN.followUp.label), {
      target: { value: '候选人有哪些大模型产品经验？' },
    })
    fireEvent.click(screen.getByRole('button', { name: zhCN.followUp.send }))
    await screen.findByText('保留的追问回答')

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.resume }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.contact }),
    )
    fireEvent.click(screen.getByRole('button', { name: zhCN.navigation.home }))
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.returnToConversation }),
    )

    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.userName}：${zhCN.conversation.followUpQuestionMessageLabel}`,
      }),
    ).toHaveTextContent('候选人有哪些大模型产品经验？')
    expect(
      screen.getByRole('article', {
        name: `${zhCN.conversation.assistantName}：${zhCN.conversation.followUpAnswerMessageLabel}`,
      }),
    ).toHaveTextContent('保留的追问回答')
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
      'http://localhost:8000/api/resume?v=30ebd7e42087fe69',
    )
    expect(
      screen.getByRole('link', { name: zhCN.resume.download }),
    ).toHaveAttribute(
      'href',
      'http://localhost:8000/api/resume?v=30ebd7e42087fe69&download=true',
    )

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.contact }),
    )
    expect(screen.getByText(zhCN.contact.email)).toHaveAttribute(
      'href',
      `mailto:${zhCN.contact.email}`,
    )
    expect(screen.getByText(zhCN.contact.phoneLabel)).toBeInTheDocument()
    expect(screen.getByLabelText(zhCN.contact.greetingLabel)).not.toHaveTextContent(
      '—— 招聘负责人',
    )
    fireEvent.click(screen.getByRole('button', { name: zhCN.contact.copyEmail }))
    expect(writeText).toHaveBeenCalledWith(zhCN.contact.email)

    fireEvent.change(screen.getByLabelText(zhCN.contact.recruiterNameLabel), {
      target: { value: '张经理' },
    })
    expect(screen.getByLabelText(zhCN.contact.greetingLabel)).toHaveTextContent(
      '您好梅唱，我是张经理。',
    )
    expect(screen.getByLabelText(zhCN.contact.greetingLabel)).not.toHaveTextContent(
      '——',
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
        '补充：证据结构清楚。\n选择项：证据清晰可核验；信息缺口标注清楚',
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
    expect(
      screen.getByRole('button', { name: '+ 报告生成时间较长' }),
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

  it('keeps the serialized feedback comment within the backend limit', async () => {
    const submit = vi.fn().mockResolvedValue(undefined)
    const analysisClient = createMockAnalysisClient({ delayMs: 0 })
    render(<App analysisClient={analysisClient} feedbackClient={{ submit }} />)
    await openCompletedAnalysis()

    fireEvent.click(
      screen.getByRole('button', { name: zhCN.feedback.helpful }),
    )
    const option = zhCN.feedback.predefinedOptions(5)[0]
    fireEvent.click(screen.getByRole('button', { name: `+ ${option}` }))
    const comment = screen.getByLabelText(zhCN.feedback.commentLabel)
    const customPrefix = zhCN.feedback.customFeedbackPrefix
    const selectedReasons = `${zhCN.feedback.selectedReasonsPrefix}${option}`
    const expectedCustomLimit =
      2000 - customPrefix.length - 1 - selectedReasons.length
    expect(comment).toHaveAttribute('maxlength', String(expectedCustomLimit))

    fireEvent.change(comment, { target: { value: '测'.repeat(2000) } })
    expect(comment).toHaveValue('测'.repeat(expectedCustomLimit))
    fireEvent.click(screen.getByRole('button', { name: zhCN.feedback.submit }))

    await screen.findByText(zhCN.feedback.successDescription)
    const submittedComment = submit.mock.calls[0][0].comment
    expect(submittedComment).toHaveLength(2000)
    expect(submittedComment).toBe(
      `${customPrefix}${'测'.repeat(expectedCustomLimit)}\n${selectedReasons}`,
    )
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

  it('emits every required privacy-safe tracking event at its interaction point', async () => {
    const track = vi.fn()
    const submit = vi.fn().mockResolvedValue(undefined)
    const analysisClient = createMockAnalysisClient({ delayMs: 0 })
    render(
      <App
        analysisClient={analysisClient}
        feedbackClient={{ submit }}
        trackingClient={{ track }}
      />,
    )

    const analysisMessage = await openCompletedAnalysis()
    fireEvent.click(
      within(analysisMessage).getByRole('button', {
        name: zhCN.report.viewResume,
      }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.resume }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.assistant }),
    )
    fireEvent.click(
      within(
        screen.getByRole('article', {
          name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
        }),
      ).getByRole('button', { name: zhCN.report.contactCandidate }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.contact }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.navigation.assistant }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: zhCN.feedback.helpful }),
    )
    fireEvent.click(
      screen.getByRole('button', { name: '+ 证据清晰可核验' }),
    )
    fireEvent.click(screen.getByRole('button', { name: zhCN.feedback.submit }))
    await screen.findByText(zhCN.feedback.successDescription)

    const conversationContext = { conversationId: 'conversation_mock_001' }
    expect(track.mock.calls).toEqual([
      ['page_visit', undefined],
      ['job_description_submitted', undefined],
      ['matching_report_generated', conversationContext],
      ['resume_previewed', conversationContext],
      ['contact_cta_clicked', conversationContext],
      ['feedback_submitted', conversationContext],
    ])
    const serializedEvents = JSON.stringify(track.mock.calls)
    expect(serializedEvents).not.toContain(zhCN.sampleJobDescription)
    expect(serializedEvents).not.toContain('证据清晰可核验')
  })

  it('keeps the recruiter journey usable when tracking throws', async () => {
    const trackingClient: TrackingClient = {
      track() {
        throw new Error('tracking unavailable')
      },
    }
    renderJourney({ trackingClient })

    const analysisMessage = await openCompletedAnalysis()
    expect(analysisMessage).toHaveTextContent('有明确证据')
    fireEvent.click(
      within(analysisMessage).getByRole('button', {
        name: zhCN.report.viewResume,
      }),
    )
    expect(
      screen.getByRole('heading', { name: zhCN.resume.title }),
    ).toBeInTheDocument()
  })

  it('emits one page visit when React Strict Mode repeats effects', () => {
    const track = vi.fn()

    render(
      <StrictMode>
        <App trackingClient={{ track }} />
      </StrictMode>,
    )

    expect(track.mock.calls).toEqual([['page_visit', undefined]])
  })

  it('does not double-count JD submission when analysis retry succeeds', async () => {
    const track = vi.fn()
    renderJourney({ failFirstRequest: true, trackingClient: { track } })
    submitExampleJobDescription()

    await screen.findByRole('alert')
    expect(track).toHaveBeenCalledWith('job_description_submitted', undefined)
    expect(track).not.toHaveBeenCalledWith(
      'matching_report_generated',
      expect.anything(),
    )

    fireEvent.click(screen.getByRole('button', { name: zhCN.failure.retry }))
    await screen.findByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    })

    expect(
      track.mock.calls.filter(
        ([eventName]) => eventName === 'job_description_submitted',
      ),
    ).toHaveLength(1)
    expect(
      track.mock.calls.filter(
        ([eventName]) => eventName === 'matching_report_generated',
      ),
    ).toEqual([
      [
        'matching_report_generated',
        { conversationId: 'conversation_mock_001' },
      ],
    ])
  })
})
