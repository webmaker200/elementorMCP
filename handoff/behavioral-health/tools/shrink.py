"""Shrink the Behavioral Health page (411549) without changing its design: every local V4 style that is repeated
on 2+ elements becomes one global class (bh-sNN, highest priority so it wins exactly like the local style did),
the elements get that class and their local copy is removed. Reads the live V4 content first (keeps manual edits).
usage: shrink.py <current-content.json>   (from get-page-structure include_content per top-level section)"""
import json, os, sys
from collections import OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402
PID = 411549
cur = json.load(open(sys.argv[1]))


def walk(es):
    for e in es:
        yield e
        yield from walk(e.get('elements', []))


groups = OrderedDict()
for sec in cur.values():
    for e in walk(sec.get('elements', [sec])):
        st = e.get('styles')
        if isinstance(st, dict) and st.get('css'):
            groups.setdefault(st['css'], []).append(e['id'])
groups = OrderedDict((k, v) for k, v in groups.items() if len(v) > 1)
print(len(groups), 'repeated styles on', sum(len(v) for v in groups.values()), 'elements')

labels = {css: f'bh-s{i + 1:02d}' for i, css in enumerate(groups)}
res = mcp.call('elementor-manage-classes', {'operations': [{'action': 'create', 'label': lab, 'css': css} for css, lab in labels.items()]})
bad = [r for r in res['results'] if r['status'] != 'ok']
assert not bad, bad
ids = {r['label']: r['id'] for r in res['results']}
json.dump({lab: {'id': ids[lab], 'css': css, 'elements': groups[css]} for css, lab in labels.items()},
          open(os.path.join(HERE, '..', 'build', 'shrink_classes.json'), 'w'), indent=1)
# highest priority (earlier = wins), so each class overrides other global classes like the local style did
print(mcp.call('elementor-reorder-classes', {'order': [ids[l] for l in labels.values()] + [x for x in res['order'] if x not in ids.values()]}).get('status'))

ops = [{'action': 'update', 'element_id': eid, 'classes': [labels[css]], 'style': '', 'style_apply_mode': 'replace'}
       for css, els in groups.items() for eid in els]
for i in range(0, len(ops), 50):
    r = mcp.call('elementor-manage-elements', {'post_id': PID, 'operations': ops[i:i + 50]})
    errs = [x for x in r['results'] if x['status'] != 'ok']
    print(i, len(ops[i:i + 50]), 'errors:', errs[:3])
print(mcp.call('elementor-publish-document', {'post_id': PID}).get('status'))
