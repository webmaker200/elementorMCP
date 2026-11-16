"""After run_build.py: make sure the two CTA links carry no site animation attribute.
The site's data-class="custom-button" animation duplicates the label text and hides the arrow on these
pill links, so it is left off; the pills have their own hover (tint + shadow) in gs.py."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, gs  # noqa: E402
xml = open(os.path.join(HERE, '..', 'build', 'resolved.xml')).read()
ids = dict(re.findall(r'configuration-id="([^"]+)" id="([^"]+)"', xml))
json.dump(ids, open(os.path.join(HERE, '..', 'build', 'ids.json'), 'w'), indent=1)
ops = [{'action': 'update', 'element_id': ids[k], 'settings': {'attributes': []}} for k in ('hb1', 'co-b')]
r = mcp.call('elementor-manage-elements', {'post_id': gs.PID, 'operations': ops})
print([x['status'] for x in r['results']])
