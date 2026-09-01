import { expect, test } from '@playwright/test'
import { zhCN } from '../src/content/zh-CN'

test('keeps the compact recruiter journey readable and keyboard operable', async ({
  page,
}) => {
  await page.goto('/')
  await page
    .getByRole('button', { name: zhCN.jobDescription.viewExampleReport })
    .click()
  await expect(
    page.getByRole('article', {
      name: `${zhCN.conversation.assistantName}：${zhCN.conversation.matchingAnalysisMessageLabel}`,
    }),
  ).toContainText(zhCN.report.exampleModeLabel)
  await expect(
    page.getByRole('heading', { name: zhCN.report.exampleFollowUpTitle }),
  ).toBeVisible()
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true)

  await page.getByRole('button', { name: zhCN.navigation.resume }).click()
  await expect(page.getByRole('heading', { name: zhCN.resume.title })).toBeVisible()
  await expect(page.getByRole('navigation', { name: zhCN.navigation.ariaLabel })).toBeVisible()
  await expect(page.getByText(zhCN.developerCredit)).toBeVisible()
  const candidateContext = page.getByRole('region', {
    name: zhCN.candidateContext.ariaLabel,
  })
  await expect(candidateContext).toContainText(zhCN.candidateContext.name)
  await expect(candidateContext).not.toContainText('固定简历')
  const candidateInfoButton = page.getByRole('button', {
    name: zhCN.candidateContext.infoButton,
  })
  expect(
    await candidateContext.locator('.candidate-context-label').evaluate(
      (label) => window.getComputedStyle(label).whiteSpace,
    ),
  ).toBe('nowrap')
  await expect(candidateInfoButton.locator('..')).toContainText(
    zhCN.candidateContext.name,
  )
  expect(
    await candidateInfoButton.evaluate(
      (button) => window.getComputedStyle(button).borderStyle,
    ),
  ).toBe('none')
  expect(
    await candidateContext.evaluate(
      (context) => window.getComputedStyle(context).textAlign,
    ),
  ).toBe('left')
  await candidateInfoButton.click()
  await expect(
    page.getByRole('region', { name: zhCN.candidateContext.hintTitle }),
  ).toContainText(zhCN.candidateContext.hintBody)
  await page.keyboard.press('Escape')
  await expect(
    page.getByRole('region', { name: zhCN.candidateContext.hintTitle }),
  ).toHaveCount(0)
  await expect(candidateInfoButton).toBeFocused()
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true)

  const contactButton = page.getByRole('button', { name: zhCN.navigation.contact })
  for (let tabCount = 0; tabCount < 12; tabCount += 1) {
    await page.keyboard.press('Tab')
    if (await contactButton.evaluate((element) => element === document.activeElement)) {
      break
    }
  }
  await expect(contactButton).toBeFocused()
  await page.keyboard.press('Enter')
  await expect(page.getByRole('heading', { name: zhCN.contact.title })).toBeVisible()
  await expect(page.getByText(zhCN.contact.noAutoSend)).toBeVisible()
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true)

  await page.getByRole('button', { name: zhCN.navigation.dashboard }).click()
  await expect(
    page.getByRole('heading', { name: zhCN.dashboard.title }),
  ).toBeVisible()
  await expect(page.getByLabel(zhCN.dashboard.startDate)).toBeVisible()
  await expect(page.getByLabel(zhCN.dashboard.endDate)).toBeVisible()
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true)
  expect(
    await page.evaluate(() => {
      const dashboard = document.querySelector('.dashboard-view')
      return dashboard !== null && dashboard.scrollHeight <= dashboard.clientHeight + 1
    }),
  ).toBe(true)
})
