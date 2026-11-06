"""Section 3 ("One patient, one chart, every step of the visit") on the HealUs page (411263): replace the V4 tabs widget
with static markup.

- e-tabs (7bf06193) -> e-div-block, same local style (column, margin-top 38px)
- e-tabs-menu (4ca8e32c) -> e-div-block, same local style (glass pill bar)
- each e-tab -> e-div-block with the same `healus-tab` class and `healus-tab-label` paragraph, so the pills look identical;
  "1 Charting" gets the old selected look as a local style (white pill, shadow, green number) since Charting is the
  content shown; cursor reset to default because the pills are no longer interactive
- e-tabs-content-area (49eb7977) -> e-div-block, same local style (margin-top 66px), holding only the Charting panel
  (164b0c49); the other five tab panels are dropped

Backs up the live _elementor_data first; writes via WP REST; then touch + publish through the Elementor MCP.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, TABS, MENU, AREA, PANEL = 411263, '7bf06193', '4ca8e32c', '49eb7977', '164b0c49'
SELECTED = ('background-color: #FFFFFF; box-shadow: 0px 8px 20px -10px rgba(2,40,66,0.3), 0px 0px 0px 1px rgba(49,131,113,0.12); '
            '& p { font-weight: 500; color: var(--HealUsInk); } '
            '& span { background-image: linear-gradient(135deg, #318371 0%, #006750 100%); color: #FFFFFF; }')

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

def local(e, css, tag):
    sid = f'e-{e["id"]}-{tag}'
    if not isinstance(e.get('styles'), dict) or not e['styles']:
        e['styles'] = {}
    e['styles'][sid] = {'id': sid, 'label': 'local', 'type': 'class', 'variants': [
        {'meta': {'breakpoint': 'desktop', 'state': None}, 'props': {}, 'custom_css': {'raw': base64.b64encode(css.encode()).decode()}}]}
    cl = e['settings'].setdefault('classes', {'$$type': 'classes', 'value': []})
    cl['value'].append(sid)

tabs, menu, area = find(TABS), find(MENU), find(AREA)
assert tabs['elType'] == 'e-tabs' and menu['elType'] == 'e-tabs-menu' and area['elType'] == 'e-tabs-content-area', 'already flattened?'
panel = find(PANEL)

tabs['elType'] = 'e-div-block'
tabs['settings'].pop('default-active-tab', None)
menu['elType'] = 'e-div-block'
for k, item in enumerate(menu['elements']):
    assert item['elType'] == 'e-tab'
    item['elType'] = 'e-div-block'
    local(item, 'cursor: default; ' + (SELECTED if k == 0 else ''), 'static')
area['elType'] = 'e-div-block'
area['elements'] = [panel]

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
            {'action': 'update', 'element_id': TABS, 'style': 'width: 100%;'}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
