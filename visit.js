const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true }); // 无头模式
  const page = await browser.newPage();
  await page.goto('https://checkoutreact.top/#/searchTennis');
  // 保持页面打开1小时（3600000毫秒）
  await page.waitForTimeout(3600000);
  await browser.close();
})();
