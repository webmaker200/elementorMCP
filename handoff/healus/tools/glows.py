"""Figma blurred ellipses -> CSS radial-gradient layers per section (writes ../glows.json).

Each ellipse (fill colour x opacity, LAYER_BLUR b) is drawn as a radial gradient whose size is the ellipse
radius + b, solid up to (r - b/2), half strength at r, transparent at r + b. Ellipses from neighbouring
frames are included where their blur reaches into a section, so sections meet without seams.
usage: python3 glows.py <frame.json>
"""
import json, os, sys
d = json.load(open(sys.argv[1]))['nodes']['671:593']['document']
OX, OY = d['absoluteBoundingBox']['x'], d['absoluteBoundingBox']['y']
SECTIONS = {'s1': '671:594', 's2': '671:976', 's3': '671:1049', 's4': '671:1221', 's5': '671:1413',
            's6': '671:1502', 's7': '671:1329', 's8': '671:1371', 's9': '671:1651'}
ells = []
def walk(n):
    if n['type'] == 'ELLIPSE' and n.get('visible', True) and any(e['type'] == 'LAYER_BLUR' for e in n.get('effects', [])):
        f = [x for x in n.get('fills', []) if x.get('visible', True) and x['type'] == 'SOLID'][0]
        bb = n['absoluteBoundingBox']; blur = [e['radius'] for e in n['effects'] if e['type'] == 'LAYER_BLUR'][0]
        c = f['color']; a = c.get('a', 1) * f.get('opacity', 1) * n.get('opacity', 1)
        ells.append(dict(cx=bb['x'] - OX + bb['width'] / 2, cy=bb['y'] - OY + bb['height'] / 2, rx=bb['width'] / 2, ry=bb['height'] / 2,
                         blur=blur, rgb=tuple(round(c[k] * 255) for k in 'rgb'), a=a))
    for k in n.get('children', []):
        walk(k)
for k in d['children']:
    walk(k)
nodes = {c['id']: c for c in d['children']}
out = {}
for sid, nid in SECTIONS.items():
    b = nodes[nid]['absoluteBoundingBox']; top, H = b['y'] - OY, b['height']
    layers = []
    for e in ells:
        R = max(e['rx'], e['ry']) + e['blur']
        if e['cy'] + e['ry'] + e['blur'] < top or e['cy'] - e['ry'] - e['blur'] > top + H:
            continue
        sx = (e['rx'] + e['blur']) / 1920 * 100
        sy = (e['ry'] + e['blur']) / H * 100
        cx = e['cx'] / 1920 * 100
        cy = (e['cy'] - top) / H * 100
        r = min(e['rx'], e['ry']); s1 = max(0, (r - e['blur'] / 2)) / (r + e['blur']) * 100; s2 = r / (r + e['blur']) * 100
        col = 'rgba(%d,%d,%d,' % e['rgb']
        layers.append(f'radial-gradient({sx:.1f}% {sy:.1f}% at {cx:.1f}% {cy:.1f}%, {col}{e["a"]:.3f}) 0%, {col}{e["a"]:.3f}) {s1:.0f}%, '
                      f'{col}{e["a"] / 2:.3f}) {s2:.0f}%, {col}0) 100%)')
    out[sid] = layers
    print(sid, len(layers), 'layers')
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'glows.json'), 'w'), indent=1)
