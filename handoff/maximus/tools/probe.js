const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [url, w, expr] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined, args:['--ignore-certificate-errors'] });
  const page = await browser.newPage({ viewport: { width: +(w||1440), height: 1000 }, ignoreHTTPSErrors: true });
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  await page.waitForTimeout(1000);
  console.log(JSON.stringify(await page.evaluate(expr), null, 1));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
