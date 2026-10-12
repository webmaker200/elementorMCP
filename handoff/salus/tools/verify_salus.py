import mcp, json, re, sys
mcp.init(); PID = 410964
ids = json.load(open('salus_ids.json'))
if '--touch' in sys.argv:
    mcp.call('elementor-manage-elements', {'post_id': PID, 'operations': [{'action': 'update', 'element_id': ids['hp-t'], 'settings': {'paragraph': 'AI-Powered healthcare'}}]})
    print(mcp.call('elementor-publish-document', {'post_id': PID})['status'])
print('struct ok', [e['id'] for e in mcp.call('elementor-get-page-structure', {'post_id': PID})['elements']][0] == ids['sa'])
h = mcp.get('https://medcaredemo.online/medcare/salus-ai/?nc=%s' % __import__('time').time(), auth=False, raw=True)
open('salus_live.html', 'w').write(h)
urls = sorted(set(re.findall(r'https://[^"\']*local-%d-frontend-[a-z_]+\.css\?ver=\w+' % PID, h)))
allcss = ''.join(mcp.get(u, auth=False, raw=True) for u in urls); open('salus_live.css', 'w').write(allcss)
cls = set(re.findall(r'\b(e-[0-9a-f]{6,8}-[0-9a-f]{3,4})\b', h))
print('html has sa', ids['sa'] in h, 'css', len(urls), len(allcss), 'missing', len([c for c in cls if c not in allcss]), 'of', len(cls))
