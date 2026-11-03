"""Make the last payer card ("Self-Pay", 9b8e881) in "Where Revenue Slips with Each Alabama Payer" span both grid
columns, so the third row has no empty half.  Adds `grid-column: 1 / -1;` to the card's desktop local style.
Backs up the live _elementor_data first; writes via WP REST; then touch + publish through the Elementor MCP.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST, CARD, CSS = 411310, '9b8e881', 'grid-column: 1 / -1;'

meta = mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'al_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

card = []
def walk(e):
    if e['id'] == CARD:
        card.append(e)
    for c in e.get('elements', []):
        walk(c)
for e in data:
    walk(e)
card = card[0]
v = [v for s in card['styles'].values() for v in s['variants'] if v['meta']['breakpoint'] == 'desktop' and v['meta']['state'] is None][0]
old = base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
if CSS not in old:
    v['custom_css'] = {'raw': base64.b64encode((old + ' ' + CSS).strip().encode()).decode()}
# padding is a % of the card's own width: halve it while the card spans two columns, restore it once the grid
# collapses to one column (mobile_extra, <=880px) so it matches the other cards at every width
v['props']['padding'] = {'$$type': 'size', 'value': {'size': 2.5, 'unit': '%'}}
style = list(card['styles'].values())[0]
style['variants'] = [x for x in style['variants'] if x['meta']['breakpoint'] != 'mobile_extra']
style['variants'].append({'meta': {'breakpoint': 'mobile_extra', 'state': None},
                          'props': {'padding': {'$$type': 'size', 'value': {'size': 5, 'unit': '%'}}}, 'custom_css': None})

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
