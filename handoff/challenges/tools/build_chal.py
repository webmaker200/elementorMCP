import mcp, json, re, sys, chal
mcp.init()
p = chal.payload(dry='--dry' in sys.argv)
print('elements', len(p['style']))
if '--dry' in sys.argv:
    print(json.dumps(mcp.call('elementor-build-composition', p))[:300]); sys.exit()
print(mcp.rest('POST', f'pages/{chal.PID}', {'status': 'draft'}).get('status'))
r = mcp.call('elementor-build-composition', p)
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml'])); json.dump(ids, open('chal_ids.json', 'w'))
assert mcp.call('elementor-get-page-structure', {'post_id': chal.PID})['elements'][0]['id'] == ids['sa'], 'build not applied'
print(mcp.call('elementor-publish-document', {'post_id': chal.PID})['status'])
mcp.call('elementor-manage-elements', {'post_id': chal.PID, 'operations': [{'action': 'update', 'element_id': ids['hp-t'], 'settings': {'paragraph': 'The #1 preventable revenue leak in medical practices'}}]})
print(mcp.call('elementor-publish-document', {'post_id': chal.PID})['status'])
import time
link = mcp.rest('GET', f'pages/{chal.PID}')['link']; print(link)
h = mcp.get(link + ('&' if '?' in link else '?') + 'nc=%d' % time.time(), auth=False, raw=True); open('chal_live.html', 'w').write(h)
urls = sorted(set(re.findall(r'https://[^"\']*local-%d-frontend-[a-z_]+\.css\?ver=\w+' % chal.PID, h)))
css = ''.join(mcp.get(u, auth=False, raw=True) for u in urls); open('chal_live.css', 'w').write(css)
i = h.find('data-elementor-id="%d"' % chal.PID); j = h.find('data-elementor-type="footer"')
cls = set(re.findall(r'\b(e-[0-9a-f]{6,8}-[0-9a-f]{3,8})\b', h[i:j if j > 0 else None]))
print('css', len(urls), len(css), 'missing', [c for c in cls if not any(('.' + c + x) in css for x in '{:,')][:8], 'h1', h.count('<h1'), 'faq schema', 'FAQPage' in h)
