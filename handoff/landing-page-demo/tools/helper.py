"""Add the page helper (one V3 HTML widget) to the landing page's Elementor data and write it back via WP REST.

V4 elements can't carry scripts, so this widget holds the design's three scroll behaviours, ported 1:1 from the
design's component code (MedCare_MSO_PPC_Landing_Page.html):
  1. "Four steps" stack (#lp-stack): cards are position: sticky (top 108/128/148/168px, set in lp.py). Sticky is kept
     only when every card fits the viewport (height + top <= innerHeight - 24) and the screen is wider than 1024px;
     while the next card slides over, a card gets scale(1 - .05p) and brightness(1 - .04p),
     p = clamp((top + height - nextTop) / (height - 20)).
  2. About statement (#lp-statement): words turn from #C9D3DB to #14212B as the paragraph scrolls through the
     viewport: r = clamp((.85vh - top) / (height + .35vh)), lit = round(r * words * 1.15).
  3. Mobile sticky bar (#lp-sticky): shown on phones (< 768px) after 640px of scroll.
prefers-reduced-motion: no transforms, all words lit (as in the design). The script is marked nowprocket so WP Rocket
doesn't delay it. Usage: helper.py  (run after run_build.py)
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, lp  # noqa: E402

HTML = r"""<style>.lp-helper{position:absolute!important;width:0!important;height:0!important;overflow:hidden!important;margin:0!important;padding:0!important}</style>
<script nowprocket>
(function(){
  function init(){
    if (window.__lpHelper) return; window.__lpHelper = 1;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var stack = document.getElementById('lp-stack');
    var cards = stack ? [].slice.call(stack.children).filter(function(c){ return c.nodeType === 1; }) : [];
    var st = document.getElementById('lp-statement');
    var words = st ? [].slice.call(st.querySelectorAll('span')) : [];
    var bar = document.getElementById('lp-sticky');
    var stackOn = false, raf = 0;
    function topOf(c){ return parseFloat(getComputedStyle(c).top) || 0; }
    function measure(){
      if (!cards.length) return;
      cards.forEach(function(c){ c.style.position = ''; });
      var desk = window.innerWidth > 1024;
      stackOn = desk && cards.every(function(c){ return getComputedStyle(c).position === 'sticky' && c.offsetHeight + topOf(c) <= window.innerHeight - 24; });
      if (!stackOn) cards.forEach(function(c){ if (desk) c.style.position = 'static'; c.style.transform = ''; c.style.filter = ''; });
      update();
    }
    function update(){
      raf = 0;
      var vh = window.innerHeight;
      if (stackOn && !reduce) {
        cards.forEach(function(card, i){
          var next = cards[i + 1];
          if (!next) { card.style.transform = ''; card.style.filter = ''; return; }
          var r = card.getBoundingClientRect(), nr = next.getBoundingClientRect();
          var p = Math.min(1, Math.max(0, (topOf(card) + r.height - nr.top) / (r.height - 20)));
          card.style.transform = 'scale(' + (1 - 0.05 * p) + ')';
          card.style.filter = 'brightness(' + (1 - 0.04 * p) + ')';
        });
      }
      if (words.length) {
        var lit = words.length;
        if (!reduce) {
          var b = st.getBoundingClientRect();
          var rv = Math.max(0, Math.min(1, (vh * 0.85 - b.top) / (b.height + vh * 0.35)));
          lit = Math.round(rv * words.length * 1.15);
        }
        words.forEach(function(w, i){ w.style.color = i < lit ? '#14212B' : ''; });
      }
      if (bar) bar.setAttribute('data-on', (window.innerWidth < 768 && window.scrollY > 640) ? '1' : '0');
    }
    function onScroll(){ if (!raf) raf = requestAnimationFrame(update); }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function(){ requestAnimationFrame(measure); });
    window.addEventListener('load', measure);
    setTimeout(measure, 300); setTimeout(measure, 1500);
    measure();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
</script>"""


def main():
    cur = mcp.rest('GET', f'wp/v2/pages/{lp.PID}?context=edit&_fields=meta')
    data = json.loads(cur['meta']['_elementor_data'])
    root = data[0]
    last = root['elements'][-1]  # contact section
    last['elements'] = [e for e in last['elements'] if e.get('widgetType') != 'html']
    last['elements'].append({'id': 'a7c1e9b2', 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                             'settings': {'html': HTML, '_css_classes': 'lp-helper'}, 'elements': []})
    body = '/tmp/claude-0/_lp_body.json'
    json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False), '_elementor_edit_mode': 'builder'}}, open(body, 'w'), ensure_ascii=False)
    res = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                          '--data-binary', '@' + body, mcp.API + f'wp/v2/pages/{lp.PID}?_fields=id,status'], capture_output=True, text=True)
    os.remove(body)
    assert 'id' in json.loads(res.stdout), res.stdout[:500]
    back = json.loads(mcp.rest('GET', f'wp/v2/pages/{lp.PID}?context=edit&_fields=meta')['meta']['_elementor_data'])
    assert back == data, 'stored data differs'
    json.dump(data, open(os.path.join(HERE, '..', 'build', 'lp_data.json'), 'w'), ensure_ascii=False)
    print('helper added; stored', len(json.dumps(data)), 'bytes')


if __name__ == '__main__':
    main()
