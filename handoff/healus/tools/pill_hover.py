"""HealUs page (411263), section 3 static pill bar (4ca8e32c): hover look on pills 2-6 = the highlighted "1 Charting"
pill (white pill + shadow, ink label, green gradient number). Hover only: no click/focus behaviour.
Font weight unchanged on hover so the bar doesn't shift. Appends to each pill's existing local "-static" style.
Backs up the live _elementor_data first; writes via WP REST; then touch + publish through the Elementor MCP.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, MENU = 411263, '4ca8e32c'
HOVER = ('transition: background-color 0.2s ease, box-shadow 0.2s ease; '
         '&:hover { background-color: #FFFFFF; box-shadow: 0px 8px 20px -10px rgba(2,40,66,0.3), 0px 0px 0px 1px rgba(49,131,113,0.12); } '
         '&:hover p { color: var(--HealUsInk); } '
         '&:hover span { background-image: linear-gradient(135deg, #318371 0%, #006750 100%); color: #FFFFFF; }')

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

menu = []
def walk(e):
    if e['id'] == MENU: menu.append(e)
    for c in e.get('elements', []): walk(c)
for e in data: walk(e)
pills = menu[0]['elements']
assert len(pills) == 6 and all(p['settings'].get('tag') is None for p in pills), 'pill bar not in the expected static state'
for p in pills[1:]:
    st = [s for k, s in p['styles'].items() if k.endswith('-static')][0]
    v = [v for v in st['variants'] if v['meta']['breakpoint'] == 'desktop'][0]
    old = base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
    old = old.split(' /*hover*/ ')[0]
    v['custom_css'] = {'raw': base64.b64encode((old + ' /*hover*/ ' + HOVER).encode()).decode()}

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
