import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { zhCN } from '../content/zh-CN'
import { ResumePanel } from './ResumePanel'

describe('ResumePanel', () => {
  it('preserves a version query when building a relative download URL', () => {
    render(<ResumePanel resumeUrl="/api/resume?v=current" />)

    expect(screen.getByTitle(zhCN.resume.previewTitle)).toHaveAttribute(
      'src',
      '/api/resume?v=current',
    )
    expect(
      screen.getByRole('link', { name: zhCN.resume.download }),
    ).toHaveAttribute('href', '/api/resume?v=current&download=true')
  })
})
