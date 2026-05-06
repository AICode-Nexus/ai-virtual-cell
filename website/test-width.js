const playwright = require('playwright');

(async () => {
  const browser = await playwright.chromium.launch({ headless: false });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  console.log('正在加载页面...');
  await page.goto('http://localhost:8888/mapping.html');
  await page.waitForLoadState('networkidle');

  console.log('\n滚动到 High-value cases 部分...');
  await page.locator('text=十二个高价值映射案例').scrollIntoViewIfNeeded();
  await page.waitForTimeout(1000);

  // 获取 section 容器的宽度
  const section = page.locator('section:has-text("十二个高价值映射案例")').first();
  const sectionBox = await section.boundingBox();

  // 获取 case-nav 的宽度
  const caseNav = section.locator('.case-nav');
  const caseNavBox = await caseNav.boundingBox();

  // 获取所有 case-tab 的宽度
  const tabs = await caseNav.locator('.case-tab').all();
  const tabCount = tabs.length;
  const firstTabBox = await tabs[0].boundingBox();

  console.log('\n=== 测试结果 ===');
  console.log(`Section 容器宽度: ${sectionBox.width}px`);
  console.log(`Case-nav 宽度: ${caseNavBox.width}px`);
  console.log(`Tab 数量: ${tabCount}`);
  console.log(`第一个 tab 宽度: ${firstTabBox.width}px`);

  // 验证修复
  const isFixed = sectionBox.width > 1180 && firstTabBox.width > 200;

  console.log('\n=== 验证结果 ===');
  console.log(`Section 宽度 > 1180px: ${sectionBox.width > 1180 ? '✅ 通过' : '❌ 失败'}`);
  console.log(`Tab 宽度 > 200px: ${firstTabBox.width > 200 ? '✅ 通过' : '❌ 失败'}`);
  console.log(`\n总体结果: ${isFixed ? '✅ 修复成功' : '❌ 修复失败'}`);

  // 截图
  await page.screenshot({ path: 'test-width-result.png', fullPage: false });
  console.log('\n截图已保存到: test-width-result.png');

  await browser.close();
})();
