"""Build the Behavioral Health specialty (411549) with elementor-build-composition. Usage: run_build.py [dry]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, bh  # noqa: E402
dry = 'dry' in sys.argv
r = mcp.call('elementor-build-composition', bh.payload(dry=dry))
if isinstance(r, dict):
    xml = r.pop('resolved_xml', '')
    if not dry:
        open(os.path.join(HERE, '..', 'build', 'resolved.xml'), 'w').write(xml)
print(json.dumps(r)[:1500] if not isinstance(r, str) else r[:1500])
if not dry:
    print(mcp.call('elementor-publish-document', {'post_id': bh.PID}).get('status'))
