"""HealUs page (411263), section 4 specialty chips: green hover like the active "Primary care" chip.

Starts from backup hu_411263_20261106-102019.json (the published state before the interrupted pill-bar change, which the
owner chose not to keep), adds a local hover style to the five other chips (healus-chip paragraphs) and writes the page.
Hover = Primary care's look: gradient 115deg #318371 -> #006750, white text, soft green shadow; font weight unchanged
so chips don't change width. `& a { color: inherit }` keeps the hover colour once links are added to the chips.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST = 411263
BASE = os.path.join(HERE, '..', 'backup', 'hu_411263_20261106-102019.json')
CHIPS = ['6c511057', '19f3e787', '7ac93f56', '56804580', '60e772e6']
CSS = ('transition: background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease; & a { color: inherit; text-decoration: none; } '
       '&:hover { background-color: #006750; background-image: linear-gradient(115deg, #318371 0%, #006750 100%); '
       'color: #FFFFFF; box-shadow: 0px 10px 24px -12px rgba(0,103,80,0.6); }')

live = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(live, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(json.load(open(BASE))['_elementor_data'])

done = []
def walk(e):
    if e['id'] in CHIPS:
        sid = f'e-{e["id"]}-hover'
        e['styles'] = e['styles'] if isinstance(e.get('styles'), dict) else {}
        e['styles'][sid] = {'id': sid, 'label': 'local', 'type': 'class', 'variants': [
            {'meta': {'breakpoint': 'desktop', 'state': None}, 'props': {}, 'custom_css': {'raw': base64.b64encode(CSS.encode()).decode()}}]}
        cl = e['settings']['classes']['value']
        if sid not in cl:
            cl.append(sid)
        done.append(e['id'])
    for c in e.get('elements', []):
        walk(c)
for e in data:
    walk(e)
assert sorted(done) == sorted(CHIPS), done

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
