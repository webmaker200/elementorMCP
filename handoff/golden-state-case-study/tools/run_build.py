"""Build the Golden State case study (411939) with elementor-build-composition. Usage: run_build.py [dry]
The post stays a draft: the build is saved, not published."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, gs  # noqa: E402
dry = 'dry' in sys.argv
d = gs.payload(dry=dry)
print('payload', len(json.dumps(d)), 'bytes')
r = mcp.call('elementor-build-composition', d)
if isinstance(r, dict):
    xml = r.pop('resolved_xml', '')
    if not dry:
        os.makedirs(os.path.join(HERE, '..', 'build'), exist_ok=True)
        open(os.path.join(HERE, '..', 'build', 'resolved.xml'), 'w').write(xml)
print(json.dumps(r)[:3000] if not isinstance(r, str) else r[:3000])
