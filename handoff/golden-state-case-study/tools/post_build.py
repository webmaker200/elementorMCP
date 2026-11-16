"""After run_build.py: add the site's CTA animation attribute (data-class="custom-button") to the two CTA links
(Book a demo, Call us). build-composition has no attributes setting; elementor-manage-elements takes a key/value list."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, gs  # noqa: E402
xml = open(os.path.join(HERE, '..', 'build', 'resolved.xml')).read()
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', xml))
json.dump(ids, open(os.path.join(HERE, '..', 'build', 'ids.json'), 'w'), indent=1)
ops = [{'action': 'update', 'element_id': ids[k], 'settings': {'attributes': [{'key': 'data-class', 'value': 'custom-button'}]}} for k in ('hb1', 'co-b')]
r = mcp.call('elementor-manage-elements', {'post_id': gs.PID, 'operations': ops})
print([x['status'] for x in r['results']])
