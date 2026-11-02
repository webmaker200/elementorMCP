"""Write build/sc_data.json to the South Carolina state page (411363) and re-save it through Elementor.

1. back up the page's current _elementor_data to ../backup/
2. write the new data via WP REST (post meta is exposed for the states post type)
3. touch one element through the Elementor MCP and publish, so Elementor regenerates the page CSS
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST = 411363
ROOT = os.path.join(HERE, '..')

cur = mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta,status,slug')
os.makedirs(os.path.join(ROOT, 'backup'), exist_ok=True)
bk = os.path.join(ROOT, 'backup', f'sc_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json')
json.dump(cur, open(bk, 'w'), ensure_ascii=False)
print('backup', bk, len(cur['meta'].get('_elementor_data') or ''), 'chars', cur['status'], cur['slug'])

data = json.load(open(os.path.join(ROOT, 'build', 'sc_data.json')))
body = '/tmp/claude-0/_sc_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False),
                    '_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-post'}},
          open(body, 'w'), ensure_ascii=False)
res = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                      '--data-binary', '@' + body, mcp.API + f'wp/v2/states/{POST}?_fields=id,status'], capture_output=True, text=True)
os.remove(body)
r = json.loads(res.stdout)
assert 'id' in r, json.dumps(r)[:500]
back = json.loads(mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta')['meta']['_elementor_data'])
assert back == data, 'stored data differs from the build'
print('written', len(data), 'sections')

# Re-save through Elementor: touch the "View All Specialties" button text and publish.
btn = [e for e in [data[9]] for e in e['elements'] if e.get('widgetType') == 'e-button'][0]
mcp.init()
print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
    {'action': 'update', 'element_id': btn['id'], 'settings': {'text': 'View All Specialties'}}]})
print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
