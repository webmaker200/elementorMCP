// usage: node shot.js <url> <outprefix> <width> [segmentHeight]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [url, out, w, segArg] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
    args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] });
  const page = await browser.newPage({ viewport: { width: +w, height: 1000 } });
  const errs = []; page.on('pageerror', e => errs.push(e.message));
  for (let attempt = 0; attempt < 3; attempt++) {
    await page.goto(url, { waitUntil: 'load', timeout: 150000 });
    if (process.env.PW && await page.$('form.post-password-form')) {
      await page.fill('form.post-password-form input[name="post_password"]', process.env.PW);
      await Promise.all([page.waitForNavigation({ waitUntil: 'load', timeout: 150000 }), page.click('form.post-password-form [type="submit"]')]);
    }
    const ok = await page.evaluate(() => [...document.styleSheets].filter(s => { try { return s.href && s.href.includes(location.host) && s.cssRules.length >= 0; } catch (e) { return false; } }).length > 3
      && document.fonts.check('16px "Poppins Optimized"'));
    if (ok) break;
  }
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); }
    await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 6000); }))); window.scrollTo(0, 0); });
  await page.waitForTimeout(1200);
  const info = await page.evaluate(() => {
    const secs = [...document.querySelectorAll('section.e-flexbox, [data-elementor-type="wp-page"] > .e-flexbox')].map(s => { const b = s.getBoundingClientRect(); return [Math.round(b.top + scrollY), Math.round(b.height)]; });
    const vw = document.documentElement.clientWidth;
    const wide = [...document.querySelectorAll('[data-elementor-type="wp-page"] *')].filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.right > vw + 1 && !e.closest('[style*="overflow"]'); })
      .filter(e => { let a = e.parentElement; while (a) { const o = getComputedStyle(a).overflowX; if (o === 'hidden' || o === 'clip' || o === 'auto') return false; a = a.parentElement; } return true; })
      .slice(0, 6).map(e => e.tagName + '.' + String(e.className).slice(0, 50) + ' r=' + Math.round(e.getBoundingClientRect().right));
    return { h: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, cw: vw, secs, wide };
  });
  console.log(JSON.stringify(info), errs.length ? 'ERRORS ' + errs.join(' | ').slice(0, 300) : '');
  const seg = +(segArg || 0);
  if (seg) {
    const page0 = await page.$('[data-elementor-type="wp-page"]'); const bb = await page0.boundingBox();
    for (let y = bb.y, i = 0; y < bb.y + bb.height; y += seg, i++)
      await page.screenshot({ path: `${out}_${i}.png`, clip: { x: 0, y, width: +w, height: Math.min(seg, bb.y + bb.height - y) }, fullPage: true });
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
