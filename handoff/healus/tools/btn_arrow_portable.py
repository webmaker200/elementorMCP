"""HealUs page (411263): make the healus-btn-ghost arrow survive copying the page to another site.

The arrow (::after) is defined in the global class with color var(--HealUsGreen); a site without that global variable
shows a white arrow on the white circle. Every button using healus-btn-ghost gets the arrow glyph + circle + hex colours
in its own local style, which travels with a copied page. "See how it works" keeps its down arrow.
Backs up the live _elementor_data first; writes via WP REST; touch + publish.
"""
import base64, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, CLS = 411263, 'g-029bdb9'
ARROW = {'31a9057f': '\\2193'}  # down arrow on "See how it works"; others default to right arrow
TAG = '/*arrow*/'

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

done = []
def walk(e):
    cl = e.get('settings', {}).get('classes')
    if isinstance(cl, dict) and CLS in cl['value']:
        glyph = ARROW.get(e['id'], '\\2192')
        css = (f"{TAG} &::after {{ content: '{glyph}'; display: flex; align-items: center; justify-content: center; "
               "border-radius: 999px; background-color: #FFFFFF; color: #006750; font-size: 14px; font-weight: 400; }")
        v = [v for s in e['styles'].values() for v in s['variants'] if v['meta']['breakpoint'] == 'desktop' and v['meta']['state'] is None][0]
        old = base64.b64decode(v['custom_css']['raw']).decode() if v.get('custom_css') else ''
        old = old.split(TAG)[0].rstrip()
        v['custom_css'] = {'raw': base64.b64encode((old + ' ' + css).strip().encode()).decode()}
        done.append(e['id'])
    for c in e.get('elements', []):
        walk(c)
for e in data:
    walk(e)
print('buttons:', done)

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
