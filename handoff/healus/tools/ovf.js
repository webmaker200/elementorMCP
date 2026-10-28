const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [url, w] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] });
  const page = await browser.newPage({ viewport: { width: +w, height: 900 } });
  await page.goto(url, { waitUntil: 'load', timeout: 150000 });
  if (await page.$('form.post-password-form')) { await page.fill('form.post-password-form input[name="post_password"]', process.env.PW);
    await Promise.all([page.waitForNavigation({ waitUntil: 'load' }), page.click('form.post-password-form [type="submit"]')]); }
  await page.waitForTimeout(1500);
  console.log(JSON.stringify(await page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const out = [...document.querySelectorAll('body *')].filter(e => e.getBoundingClientRect().right > vw + 0.5 && e.getBoundingClientRect().width > 0)
      .map(e => { const t = e.closest('[data-elementor-type]'); return (t ? t.getAttribute('data-elementor-type') : 'none') + ' ' + e.tagName + '.' + String(e.className).slice(0, 40) + ' r=' + Math.round(e.getBoundingClientRect().right); });
    return { vw, n: out.length, sample: out.slice(0, 12) };
  })));
  await browser.close();
})();
