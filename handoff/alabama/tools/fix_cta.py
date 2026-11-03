"""Replace the leftover Texas copy in the Alabama page's claims-review CTA (section 348f7d7) with Alabama copy.

Backs up the live _elementor_data, changes only the CTA heading (2347003) and paragraph (e87e952), writes via
WP REST, then touches + publishes through the Elementor MCP.  The deadlines named are the ones the page's own
"Alabama's Clean Deadlines" section states (Ala. Code § 27-1-17: 30-day clean claim, 180-day window; Medicaid 1 year).
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST = 411310
NEW = {'2347003': 'Are your claims meeting Alabama deadlines?',
       'e87e952': 'We check your claims against the deadlines that matter in Alabama, from the 30-day prompt-pay clock and 180-day filing window to Alabama Medicaid’s one-year limit, and show you where revenue is slipping. Find out with a free billing audit.'}

meta = mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'al_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

hits = {}
def walk(e):
    if e['id'] in NEW:
        key = 'title' if e.get('widgetType') == 'e-heading' else 'paragraph'
        assert 'Texas' in e['settings'][key]['value'], e['settings'][key]['value']
        e['settings'][key]['value'] = NEW[e['id']]
        hits[e['id']] = key
    for c in e.get('elements', []):
        walk(c)
for e in data:
    walk(e)
assert len(hits) == 2, hits
assert 'Texas' not in json.dumps(data), 'other Texas copy remains'

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
            {'action': 'update', 'element_id': '2347003', 'settings': {'title': NEW['2347003']}}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
