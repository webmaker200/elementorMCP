"""HealUs page (411263): FAQ answers full width -- max-width 660px -> 100% on every answer paragraph in accordion 1ebd8d4a.
Backs up the live _elementor_data first; writes via WP REST; touch + publish.
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, ACC = 411263, '1ebd8d4a'
FULL = {'$$type': 'size', 'value': {'size': 100, 'unit': '%'}}

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

acc = []
def find(e):
    if e['id'] == ACC: acc.append(e)
    [find(c) for c in e.get('elements', [])]
[find(e) for e in data]
n = 0
for item in acc[0]['elements']:
    content = [c for c in item['elements'] if c['elType'] == 'e-accordion-item-content'][0]
    for para in content['elements']:
        for s in para['styles'].values():
            for v in s['variants']:
                if 'max-width' in v['props'] and v['meta']['breakpoint'] == 'desktop':
                    v['props']['max-width'] = FULL; n += 1
print('answers widened:', n)
assert n == len(acc[0]['elements'])

body = '/tmp/claude-0/_hu_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, open(body, 'w'), ensure_ascii=False)
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                    '--data-binary', '@' + body, mcp.API + f'wp/v2/pages/{POST}?_fields=id'], capture_output=True, text=True)
os.remove(body)
assert json.loads(r.stdout).get('id') == POST, r.stdout[:300]

for attempt in range(4):
    try:
        mcp.init()
        mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
            {'action': 'update', 'element_id': '7bf06193', 'style': 'width: 100%;'}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
