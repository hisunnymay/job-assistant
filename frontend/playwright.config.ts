import { defineConfig } from '@playwright/test'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const frontendDirectory = path.dirname(fileURLToPath(import.meta.url))
const backendDirectory = path.resolve(frontendDirectory, '../backend')
const frontendUrl = 'http://127.0.0.1:5174'
const backendUrl = 'http://127.0.0.1:8010'
const databaseUrl =
  'postgresql+psycopg://job_assistant:job_assistant@127.0.0.1:55432/job_assistant'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  timeout: 30_000,
  expect: { timeout: 8_000 },
  reporter: 'list',
  use: {
    baseURL: frontendUrl,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command:
        'uv run python -m app.db.init_db && uv run uvicorn app.main:app --host 127.0.0.1 --port 8010',
      cwd: backendDirectory,
      env: {
        APP_ENV: 'test',
        DATABASE_URL: databaseUrl,
        FRONTEND_ORIGIN: frontendUrl,
      },
      url: `${backendUrl}/health`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 5174',
      cwd: frontendDirectory,
      env: { VITE_API_BASE_URL: backendUrl },
      url: frontendUrl,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
  projects: [
    {
      name: 'desktop-chromium',
      testIgnore: /compact\.spec\.ts/,
      use: {
        browserName: 'chromium',
        viewport: { width: 1536, height: 1024 },
      },
    },
    {
      name: 'compact-chromium',
      testMatch: /compact\.spec\.ts/,
      use: {
        browserName: 'chromium',
        viewport: { width: 390, height: 844 },
      },
    },
  ],
})
