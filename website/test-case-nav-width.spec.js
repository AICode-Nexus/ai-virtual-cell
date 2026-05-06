const { test, expect } = require('@playwright/test');

test.describe('High-value cases section width', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8888/mapping.html');
    await page.waitForLoadState('networkidle');
  });

  test('RED - case-nav should have adequate width', async ({ page }) => {
    // 滚动到 High-value cases 部分
    await page.locator('text=十二个高价值映射案例').scrollIntoViewIfNeeded();

    // 获取 section 容器的宽度
    const section = page.locator('section:has-text("十二个高价值映射案例")').first();
    const sectionBox = await section.boundingBox();

    // 获取 case-nav 的宽度
    const caseNav = section.locator('.case-nav');
    const caseNavBox = await caseNav.boundingBox();

    // 获取第一个 case-tab 的宽度
    const firstTab = caseNav.locator('.case-tab').first();
    const firstTabBox = await firstTab.boundingBox();

    console.log('Section width:', sectionBox.width);
    console.log('Case-nav width:', caseNavBox.width);
    console.log('First tab width:', firstTabBox.width);
    console.log('Number of tabs:', await caseNav.locator('.case-tab').count());

    // 测试失败条件:
    // 1. section 宽度应该大于 1180px (当前默认容器宽度)
    // 2. 每个 tab 的宽度应该大于 200px (合理的最小宽度)

    expect(sectionBox.width).toBeGreaterThan(1180);
    expect(firstTabBox.width).toBeGreaterThan(200);
  });
});
