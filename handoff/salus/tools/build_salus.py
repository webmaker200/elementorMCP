import mcp, json, re, salus
mcp.init()
print(mcp.rest('POST', 'pages/410964', {'status': 'draft'}).get('status'))
r = mcp.call('elementor-build-composition', salus.payload())
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml'])); json.dump(ids, open('salus_ids.json', 'w'))
s = mcp.call('elementor-get-page-structure', {'post_id': 410964})
assert s['elements'][0]['id'] == ids['sa'], 'build not applied'
print(mcp.call('elementor-publish-document', {'post_id': 410964})['status'])
