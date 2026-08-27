import { act, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { zhCN } from '../content/zh-CN'
import { LoadingStatus } from './LoadingStatus'

describe('LoadingStatus', () => {
  afterEach(() => {
    vi.useRealTimers()
  })

  it('shows actual elapsed seconds and extended guidance without fake progress', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-08-27T00:00:00Z'))
    const { unmount } = render(<LoadingStatus title={zhCN.loading.title} />)

    expect(screen.getByText(zhCN.loading.typicalDuration)).toBeInTheDocument()
    expect(screen.getByText(zhCN.loading.elapsed(0))).toBeInTheDocument()
    expect(screen.queryByText(zhCN.loading.extendedWait)).not.toBeInTheDocument()
    expect(document.body.textContent).not.toMatch(/%|百分比/)

    act(() => {
      vi.advanceTimersByTime(61_000)
    })

    expect(screen.getByText(zhCN.loading.elapsed(61))).toBeInTheDocument()
    expect(screen.getByText(zhCN.loading.extendedWait)).toBeInTheDocument()

    unmount()
    expect(vi.getTimerCount()).toBe(0)
  })
})
