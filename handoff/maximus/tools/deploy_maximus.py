"""Rebuild + publish the Maximus page and force Elementor to regenerate its local CSS.

usage: WP_BASIC_AUTH=... python3 deploy_maximus.py <frame.json>
"""
import json, re, sys, subprocess, os
import mcp

PID = 410364
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, 'build_maximus.py')] + sys.argv[1:], check=True)
p = json.load(open(os.path.join(HERE, '_payload.json')))
p['dry_run'] = False
print('status ->', mcp.rest('POST', f'pages/{PID}', {'status': 'draft'}).get('status'))
r = mcp.call('elementor-build-composition', p)
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml']))
json.dump(ids, open(os.path.join(HERE, 'ids_live.json'), 'w'))
print('built', len(ids), 'elements; removed', len(r.get('removed_element_ids', [])))
print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
# a trivial update + second publish makes Elementor regenerate the page's local CSS file
mcp.call('elementor-manage-elements', {'post_id': PID, 'operations': [
    {'action': 'update', 'element_id': ids['hero-btn-demo'], 'settings': {'text': 'Request a Demo'}}]})
print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
h = mcp.get('https://medcaredemo.online/medcare/maximus-ai-product/', auth=False, raw=True)
u = re.findall(r'https://[^"\']*local-%d-frontend-desktop\.css\?ver=\w+' % PID, h)[0]
css = mcp.get(u, auth=False, raw=True)
missing = [c for c in set(re.findall(r'\b(e-[0-9a-f]{6,8}-[0-9a-f]{3,4})\b', h)) if c not in css]
print('css bytes', len(css), 'style classes missing:', len(missing), '| h1 count', len(re.findall(r'<h1', h)))
