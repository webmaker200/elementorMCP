"""HealUs page (411263), section 2 KPI strip (grid 78020665): make the KPI numbers safe to edit.

Each KPI was one paragraph "<span>80,000+</span>Providers supported..." whose big gradient number depended on the inline
<span>; retyping the number in Elementor's text editor removed the span and broke the style. Each KPI becomes an
e-div-block (keeps the cell padding / divider line) with two plain paragraphs: the number (gradient style, 46px / 32px on
mobile) and the label (14px slate). Same look, no inline markup to break.
Backs up the live _elementor_data first; writes via WP REST; touch + publish.
"""
import base64, copy, json, os, random, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, GRID = 411263, '78020665'
BOX_PROPS = ('padding', 'margin', 'border-width')
LABEL_PROPS = ('font-family', 'font-size', 'color', 'line-height')
ZERO = {'$$type': 'size', 'value': {'size': 0, 'unit': 'px'}}

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

ids = set()
def collect(e):
    ids.add(e['id']); [collect(c) for c in e.get('elements', [])]
[collect(e) for e in data]
def nid():
    while True:
        i = '%08x' % random.getrandbits(32)
        if i not in ids:
            ids.add(i); return i
def raw(css): return {'raw': base64.b64encode(css.encode()).decode()} if css.strip() else None
def unraw(v): return base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
def el(kind, variants, settings=None, children=None, widget=False):
    i = nid(); sid = f'e-{i}-{nid()[:4]}'
    e = {'id': i, 'elType': 'widget' if widget else kind, 'settings': dict(settings or {}), 'isInner': False, 'elements': children or [],
         'styles': {sid: {'id': sid, 'label': 'local', 'type': 'class', 'variants': variants}}, 'interactions': [], 'editor_settings': [], 'version': '0.0'}
    if widget: e['widgetType'] = kind
    e['settings']['classes'] = {'$$type': 'classes', 'value': [sid]}
    return e
def var(bp, props, css=''):
    return {'meta': {'breakpoint': bp, 'state': None}, 'props': props, 'custom_css': raw(css)}
def para(text, variants):
    return el('e-paragraph', variants, {'paragraph': {'$$type': 'escaped-html', 'value': text}}, widget=True)

grid = []
def find(e):
    if e['id'] == GRID: grid.append(e)
    [find(c) for c in e.get('elements', [])]
[find(e) for e in data]
grid = grid[0]
assert all(c.get('widgetType') == 'e-paragraph' for c in grid['elements']), 'KPIs already split?'

new = []
for p in grid['elements']:
    m = re.match(r'\s*<span>(.*?)</span>(.*)$', p['settings']['paragraph']['value'], re.S)
    value, label = m.group(1).strip(), m.group(2).strip()
    variants = list(p['styles'].values())[0]['variants']
    box_v, val_v, lab_v = [], [], []
    for v in variants:
        bp, props, css = v['meta']['breakpoint'], v['props'], unraw(v)
        span = re.search(r'&\s*span\s*\{([^}]*)\}', css)
        rest = re.sub(r'&\s*span\s*\{[^}]*\}', '', css).strip()
        bprops = {k: copy.deepcopy(props[k]) for k in BOX_PROPS if k in props}
        if bp == 'desktop':
            bprops['display'] = {'$$type': 'string', 'value': 'block'}
        if bprops or rest:
            box_v.append(var(bp, bprops, rest))
        if span:
            vprops = {'margin': ZERO, 'padding': ZERO}
            if bp == 'desktop' and 'font-family' in props:
                vprops['font-family'] = copy.deepcopy(props['font-family'])
            val_v.append(var(bp, vprops if bp == 'desktop' else {}, span.group(1).strip()))
        lprops = {k: copy.deepcopy(props[k]) for k in LABEL_PROPS if k in props}
        if bp == 'desktop':  # 6px gap as margin-top: the theme forces p { margin-block-end: 0 !important }
            lprops.update({'padding': ZERO, 'margin': {'$$type': 'dimensions', 'value': {'block-start': {'$$type': 'size', 'value': {'size': 6, 'unit': 'px'}},
                           'inline-end': ZERO, 'block-end': ZERO, 'inline-start': ZERO}}})
        if lprops:
            lab_v.append(var(bp, lprops))
    new.append(el('e-div-block', box_v, children=[para(value, val_v), para(label, lab_v)]))
    print(value, '|', label)
grid['elements'] = new

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
            {'action': 'update', 'element_id': '7bf06193', 'style': 'width: 100%;'}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
