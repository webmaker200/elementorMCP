const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
(async () => {
  const [url, out] = process.argv.slice(2);
  const b = await chromium.launch({ proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors-spki-list=PS48cX347wDVcRynzq+DFqswl2PLNE1sG6uQvxMCOS0='] });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(url, { waitUntil: 'load', timeout: 150000 }); await p.waitForTimeout(2500);
  const blocks = await p.evaluate(() => {
    const root = [...document.querySelectorAll('[data-elementor-type="wp-post"]')].sort((a, b) => b.children.length - a.children.length)[0];
    const skip = e => e.closest('script,style,noscript,svg,.swiper-slide-duplicate,[data-elementor-type="section"],[data-elementor-type="loop-item"],.elementor-widget-shortcode,.elementor-widget-template');
    const res = []; const taken = new Set();
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
    let e;
    while ((e = walker.nextNode())) {
      if (skip(e)) continue;
      let anc = e.parentElement, inside = false;
      while (anc && anc !== root) { if (taken.has(anc)) { inside = true; break; } anc = anc.parentElement; }
      if (inside) continue;
      const direct = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      if (!direct) continue;
      taken.add(e);
      const sec = e.closest('[data-elementor-type="wp-post"] > *');
      res.push({ tag: e.tagName.toLowerCase(), sec: sec ? sec.dataset.id : '', id: (e.closest('[data-id]') || {}).dataset?.id || '', text: e.textContent });
    }
    return res;
  });
  fs.writeFileSync(out, JSON.stringify(blocks, null, 1));
  console.log(blocks.length);
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
