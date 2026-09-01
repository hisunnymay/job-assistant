import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { zhCN } from '../content/zh-CN'
import type { DashboardAggregate, DashboardClient } from '../types/dashboard'
import { DashboardPanel } from './DashboardPanel'

const defaultRangeAggregate: DashboardAggregate = {
  reportingPeriod: {
    mode: 'custom',
    startDate: '2026-09-01',
    endDate: '2026-09-03',
    timezone: 'Asia/Shanghai',
  },
  updatedAt: '2026-09-01T02:00:00.000Z',
  contactConversion: { rate: 0.423, numerator: 128, denominator: 303 },
  eventTotals: {
    pageVisits: 12845,
    jobDescriptionSubmissions: 1203,
    matchingReportsGenerated: 303,
    resumePreviews: 1874,
    contactCtaClicks: 128,
    feedbackSubmissions: 56,
  },
}

const allRetainedAggregate: DashboardAggregate = {
  ...defaultRangeAggregate,
  reportingPeriod: {
    mode: 'all_retained',
    startDate: null,
    endDate: null,
    timezone: 'Asia/Shanghai',
  },
}

describe('data dashboard panel', () => {
  beforeEach(() => {
    vi.spyOn(Date, 'now').mockReturnValue(
      Date.parse('2026-09-02T16:30:00.000Z'),
    )
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the primary conversion and six backend-provided totals', async () => {
    const getAggregate = vi.fn().mockResolvedValue(defaultRangeAggregate)
    render(<DashboardPanel client={{ getAggregate }} />)

    expect(await screen.findByText('42.3%')).toBeInTheDocument()
    expect(screen.getByText('128 / 303')).toBeInTheDocument()
    expect(screen.getByText('12,845')).toBeInTheDocument()
    expect(screen.getByText('1,203')).toBeInTheDocument()
    expect(screen.getByText('1,874')).toBeInTheDocument()
    expect(screen.getByText('简历预览会话数')).toBeInTheDocument()
    expect(screen.getByText('联系 CTA 会话数')).toBeInTheDocument()
    expect(screen.getByText('查看过简历的会话数，同一会话仅计一次。')).toBeInTheDocument()
    expect(
      screen.getByText('点击过联系入口的会话数，同一会话仅计一次。'),
    ).toBeInTheDocument()
    expect(document.querySelectorAll('.metric-grid .metric-icon svg')).toHaveLength(
      6,
    )
    expect(document.querySelectorAll('.conversion-visual svg')).toHaveLength(2)
    expect(document.querySelector('.metric-grid .metric-icon')).toHaveTextContent('')
    expect(
      screen.getByText('2026-09-01 至 2026-09-03（含首尾日期）'),
    ).toBeInTheDocument()
    expect(screen.getByText('Asia/Shanghai')).toBeInTheDocument()
    expect(screen.queryByText('产品使用概览')).not.toBeInTheDocument()
    expect(screen.getByLabelText(zhCN.dashboard.startDate)).toHaveValue(
      '2026-09-01',
    )
    expect(screen.getByLabelText(zhCN.dashboard.endDate)).toHaveValue(
      '2026-09-03',
    )
    expect(getAggregate).toHaveBeenCalledWith({
      startDate: '2026-09-01',
      endDate: '2026-09-03',
    })
  })

  it('applies one inclusive date pair and updates every metric together', async () => {
    const customAggregate: DashboardAggregate = {
      ...allRetainedAggregate,
      reportingPeriod: {
        mode: 'custom',
        startDate: '2026-08-01',
        endDate: '2026-08-31',
        timezone: 'Asia/Shanghai',
      },
      contactConversion: { rate: null, numerator: 0, denominator: 0 },
      eventTotals: {
        pageVisits: 2,
        jobDescriptionSubmissions: 0,
        matchingReportsGenerated: 0,
        resumePreviews: 0,
        contactCtaClicks: 0,
        feedbackSubmissions: 0,
      },
    }
    const getAggregate = vi
      .fn<DashboardClient['getAggregate']>()
      .mockResolvedValueOnce(defaultRangeAggregate)
      .mockResolvedValueOnce(customAggregate)
    render(<DashboardPanel client={{ getAggregate }} />)
    await screen.findByText('42.3%')

    fireEvent.change(screen.getByLabelText(zhCN.dashboard.startDate), {
      target: { value: '2026-08-01' },
    })
    fireEvent.change(screen.getByLabelText(zhCN.dashboard.endDate), {
      target: { value: '2026-08-31' },
    })
    fireEvent.click(screen.getByRole('button', { name: zhCN.dashboard.apply }))

    expect(await screen.findByText(zhCN.dashboard.unavailableRate)).toBeInTheDocument()
    expect(getAggregate).toHaveBeenLastCalledWith({
      startDate: '2026-08-01',
      endDate: '2026-08-31',
    })
    expect(
      screen.getByText('2026-08-01 至 2026-08-31（含首尾日期）'),
    ).toBeInTheDocument()
  })

  it('blocks invalid ranges and preserves the last valid result after retrieval failure', async () => {
    const getAggregate = vi
      .fn<DashboardClient['getAggregate']>()
      .mockResolvedValueOnce(defaultRangeAggregate)
      .mockRejectedValueOnce(new Error('backend unavailable'))
      .mockResolvedValueOnce(allRetainedAggregate)
    render(<DashboardPanel client={{ getAggregate }} />)
    await screen.findByText('42.3%')

    fireEvent.change(screen.getByLabelText(zhCN.dashboard.startDate), {
      target: { value: '2026-09-02' },
    })
    fireEvent.change(screen.getByLabelText(zhCN.dashboard.endDate), {
      target: { value: '2026-09-01' },
    })
    fireEvent.click(screen.getByRole('button', { name: zhCN.dashboard.apply }))
    expect(screen.getByRole('alert')).toHaveTextContent(
      zhCN.dashboard.invalidRangeError,
    )
    expect(getAggregate).toHaveBeenCalledTimes(1)
    expect(screen.getByText('12,845')).toBeInTheDocument()

    fireEvent.change(screen.getByLabelText(zhCN.dashboard.startDate), {
      target: { value: '2026-08-01' },
    })
    fireEvent.click(screen.getByRole('button', { name: zhCN.dashboard.apply }))
    expect(await screen.findByText(zhCN.dashboard.retrievalError)).toBeInTheDocument()
    expect(screen.getByText('12,845')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: zhCN.dashboard.retry }))
    await waitFor(() => expect(getAggregate).toHaveBeenCalledTimes(3))
  })
})
