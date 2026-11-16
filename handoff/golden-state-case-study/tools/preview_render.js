// node render.js <shellUrl> <content.html> <styles.css> <outprefix> <width>
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [url, contentF, cssF, out, w] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] });
  const page = await browser.newPage({ viewport: { width: +w, height: 900 } });
  await page.goto(url, { waitUntil: 'load', timeout: 150000 });
  await page.mouse.move(200, 300); await page.mouse.wheel(0, 600); await page.waitForTimeout(4000);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.evaluate(([html, css]) => {
    const root = document.querySelector('[data-elementor-type=wp-post]');
    root.outerHTML = html;
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
  }, [fs.readFileSync(contentF, 'utf8'), fs.readFileSync(cssF, 'utf8')]);
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); }); // lazyDone
  await page.waitForTimeout(3000);
  const info = await page.evaluate(() => {
    const W = document.documentElement.clientWidth, wide = [];
    document.querySelectorAll('[data-elementor-type=wp-post] *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width && r.right > W + 1) { let p = e.parentElement, clip = false; while (p) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { clip = true; break; } p = p.parentElement; } if (!clip) wide.push((e.className + '').slice(0, 50) + ' ' + Math.round(r.right)); } });
    const sec = [...document.querySelectorAll('[data-elementor-type=wp-post] section')].map(s => s.id + ':' + Math.round(s.getBoundingClientRect().height));
    const pc = document.querySelector('[data-elementor-type=wp-post] .parent-container'); const cs = getComputedStyle(pc);
    return { docW: document.documentElement.scrollWidth, W, wide: wide.slice(0, 12), sec, pcPad: cs.paddingLeft + ' ' + cs.paddingTop };
  });
  console.log(w, JSON.stringify(info));
  await page.screenshot({ path: `${out}-full.png`, fullPage: true });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
