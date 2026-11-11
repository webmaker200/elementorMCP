"""After run_build.py: add the site's CTA animation attribute (data-class="custom-button") to every button, then publish.
build-composition has no attributes setting, but elementor-manage-elements accepts a plain key/value list."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, bh  # noqa: E402
xml = open(os.path.join(HERE, '..', 'build', 'resolved.xml')).read()
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', xml))
json.dump(ids, open(os.path.join(HERE, '..', 'build', 'ids.json'), 'w'), indent=1)
buttons = [ids[k] for k in ('h-b', 'c1-b', 'ai-b', 'ch-b', 'fc-b')]
ops = [{'action': 'update', 'element_id': i, 'settings': {'attributes': [{'key': 'data-class', 'value': 'custom-button'}]}} for i in buttons]
r = mcp.call('elementor-manage-elements', {'post_id': bh.PID, 'operations': ops})
print([x['status'] for x in r['results']])
print(mcp.call('elementor-publish-document', {'post_id': bh.PID}).get('status'))
