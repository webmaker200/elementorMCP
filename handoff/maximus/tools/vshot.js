// usage: node vshot.js <url> <out.png> <width> <scrollY> [height]  -- plain viewport screenshot at a scroll offset
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [url, out, w, y, h] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined, args: ['--ignore-certificate-errors'] });
  const page = await browser.newPage({ viewport: { width: +w, height: +(h || 1200) }, ignoreHTTPSErrors: true });
  for (let i = 0; i < 6; i++) {
    try { await page.goto(url, { waitUntil: 'load', timeout: 120000 }); } catch (e) { if (i === 5) throw e; }
    const ok = await page.evaluate(async () => { await document.fonts.ready; return !/upstream request failed/.test(document.body.innerText.slice(0, 200)) && [...document.querySelectorAll('link[rel=stylesheet]')].every(l => !l.href.startsWith(location.origin) || l.sheet) && [...document.fonts].some(f => /Poppins/.test(f.family) && f.status === 'loaded'); });
    if (ok) break; await page.waitForTimeout(3000);
  }
  await page.evaluate(async y => { for (let s = 0; s <= y; s += 500) { window.scrollTo(0, s); await new Promise(r => setTimeout(r, 80)); } window.scrollTo(0, y); }, +y);
  await page.waitForTimeout(1500);
  await page.screenshot({ path: out });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
