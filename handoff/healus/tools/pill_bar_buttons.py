"""HealUs page (411263), section 3 pill bar (4ca8e32c): make the six static pills behave like the old tab buttons
without switching content.

- each pill -> real <button> (V4 div-block tag "button"): focusable, Enter/Space, keeps the `healus-tab` focus ring;
  label paragraph rendered as <span> (valid inside a button)
- highlight follows aria-pressed: the bar's local CSS styles `[aria-pressed="true"]` exactly like the old selected tab;
  the first pill shows it until the script has run (no flash); light hover on the other pills
- a tiny script (V3 HTML widget, zero size, after the bar) sets aria-pressed on click so only one pill is highlighted
- removes the per-pill local styles added by flatten_features.py (cursor default + Charting highlight)
Backs up the live _elementor_data first; writes via WP REST; then touch + publish through the Elementor MCP.
"""
import base64, json, os, random, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, WRAP, MENU = 411263, '7bf06193', '4ca8e32c'
ON = ('background-color: #FFFFFF; box-shadow: 0px 8px 20px -10px rgba(2,40,66,0.3), 0px 0px 0px 1px rgba(49,131,113,0.12);')
ON_LABEL = 'font-weight: 500; color: var(--HealUsInk);'
ON_NUM = 'background-image: linear-gradient(135deg, #318371 0%, #006750 100%); color: #FFFFFF;'
SEL_ON = '& > .healus-tab[aria-pressed="true"], & > .healus-tab:first-child:not([aria-pressed])'
BAR_CSS = (f'{SEL_ON} {{ {ON} }} '
           f'& > .healus-tab[aria-pressed="true"] .healus-tab-label, & > .healus-tab:first-child:not([aria-pressed]) .healus-tab-label {{ {ON_LABEL} }} '
           f'& > .healus-tab[aria-pressed="true"] .healus-tab-label span, & > .healus-tab:first-child:not([aria-pressed]) .healus-tab-label span {{ {ON_NUM} }} '
           '& > .healus-tab:hover:not([aria-pressed="true"]) { background-color: rgba(255,255,255,0.6); } '
           '& > .healus-tab { font: inherit; text-align: start; }')
SCRIPT = ('<script>(function(){function init(){document.querySelectorAll(".elementor-element-' + MENU + '").forEach(function(bar){'
          'var pills=Array.prototype.slice.call(bar.querySelectorAll(":scope > .healus-tab"));'
          'pills.forEach(function(p,i){p.setAttribute("type","button");p.setAttribute("aria-pressed",i===0?"true":"false");'
          'p.addEventListener("click",function(){pills.forEach(function(q){q.setAttribute("aria-pressed",q===p?"true":"false");});});});});}'
          'if(document.readyState==="loading"){document.addEventListener("DOMContentLoaded",init);}else{init();}})();</script>')

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

def find(i):
    out = []
    def w(e):
        if e['id'] == i: out.append(e)
        for c in e.get('elements', []): w(c)
    for e in data: w(e)
    return out[0]

wrap, menu = find(WRAP), find(MENU)
# pills: button tag, drop the local static styles, label as span
for item in menu['elements']:
    item['settings']['tag'] = {'$$type': 'string', 'value': 'button'}
    st = item.get('styles') if isinstance(item.get('styles'), dict) else {}
    for sid in [s for s in st if s.endswith('-static')]:
        st.pop(sid)
        item['settings']['classes']['value'].remove(sid)
    for lab in item['elements']:
        lab['settings']['tag'] = {'$$type': 'string', 'value': 'span'}
# bar: pressed/hover rules
v = [v for s in menu['styles'].values() for v in s['variants'] if v['meta']['breakpoint'] == 'desktop' and v['meta']['state'] is None][0]
old = base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
old = old.split(' /*pills*/ ')[0]
v['custom_css'] = {'raw': base64.b64encode((old + ' /*pills*/ ' + BAR_CSS).encode()).decode()}
# script widget after the bar (zero size, no spacing)
wrap['elements'] = [e for e in wrap['elements'] if not (e.get('widgetType') == 'html' and 'aria-pressed' in e['settings'].get('html', ''))]
zero = {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True}
wrap['elements'].insert(1, {'id': '%07x' % random.getrandbits(28), 'elType': 'widget', 'widgetType': 'html', 'isInner': False,
                            'settings': {'html': SCRIPT, '_margin': zero, '_padding': zero}, 'elements': []})

body = '/tmp/claude-0/_hu_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, open(body, 'w'), ensure_ascii=False)
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                    '--data-binary', '@' + body, mcp.API + f'wp/v2/pages/{POST}?_fields=id'], capture_output=True, text=True)
os.remove(body)
assert json.loads(r.stdout).get('id') == POST, r.stdout[:300]
print('written')

for attempt in range(4):
    try:
        mcp.init()
        mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
            {'action': 'update', 'element_id': WRAP, 'style': 'width: 100%;'}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
