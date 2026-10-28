"""Build the HealUs page (draft) and print a fresh anonymous preview URL for verification.
usage: python3 build_healus.py [--dry]"""
import json, re, sys
import healus, mcp
p = healus.payload(dry='--dry' in sys.argv)
print('elements', p['xml_structure'].count('configuration-id='))
r = mcp.call('elementor-build-composition', p)
if r.get('warnings'):
    print('WARNINGS', json.dumps(r['warnings'])[:2000])
if '--dry' in sys.argv:
    sys.exit()
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', r['resolved_xml']))
json.dump(ids, open('healus_ids.json', 'w'))
top = mcp.call('elementor-get-page-structure', {'post_id': healus.PID})['elements']
assert top and top[0]['id'] == ids['s1'] and len(top) == len(healus.SECTIONS), 'build not applied'
print('built', len(ids), 'ids; sections', len(top))
pv = mcp.call('elementor-create-preview-link', {'post_id': healus.PID})
open('/tmp/claude-0/healus_preview_url.txt', 'w').write(pv['url'])
print('preview ready')
