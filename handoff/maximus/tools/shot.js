// usage: node shot.js <url> <outprefix> <width> [full]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const [url, out, w, full] = process.argv.slice(2);
  const browser = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined, args:['--ignore-certificate-errors'] });
  const page = await browser.newPage({ viewport: { width: +w, height: 1000 }, ignoreHTTPSErrors: true });
  for (let i = 0; i < 5; i++) {  // the egress proxy sometimes resets the first request
    try { await page.goto(url.startsWith('/')?'file://'+url:url, { waitUntil: 'load', timeout: 120000 }); } catch (e) { if (i === 4) throw e; }
    const ok = await page.evaluate(async () => {
      if (/upstream request failed/.test(document.body.innerText.slice(0, 200))) return false;
      const bad = [...document.querySelectorAll('link[rel=stylesheet]')].filter(l => l.href.startsWith(location.origin) && !l.sheet);
      await document.fonts.ready;
      return bad.length === 0 && [...document.fonts].some(f => /Poppins/.test(f.family) && f.status === 'loaded');
    });
    if (ok) break;
    console.error('reload: stylesheet/font missing');
    await page.waitForTimeout(3000);
  }
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); } await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 4000); }))); window.scrollTo(0,0); });
  await page.waitForTimeout(1500);
  const info = await page.evaluate(() => ({ cssok: [...document.styleSheets].filter(x => { try { return x.cssRules.length >= 0 } catch (e) { return false } }).length + '/' + document.styleSheets.length, wide: [...document.querySelectorAll('.elementor-' + (window.__pid || '410364') + ' *')].filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 1 && !e.closest('[style*=overflow],.e-grid-base')).slice(0,5).map(e => e.tagName + '.' + (e.className.baseVal ?? e.className).toString().slice(0,60) + ' r=' + Math.round(e.getBoundingClientRect().right)), h: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
  console.log(JSON.stringify(info));
  const H = info.h, seg = 2400;
  if (full) { for (let y = 0, i = 0; y < H; y += seg, i++) await page.screenshot({ path: `${out}_${i}.png`, clip: { x: 0, y, width: +w, height: Math.min(seg, H - y) }, fullPage: true }); }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
