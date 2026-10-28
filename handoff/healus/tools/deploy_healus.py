"""Rebuild page 411263: draft -> build-composition (replace) -> publish -> trivial touch + publish (forces local CSS regeneration).
The page stays password-protected until the owner approves it; the password is kept outside the repo."""
import json, re, sys, time
import healus, mcp
PID = healus.PID
print(mcp.rest('POST', f'wp/v2/pages/{PID}', {'status': 'draft'}).get('status'))
p = healus.payload()
r = mcp.call('elementor-build-composition', p)
if r.get('warnings'):
    print('WARNINGS', json.dumps(r['warnings'])[:1500])
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml']))
json.dump(ids, open('healus_ids.json', 'w'))
top = mcp.call('elementor-get-page-structure', {'post_id': PID})['elements']
assert top and top[0]['id'] == ids['s1'] and len(top) == len(healus.SECTIONS), 'build not applied'
print('built', len(ids))
print(mcp.rest('POST', f'wp/v2/pages/{PID}', {'status': 'publish'}).get('status'))
print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
mcp.call('elementor-manage-elements', {'post_id': PID, 'operations': [{'action': 'update', 'element_id': ids['hp-t'], 'settings': {'paragraph': 'AI-Powered healthcare'}}]})
print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
