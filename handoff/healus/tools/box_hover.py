"""HealUs page (411263): soft hover shadow on the boxes in sections 2, 6, 7 and 8 (problem cards + "HealUs changes that."
bar, insight rows 01-03, integration cards HL7/FHIR/e-Rx/APIs, "why" cards 01-04).
Each box keeps its own shadow and adds `0px 18px 40px -18px rgba(2,40,66,0.22)` on hover (0.25s transition).
Adds one local "-hover" style per box. Backs up the live _elementor_data first; writes via WP REST; touch + publish.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST = 411263
SOFT = '0px 18px 40px -18px rgba(2,40,66,0.22)'
GLASS = '0px 15px 15px 0px rgba(194,194,194,0.1), 0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5)'
RING = '0px 0px 0px 1px rgba(49,131,113,0.1), inset 0px 0px 0px 1px rgba(255,255,255,0.5)'
BOXES = {i: GLASS for i in ['29eebb73', '6bf8e8cd', '771cfb68', '56748b21', '5f22af90', '24acea45', '57df15b7', '293ef204',
                            '3477b195', '68e536d9', '1ff7a280', '78d284e5']}
BOXES.update({i: RING for i in ['1fb3bc1a', '398775e2', '4d7049bc', '571294cf']})

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

done = []
def walk(e):
    if e['id'] in BOXES:
        css = f'transition: box-shadow 0.25s ease; &:hover {{ box-shadow: {BOXES[e["id"]]}, {SOFT}; }}'
        sid = f'e-{e["id"]}-hover'
        e['styles'] = e['styles'] if isinstance(e.get('styles'), dict) else {}
        e['styles'][sid] = {'id': sid, 'label': 'local', 'type': 'class', 'variants': [
            {'meta': {'breakpoint': 'desktop', 'state': None}, 'props': {}, 'custom_css': {'raw': base64.b64encode(css.encode()).decode()}}]}
        if sid not in e['settings']['classes']['value']:
            e['settings']['classes']['value'].append(sid)
        done.append(e['id'])
    for c in e.get('elements', []):
        walk(c)
for e in data:
    walk(e)
assert sorted(done) == sorted(BOXES), set(BOXES) - set(done)

body = '/tmp/claude-0/_hu_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, open(body, 'w'), ensure_ascii=False)
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                    '--data-binary', '@' + body, mcp.API + f'wp/v2/pages/{POST}?_fields=id'], capture_output=True, text=True)
os.remove(body)
assert json.loads(r.stdout).get('id') == POST, r.stdout[:300]
print('written', len(done))

for attempt in range(4):
    try:
        mcp.init()
        mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
            {'action': 'update', 'element_id': '7bf06193', 'style': 'width: 100%;'}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
