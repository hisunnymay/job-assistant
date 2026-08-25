import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { App } from './App'
import { zhCN } from './content/zh-CN'

describe('App', () => {
  it('renders the localized project scaffold', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', { level: 1, name: zhCN.appName }),
    ).toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent(zhCN.scaffoldStatus)
  })
})
