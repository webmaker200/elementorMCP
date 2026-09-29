import build, mcp, json, re
PID = 410324
print(mcp.rest('POST', f'specialties/{PID}', {'status': 'draft'}).get('status'))
r = mcp.call('elementor-build-composition', build.payload(build.SECTIONS, PID, mode='replace_children'))
open('build_result.json', 'w').write(json.dumps(r))
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml']))
json.dump(ids, open('ids_live.json', 'w'))
print('built', len(ids), 'elements; removed', len(r.get('removed_element_ids', [])))
print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
# touch + republish so Elementor regenerates the page's local CSS files
mcp.call('elementor-manage-elements', {'post_id': PID, 'operations': [{'action': 'update', 'element_id': ids['hero-btn'], 'settings': {'text': 'Schedule Consultation'}}]})
print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
s = mcp.call('elementor-get-page-structure', {'post_id': PID}); print([e['title'] for e in s['elements']])
h = mcp.get(f'https://medcaredemo.online/medcare/specialties/wound-care-ai/', auth=False, raw=True)
u = re.findall(r'https://[^"\']*local-410324-frontend-desktop\.css\?ver=\w+', h)[0]
css = mcp.get(u, auth=False, raw=True)
missing = [c for c in set(re.findall(r'\b(e-[0-9a-f]{6,8}-[0-9a-f]{3,4})\b', h)) if c not in css]
print('css bytes', len(css), 'style classes missing from desktop css:', len(missing))
