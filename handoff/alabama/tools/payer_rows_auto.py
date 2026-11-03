"""Size the rows of the payer-card grid (72ea8f9, "Where Revenue Slips with Each Alabama Payer") to their content.

The grid had `grid-template-rows` set to 3 equal fr rows (4 on mobile_extra), so every row was as tall as the
tallest card. Removes those props and sets `grid-template-rows: none; grid-auto-rows: auto;` instead.
Backs up the live _elementor_data first; writes via WP REST; then touch + publish through the Elementor MCP.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST, GRID, CSS = 411310, '72ea8f9', 'grid-template-rows: none; grid-auto-rows: auto;'

meta = mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'al_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

found = []
def walk(e):
    if e['id'] == GRID:
        found.append(e)
    for c in e.get('elements', []):
        walk(c)
for e in data:
    walk(e)
grid = found[0]
for s in grid['styles'].values():
    for v in s['variants']:
        v['props'].pop('grid-template-rows', None)
        old = base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
        if CSS not in old:
            v['custom_css'] = {'raw': base64.b64encode((old + ' ' + CSS).strip().encode()).decode()}

body = '/tmp/claude-0/_al_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, open(body, 'w'), ensure_ascii=False)
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                    '--data-binary', '@' + body, mcp.API + f'wp/v2/states/{POST}?_fields=id'], capture_output=True, text=True)
os.remove(body)
assert json.loads(r.stdout).get('id') == POST, r.stdout[:300]
print('written')

for attempt in range(4):
    try:
        mcp.init()
        mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
            {'action': 'update', 'element_id': '2347003', 'settings': {'title': 'Are your claims meeting Alabama deadlines?'}}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
