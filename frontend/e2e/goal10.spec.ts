import { expect, test, type APIRequestContext } from '@playwright/test'
import { zhCN } from '../src/content/zh-CN'

const backendUrl = process.env.E2E_BACKEND_URL ?? 'http://127.0.0.1:8010'
const pendingEventsKey = 'ai-job-fit-assistant.tracking-events.v1'
const trackingSessionKey = 'ai-job-fit-assistant.tracking-session.v1'
const defaultDashboardStartDate = '2026-09-01'

function currentShanghaiDate() {
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date())
  const valueByType = Object.fromEntries(
    parts.map((part) => [part.type, part.value]),
  )
  return `${valueByType.year}-${valueByType.month}-${valueByType.day}`
}

async function pageVisitTotal(request: APIRequestContext) {
  const response = await request.get(`${backendUrl}/api/dashboard`)
  expect(response.ok()).toBe(true)
  return ((await response.json()) as { eventTotals: { pageVisits: number } })
    .eventTotals.pageVisits
}

test('excludes the acknowledged test session retroactively and after queued delivery', async ({
  page,
  request,
}) => {
  const baselinePageVisits = await pageVisitTotal(request)
  await page.route('**/api/tracking-events', (route) => route.abort('failed'))
  await page.goto('/')
  await expect
    .poll(() =>
      page.evaluate((storageKey) => {
        const value = window.localStorage.getItem(storageKey)
        return value ? (JSON.parse(value) as unknown[]).length : 0
      }, pendingEventsKey),
    )
    .toBe(1)
  const testSessionId = await page.evaluate(
    (storageKey) => window.sessionStorage.getItem(storageKey),
    trackingSessionKey,
  )

  const trigger = page.getByRole('button', { name: zhCN.testMode.triggerLabel })
  await trigger.click()
  await trigger.click()
  const designation = page.waitForResponse(
    (response) =>
      response.request().method() === 'POST' &&
      response.url().endsWith('/api/tracking-sessions/test-mode'),
  )
  await trigger.click()
  expect((await designation).ok()).toBe(true)
  await expect(
    page.getByText(zhCN.testMode.activeLabel, { exact: true }),
  ).toBeVisible()

  await page.unroute('**/api/tracking-events')
  await page
    .getByRole('button', { name: zhCN.jobDescription.viewExampleReport })
    .click()
  await page.getByRole('button', { name: zhCN.navigation.resume }).click()
  await expect
    .poll(() =>
      page.evaluate((storageKey) => {
        const value = window.localStorage.getItem(storageKey)
        return value ? (JSON.parse(value) as unknown[]).length : 0
      }, pendingEventsKey),
    )
    .toBe(0)
  await expect.poll(() => pageVisitTotal(request)).toBe(baselinePageVisits)

  await page.reload()
  await expect(
    page.getByText(zhCN.testMode.activeLabel, { exact: true }),
  ).toBeVisible()
  await page
    .getByRole('button', { name: zhCN.jobDescription.viewExampleReport })
    .click()
  await page.getByRole('button', { name: zhCN.navigation.dashboard }).click()
  await expect(
    page.getByRole('heading', { name: zhCN.dashboard.title }),
  ).toBeVisible()
  const startDate = page.getByLabel(zhCN.dashboard.startDate)
  const endDate = page.getByLabel(zhCN.dashboard.endDate)
  const today = currentShanghaiDate()
  await expect(startDate).toHaveValue(defaultDashboardStartDate)
  await expect(endDate).toHaveValue(today)
  await expect(
    page.getByText(`${defaultDashboardStartDate} 至 ${today}（含首尾日期）`),
  ).toBeVisible()
  await expect(page.getByText('产品使用概览')).toHaveCount(0)

  await page.getByRole('button', { name: zhCN.testMode.exit }).click()
  await expect(
    page.getByText(zhCN.testMode.activeLabel, { exact: true }),
  ).toHaveCount(0)
  const normalSessionId = await page.evaluate(
    (storageKey) => window.sessionStorage.getItem(storageKey),
    trackingSessionKey,
  )
  expect(normalSessionId).not.toBe(testSessionId)
  await expect
    .poll(() => pageVisitTotal(request))
    .toBe(baselinePageVisits + 1)
})

test('filters the dashboard without losing the active matching conversation', async ({
  page,
}) => {
  await page.goto('/')
  await page.getByRole('button', { name: zhCN.jobDescription.useExample }).click()
  await page.getByRole('button', { name: zhCN.jobDescription.submit }).click()
  await expect(
    page.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    }),
  ).toContainText('有明确证据')

  await page.getByRole('button', { name: zhCN.navigation.dashboard }).click()
  const today = currentShanghaiDate()
  await expect(
    page.getByText(
      `${defaultDashboardStartDate} 至 ${today}（含首尾日期）`,
    ),
  ).toBeVisible()
  const startDate = page.getByLabel(zhCN.dashboard.startDate)
  const endDate = page.getByLabel(zhCN.dashboard.endDate)
  await expect(startDate).toHaveValue(defaultDashboardStartDate)
  await expect(endDate).toHaveValue(today)
  await startDate.fill('2026-09-02')
  await endDate.fill('2026-09-01')
  await page.getByRole('button', { name: zhCN.dashboard.apply }).click()
  await expect(page.getByRole('alert')).toContainText(
    zhCN.dashboard.invalidRangeError,
  )
  await expect(
    page.getByText(
      `${defaultDashboardStartDate} 至 ${today}（含首尾日期）`,
    ),
  ).toBeVisible()

  await startDate.fill('2026-01-01')
  await endDate.fill('2026-12-31')
  await page.getByRole('button', { name: zhCN.dashboard.apply }).click()
  await expect(page.getByText(/2026-01-01 至 2026-12-31/)).toBeVisible()
  await page.getByRole('button', { name: zhCN.dashboard.reset }).click()
  await expect(page.getByText(zhCN.dashboard.allRetainedPeriod)).toBeVisible()

  await page.getByRole('button', { name: zhCN.navigation.assistant }).click()
  await expect(
    page.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    }),
  ).toContainText('有明确证据')
})
