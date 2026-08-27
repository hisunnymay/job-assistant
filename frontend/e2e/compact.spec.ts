import { expect, test } from '@playwright/test'
import { zhCN } from '../src/content/zh-CN'

test('keeps the compact recruiter journey readable and keyboard operable', async ({
  page,
}) => {
  await page.goto('/#resume')
  await expect(page.getByRole('heading', { name: zhCN.resume.title })).toBeVisible()
  await expect(page.getByRole('navigation', { name: zhCN.navigation.ariaLabel })).toBeVisible()
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
})
