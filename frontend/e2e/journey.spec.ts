import { expect, test, type Request } from '@playwright/test'
import { zhCN } from '../src/content/zh-CN'

const pendingTrackingEventsStorageKey =
  'ai-job-fit-assistant.tracking-events.v1'

const requiredTrackingEvents = [
  'page_visit',
  'job_description_submitted',
  'matching_report_generated',
  'resume_previewed',
  'contact_cta_clicked',
  'feedback_submitted',
] as const

type RequiredTrackingEvent = (typeof requiredTrackingEvents)[number]
type TrackingEventCounts = Record<RequiredTrackingEvent, number>

test('completes the primary recruiter journey through the real backend', async ({
  context,
  page,
}) => {
  const acceptedTrackingEvents: string[] = []
  let matchingAnalysisRequests = 0
  let activeTrackingRequests = 0
  const acceptedCount = (eventName: string) =>
    acceptedTrackingEvents.filter((acceptedEvent) => acceptedEvent === eventName)
      .length
  const acceptedTrackingCounts = (): TrackingEventCounts =>
    Object.fromEntries(
      requiredTrackingEvents.map((eventName) => [
        eventName,
        acceptedCount(eventName),
      ]),
    ) as TrackingEventCounts
  const isTrackingRequest = (request: Request) =>
    request.method() === 'POST' &&
    request.url().endsWith('/api/tracking-events')
  const pendingTrackingEventCount = () =>
    page.evaluate((storageKey) => {
      const storedEvents = window.localStorage.getItem(storageKey)
      if (!storedEvents) {
        return 0
      }

      try {
        const parsedEvents: unknown = JSON.parse(storedEvents)
        return Array.isArray(parsedEvents) ? parsedEvents.length : -1
      } catch {
        return -1
      }
    }, pendingTrackingEventsStorageKey)
  const expectAcceptedTrackingCounts = async (
    expectedCounts: TrackingEventCounts,
  ) => {
    await expect
      .poll(async () => ({
        acceptedCounts: acceptedTrackingCounts(),
        activeTrackingRequests,
        pendingTrackingEvents: await pendingTrackingEventCount(),
      }))
      .toEqual({
        acceptedCounts: expectedCounts,
        activeTrackingRequests: 0,
        pendingTrackingEvents: 0,
      })
  }
  page.on('request', (request) => {
    if (
      request.method() === 'POST' &&
      request.url().endsWith('/api/matching-analysis')
    ) {
      matchingAnalysisRequests += 1
    }
    if (isTrackingRequest(request)) {
      activeTrackingRequests += 1
    }
  })
  const markTrackingRequestFinished = (request: Request) => {
    if (isTrackingRequest(request)) {
      activeTrackingRequests -= 1
    }
  }
  page.on('requestfinished', markTrackingRequestFinished)
  page.on('requestfailed', markTrackingRequestFinished)
  page.on('response', (response) => {
    const request = response.request()
    if (response.ok() && isTrackingRequest(request)) {
      const payload = request.postDataJSON() as { eventName?: string }
      if (payload.eventName) {
        acceptedTrackingEvents.push(payload.eventName)
      }
    }
  })

  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  await page.goto('/')
  await expect(
    page.getByRole('heading', { level: 1, name: zhCN.hero.title }),
  ).toBeVisible()

  await page
    .getByRole('button', { name: zhCN.jobDescription.viewExampleReport })
    .click()
  const exampleReport = page.getByRole('article', {
    name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
  })
  await expect(exampleReport).toContainText(zhCN.report.exampleModeLabel)
  await expect(page.getByLabel(zhCN.followUp.label)).toHaveCount(0)
  await expect(
    page.getByRole('heading', { name: zhCN.report.exampleFollowUpTitle }),
  ).toBeVisible()
  expect(matchingAnalysisRequests).toBe(0)
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 0,
    matching_report_generated: 0,
    resume_previewed: 0,
    contact_cta_clicked: 0,
    feedback_submitted: 0,
  })
  await page
    .getByRole('button', { name: zhCN.report.submitOwnJobDescription })
    .click()

  await page.getByRole('button', { name: zhCN.jobDescription.useExample }).click()
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 0,
    matching_report_generated: 0,
    resume_previewed: 0,
    contact_cta_clicked: 0,
    feedback_submitted: 0,
  })
  await page.getByRole('button', { name: zhCN.jobDescription.submit }).click()
  expect(matchingAnalysisRequests).toBe(1)

  const matchingReport = page.getByRole('article', {
    name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
  })
  await expect(matchingReport).toContainText('有明确证据')
  await expect(matchingReport).toContainText('部分信息')
  await expect(matchingReport).toContainText('信息缺失')
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 0,
    contact_cta_clicked: 0,
    feedback_submitted: 0,
  })
  const followUpInput = page.getByLabel(zhCN.followUp.label)
  await followUpInput.fill('候选人的 AI Agent 经验有哪些？')
  await page.getByRole('button', { name: zhCN.followUp.send }).click()
  await expect(
    page.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.followUpAnswerMessageLabel}`,
    }),
  ).toContainText('AI Agent 相关经验')

  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 0,
    contact_cta_clicked: 0,
    feedback_submitted: 0,
  })
  await matchingReport
    .getByRole('button', { name: zhCN.feedback.helpful })
    .click()
  await page
    .getByRole('button', { name: `+ ${zhCN.feedback.predefinedOptions(5)[0]}` })
    .click()
  await page
    .getByLabel(zhCN.feedback.commentLabel)
    .fill('希望增加岗位要求逐项对照。')
  const feedbackRequestPromise = page.waitForRequest(
    (request) =>
      request.method() === 'POST' && request.url().endsWith('/api/feedback'),
  )
  await page.getByRole('button', { name: zhCN.feedback.submit }).click()
  const feedbackRequest = await feedbackRequestPromise
  expect(feedbackRequest.postDataJSON()).toMatchObject({
    rating: 5,
    comment:
      '补充：希望增加岗位要求逐项对照。\n选择项：证据清晰可核验',
  })
  await expect(page.getByText(zhCN.feedback.successDescription)).toBeVisible()
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 0,
    contact_cta_clicked: 0,
    feedback_submitted: 1,
  })

  await matchingReport
    .getByRole('button', { name: zhCN.report.viewResume })
    .click()
  await expect(page.getByRole('heading', { name: zhCN.resume.title })).toBeVisible()
  await expect(page.getByTitle(zhCN.resume.previewTitle)).toBeVisible()
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 1,
    contact_cta_clicked: 0,
    feedback_submitted: 1,
  })
  const downloadPromise = page.waitForEvent('download')
  await page.getByRole('link', { name: zhCN.resume.download }).click()
  const download = await downloadPromise
  expect(download.suggestedFilename()).toMatch(/\.pdf$/)

  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 1,
    contact_cta_clicked: 0,
    feedback_submitted: 1,
  })
  await page.getByRole('button', { name: zhCN.navigation.contact }).click()
  await expect(page.getByRole('heading', { name: zhCN.contact.title })).toBeVisible()
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 1,
    contact_cta_clicked: 1,
    feedback_submitted: 1,
  })
  await page.getByLabel(zhCN.contact.recruiterNameLabel).fill('张经理')
  await page.getByRole('button', { name: zhCN.contact.copyGreeting }).click()
  await expect(page.getByText(zhCN.contact.copySuccess)).toBeVisible()
  await expect
    .poll(() => page.evaluate(() => navigator.clipboard.readText()))
    .toContain('张经理')
  await expectAcceptedTrackingCounts({
    page_visit: 1,
    job_description_submitted: 1,
    matching_report_generated: 1,
    resume_previewed: 1,
    contact_cta_clicked: 1,
    feedback_submitted: 1,
  })
})
