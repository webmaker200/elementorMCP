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
    document.querySelectorAll('[data-elementor-type=wp-page] script').forEach(old => { const n = document.createElement('script'); n.textContent = old.textContent; document.body.appendChild(n); });
    window.dispatchEvent(new Event('load'));
  }, [fs.readFileSync(contentF, 'utf8'), fs.readFileSync(cssF, 'utf8')]);
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); }); // lazyDone
  await page.waitForTimeout(3000);

  const st0 = await page.evaluate(() => { const s = document.getElementById('lp-stack'); return s.getBoundingClientRect().top + scrollY; });
  const rows = [];
  for (const off of [-200, 100, 400, 700, 1000, 1300, 1600, 1900]) {
    await page.evaluate(y => window.scrollTo(0, y), st0 + off); await page.waitForTimeout(350);
    rows.push(await page.evaluate(off => { const cs = [...document.getElementById('lp-stack').children];
      return off + ' | ' + cs.map((c, i) => { const r = c.getBoundingClientRect(), k = getComputedStyle(c); return `#${i + 1} top${Math.round(r.top)} ${k.position} ${(c.style.transform || '-').replace('scale', 's')} ${(c.style.filter || '-').replace('brightness', 'b')}`; }).join('  ');
    }, off));
    if (off === 1000) await page.screenshot({ path: `${out}-stack-mid.png` });
    if (off === 1600) await page.screenshot({ path: `${out}-stack-late.png` });
  }
  console.log(rows.join('\n'));
  const words = await page.evaluate(async () => { const st = document.getElementById('lp-statement'); const r = st.getBoundingClientRect();
    window.scrollTo(0, r.top + scrollY - window.innerHeight * 0.6); await new Promise(z => setTimeout(z, 500));
    const sp = [...st.querySelectorAll('span')]; return sp.filter(s => s.style.color).length + ' of ' + sp.length + ' words lit at 60% viewport'; });
  console.log(words);

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
