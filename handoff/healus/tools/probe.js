// usage: PW=... node probe.js <url> <width>  -> section heights, tab switching, accordion, overflow
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [url, w] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] });
  const page = await browser.newPage({ viewport: { width: +w, height: 900 } });
  const errs = []; page.on('pageerror', e => errs.push(e.message)); page.on('console', m => m.type() === 'error' && errs.push('console: ' + m.text().slice(0, 120)));
  await page.goto(url, { waitUntil: 'load', timeout: 150000 });
  if (process.env.PW && await page.$('form.post-password-form')) {
    await page.fill('form.post-password-form input[name="post_password"]', process.env.PW);
    await Promise.all([page.waitForNavigation({ waitUntil: 'load', timeout: 150000 }), page.click('form.post-password-form [type="submit"]')]);
  }
  await page.waitForTimeout(1500);
  const r = await page.evaluate(() => {
    const root = document.querySelector('[data-elementor-id="411263"]');
    const secs = [...root.children].map(s => Math.round(s.getBoundingClientRect().height));
    const tabs = [...document.querySelectorAll('[data-elementor-id="411263"] [role="tab"]')].map(t => [t.getAttribute('aria-selected'), t.outerHTML.slice(0, 140)]);
    return { secs, tabsN: tabs.length, tab0: tabs[0] && tabs[0][1], sel: tabs.map(t => t[0]).join(','), h1: document.querySelectorAll('h1').length,
             sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth };
  });
  console.log(JSON.stringify(r));
  const tabs = await page.$$('[data-elementor-id="411263"] [role="tab"]');
  for (const i of [3, 5, 0]) {
    if (!tabs[i]) break;
    await tabs[i].click(); await page.waitForTimeout(400);
    const s = await page.evaluate(i => { const ts = [...document.querySelectorAll('[data-elementor-id="411263"] [role="tab"]')]; const ps = [...document.querySelectorAll('[data-elementor-id="411263"] [role="tabpanel"]')];
      const vis = ps.map(p => p.offsetParent !== null || getComputedStyle(p).display !== 'none'); const bg = getComputedStyle(ts[i]).backgroundColor;
      return { selected: ts.map(t => t.getAttribute('aria-selected') === 'true' ? 1 : 0).join(''), visiblePanels: vis.map(v => v ? 1 : 0).join(''), activeBg: bg,
               next: ps.find(p => p.offsetParent !== null)?.innerText.match(/Next: [^\n]+/)?.[0] }; }, i);
    console.log('click tab', i, JSON.stringify(s));
  }
  const acc = await page.evaluate(() => [...document.querySelectorAll('[data-elementor-id="411263"] details')].map(d => d.open ? 1 : 0).join(''));
  const sums = await page.$$('[data-elementor-id="411263"] details summary'); if (sums[2]) { await sums[2].click(); await page.waitForTimeout(400); }
  const acc2 = await page.evaluate(() => [...document.querySelectorAll('[data-elementor-id="411263"] details')].map(d => d.open ? 1 : 0).join(''));
  console.log('accordion before/after clicking #3:', acc, acc2, '| errors:', errs.join(' | ').slice(0, 400) || 'none');
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
