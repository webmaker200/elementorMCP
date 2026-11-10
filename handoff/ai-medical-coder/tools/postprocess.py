"""Add the page helper widget to build/built.json -> build/coder_data.json.

V4 local styles can't hold @keyframes, `animation`, page-wide backgrounds or scripts, so one small V3 HTML
widget at the end of the testimonial section carries:
  - the page background glows from the design (three soft blue / yellow / green glow images);
  - the marquee animation;
  - the testimonial slider (prev / next, counter).
Nothing in it depends on element or page IDs: it finds its targets from the page structure, so it keeps
working when the page is copied to another site (where Elementor gives everything new IDs).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
import coder  # noqa: E402

d = json.load(open(os.path.join(ROOT, 'build', 'built.json')))
M = coder.MEDIA
BLUE, YELLOW, GREEN = (M[f'sophus-glow-{c}-sm']['url'] for c in ('blue', 'yellow', 'green'))

# Glow layers from the design's page wrapper (file, horizontal offset from centre, top). The design's
# tops include its 84px header; the site header sits outside the Elementor page, so they move up 84px.
LAYERS = [(BLUE, -1500, -500), (YELLOW, 0, -760), (GREEN, -150, 300), (YELLOW, -1850, 1300), (BLUE, -1000, 2000),
          (GREEN, -150, 2700), (YELLOW, -1850, 3500), (BLUE, -150, 4300), (GREEN, -1000, 5000), (YELLOW, -1850, 5700),
          (BLUE, -150, 6400), (GREEN, -1850, 7100), (YELLOW, -1000, 7800)]
bg = ', '.join(f"url('{u}') left calc(50% {'+' if x >= 0 else '-'} {abs(x)}px) top {y - 84}px / 2000px auto no-repeat" for u, x, y in LAYERS)

html = """<style>
.elementor:has(.sophus-page-js),.sophus-page{background:%(bg)s,#fff;overflow-x:clip}
@keyframes sophus-marquee{from{transform:translateX(0)}to{transform:translateX(-50%%)}}
/* marquee row = band > track in the section just before this widget's section (CSS only, no JS needed) */
section:has(+ section > .sophus-page-js) > div > div:first-child > div:first-child,.sophus-marquee-track{animation:sophus-marquee 60s linear infinite;will-change:transform}
@media (prefers-reduced-motion:reduce){section:has(+ section > .sophus-page-js) > div > div:first-child > div:first-child,.sophus-marquee-track{animation:none}}
.sophus-page-js{position:absolute!important;width:0!important;height:0!important;overflow:hidden;pointer-events:none}
</style>
<script nowprocket>
(function(){
  function init(){
    var me=document.querySelector('.sophus-page-js');if(!me||me.dataset.ready)return;me.dataset.ready=1;
    var page=me.closest('.elementor');if(page)page.classList.add('sophus-page');
    /* testimonial slider: everything lives in this widget's section */
    var sec=me.closest('section');if(!sec)return;
    var btns=sec.querySelectorAll('button');if(btns.length<2)return;
    var pv=btns[0],nx=btns[1],c=null;
    [].forEach.call(sec.querySelectorAll('p'),function(p){if(/^\\d+ \\/ \\d+$/.test(p.textContent.trim()))c=p;});
    var P=[].slice.call(sec.querySelectorAll('img'));
    var Q=[];[].forEach.call(sec.querySelectorAll('div'),function(d){
      var k=d.children;if(!Q.length&&k.length===P.length&&[].every.call(k,function(x){return x.querySelectorAll('p').length>=3;}))Q=[].slice.call(k);});
    var n=P.length,i=0;if(n<2||Q.length!==n)return;
    function show(k){
      i=(k+n)%%n;
      P.concat(Q).forEach(function(el,j){var on=(j%%n)===i;
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
</script>""" % {'bg': bg}

s9 = d[8]
assert any('What our clients say' in json.dumps(e, ensure_ascii=False) for e in s9['elements']), 'section 9 is not the testimonials'
s9['elements'] = [e for e in s9['elements'] if e.get('widgetType') != 'html']
s9['elements'].append({'id': 'a7c0de51', 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                       'settings': {'html': html, '_css_classes': 'sophus-page-js'}, 'elements': []})
json.dump(d, open(os.path.join(ROOT, 'build', 'coder_data.json'), 'w'), ensure_ascii=False)
print('ok')
