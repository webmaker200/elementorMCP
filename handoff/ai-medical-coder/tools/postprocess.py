"""Add the testimonial slider script and the marquee keyframes to build/built.json -> build/coder_data.json.

The V4 local styles can't hold @keyframes or scripts, so one small V3 HTML widget at the end of the
testimonial section carries both. Element IDs are looked up from the built data by content.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
import coder  # noqa: E402

d = json.load(open(os.path.join(ROOT, 'build', 'built.json')))


def walk(es, parent=None):
    for e in es:
        yield e, parent
        yield from walk(e.get('elements', []), e)


def txt(e):
    s = e.get('settings', {})
    v = s.get('paragraph', {}).get('value') if isinstance(s.get('paragraph'), dict) else None
    if isinstance(v, dict):
        v = v.get('content', {}).get('value') if isinstance(v.get('content'), dict) else json.dumps(v)
    return v or ''


all_ = list(walk(d))
photo_ids = [t[3] for t in coder.TESTIMONIALS]
photos, quotes = [], []
for q, n, r, mid in coder.TESTIMONIALS:
    photos.append(next(e['id'] for e, _ in all_ if e.get('widgetType') == 'e-image' and json.dumps(e['settings']).find(f'"id": {mid}') >= 0
                       or e.get('widgetType') == 'e-image' and f'"value": {mid}' in json.dumps(e['settings'])))
    quotes.append(next(p['id'] for e, p in all_ if e.get('widgetType') == 'e-paragraph' and q[:40] in json.dumps(e['settings'], ensure_ascii=False)))
count = next(e['id'] for e, _ in all_ if e.get('widgetType') == 'e-paragraph' and '1 / 5' in json.dumps(e['settings']))
prev = next(p['id'] for e, p in all_ if e.get('widgetType') == 'e-paragraph' and '"←"' in json.dumps(e['settings'], ensure_ascii=False))
nxt = next(p['id'] for e, p in all_ if e.get('widgetType') == 'e-paragraph' and '"→"' in json.dumps(e['settings'], ensure_ascii=False))
sec = next(p['id'] for e, p in all_ if e['id'] == photos[0])  # photos box
s9 = d[8]
print('photos', photos, 'quotes', quotes, count, prev, nxt)

E = lambda i: f'[data-id="{i}"]'
html = """<style>
@keyframes sophus-marquee{from{transform:translateX(0)}to{transform:translateX(-50%%)}}
@media (prefers-reduced-motion:reduce){.elementor-411494 *{animation-play-state:paused!important}}
</style>
<script>
(function(){
  function init(){
    var P=%(P)s,Q=%(Q)s,i=0,n=P.length;
    function q(s){return document.querySelector(s);}
    var c=q('%(C)s'),pv=q('%(PV)s'),nx=q('%(NX)s');
    if(!pv||!nx||pv.dataset.sophus)return;
    pv.dataset.sophus=1;
    function show(k){
      i=(k+n)%%n;
      P.concat(Q).forEach(function(s,j){var el=q(s);if(!el)return;var on=(j%%n)===i;
        el.style.setProperty('opacity',on?'1':'0','important');el.style.setProperty('visibility',on?'visible':'hidden','important');
        el.setAttribute('aria-hidden',on?'false':'true');});
      if(c)c.textContent=(i+1)+' / '+n;
    }
    [[pv,-1,'Previous testimonial'],[nx,1,'Next testimonial']].forEach(function(b){
      b[0].setAttribute('aria-label',b[2]);b[0].setAttribute('type','button');
      b[0].addEventListener('click',function(e){e.preventDefault();show(i+b[1]);});
    });
    show(0);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>""" % {
    'P': json.dumps([E(x) for x in photos]), 'Q': json.dumps([E(x) for x in quotes]),
    'C': E(count), 'PV': E(prev), 'NX': E(nxt)}

# the track holds 4 copies; -50% loops seamlessly because the 2nd half repeats the 1st
s9['elements'] = [e for e in s9['elements'] if e.get('widgetType') != 'html']
s9['elements'].append({'id': 'a7c0de51', 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                       'settings': {'html': html, '_css_classes': 'sophus-slider-js', '_element_width': 'initial',
                                    '_position': 'absolute', '_element_custom_width': {'unit': 'px', 'size': 0, 'sizes': []}},
                       'elements': []})
json.dump(d, open(os.path.join(ROOT, 'build', 'coder_data.json'), 'w'), ensure_ascii=False)
print('ok')
