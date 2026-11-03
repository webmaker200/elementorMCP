"""Swap the city photos in the Alabama page's "From Huntsville to Mobile" section (644f9b8) for the Alabama uploads.

Backs up the live _elementor_data to ../backup/, changes only the 10 e-image attachment ids in that section,
writes via WP REST, then touches + publishes through the Elementor MCP so the page re-renders.
"""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402

POST, SECTION = 411310, '644f9b8'
PHOTOS = {'Tuscaloosa': 411462, 'Montgomery': 411461, 'Mobile': 411460, 'Huntsville': 411459, 'Gadsden': 411458,
          'Florence-Muscle Shoals': 411457, 'Dothan': 411456, 'Decatur': 411455, 'Birmingham-Hoover': 411454,
          'Auburn-Opelika': 411453}

meta = mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta')['meta']
bk = os.path.join(HERE, '..', 'backup', f'al_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json')
json.dump(meta, open(bk, 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

sec = [e for e in data if e['id'] == SECTION][0]
done = {}
def walk(e):
    els = e.get('elements', [])
    img = [c for c in els if c.get('widgetType') == 'e-image']
    par = [c for c in els if c.get('widgetType') == 'e-paragraph']
    if len(img) == 1 and len(par) == 1 and par[0]['settings']['paragraph']['value'].strip() in PHOTOS:
        city = par[0]['settings']['paragraph']['value'].strip()
        img[0]['settings']['image']['value']['src']['value']['id']['value'] = PHOTOS[city]
        done[city] = img[0]['id']
    for c in els:
        walk(c)
walk(sec)
assert len(done) == len(PHOTOS), f'matched {len(done)} of {len(PHOTOS)}: {sorted(done)}'

body = '/tmp/claude-0/_al_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, open(body, 'w'), ensure_ascii=False)
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                    '--data-binary', '@' + body, mcp.API + f'wp/v2/states/{POST}?_fields=id'], capture_output=True, text=True)
os.remove(body)
assert json.loads(r.stdout).get('id') == POST, r.stdout[:300]
assert json.loads(mcp.rest('GET', f'wp/v2/states/{POST}?context=edit&_fields=meta')['meta']['_elementor_data']) == data
print('written; swapped', len(done))

for city, i in PHOTOS.items():
    mcp.rest('POST', f'wp/v2/media/{i}?_fields=id', {'alt_text': f'{city}, Alabama'})

par = [c for e in [sec] for c in e['elements'] if c.get('widgetType') == 'e-paragraph'][0]
for attempt in range(4):
    try:
        mcp.init()
        mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
            {'action': 'update', 'element_id': par['id'], 'settings': {'paragraph': par['settings']['paragraph']['value']}}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:  # stale session / bot-protection hiccup
        print('retry', str(e)[:120]); time.sleep(10)
