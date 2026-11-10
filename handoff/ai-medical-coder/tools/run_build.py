"""Build the page with elementor-build-composition. Usage: run_build.py [dry]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp, coder  # noqa: E402
dry = 'dry' in sys.argv
p = coder.payload(dry=dry)
mcp.init()
r = mcp.call('elementor-build-composition', p)
r.pop('resolved_xml', None) if isinstance(r, dict) else None
print(json.dumps(r)[:600] if not isinstance(r, str) else r[:600])
if not dry:  # a published page takes the build as an autosave: publish it so the stored data is the new build
    print(mcp.call('elementor-publish-document', {'post_id': coder.PID}).get('status'))
