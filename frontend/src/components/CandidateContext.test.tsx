import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { zhCN } from '../content/zh-CN'
import { CandidateContext } from './CandidateContext'

describe('CandidateContext', () => {
  it('discloses future candidate support and closes with Escape', () => {
    render(<CandidateContext />)

    const infoButton = screen.getByRole('button', {
      name: zhCN.candidateContext.infoButton,
    })
    expect(infoButton.parentElement).toHaveTextContent(
      zhCN.candidateContext.name,
    )
    expect(infoButton).toHaveAttribute('aria-expanded', 'false')

    fireEvent.click(infoButton)
    expect(infoButton).toHaveAttribute('aria-expanded', 'true')
    expect(
      screen.getByRole('region', {
        name: zhCN.candidateContext.hintTitle,
      }),
    ).toHaveTextContent(zhCN.candidateContext.hintBody)

    fireEvent.keyDown(document, { key: 'Escape' })
    expect(infoButton).toHaveAttribute('aria-expanded', 'false')
    expect(infoButton).toHaveFocus()
  })

  it('closes the disclosure after an outside pointer action', () => {
    render(<CandidateContext />)

    fireEvent.click(
      screen.getByRole('button', {
        name: zhCN.candidateContext.infoButton,
      }),
    )
    fireEvent.pointerDown(document.body)

    expect(
      screen.queryByRole('region', {
        name: zhCN.candidateContext.hintTitle,
      }),
    ).not.toBeInTheDocument()
  })
})
