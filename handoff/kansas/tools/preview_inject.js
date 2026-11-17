// node inject.js <url> <rendered.html> <css> <out> <width> : insert the two new sections after a81510a and b3e8ba0 on the live page
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [url, htmlF, cssF, out, w] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] });
  const p = await b.newPage({ viewport: { width: +w, height: 900 } });
  await p.goto(url, { waitUntil: 'load', timeout: 150000 });
  await p.mouse.move(200, 300); await p.mouse.wheel(0, 600); await p.waitForTimeout(3500);
  const info = await p.evaluate(([html, css]) => {
    const t = document.createElement('div'); t.innerHTML = html;
    const s1 = t.querySelector('[data-id="78f76fc0"]'), s2 = t.querySelector('[data-id="4c973069"]');
    const a = document.querySelector('[data-id="a81510a"]'), c = document.querySelector('[data-id="b3e8ba0"]');
    if (!a || !c || !s1 || !s2) return 'missing ' + [!!a, !!c, !!s1, !!s2];
    a.after(s1); c.after(s2);
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    return 'ok';
  }, [fs.readFileSync(htmlF, 'utf8'), fs.readFileSync(cssF, 'utf8')]);
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
  await p.evaluate(async () => { document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; }); await new Promise(r => setTimeout(r, 2500)); });
  const mapOk = await p.evaluate(() => { const i = document.querySelector('img[src*="kansas-cities-map"]'); return i ? i.complete + ' ' + i.naturalWidth + 'x' + i.naturalHeight + ' shown ' + Math.round(i.getBoundingClientRect().width) + 'x' + Math.round(i.getBoundingClientRect().height) : 'noimg'; });
  console.log('map', mapOk);
  await p.addStyleTag({ content: 'header, [data-elementor-type=header]{display:none!important}' });
  const r = await p.evaluate(() => { const W = document.documentElement.clientWidth; const g = id => { const e = document.querySelector(`[data-id="${id}"]`); const rr = e.getBoundingClientRect(); return [Math.round(rr.top + scrollY), Math.round(rr.height)]; };
    return { docW: document.documentElement.scrollWidth, W, os: g('78f76fc0'), cr: g('4c973069') }; });
  console.log(w, info, JSON.stringify(r));
  for (const [k, id] of [['os', '78f76fc0'], ['cr', '4c973069']]) await (await p.$(`[data-id="${id}"]`)).screenshot({ path: `${out}-${k}.png` });
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
