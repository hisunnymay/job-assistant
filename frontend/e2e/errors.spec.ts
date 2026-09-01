import { expect, test } from '@playwright/test'
import { zhCN } from '../src/content/zh-CN'

const backendUrl = process.env.E2E_BACKEND_URL ?? 'http://127.0.0.1:8010'

async function openMatchingReport(page: import('@playwright/test').Page) {
  await page.goto('/')
  await page.getByRole('button', { name: zhCN.jobDescription.useExample }).click()
  await page.getByRole('button', { name: zhCN.jobDescription.submit }).click()
  return page.getByRole('article', {
    name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
  })
}

test('rejects invalid and missing-record API requests with safe errors', async ({
  page,
  request,
}) => {
  await page.goto('/')
  const jobDescription = page.getByLabel(zhCN.jobDescription.label)
  await jobDescription.fill('过短的职位描述')
  await expect(page.getByRole('alert')).toContainText(
    zhCN.jobDescription.shortError,
  )
  await expect(
    page.getByRole('button', { name: zhCN.jobDescription.submit }),
  ).toBeDisabled()

  const invalidAnalysis = await request.post(
    `${backendUrl}/api/matching-analysis`,
    { data: { jobDescription: '仍然过短' } },
  )
  expect(invalidAnalysis.status()).toBe(400)
  expect(await invalidAnalysis.json()).toEqual({
    code: 'INVALID_REQUEST',
    message: '请求格式无效，请检查职位描述。',
  })

  const missingConversation = await request.post(
    `${backendUrl}/api/conversations/conversation_missing/messages`,
    { data: { question: '候选人的产品经验是什么？' } },
  )
  expect(missingConversation.status()).toBe(404)
  const missingBody = await missingConversation.json()
  expect(missingBody).toEqual({
    code: 'CONVERSATION_NOT_FOUND',
    message: '未找到对应的匹配对话，请重新生成匹配报告。',
  })
  expect(JSON.stringify(missingBody)).not.toContain('Traceback')
})

test('shows a safe analysis failure and recovers on retry', async ({ page }) => {
  let failAnalysis = true
  await page.route('**/api/matching-analysis', async (route) => {
    if (failAnalysis) {
      await route.fulfill({
        status: 503,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 'AI_SERVICE_UNAVAILABLE',
          message: 'internal provider detail must stay hidden',
        }),
      })
      return
    }
    await route.continue()
  })

  await page.goto('/')
  await page.getByRole('button', { name: zhCN.jobDescription.useExample }).click()
  await page.getByRole('button', { name: zhCN.jobDescription.submit }).click()
  const failure = page.getByRole('alert', {
    name: `${zhCN.conversation.assistantName}：${zhCN.failure.title}`,
  })
  await expect(failure).toContainText(zhCN.failure.aiUnavailable)
  await expect(failure).not.toContainText('internal provider detail')

  failAnalysis = false
  await failure.getByRole('button', { name: zhCN.failure.retry }).click()
  await expect(
    page.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    }),
  ).toContainText('有明确证据')
})

test('shows truthful elapsed waiting state while analysis is pending', async ({
  page,
}) => {
  let releaseRequest: (() => void) | undefined
  const requestGate = new Promise<void>((resolve) => {
    releaseRequest = resolve
  })
  await page.route('**/api/matching-analysis', async (route) => {
    await requestGate
    await route.continue()
  })

  await page.goto('/')
  await page.getByRole('button', { name: zhCN.jobDescription.useExample }).click()
  await page.getByRole('button', { name: zhCN.jobDescription.submit }).click()

  const loading = page.getByRole('status', {
    name: `${zhCN.conversation.assistantName}：${zhCN.loading.title}`,
  })
  await expect(loading).toContainText(zhCN.loading.typicalDuration)
  await expect(loading).toContainText(zhCN.loading.elapsed(0))
  await expect(loading).not.toContainText('%')
  await expect(loading).not.toContainText(zhCN.loading.extendedWait)
  await page.waitForTimeout(1_100)
  await expect(loading).toContainText(zhCN.loading.elapsed(1))

  await page.getByRole('button', { name: zhCN.navigation.resume }).click()
  await expect(loading).toHaveCount(0)
  await page.waitForTimeout(1_100)
  await page.getByRole('button', { name: zhCN.navigation.assistant }).click()
  await expect(
    page.getByRole('status', {
      name: `${zhCN.conversation.assistantName}：${zhCN.loading.title}`,
    }),
  ).toContainText(/已等待 (?:[2-9]|[1-9]\d+) 秒/)

  releaseRequest?.()
  await expect(
    page.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    }),
  ).toBeVisible()
  await expect(loading).toHaveCount(0)
})

test('keeps feedback recoverable after a storage failure', async ({ page }) => {
  const matchingReport = await openMatchingReport(page)
  await expect(matchingReport).toContainText('有明确证据')

  let failFeedback = true
  await page.route('**/api/feedback', async (route) => {
    if (failFeedback) {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 'PERSISTENCE_ERROR',
          message: 'database driver detail must stay hidden',
        }),
      })
      return
    }
    await route.continue()
  })

  await matchingReport
    .getByRole('button', { name: zhCN.feedback.notHelpful })
    .click()
  await page
    .getByRole('button', { name: `+ ${zhCN.feedback.predefinedOptions(1)[0]}` })
    .click()
  await page.getByRole('button', { name: zhCN.feedback.submit }).click()
  await expect(page.getByRole('alert')).toContainText(zhCN.feedback.submitError)
  await expect(page.getByRole('alert')).not.toContainText('database driver')

  failFeedback = false
  await page.getByRole('button', { name: zhCN.feedback.submit }).click()
  await expect(page.getByText(zhCN.feedback.successDescription)).toBeVisible()
})
