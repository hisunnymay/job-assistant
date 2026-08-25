import { describe, expect, it } from 'vitest'
import { appConfig } from './env'

describe('appConfig', () => {
  it('provides a safe local API URL by default', () => {
    expect(appConfig.apiBaseUrl).toBe('http://localhost:8000')
  })
})
