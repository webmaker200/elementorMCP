"""Write build/coder_data.json to the AI Medical Coder page (411494) and publish through Elementor.

1. back up the page's current _elementor_data to ../backup/
2. write the new data via WP REST
3. touch one V4 element through the Elementor MCP and publish, so Elementor regenerates the page CSS
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST = 411494
ROOT = os.path.join(HERE, '..')
cur = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta,status,slug')
bk = os.path.join(ROOT, 'backup', f'coder_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json')
json.dump(cur, open(bk, 'w'), ensure_ascii=False)
print('backup', bk, cur['status'], cur['slug'])

data = json.load(open(os.path.join(ROOT, 'build', 'coder_data.json')))
body = '/tmp/claude-0/_coder_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False), '_elementor_edit_mode': 'builder'}}, open(body, 'w'), ensure_ascii=False)
res = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                      '--data-binary', '@' + body, mcp.API + f'wp/v2/pages/{POST}?_fields=id,status'], capture_output=True, text=True)
os.remove(body)
assert 'id' in json.loads(res.stdout), res.stdout[:500]
back = json.loads(mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']['_elementor_data'])
assert back == data, 'stored data differs from the build'
print('written', len(data), 'sections')

# touch the hero caption text and publish (Elementor regenerates the CSS)
cap = data[0]['elements'][1]['elements'][1]['elements'][0]['elements'][1]
assert cap.get('widgetType') == 'e-paragraph', cap.get('widgetType')
mcp.init()
mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
    {'action': 'update', 'element_id': cap['id'], 'settings': {'paragraph': 'Coder view: suggested codes with the evidence behind each one. Sample data.'}}]})
print(mcp.call('elementor-publish-document', {'post_id': POST}))
